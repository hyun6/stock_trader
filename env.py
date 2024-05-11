from dotenv import load_dotenv
import os

load_dotenv()

def get(env_name: str) -> str:
    return os.environ.get(env_name)