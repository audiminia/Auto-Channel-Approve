from os import getenv
import dotenv

dotenv.load_dotenv('config.env')

class Config:
    API_ID = int(getenv("API_ID"))
    API_HASH = getenv("API_HASH")
    BOT_TOKEN = getenv("BOT_TOKEN")
    CHAT_ID = int(getenv("CHAT_ID"))
    APPROVED_WELCOME=getenv("APPROVED_WELCOME").lower()
    SUDO = list(map(int, getenv("SUDO").split()))
    MONGO_URI = getenv("MONGO_URI", "")

cfg = Config()
