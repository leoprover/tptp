from pathlib import Path

import boto3
from botocore.exceptions import ClientError


class BucketCreationError(Exception):
    pass


class BucketDeletionError(Exception):
    pass


class ObjectCreationError(Exception):
    pass


class ObjectDeletionError(Exception):
    pass


class ObjectDownloadError(Exception):
    pass


def createBucket(bucket:str, region:str) -> None:
    """
    Creates a S3 bucket in a specific region.
    :param name: bucket of the S3 bucket, has to be unique across the region
    :param region: AWS region where the bucket should be created
    :return: None
    """
    client = boto3.client('s3', region_name=region)
    try:
        client.create_bucket(
            ACL='authenticated-read',
            Bucket=bucket,
            CreateBucketConfiguration={
                'LocationConstraint': region
            }
        )
    except Exception as e:
        raise BucketCreationError(e)


def deleteBucket(bucket:str, region:str) -> None:
    """
    Deletes a S3 bucket in a specific region.
    :param bucket: name of the S3 bucket
    :param region: AWS region where the S3 bucket is located
    :return: None
    """
    client = boto3.client('s3', region_name=region)
    try:
        client.delete_bucket(Bucket=bucket)
    except ClientError as e:
        raise BucketDeletionError(e)


def createObject(bucket:str, object:str, region:str, path:Path) -> None:
    """
    Creates an object in a S3 bucket from a file. Overwrites an existing object.
    :param bucket: name of the S3 bucket
    :param object: name of the object representing the file in the bucket, will be overwritten, if existing
    :param region: AWS region where the S3 bucket is located
    :param path: path to the file which has to be uploaded
    :return: None
    """
    data = path.read_bytes()
    client = boto3.client('s3', region_name=region)
    client.upload_fileobj(
        data,
        bucket,
        object,
        #Callback=callback
    )


def deleteObject(bucket:str, object:str, region:str, version:str=None) -> None:
    """
    Deletes an object in a S3 bucket.
    :param bucket: name of the bucket
    :param object: name of the object representing the file in the bucket, will be overwritten, if existing
    :param region: AWS region where the S3 bucket is located
    :param version: version of the object (optional)
    :return: None
    """
    client = boto3.client('s3', region_name=region)
    if version:
        client.delete_object(
            Bucket=bucket,
            Key=object,
            VersionId=version,
    )
    else:
        client.delete_object(
            Bucket=bucket,
            Key=object,
        )


def downloadObject(bucket:str, object:str, region:str, path:Path) -> None:
    """
    Downloads an object from a S3 bucket.
    :param bucket: name of the S3 bucket
    :param object: name of the object to download
    :param region: AWS region where the S3 bucket is located
    :param path: path where to save the object locally
    :return: None
    """
    client = boto3.client('s3', region_name=region)
    try:
        with open(str(path), 'wb') as data:
            client.download_fileobj(Bucket=bucket, Object=object, Data=data)
    except Exception as e:
        raise ObjectDownloadError(e)


