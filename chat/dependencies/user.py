from nameko.dependencies import (
    InjectionProvider, injection, DependencyFactory)


class UserState(object):
    username = None

    @property
    def logged_in(self):
        return self.username is not None

    def login(self, username):
        self.username = username


class UserProvider(InjectionProvider):

    def __init__(self):
        self.state = UserState()

    def acquire_injection(self, worker_ctx):
        return self.state


@injection
def user():
    return DependencyFactory(UserProvider)
