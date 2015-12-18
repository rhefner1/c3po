import logging
import urllib

from google.appengine.ext.webapp import blobstore_handlers
import webapp2


class DownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
    """Handler to download blob by blobkey."""

    def get(self, key):
        key = str(urllib.unquote(key)).strip()
        logging.debug("key is %s" % key)
        self.send_blob(key)


app = webapp2.WSGIApplication(
        [
            (r'/blobstore/(.*)', DownloadHandler),
        ],
        debug=True)
