import boto3

def getecsclient(awsaccessid, awssecretkey, region):
    ecs_client = boto3.client(
        'ecs',
        aws_access_key_id=awsaccessid,
        aws_secret_access_key=awssecretkey,
        region_name=region
    )
    return ecs_client


def getec2client(awsaccessid, awssecretkey, region):
    ec2_client = boto3.client(
        'ec2',
        aws_access_key_id=awsaccessid,
        aws_secret_access_key=awssecretkey,
        region_name=region
    )
    return ec2_client


def getelbclient(awsaccessid, awssecretkey, region):
    elb_client = boto3.client(
        'elb',
        aws_access_key_id=awsaccessid,
        aws_secret_access_key=awssecretkey,
        region_name=region
    )
    return elb_client


def getec2resoure(awsaccessid, awssecretkey, region):
    ec2_resource = boto3.resource(
        'ec2',
        aws_access_key_id=awsaccessid,
        aws_secret_access_key=awssecretkey,
        region_name=region

    )
    return ec2_resource
