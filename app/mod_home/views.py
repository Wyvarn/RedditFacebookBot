from . import home
from flask import request, current_app
import json
import requests
import click
from app import db  # , reddit
from config import Config
from app.models import Users, Posts
import os
import praw


reddit = praw.Reddit(client_id=os.environ.get("REDDIT_CLIENT_ID"),
                     client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
                     user_agent=os.environ.get("USER_AGENT"))


# TODO: move to auth module
@home.route('', methods=['GET'])
def handle_verification():
    """
    Handles verification of this request
    :return: request from Facebook if valid, Error message
    """
    click.echo(click.style("Handling Verification.", fg="green", bold=True))
    facebook_webhook_token = current_app.config.get("FACEBOOK_WEBHOOK_VERIFY_TOKEN")
    if request.args.get('hub.verify_token', '') == facebook_webhook_token:
        click.echo(click.style("Verification successful!", fg="green", bold=True))
        return request.args.get('hub.challenge', '')
    else:
        click.echo(click.style("Verification failed!", fg="red", bold=True))
        return 'Error, wrong validation token'


@home.route('', methods=['POST'])
def handle_messages():
    # retrieve PAGE ACCESS TOKEN from facebook
    page_access_token = current_app.config.get("FACEBOOK_PAGE_ACCESS_TOKEN")

    click.echo(click.style("Handling Messages", fg="green", bold=True))

    # get the payload
    payload = request.get_data()

    click.echo(click.style("Payload: {}".format(payload), fg="green", bold=True))

    # for each sender and message
    for sender, message in messaging_events(payload):
        click.echo(click.style("Incoming from %s: %s" % (sender, message), fg="green", bold=True))
        # send them a message
        send_message(page_access_token, sender, message)
    return "ok"


def messaging_events(payload):
    """Generate tuples of (sender_id, message_text) from the
    provided payload.
    """
    data = json.loads(payload)
    message_events = data["entry"][0]["messaging"]
    for event in message_events:
        if "message" in event and "text" in event["message"]:
            yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
        else:
            yield event["sender"]["id"], "I can't echo this"


def send_message(token, recipient, text):
    """
    Send the message text to recipient with id recipient.
    
    payload = "http://imgur.com/WeyNGtQ.jpg"
    
    It makes sure that if no new posts are found for a particular user 
    (every subreddit has a maximum number of “hot” posts) we have at least something to return.
     Otherwise we will get a variable undeclared error.
    """
    quick_replies_list = Config.QUICK_REPLIES_LIST

    if "meme" in text.lower():
        subreddit_name = "memes"
    elif "shower" in text.lower():
        subreddit_name = "Showerthoughts"
    elif "joke" in text.lower():
        subreddit_name = "Jokes"
    else:
        subreddit_name = "GetMotivated"

    user = get_or_create(db.session, Users, name=recipient)

    if subreddit_name == "Showerthoughts":
        for submission in reddit.subreddit(subreddit_name).hot(limit=None):
            if submission.is_self:
                query_result = Posts.query.filter(Posts.name == submission.id).first()

                if query_result is None:
                    post = Posts(submission.id, submission.title)
                    user.posts.append(post)
                    db.session.commit()
                    payload = submission.title
                    break

                elif user not in query_result.users:
                    user.posts.append(query_result)
                    db.session.commit()
                    payload = submission.title
                    break
                else:
                    continue

        r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                          params={"access_token": token},
                          data=json.dumps({
                              "recipient": {"id": recipient},
                              "message": {"text": payload,
                                          "quick_replies": quick_replies_list}
                          }),
                          headers={'Content-type': 'application/json'})
    elif subreddit_name == "Jokes":
        for submission in reddit.subreddit(subreddit_name).hot(limit=None):
            if (submission.is_self == True) and (submission.link_flair_text is None):
                query_result = Posts.query.filter(Posts.name == submission.id).first()
                if query_result is None:
                    post = Posts(submission.id, submission.title)
                    user.posts.append(post)
                    db.session.commit()
                    payload = submission.title
                    payload_text = submission.selftext
                    break
                elif user not in query_result.users:
                    user.posts.append(query_result)
                    db.session.commit()
                    payload = submission.title
                    payload_text = submission.selftext
                    break
                else:
                    continue

        r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                          params={"access_token": token},
                          data=json.dumps({
                              "recipient": {"id": recipient},
                              "message": {"text": payload_text,
                                          "quick_replies": quick_replies_list}
                          }),
                          headers={'Content-type': 'application/json'})

    else:
        payload = "http://imgur.com/WeyNGtQ.jpg"
        for submission in reddit.subreddit(subreddit_name).hot(limit=None):
            if (submission.link_flair_css_class == 'image') or (
                        (submission.is_self != True) and ((".jpg" in submission.url) or (".png" in submission.url))):
                query_result = Posts.query.filter(Posts.name == submission.id).first()
                if query_result is None:
                    post = Posts(submission.id, submission.url)
                    user.posts.append(post)
                    db.session.commit()
                    payload = submission.url
                    break
                elif user not in query_result.users:
                    user.posts.append(query_result)
                    db.session.commit()
                    payload = submission.url
                    break
                else:
                    continue

        r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                          params={"access_token": token},
                          data=json.dumps({
                              "recipient": {"id": recipient},
                              "message": {"attachment": {
                                  "type": "image",
                                  "payload": {
                                      "url": payload
                                  }},
                                  "quick_replies": quick_replies_list}
                          }),
                          headers={'Content-type': 'application/json'})

    if r.status_code != requests.codes.ok:
        click.echo(click.style(r.text, fg="green", bold=True))


def get_or_create(session, model, **kwargs):
    """
    checks whether a user with the particular name exists or not. 
    If it exists it selects that user from the db and returns it. In case it doesn’t exist
     (user), it creates it and then returns that newly created user:
    :param session: 
    :param model: 
    :param kwargs: 
    :return: 
    """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance
