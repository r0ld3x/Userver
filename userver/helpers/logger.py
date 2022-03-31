import logging
import os
from loguru import logger


class InterceptHandler(logging.Handler):
    LEVELS_MAP = {
        logging.CRITICAL: "CRITICAL",
        logging.ERROR: "ERROR",
        logging.WARNING: "WARNING",
        logging.INFO: "INFO",
        logging.DEBUG: "DEBUG",
    }

    def _get_level(self, record):
        return self.LEVELS_MAP.get(record.levelno, record.levelno)

    def emit(self, record):
        logger_opt = logger.opt(
            depth=6, exception=record.exc_info, ansi=True, lazy=True
        )
        logger_opt.log(self._get_level(record), record.getMessage())


logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)
log = logging.getLogger(__name__)
TelethonLogger = logging.getLogger("Telethon")
TelethonLogger.setLevel("INFO")


if os.path.exists('userver.log'):
    os.remove('userver.log')


logger.add(
    "userver.log",
    format = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    # format = "%(name)s - %(asctime)-15s - %(level)s: %(message)s",
    rotation="5 days",
    compression="tar.xz",
    backtrace=True,
    diagnose=True,
    level="INFO",
    colorize=True,
)

log.info(f"Enabled logging intro userver.log file.")