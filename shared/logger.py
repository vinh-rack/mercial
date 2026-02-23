import json
import logging
from datetime import datetime
from logging import Formatter, LogRecord
from logging.handlers import RotatingFileHandler
from pathlib import Path

from shared.config import settings

LOG_LEVEL = getattr(logging, settings.log_level.upper(), logging.INFO)


class TraceFormatter(Formatter):
    def format(self, record: LogRecord):
        return super().format(record)


class JsonFormatter(Formatter):
    def format(self, record: LogRecord) -> str:
        log = {
            "timestamp": datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
            "level": record.levelname,
            "service": record.name,
            "message": record.getMessage(),
        }

        metadata = {}
        for key, value in record.__dict__.items():
            if key not in ("filename", "levelname", "msg", "args", "exc_info", "exc_text", "stack_info"):
                if key not in log and not key.startswith("_"):
                    metadata[key] = value

        if metadata:
            log["metadata"] = metadata

        if record.exc_info:
            log["exception"] = self.formatException(record.exc_info)

        return json.dumps(log)


CONSOLE_FORMATTER = TraceFormatter("[ %(levelname)s ] %(message)s")
FILE_FORMATTER = JsonFormatter()


def setup_logger(name: str, log_file: str = None) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    logger.propagate = False

    if not logger.handlers:
        if log_file:
            log_file_path = Path(log_file) if Path(log_file).is_absolute() else Path(settings.log_dir) / log_file
            log_file_path.parent.mkdir(parents=True, exist_ok=True)
            log_file_path.touch(exist_ok=True)

            file_handler = RotatingFileHandler(
                log_file_path, maxBytes=5_000_000, backupCount=5, encoding="utf-8"
            )
            file_handler.setFormatter(FILE_FORMATTER)
            file_handler.setLevel(LOG_LEVEL)
            logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(CONSOLE_FORMATTER)
        console_handler.setLevel(LOG_LEVEL)
        logger.addHandler(console_handler)

    return logger
