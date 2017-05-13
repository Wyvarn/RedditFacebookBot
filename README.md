# Reddit Facebook Bot

A simple `motivational` Reddit facebook messenger bot made with flask.

### Requirements

You will need a couple of things for setting up

1. __Facebook Account__
    
   This will be for both the facebook page and the developer account
    Create a facebook page [here](https://www.facebook.com/pages/create) and an application [here](https://developers.facebook.com/apps/)
    
    From there, you will need to add a product to the newly created application [here](https://developers.facebook.com/apps/)
    
    You will then need to create a token and save the `PAGE ACCESS TOKEN` you will receive from Facebook

2. __Heroku Account__
    
   This will be used to deploy the application. A handy tool to have is the [heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) 

3. __Reddit Account__

   This will be used when setting up an application with Reddit for retrieving motivational images and quotes.
   
   Create a Reddit application [here](https://www.reddit.com/prefs/apps/).
   
   After which save the client id and secret you will get from reddit.
  

### Setup

Setting up is really simple and requires a simple cloning of the repo and installing dependencies

Simply clone this repo and do the following:

```bash
cd redditfacebookbot
virtualenv -p python3 venv
. venv/bin/activate
pip install -r requirements.txt
```
> This sets up the environment for use

Next, you will need to create an environment file from which the application will pick up the required environment variables

```bash
touch .env
export REDDIT_CLIENT_SECRET=<YOUR_CLIENT_SECRET> >> .env
export REDDIT_CLIENT_KEY=<YOUR_CLIENT_KEY> >> .env
...
# other environmnent variables you will need
# such as DATABASE_URL,
```
> Although this .env file will not be pushed to production, it will be good for local testing and development

Another setup that may be needed is a `praw.ini` file. Although not necessary it will be easier to interact with Reddit API through this file. This allows setting up your configurations with the `praw` library from Reddit and will be parsed by the `praw` library when the application starts.

Check [praw.copy.ini](praw.copy.ini) file for a bit more information and also [here](https://praw.readthedocs.io/en/latest/index.html) for a complete reference when interacting with Reddit API


For a detailed description check 
[here](https://pythontips.com/2017/04/13/making-a-reddit-facebook-messenger-bot/?utm_source=mybridge&utm_medium=blog&utm_campaign=read_more) and [here](https://tsaprailis.com/2016/06/02/How-to-build-and-deploy-a-Facebook-Messenger-bot-with-Python-and-Flask-a-tutorial/)
