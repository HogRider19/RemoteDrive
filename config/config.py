from dotenv import load_dotenv
import os


load_dotenv()

SECRETKEY = os.getenv('secret_key')
