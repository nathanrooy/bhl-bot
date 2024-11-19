from os import environ
from datetime import datetime, timezone
from atproto import Client, models, client_utils


def _post(client, post):

    # construct rich text description
    description_lines = [v.strip().replace('\x00','') for v in post['img_desc'].split('\n')]
    text_builder = client_utils.TextBuilder()
    text_builder.text(' '.join(description_lines[:2]) + ' (source: ')
    text_builder.link(description_lines[-1], description_lines[-1])
    text_builder.text(') ')
    text_builder.tag('#nature', 'nature')
    text_builder.text(' ')
    text_builder.tag('#illustration', 'illustration')
    text_builder.text(' ')
    text_builder.tag('#art', 'art')

    # assemble and post
    client.send_image(text=text_builder, image=post['img_buf'].getvalue(), image_alt=post['img_desc'])


def _purge(client):

    # find old posts for purging
    profile_feed = client.get_author_feed(actor=environ.get('BSKY_USER'))
    for feed_view in profile_feed.feed:
        
        # determine post age
        post_ts = datetime.fromisoformat(feed_view.post.record.created_at)
        post_age_sec = (datetime.now(timezone.utc) - post_ts).total_seconds()

        # delete old posts
        if post_age_sec >= 365 * 24 * 3600:
            print(f'> deleting post:{feed_view.post.uri} ---', client.delete_post(feed_view.post.uri))


def run(post):
    print('> posting to bsky...')
    client = Client()
    profile = client.login(environ.get('BSKY_USER'), environ.get('BSKY_PSWD'))
    _post(client, post)
    _purge(client)
    print('> finished')
