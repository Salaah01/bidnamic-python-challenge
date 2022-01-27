from .base import *  # noqa: F403, F401

DEBUG = True
ALLOWED_HOSTS = ["*"]

# Enabling template debug option for coverage tests.
TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG  # noqa: F405
