# modules/dig.py
import subprocess
from pathlib import Path

from utils.file_helper import ensure_dir
from utils.logger import get_logger

logger = get_logger(__name__)

def run_dig(target: str, output_dir: Path, record_type: str = None, filename: str = None, dry_run: bool = False) -> Path:
    """
    Run `dig` on the given target (domain or IP) and save output to a file.

    :param target: Domain or IP to query.
    :param output_dir: Directory where the output file will be stored.
    :param record_type: Optional DNS record type (e.g., 'A', 'MX'). Defaults to None (all records).
    :param filename: Optional custom filename. Defaults to 'Dig-<target>.txt' or 'Dig-<target>-<type>.txt'.
    :param dry_run: If True, do not execute the command, only return expected path.
    :return: Path to the output file.
    """
    # Ensure output directory exists
    ensure_dir(output_dir)

    # Build dig command
    cmd = ['dig', target]
    if record_type:
        cmd.extend([record_type])

    # Determine filename
    safe_target = target.replace('/', '_')
    if filename:
        out_filename = filename
    else:
        if record_type:
            out_filename = f"Dig-{safe_target}-{record_type}.txt"
        else:
            out_filename = f"Dig-{safe_target}.txt"

    outpath = output_dir / out_filename
    logger.info(f"Running dig for {target} -> {outpath}")

    if dry_run:
        return outpath

    try:
        with open(outpath, 'w') as f:
            subprocess.run(
                cmd,
                stdout=f,
                stderr=subprocess.DEVNULL,
                text=True,
                check=False
            )
    except Exception as e:
        logger.error(f"Error running dig for {target}: {e}")

    return outpath
