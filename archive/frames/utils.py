import boto3
from functools import lru_cache
from django.conf import settings
import os
import logging

from kombu.connection import Connection
from kombu import Exchange


logger = logging.getLogger()


@lru_cache(maxsize=1)
def get_s3_client():
    config = boto3.session.Config(region_name='us-west-2', signature_version='s3v4')
    return boto3.client('s3', config=config)


def remove_dashes_from_keys(dictionary):
    new_dictionary = {}
    for k in dictionary:
        new_key = k.replace('-', '_')
        new_dictionary[new_key] = dictionary[k]
    return new_dictionary


def fits_keywords_only(dictionary):
    new_dictionary = {}
    for k in dictionary:
        if k[0].isupper():
            new_dictionary[k] = dictionary[k]
    return new_dictionary


def archived_queue_payload(dictionary, frame):
    new_dictionary = dictionary.copy()
    new_dictionary['filename'] = frame.filename
    new_dictionary['frameid'] = frame.id
    return new_dictionary


def post_to_archived_queue(payload):
    if settings.PROCESSED_EXCHANGE_ENABLED:
        retry_policy = {
            'interval_start': 0,
            'interval_step': 1,
            'interval_max': 4,
            'max_retries': 5,
        }
        processed_exchange = Exchange(settings.PROCESSED_EXCHANGE_NAME, type='fanout')
        with Connection(settings.QUEUE_BROKER_URL, transport_options=retry_policy) as conn:
            producer = conn.Producer(exchange=processed_exchange)
            producer.publish(payload, delivery_mode='persistent', retry=True, retry_policy=retry_policy)


def build_nginx_zip_text(frames, directory):
    client = get_s3_client()
    ret = []
    new_bucket = os.getenv('NEW_AWS_BUCKET', 'archive-lco-global')

    for frame in frames:
        # Parameters for AWS S3 URL signing request
        version = frame.version_set.first()
        bucket, s3_key = version.get_bucket_and_s3_key()
        params = {
            'Key': s3_key,
            'Bucket': bucket,
        }
        # Generate a presigned AWS S3 V4 URL which expires in 86400 seconds (1 day)
        url = client.generate_presigned_url('get_object', Params=params, ExpiresIn=86400)
        # The NGINX mod_zip module requires that the files which are used to build the
        # ZIP file must be loaded from an internal NGINX location. Replace the leading
        # portion of the generated URL with an internal NGINX location which proxies all
        # traffic to AWS S3.
        if version.migrated:
            location = url.replace('https://' + new_bucket + '.s3.amazonaws.com', '/news3')
        else:
            location = url.replace('https://s3.us-west-2.amazonaws.com', '/s3')
        # The NGINX mod_zip module builds ZIP files using a manifest. Build the manifest
        # line for this frame.
        line = '- {size} {location} {directory}/{basename}{extension}\n'.format(
            size=version.size,
            location=location,
            directory=directory,
            basename=frame.basename,
            extension=version.extension,
        )
        logger.error(line)
        # Add to returned lines
        ret.append(line)

    # Concatenate all lines together into a single string
    return ''.join(ret)
