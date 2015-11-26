"""Reads in a GroupMe JSON file and POSTs its data to an endpoint."""

import json
import threading
import urllib2
import time
import Queue

# Change these values before use
JSON_FILE = 'group.json'
SETTINGS_ID = 00000000

POST_URL = 'https://c3po-bot.appspot.com/storedata'
NUM_ATTEMPTS = 3
RETRY_TIMEOUT = 300
THREAD_COUNT = 8
SUCCESS_TIMEOUT = 0


def post_data(queue):
    """Worker thread function, so it pulls from the Queue until it's empty."""
    # This infinite loop will exit when there are no more items in the queue
    while True:
        # Try again x number of times if the first one fails
        for _ in range(NUM_ATTEMPTS):

            # Unpacking values from queue
            name, picture_url, text, time_sent = queue.get()

            # Packing up values for POST request
            values = {
                'name': name,
                'picture_url': picture_url,
                'text': text,
                'time_sent': time_sent,
                'settings': SETTINGS_ID
            }
            msg_data = json.dumps(values)
            req = urllib2.Request(POST_URL, msg_data)

            try:
                # Making the actual request
                urllib2.urlopen(req)

                # Marking this message as done
                queue.task_done()
                print "%s finished processing %s's message" % (
                    threading.current_thread().getName(), name)

                # Timeout so we don't overload the server
                time.sleep(SUCCESS_TIMEOUT)

                # Break out of the retry loop
                break

            except urllib2.HTTPError as exception:
                print "%s got error: '%s'. Retrying in %d seconds." % (
                    threading.currentThread().getName(), exception.message,
                    RETRY_TIMEOUT)
                time.sleep(RETRY_TIMEOUT)


def main():
    """Queues everything up and starts the threads."""
    # Initializing the queue
    queue = Queue.Queue()

    # Initializing worker threads
    for _ in range(THREAD_COUNT):
        worker = threading.Thread(target=post_data, args=(queue,))
        worker.setDaemon(True)
        worker.start()

    # Getting message data from filesystem
    raw_json_data = open(JSON_FILE).read()
    data = json.loads(raw_json_data)

    # Adding messages to task queue
    for msg in data:
        args = (msg['name'], msg['picture_url'], msg['text'],
                float(msg['created_at']))
        queue.put(args)

    print queue.unfinished_tasks

    # Wait until the queue is empty before exiting main thread
    queue.join()


if __name__ == '__main__':
    main()
