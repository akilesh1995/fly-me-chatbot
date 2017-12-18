# Fly Me - An Airline Customer Service Chatbot

Fly Me is a simple customer service chatbot that leverages the Facebook Messenger API. The application is deployed on Heroku. It makes use of popular python-NLP packages such as NLTK for text classification and spaCy for entity recognition and part-of-speech tagging.

## Installing dependencies

Use of virtualenv is recommended. Make sure pip in installed before running this command.

    $ pip install -r requirements.txt

## Setting up a Facebook app for Facebook messenger

* Your applications needs to be deployed on a server. I have used heroku for this. Follow instructions provided on this [blog post](https://tsaprailis.com/2016/06/02/How-to-build-and-deploy-a-Facebook-Messenger-bot-with-Python-and-Flask-a-tutorial/)
* You also need to configure the webhooks to your applications. Use this [tutorial](https://tutorials.botsfloor.com/creating-your-messenger-bot-4f71af99d26b) and setup your messenger app and webhooks.

## Demos
* You can find images of the application [here](https://imgur.com/a/SrEXZ) and [here](https://imgur.com/a/HgdoA).
* Here is a small demo video on [YouTube]().


## Contact
Feel free to contact me in case of any queries / suggestions via [mail](mailto:akilesh1995@gmail.com) or [twitter](https://twitter.com/leshtalks).


## TODO

* Tests
* Handle postbacks
* Messenger app beautification using API capabilities
* Improve NLP capabilities by building custom language models on spaCy