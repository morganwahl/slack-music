import json

from slacker import Slacker
import IPython

_SECRET_TOKEN = 'xoxp-3312287274-5079590165-168774511872-d8bde62260ad21dc64c21513ef348536'

def get_tune():
    # <tune xmlns='http://jabber.org/protocol/tune'>
    #  <artist>%s</artist>
    #  <title>%s</title>
    #  <source>%s</source>
    #  <track>%d</track>
    #  <length>%d</length>
    # </tune>

def set_status(text='', emoji=''):
    slack = Slacker(_SECRET_TOKEN)
    # print slack.users.profile.get()
    status = json.dumps({
        'status_text': text,
        u'status_emoji': emoji,
    })
    # print status
    # print slack.users.profile.set(profile=status)

def main():
    # Read the tune file
    artist, title = get_tune()
    message = u"{}: {}".format(artist, title)
    emoji = u':musical_note:'
    set_status(text=message, emoji=emoji)


if __name__ == '__main__':
    main()
