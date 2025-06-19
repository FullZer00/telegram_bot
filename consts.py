import os
from dotenv import load_dotenv

load_dotenv()

class Sites:
    REPO = os.getenv("GH_REPO")