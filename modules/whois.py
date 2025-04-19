# modules/whois.py
import subprocess
from pathlib import Path

from utils.file_helper import ensure_dir
from utils.logger import get_logger

logger = get_logger(__name__)

def run_whois(target: str, output_dir: Path, filename: str = None, dry_run: bool = False) -> Path:
    """
    Run `whois` on the given target (domain or IP) and save output to a file.

    :param target: Domain or IP to query.
    :param output_dir: Directory where the output file will be stored.
    :param filename: Optional custom filename. Defaults to 'Whois-<target>.txt'.
    :param dry_run: If True, do not execute the command, only return expected path.
    :return: Path to the output file.
    """
    # Ensure output directory exists
    ensure_dir(output_dir)

    # Determine filename
    safe_target = target.replace('/', '_')
    if filename:
        out_filename = filename
    else:
        out_filename = f"Whois-{safe_target}.txt"

    outpath = output_dir / out_filename
    logger.info(f"Running whois for {target} -> {outpath}")

    if dry_run:
        return outpath

    try:
        with open(outpath, 'w') as f:
            subprocess.run(
                ['whois', target],
                stdout=f,
                stderr=subprocess.DEVNULL,
                text=True,
                check=False
            )
    except Exception as e:
        logger.error(f"Error running whois for {target}: {e}")

    return outpath
