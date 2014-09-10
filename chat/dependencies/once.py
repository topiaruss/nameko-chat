from nameko.dependencies import (
    EntrypointProvider, entrypoint, DependencyFactory)
from nameko.exceptions import ContainerBeingKilled


class OnceProvider(EntrypointProvider):

    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs

    def start(self):
        try:
            self.container.spawn_worker(self, self.args, self.kwargs)
        except ContainerBeingKilled:
            pass


@entrypoint
def once(*args, **kwargs):
    """ Fire the decorated entrypoint once, immediately.
    """
    return DependencyFactory(OnceProvider, args, kwargs)
