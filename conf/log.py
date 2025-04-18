from logging import Formatter, LogRecord
from datetime import datetime


class LocalFormatter(Formatter):
    """Custom formatter for logging locally."""

    def format(self, record: LogRecord):
        all_data = record.__dict__
        data = all_data.get("data")
        message = record.msg
        record.msg = f"{record.levelname}: MSG:{message} - DATA:{data} - {datetime.now().isoformat()}"
        return super().format(record)


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default_formatter": {"format": "[%(levelname)s:%(asctime)s] %(message)s"},
        "local": {"class": "conf.log.LocalFormatter"},
    },
    "handlers": {
        "stream_handler": {
            "class": "logging.StreamHandler",
            "formatter": "default_formatter",
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "default_formatter",
        },
        "local": {"class": "logging.StreamHandler", "formatter": "local"},
    },
    "loggers": {
        "blockstak_news_api": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "local": {"handlers": ["local"], "level": "INFO", "propagate": True},
    },
}
