import contextvars
import functools
import inspect
import time
import uuid
from typing import Any, Callable, Optional

from src.utils.logger import setup_logger

LOGGER = setup_logger(__name__, "traced_operations.log")

# CONTEXT VARS
# for storing trace IDs
# (thread-safe and async-safe)
request_id_var: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar('request_id', default=None)
session_id_var: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar('session_id', default=None)

# HELPER FUNCS
def generate_request_id() -> str:
    return f"req_{uuid.uuid4().hex[:16]}"


def generate_session_id() -> str:
    return f"sess_{uuid.uuid4().hex[:16]}"


def set_request_id(request_id: str) -> None:
    request_id_var.set(request_id)


def set_session_id(session_id: str) -> None:
    session_id_var.set(session_id)


def get_request_id() -> Optional[str]:
    return request_id_var.get()


def get_session_id() -> Optional[str]:
    return session_id_var.get()


def get_trace_context() -> dict:
    return {
        "request_id": get_request_id(),
        "session_id": get_session_id()
    }


def format_trace_prefix() -> str:
    req_id = get_request_id()
    sess_id = get_session_id()

    parts = []
    if sess_id:
        parts.append(f"[ {sess_id} ]")
    if req_id:
        parts.append(f"[ {req_id} ]")

    return " ".join(parts) if parts else ""


def traced_operation(operation_name: str = None):
    """Decorator to trace function execution with timing and error handling."""

    def decorator(func: Callable) -> Callable:
        op_name = operation_name or func.__name__

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            trace_ctx = get_trace_context()
            LOGGER.info(f"[ RUN ] {op_name}")

            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                elapsed = time.time() - start_time
                LOGGER.info(f"[ OK ] {op_name} in {elapsed:.3f}s")
                return result
            except Exception as e:
                elapsed = time.time() - start_time
                LOGGER.error(f"{op_name} after {elapsed:.3f}s - Error: {str(e)}", exc_info=True)
                raise

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            trace_ctx = get_trace_context()
            LOGGER.info(f"[ RUN ] {op_name}")

            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                elapsed = time.time() - start_time
                LOGGER.info(f"[ OK ] {op_name} in {elapsed:.3f}s")
                return result
            except Exception as e:
                elapsed = time.time() - start_time
                LOGGER.error(f"{op_name} after {elapsed:.3f}s - Error: {str(e)}", exc_info=True)
                raise

        # Return appropriate wrapper
        # after inspecting the func type
        if inspect.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator

# OPERATION TRACER CLASS
class OperationTracer:
    """Context manager for tracing operations with automatic timing and logging."""

    def __init__(self, operation_name: str):
        self.operation_name = operation_name
        self.start_time = None
        self.trace_ctx = None

    def __enter__(self):
        self.trace_ctx = get_trace_context()
        self.start_time = time.time()
        LOGGER.info(f"[ RUN ] Starting operation: {self.operation_name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.time() - self.start_time

        if exc_type is None:
            LOGGER.info(f"[ OK ] Completed operation: {self.operation_name} in {elapsed:.3f}s")
        else:
            LOGGER.error(
                f" Failed operation: {self.operation_name} after {elapsed:.3f}s - "
                f"\nError: {exc_type.__name__}: {str(exc_val)}",
                exc_info=True
            )

        return False
