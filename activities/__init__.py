from dotenv import dotenv_values
from pathlib import Path

# Used to keep dotenv isolated from default logging
env_path = Path(__file__).resolve().parent.parent / ".env"
config = dotenv_values(dotenv_path=env_path)
