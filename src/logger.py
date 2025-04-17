import asyncio
import logging
from functools import wraps

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("execution.log", mode="w"),
    ],
)


def log_execution(func):
    """Decorator para logar execução de funções assíncronas e síncronas."""

    if asyncio.iscoroutinefunction(func):

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            logging.info(f"[ASYNC] Iniciando: {func.__name__} | Args: {args} | Kwargs: {kwargs}")
            try:
                result = await func(*args, **kwargs)
                logging.info(f"[ASYNC] Finalizado: {func.__name__} -> Retorno: {result}")
                return result
            except Exception as e:
                logging.error(f"[ASYNC] Erro em {func.__name__}: {e}", exc_info=True)
                raise

        return async_wrapper
    else:

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            logging.info(f"[SYNC] Iniciando: {func.__name__} | Args: {args} | Kwargs: {kwargs}")
            try:
                result = func(*args, **kwargs)
                logging.info(f"[SYNC] Finalizado: {func.__name__} -> Retorno: {result}")
                return result
            except Exception as e:
                logging.error(f"[SYNC] Erro em {func.__name__}: {e}", exc_info=True)
                raise

        return sync_wrapper
