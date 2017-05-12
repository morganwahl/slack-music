#!/usr/bin/env python3

import os

import logging
L = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARN)

L.debug('__main__')


def get_tune_from_jabber_file():
    L.debug("get_tune_from_jabber_file")
    from lxml import objectify

    # <tune xmlns='http://jabber.org/protocol/tune'>
    #  <artist>%s</artist>
    #  <title>%s</title>
    #  <source>%s</source>
    #  <track>%d</track>
    #  <length>%d</length>
    # </tune>
    jabber_file = os.path.join(
        os.environ['HOME'],
        '.quodlibet',
        'jabber',
    )
    if not os.path.exists(jabber_file):
        return ''
    tune = objectify.parse(jabber_file).getroot()
    os.unlink(jabber_file)
    return "{}: {}".format(tune.artist, tune.title)


def get_tune_from_quodlibet():
    L.debug("get_tune_from_quodlibet")
    import subprocess
    try:
        L.debug("running quodlibet")
        return subprocess.check_output((
            'quodlibet',
            '--print-playing', '<artist>: <title>',
            # quodlibet sometimes prints spurious error messages on stderr.
            # Make sure those don't get printed since we're running in a cron
            # job.
        ), stderr=subprocess.DEVNULL).decode('utf8').strip()
    except subprocess.CalledProcessError:
        return ''


def set_status(text='', emoji=''):
    L.debug("set_status %r %r", text, emoji)
    import json
    from slacker import Slacker
    token = os.environ['SLACK_SECRET_TOKEN']

    slack = Slacker(token)
    # print slack.users.profile.get()
    status = json.dumps({
        'status_text': text,
        'status_emoji': emoji,
    })
    # print status
    slack.users.profile.set(profile=status)


def main():
    L.debug("main")
    tune = get_tune_from_quodlibet()
    if tune:
        message = tune
        emoji = ':musical_note:'
    else:
        message = ''
        emoji = ''
    set_status(text=message, emoji=emoji)


if __name__ == '__main__':
    main()
