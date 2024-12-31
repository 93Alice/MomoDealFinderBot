""" 
This module handles environment variable operations. 
"""

import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

def get_env_var(var_name):
    """
    Retrieve an environment variable's value or return a default value.
    """
    return os.getenv(var_name)
