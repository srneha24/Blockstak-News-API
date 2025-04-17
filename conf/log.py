import os
from logging import Formatter, LogRecord
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)


class LocalFormatter(Formatter):
    def format(self, record: LogRecord):
        all_data = record.__dict__
        data = all_data.get('data')
        message = record.msg
        record.msg = f'{record.levelname}: MSG:{message} - DATA:{data} - {datetime.now().isoformat()}'
        return super().format(record)


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default_formatter': {
            'format': '[%(levelname)s:%(asctime)s] %(message)s'
        },
        "local": {
            "class": 'conf.log.LocalFormatter'
        }
    },
    'handlers': {
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "default_formatter",
        },
        "file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": f"{BASE_DIR}/logs/blockstak_news_api.log",
            "formatter": "local",
            "interval": 1,
            'backupCount': 5
        },
        "local": {
            "class": "logging.StreamHandler",
            "formatter": "local"
        }
    },
    'loggers': {
        'blockstak_news_api': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True
        },
        'file': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True
        },
        "local": {
            'handlers': ['local'],
            'level': 'INFO',
            'propagate': True
        }
    }
}
