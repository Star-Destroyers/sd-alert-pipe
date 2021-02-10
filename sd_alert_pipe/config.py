from pydantic import BaseSettings 
from typing import Set


class Settings(BaseSettings):
    """Settings for various brokers, API keys, etc.
    Environmental variables take precedence.
    See https://pydantic-docs.helpmanual.io/usage/settings/
    """
    LASAIR_API_KEY: str = '4b762569bb349bd8d60f1bc7da3f39dbfaefff9a'
    LASAIR_WATCHLISTS: Set[int] = {139}


settings = Settings()
