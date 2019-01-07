import facebook
import requests


def some_action(post):
    """ Here you might want to do something with each post. E.g. grab the
    post's message (post['message']) or the post's picture (post['picture']).
    In this implementation we just print the post's created time.
    """
    print(post["created_time"])


# You'll need an access token here to do anything.  You can get a temporary one
# here: https://developers.facebook.com/tools/explorer/
access_token = "2007205232652231|ExJRTwx6yD8EvanojkQgE_-WxyU"
# Look at Bill Gates's profile for this example by using his Facebook id.
user = "me"

graph = facebook.GraphAPI(access_token)
profile = graph.get_object(user)

print(profile)

