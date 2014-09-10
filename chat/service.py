# Nameko relies on eventlet
# You should monkey patch the standard library as early as possible to avoid
# importing anything before the patch is applied.
# See http://eventlet.net/doc/patching.html#monkeypatching-the-standard-library
import eventlet
eventlet.monkey_patch()

import logging

from nameko.events import event_handler, event_dispatcher, Event, BROADCAST
from nameko.runners import ServiceRunner


from dependencies.stdin import stdin
from dependencies.stdout import stdout
from dependencies.once import once
from dependencies.user import user


class Message(Event):
    type = "message"

    def __init__(self, author, msg):
        self.data = {
            'author': author,
            'msg': msg
        }


class Chat(object):

    dispatch = event_dispatcher()
    stdout = stdout()
    user = user()

    def send_message(self, msg):
        event = Message(self.user.username, msg)
        self.dispatch(event)

    def prompt(self):
        self.stdout.write(">>> ")
        self.stdout.flush()

    @once
    def login(self):
        self.stdout.write("Please enter your name:\n")
        self.prompt()

    @stdin
    def handle_stdin(self, line):
        if not self.user.logged_in:
            self.user.login(line)
            self.stdout.write(
                'Welcome to chat, {}!\n'.format(self.user.username))
            self.prompt()
        else:
            self.send_message(line)

    @event_handler('chat', 'message',
                   handler_type=BROADCAST, reliable_delivery=False)
    def handle_message(self, event_data):
        if not self.user.logged_in:
            return

        author = event_data.get('author')
        msg = event_data.get('msg')
        out = "\r{}: {}\n".format(author, msg)
        self.stdout.write(out)
        self.prompt()


def main():

    logging.basicConfig(level=logging.DEBUG)

    # disable most logging so we can see the console
    logger = logging.getLogger('')
    logger.setLevel(logging.WARNING)

    config = {'AMQP_URI': 'amqp://guest:guest@localhost:5672/chat'}
    runner = ServiceRunner(config)
    runner.add_service(Chat)
    runner.start()
    try:
        runner.wait()
    except KeyboardInterrupt:
        runner.stop()

if __name__ == '__main__':
    main()
