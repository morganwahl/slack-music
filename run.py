import os


def get_tune_from_jabber_file():
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
        return u''
    tune = objectify.parse(jabber_file).getroot()
    os.unlink(jabber_file)
    return u"{}: {}".format(tune.artist, tune.title)


def get_tune_from_quodlibet():
    import subprocess
    try:
        return subprocess.check_output((
            'quodlibet',
            '--print-playing', '<artist>: <title>',
        )).strip()
    except subprocess.CalledProcessError:
        return u''


def set_status(text='', emoji=''):
    import json
    from slacker import Slacker
    token = os.environ['SLACK_SECRET_TOKEN']

    slack = Slacker(token)
    # print slack.users.profile.get()
    status = json.dumps({
        'status_text': text,
        u'status_emoji': emoji,
    })
    # print status
    slack.users.profile.set(profile=status)


def main():
    tune = get_tune_from_quodlibet()
    if tune:
        message = tune
        emoji = u':musical_note:'
    else:
        message = u''
        emoji = u''
    set_status(text=message, emoji=emoji)


if __name__ == '__main__':
    main()
