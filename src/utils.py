from io import BytesIO
from os import environ
from random import choice

import boto3
from PIL import Image


def create_post():
    s3 = boto3.client('s3',
        aws_access_key_id=environ.get('AWS_USER'),
        aws_secret_access_key=environ.get('AWS_PSWD'),
        region_name=environ.get('AWS_REGN')
    )

    # generate a list of all candidate images
    candidates = []
    paginator = s3.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=environ.get('AWS_BUCK'))  
    for page in page_iterator:
        for obj in page['Contents']:
            if '.jpg' in obj['Key']: candidates.append(obj['Key'])

    # pick a random image to post
    obj_key = choice(candidates)
    print('> image choice:', obj_key)

    # download image into buffer
    response = s3.get_object(Bucket=environ.get('AWS_BUCK'), Key=obj_key)
    buf =  BytesIO(response['Body'].read())
    img = Image.open(buf)

    # construct post object and return
    return {
        'img_buf':buf,
        'img_desc':img.app["COM"].decode('utf8')
    }
