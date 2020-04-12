# settings.py
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), 'script.env')
load_dotenv(dotenv_path)

print(dirname(__file__))

# Accessing variables.
apiEntityId = os.getenv('apiEntityId')
git_token = os.getenv('git-token')

# Using variables.
print(apiEntityId)
print(git_token)