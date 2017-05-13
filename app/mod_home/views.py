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
    return "Hello world"
