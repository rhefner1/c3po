"""This contains the pipelines required to run
MapReduce jobs for message analysis.

Derived from the App Engine MapReduce sample application:
https://github.com/GoogleCloudPlatform/appengine-mapreduce/tree/master/python/demo
"""

import logging
import re
import string

from google.appengine.ext import blobstore
from google.appengine.api import app_identity
from mapreduce import base_handler
from mapreduce import mapreduce_pipeline
from c3po.db.analytics import AnalyticsResults

SHARD_COUNT = 4


def start_analysis(settings_key):
    """Starts the full analysis process."""
    results = AnalyticsResults(settings=settings_key)
    results.put()

    pipeline = WordCountPipeline(results.key.id(), settings_key.id())
    pipeline.start()


class WordCountPipeline(base_handler.PipelineBase):
    """Pipeline computing how many times a word appears throughout all
    stored messages."""
    def run(self, results_id, settings_id):
        """Sets up and executes the WordCount pipeline."""
        bucket_name = app_identity.get_default_gcs_bucket_name()

        # This pipeline returns a list of files that each contain partial
        # computed output (# files == SHARD_COUNT)
        shard_outputs = yield mapreduce_pipeline.MapreducePipeline(
                "Word Count; counts word occurrences throughout messages ",
                "analytics.helpers.word_count_map",
                "analytics.helpers.word_count_reduce",
                "mapreduce.input_readers.DatastoreInputReader",
                "mapreduce.output_writers.GoogleCloudStorageOutputWriter",
                mapper_params={
                    "entity_kind": "c3po.db.stored_message.StoredMessage",
                    # "filters": [('settings_id', '=', settings_id)]
                },
                reducer_params={
                    "output_writer": {
                        "bucket_name": bucket_name,
                        "content_type": "text/plain",
                    }
                },
                shards=SHARD_COUNT)

        # Passing the partial output into a merge pipeline that will simply
        # take all of the files and create a larger one.
        yield MergeOutput("word_count", bucket_name, results_id, shard_outputs)


class MergeOutput(base_handler.PipelineBase):
    """A pipeline to store the result of the MapReduce job in the database.

    Args:
      mr_type: the type of mapreduce job run (e.g., WordCount, Index)
      encoded_key: the DB key corresponding to the metadata of this job
      output: the gcs file path where the output of the job is stored
    """

    def run(self, mr_type, bucket_name, results_id, shard_outputs):
        shard_outputs = [s.replace("/%s/" % bucket_name, "") for s in
                         shard_outputs]
        output_path = yield mapreduce_pipeline.MapreducePipeline(
                "word_count",
                "analytics.helpers.reduce_map",
                "analytics.helpers.reduce_reduce",
                "mapreduce.input_readers.GoogleCloudStorageInputReader",
                "mapreduce.output_writers.GoogleCloudStorageOutputWriter",
                mapper_params={
                    "input_reader": {
                        "bucket_name": bucket_name,
                        "objects": shard_outputs
                    }
                },
                reducer_params={
                    "output_writer": {
                        "bucket_name": bucket_name,
                        "content_type": "text/plain",
                    }
                },
                shards=1)
        yield StoreOutput(mr_type, results_id, output_path)


class StoreOutput(base_handler.PipelineBase):
    """A pipeline to store the result of the MapReduce job in the database.

    Args:
      mr_type: the type of mapreduce job run (e.g., WordCount, Index)
      encoded_key: the DB key corresponding to the metadata of this job
      output: the gcs file path where the output of the job is stored
    """

    def run(self, mr_type, results_id, output_path):
        results = AnalyticsResults.get_by_id(results_id)
        logging.info("WOMBAT on StoreOutput with mr_type: %s", mr_type)
        logging.info("WOMBAT OUTPUT PATHS %s", output_path)
        blobstore_filename = "/gs" + output_path[0]
        blobstore_gs_key = blobstore.create_gs_key(blobstore_filename)
        url_path = "/blobstore/" + blobstore_gs_key

        if mr_type == "word_count":
            results.word_count_link = url_path

        results.finished = True
        results.put()
