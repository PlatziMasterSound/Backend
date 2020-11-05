import os

from app import create_app
from config import default

settings_module = default
app = create_app(settings_module)

