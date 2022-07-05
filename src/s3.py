"""This module is to upload and download files from S3 bucket"""
import logging.config
import re
from typing import Tuple

import boto3
import botocore

logger = logging.getLogger(__name__)


def parse_s3(s3path: str) -> Tuple[str, str]:
    """ split s3 path into bucket and file path

    Args:
        s3path (`str`): s3 URL

    Returns:
        s3bucket (`str`): bucket name
        s3path (`str`): file location
    """
    # parse s3 path
    regex = r"s3://([\w._-]+)/([\w./_-]+)"
    # split s3 path to s3 bucket and file path
    paths = re.match(regex, s3path)
    s3bucket = paths.group(1)
    s3path = paths.group(2)

    return s3bucket, s3path


def upload_file_to_s3(local_path: str, s3path: str) -> None:
    """ Upload a file to S3 bucket

    Args:
        local_path (`str`): path to data in local
        s3path (`str`): s3 path to upload data

    Returns:
        None
    """
    # parse s3 path
    s3bucket, s3_just_path = parse_s3(s3path)
    # access s3
    aws_s3 = boto3.resource("s3")
    bucket = aws_s3.Bucket(s3bucket)
    # upload file
    try:
        bucket.upload_file(local_path, s3_just_path)
    except botocore.exceptions.NoCredentialsError:
        logger.error("Please provide AWS credentials via AWS_ACCESS_KEY_ID "
                     "and AWS_SECRET_ACCESS_KEY env variables.")
    else:
        logger.info("Data uploaded from %s to %s", local_path, s3path)


def download_file_from_s3(local_path: str, s3path: str) -> None:
    """Download a data file from s3

    Args:
        local_path (`str`): the path that will store the downloaded data
        s3path (`str`): the s3 path that the data will be downloaded from
    Returns:
        None
    """
    # parse s3 path
    s3bucket, s3_just_path = parse_s3(s3path)
    # access s3 bucket
    aws_s3 = boto3.resource("s3")
    bucket = aws_s3.Bucket(s3bucket)
    # download file
    try:
        bucket.download_file(s3_just_path, local_path)
    except botocore.exceptions.NoCredentialsError:
        logger.error("Please provide AWS credentials via AWS_ACCESS_KEY_ID "
                     "and AWS_SECRET_ACCESS_KEY env variables.")
    else:
        logger.info("Data downloaded from %s to %s", s3path, local_path)
