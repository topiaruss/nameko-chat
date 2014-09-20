import sys

from eventlet import tpool
from nameko.dependencies import (
    EntrypointProvider, entrypoint, DependencyFactory)
from nameko.exceptions import ContainerBeingKilled


class StdinProvider(EntrypointProvider):
    def __init__(self):
        self._gt = None
        self._stdin = tpool.Proxy(sys.stdin)

    def _run(self):
        while True:
            line = self._stdin.readline()

            args = (line.strip(),)
            kwargs = {}

            try:
                self.container.spawn_worker(self, args, kwargs)
            except ContainerBeingKilled:
                pass

    def start(self):
        gt = self.container.spawn_managed_thread(self._run, protected=True)
        self._gt = gt

    def stop(self):
        if self._gt is not None:
            self._gt.kill()


@entrypoint
def stdin():
    """ Receive messages from `sys.stdin`
    """
    return DependencyFactory(StdinProvider)
