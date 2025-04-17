import inspect
import logging.config

from conf.log import LOGGING_CONFIG
from conf.vars import LOGGER_TO_USE


__all__ = ['Log']


logging.config.dictConfig(LOGGING_CONFIG)
LOGGER = logging.getLogger(LOGGER_TO_USE)


class Log:
    @staticmethod
    def _send_log(log_level: str, **kwargs) -> None:
        _logger = getattr(LOGGER, log_level)

        _logger(kwargs.get('message'), extra={
            'data': kwargs.get('data'),
            'method_info': {'file_path': kwargs.get('file_path'), 'method': kwargs.get('method')}
        })
        return

    @classmethod
    def info(cls, message: str,  data: dict = None):
        _inspect = inspect.stack()
        file_path = _inspect[1].filename
        method = _inspect[1].function
        cls._send_log(log_level='info',
                      message=message,
                      data=data,
                      file_path=file_path,
                      method=method)

    @classmethod
    def warning(cls, message: str, data: dict = None):
        _inspect = inspect.stack()
        file_path = _inspect[1].filename
        method = _inspect[1].function
        cls._send_log(log_level='warning',
                      message=message,
                      data=data,
                      file_path=file_path,
                      method=method)

    @classmethod
    def error(cls, message: str, data: dict = None):
        _inspect = inspect.stack()
        file_path = _inspect[1].filename
        method = _inspect[1].function
        cls._send_log(log_level='error',
                      message=message,
                      data=data,
                      file_path=file_path,
                      method=method)
