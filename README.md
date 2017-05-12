# Reddit Facebook Bot

Reddit facebook bot made with flask.

### Requirements

You will need a couple of things for setting up

1. Facebook Account
    
   This will be for both the facebook page and the developer account
    Create a facebook page [here](https://www.facebook.com/pages/create) and an application [here](https://developers.facebook.com/apps/)
    
    From there, you will need to add a product to the newly created application [here](https://developers.facebook.com/apps/)
    
    You will then need to create a token and save the `PAGE ACCESS TOKEN` you will receive from Facebook
    
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

For a detailed description check [here](https://pythontips.com/2017/04/13/making-a-reddit-facebook-messenger-bot/?utm_source=mybridge&utm_medium=blog&utm_campaign=read_more)