from os import environ

from src import bsky
from src import mastodon
from src import nostr
from src.utils import create_post


assert environ.get('BSKY_USER') is not None, 'could not get bsky username from env'
assert environ.get('BSKY_PSWD') is not None, 'could not get bsky password from from env'
assert environ.get('AWS_USER') is not None, 'could not get "aws_access_key_id" from env'
assert environ.get('AWS_PSWD') is not None, 'could not get "aws_secret_access_key" from env'
assert environ.get('AWS_REGN') is not None, 'could not get "aws_region_name" from env'
assert environ.get('AWS_BUCK') is not None, 'could not get aws bucket from env'


new_post = create_post()
bsky.run(new_post)