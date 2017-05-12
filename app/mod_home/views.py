from . import home
from flask import request
import json
import requests
import click

# This needs to be filled with the Page Access Token that will be provided
# by the Facebook App that will be created.
PAT = ''


@home.route('', methods=['GET'])
def handle_verification():
    click.echo(click.style("Handling Verification.", fg="green", bold=True, bg="black"))
    if request.args.get('hub.verify_token', '') == 'my_voice_is_my_password_verify_me':
        click.echo(click.style("Verification successful!", fg="green", bold=True, bg="black"))
        return request.args.get('hub.challenge', '')
    else:
        click.echo(click.style("Verification failed!", fg="green", bold=True, bg="black"))
        return 'Error, wrong validation token'


@home.route('', methods=['POST'])
def handle_messages():
    click.echo(click.style("Handling Messages", fg="green", bold=True, bg="black"))
    payload = request.get_data()
    click.echo(click.style("Payload: {}".format(payload), fg="green", bold=True, bg="black"))
    for sender, message in messaging_events(payload):
        click.echo(click.style("Incoming from %s: %s" % (sender, message), fg="green", bold=True, bg="black"))
        send_message(PAT, sender, message)
    return "ok"


def messaging_events(payload):
    """Generate tuples of (sender_id, message_text) from the
    provided payload.
    """
    data = json.loads(payload)
    messaging_events = data["entry"][0]["messaging"]
    for event in messaging_events:
        if "message" in event and "text" in event["message"]:
            yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
        else:
            yield event["sender"]["id"], "I can't echo this"


def send_message(token, recipient, text):
    """Send the message text to recipient with id recipient.
    """

    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params={"access_token": token},
                      data=json.dumps({
                          "recipient": {"id": recipient},
                          "message": {"text": text.decode('unicode_escape')}
                      }),
                      headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        click.echo(click.style(r.text, fg="green", bold=True, bg="black"))

