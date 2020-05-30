from .common import *  # noqa

ALLOWED_HOSTS = ["*"]


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"level": "DEBUG", "class": "logging.StreamHandler"}},
    "loggers": {"": {"handlers": ["console"], "propagate": False, "level": "WARNING"}},
}
