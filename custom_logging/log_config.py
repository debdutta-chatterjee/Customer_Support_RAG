import logging
import os
from datetime import datetime


LOG_DIR = os.path.join(os.getcwd(), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = f'{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log'
LOG_FILE_PATH = os.path.join(LOG_DIR,LOG_FILE)


#Logging config
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE_PATH),
        logging.StreamHandler()
    ]
)


logger = logging.getLogger('custom_support_logger')