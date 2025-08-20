"""
Configuration settings loaded from environment variables.
"""
from os import getenv
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Intercom settings
INTERCOM_ACCESS_TOKEN = getenv('INTERCOM_ACCESS_TOKEN')
INTERCOM_AUTHOR_ID = getenv('INTERCOM_AUTHOR_ID')

# Review mode
REVIEW_MODE = getenv('REVIEW_MODE', 'True').lower() == 'true'
AUTO_PUBLISH = getenv('AUTO_PUBLISH', 'False').lower() == 'true'