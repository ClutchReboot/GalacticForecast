from dotenv import load_dotenv
import os
from pathlib import Path

# Used to keep dotenv isolated from default logging
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
