# modules/wpscan.py
import subprocess
from pathlib import Path

from utils.file_helper import ensure_dir
from utils.logger import get_logger

logger = get_logger(__name__)

def run_wpscan(target: str, output_dir: Path, filename: str = None, dry_run: bool = False) -> Path:
    """
    Run WPScan against a given URL (domain or subdomain) and save the output to a file.

    :param target: URL to scan (e.g., 'https://example.com').
    :param output_dir: Directory where the output file will be stored.
    :param filename: Optional custom filename. Defaults to 'WpScan-<target>.txt'.
    :param dry_run: If True, do not execute the command, only return expected path.
    :return: Path to the output file.
    """
    ensure_dir(output_dir)
    safe = target.replace('://', '_').replace('/', '_')
    out_fname = filename or f"WpScan-{safe}.txt"
    outpath = output_dir / out_fname

    logger.info(f"Running WPScan for {target} -> {outpath}")
    if dry_run:
        return outpath

    cmd = ["wpscan", "--url", target, "--random-user-agent", "-o", str(outpath)]
    try:
        with open(outpath, 'w') as f:
            subprocess.run(cmd, stdout=f, stderr=subprocess.DEVNULL, text=True, check=False)
    except Exception as e:
        logger.error(f"Error running WPScan for {target}: {e}")

    return outpath
