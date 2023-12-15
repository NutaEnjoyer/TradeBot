from .main.main import register_handlers
from .helper.main import register_handlers as helper
from .main.worker import register_worker_handlers

def register(dp):
	handlers = (
		register_handlers,
		register_worker_handlers
	)
	for handler in handlers:
		handler(dp)

def register_helper(dp):
	helper(dp)


def foo(*args):
	print(*args)