import os
from os import getenv

# ------------------------------------------------

API_ID = int(os.environ.get("API_ID", "28795512"))
API_HASH = os.environ.get("API_HASH", "c17e4eb6d994c9892b8a8b6bfea4042a")

# ------------------------------------------------

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
BOT_USERNAME = os.environ.get("BOT_USERNAME", "Vcznbot")

# -----------------------------------------------

OWNER_ID = int(os.environ.get("OWNER_ID", "7682307978"))
SPECIAL_ID = int(os.environ.get("SPECIAL_ID", "7682307978"))
# ------------------------------------------------

# ------------------------------------------------
LOGGER_ID = int(os.environ.get("LOGGER_ID", "-100"))
OTHER_LOGS = int(os.environ.get("OTHER_LOGS", "-100"))

# ------------------------------------------------

MONGO_URL = os.environ.get("MONGO_URL", "")

# ------------------------------------------------
