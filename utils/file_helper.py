from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def ensure_dir(path):
    """
    Ensure that a directory exists; create it if necessary.

    :param path: Path-like or string for directory.
    """
    p = Path(path)
    try:
        p.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Directory ensured: {p}")
    except Exception as e:
        logger.error(f"Failed to create directory {p}: {e}")
        raise


def create_symlink(target, link_name):
    """
    Create a symbolic link pointing to target named link_name.

    :param target: Path-like or string for the existing file/directory.
    :param link_name: Path-like or string for the symlink to create.
    """
    t = Path(target)
    ln = Path(link_name)
    try:
        ln.parent.mkdir(parents=True, exist_ok=True)
        if ln.exists() or ln.is_symlink():
            logger.debug(f"Symlink already exists: {ln}")
        else:
            ln.symlink_to(t)
            logger.debug(f"Symlink created: {ln} -> {t}")
    except Exception as e:
        logger.error(f"Failed to create symlink {ln} -> {t}: {e}")
        raise
