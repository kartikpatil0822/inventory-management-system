import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    today_date = datetime.now().strftime('%Y-%m-%d')
    log_file_path = os.path.join(log_dir, f'{today_date}_ims.log')

    handler = TimedRotatingFileHandler(log_file_path, when='midnight', interval=1, backupCount=7)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


if __name__ == "__main__":
    setup_logging()
