import sys

from nameko.dependencies import (
    InjectionProvider, injection, DependencyFactory)


class StdoutProvider(InjectionProvider):
    def acquire_injection(self, worker_ctx):
        return sys.stdout

    def stop(self):
        sys.stdout.write('\n')
        sys.stdout.flush()


@injection
def stdout():
    return DependencyFactory(StdoutProvider)
