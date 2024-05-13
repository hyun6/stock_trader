from enum import StrEnum
from dotenv import load_dotenv
import os

load_dotenv()

class EnvNames(StrEnum):
    APPKEY = 'APPKEY'
    APPSECRET = 'APPSECRET'
    TELEGRAM_TOKEN = 'TELEGRAM_TOKEN'
    TELEGRAM_CHAT_ID = 'TELEGRAM_CHAT_ID'


def get(env_name: EnvNames) -> str:
    return os.environ.get(env_name)