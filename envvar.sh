#!/usr/bin/env bash

export DATABASE_URL="postgresql://lusinabrian:g4110wsclyve7#@localhost/redditbot"
export FLASK_COVERAGE="1"
export FLASK_CONFIG="develop"
export REDDIT_CLIENT_SECRET="GXBuw8zHOc286OfBS7mXb0njA6c"
export REDDIT_CLIENT_ID="RgVuetGp6Y5qGQ"
export REDDIT_APP_NAME="RedditFacebookBot"
export REDDIT_REDIRECT_URI="https://redditfacebookbot.herokuapp.com/"
export FACEBOOK_PAGE_ACCESS_TOKEN="EAADhbWtdJQkBAMZBcgkz4ZByAM1MgXAHQcUnvBmJ8M8vHsYyZCxWecMtpCQ6d9ZCr9ilU06ENUWbE67CnbNKjFZAE59u6VPFrvptQdVL3OXOVvdk56VfbicIjdvNFv5oUjL3wzFNzVZClQfrvenMthPisoflfQ6zWwyGl8bEyQHAZDZD"
export FACEBOOK_WEBHOOK_VERIFY_TOKEN="redditfb_bot_its_me"
export USER_AGENT="redditfbbot_user_agent"
export POSTGRES_USER="lusinabrian"
export POSTGRES_DB="redditbot"
export POSTGRES_PASSWORD="g4110wsclyve7#"
export SECRET_KEY="T0ea9e0a2S80bac408/c81703b89204e3?Vde1f0d6bfea89ga31c0-Ov"
export CSRF_SESSION_KEY="868d96ad.desd3b9Vd9c1becc1ad9e7ba89kQ86aX15eaf11ceaEz94ps"
export SECURITY_PASSWORD_SALT="d1a89b81d7ebafd7c40cee1310Bc8abf938bod7fagN00fb8ba0ltq9d8fbc"
export ADMIN_EMAIL_1="chiefsdome@gmail.com"
export FLASK_CONFIG="develop"
export MAIL_USERNAME="chiefsdome@gmail.com"
export MAIL_PASSWORD="eyqydbvwinqiimar"
export MAIL_DEFAULT_SENDER="chiefsdome@gmail.com"

heroku addons:add heroku-postgresql:hobby-dev
heroku pg:promote HEROKU_POSTGRESQL_JADE_URL

# setting configuration variables on heroku
heroku config:set DATABASE_URL="postgresql://lusinabrian:g4110wsclyve7#@localhost/hadithi"
heroku config:set DATABASE_URL=postgresql://lusinabrian:g4110wsclyve7#@localhost/redditbot
heroku config:set FLASK_COVERAGE=1
heroku config:set FLASK_CONFIG=develop
heroku config:set REDDIT_CLIENT_SECRET=GXBuw8zHOc286OfBS7mXb0njA6c
heroku config:set REDDIT_CLIENT_ID=RgVuetGp6Y5qGQ
heroku config:set REDDIT_APP_NAME=RedditFacebookBot
heroku config:set REDDIT_REDIRECT_URI=https://redditfacebookbot.herokuapp.com/
heroku config:set FACEBOOK_PAGE_ACCESS_TOKEN=EAADhbWtdJQkBAMZBcgkz4ZByAM1MgXAHQcUnvBmJ8M8vHsYyZCxWecMtpCQ6d9ZCr9ilU06ENUWbE67CnbNKjFZAE59u6VPFrvptQdVL3OXOVvdk56VfbicIjdvNFv5oUjL3wzFNzVZClQfrvenMthPisoflfQ6zWwyGl8bEyQHAZDZD
heroku config:set FACEBOOK_WEBHOOK_VERIFY_TOKEN=redditfb_bot_its_me
heroku config:set USER_AGENT=redditfbbot_user_agent
heroku config:set POSTGRES_USER=lusinabrian
heroku config:set POSTGRES_DB=redditbot
heroku config:set POSTGRES_PASSWORD=g4110wsclyve7#
heroku config:set SECRET_KEY=T0ea9e0a2S80bac408/c81703b89204e3?Vde1f0d6bfea89)ga31c0-Ov
heroku config:set CSRF_SESSION_KEY=868d96ad.desd3b9Vd9c1becc1ad9e7ba89kQ86aX15eaf11ceaEz94|]
heroku config:set SECURITY_PASSWORD_SALT=d1a89b81d7ebafd7c40cee1310Bc8abf938bod7fagN00fb8ba0;tq9d8fbc
heroku config:set ADMIN_EMAIL_1=chiefsdome@gmail.com
heroku config:set FLASK_CONFIG=develop
heroku config:set MAIL_USERNAME=chiefsdome@gmail.com
heroku config:set MAIL_PASSWORD=eyqydbvwinqiimar
heroku config:set MAIL_DEFAULT_SENDER=chiefsdome@gmail.com


# run migrations
heroku run python manage.py db init
heroku run python manage.py db migrate
heroku run python manage.py db upgrade
heroku run python manage.py create_db

#connect to remote db
heroku pg:psql

# create a new db with
heroku pg:reset DATABASE

# push db to heroku
heroku pg:push hadithi HEROKU_POSTGRESQL_AQUA --app redditfacebookbot