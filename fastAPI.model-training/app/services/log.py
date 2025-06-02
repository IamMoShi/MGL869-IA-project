import inspect
import logging

logger = logging.getLogger("uvicorn")


def clean_info_log(message: str):
    frame = inspect.currentframe().f_back
    logger.info(
        f"[{frame.f_globals['__name__']}.{frame.f_code.co_name} - {frame.f_lineno}] - {message}"
    )
