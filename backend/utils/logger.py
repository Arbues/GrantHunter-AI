"""
Centralized logger for GrantHunter AI.

Usage:
    from backend.utils.logger import get_logger
    logger = get_logger("IdentityAgent", session_id)
    logger.info("Profile parsed successfully.")

Each session writes to its own log file: output/<session_id>/run.log
This design is multi-user safe: no shared log state between sessions.
"""

import logging
import pathlib
import sys


def get_logger(agent_name: str, session_id: str = "dev") -> logging.Logger:
    """
    Returns a logger for the given agent scoped to a session.

    - In dev (session_id='dev'), logs are written to output/dev/run.log
      and also to stdout (for easy debugging).
    - In production (any other session_id), logs go to file only.

    The logger is named '<session_id>.<agent_name>' to avoid handler
    duplication when called multiple times within the same session.
    """
    logger_name = f"{session_id}.{agent_name}"
    logger = logging.getLogger(logger_name)

    # Avoid adding duplicate handlers on repeated calls (e.g., during tests)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # --- File handler (always active) ---
    log_dir = pathlib.Path("output") / session_id
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "run.log"

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "[%(asctime)s][%(levelname)s][%(name)s] %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # --- Stdout handler (dev only, for easy terminal debugging) ---
    if session_id == "dev":
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)
        stream_formatter = logging.Formatter(
            "[%(levelname)s][%(name)s] %(message)s"
        )
        stream_handler.setFormatter(stream_formatter)
        logger.addHandler(stream_handler)

    # Prevent log records from being passed to the root logger
    logger.propagate = False

    return logger
