import os
from dotenv import load_dotenv

load_dotenv()

print('The token : ' , os.environ.get('TOKEN'))