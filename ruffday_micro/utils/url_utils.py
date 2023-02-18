""" Utils to help with URL redirects """
import os
from core.config import Settings


def get_base_url():
    env = os.environ.get(Settings.ENVIONMENT_LABEL)

    if env == "local":
        return "http://localhost:8000/"
    else:
        return "https://ruffday.ca"
