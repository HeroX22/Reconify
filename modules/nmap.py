# modules/nmap.py
import subprocess
from pathlib import Path

from utils.file_helper import ensure_dir
from utils.logger import get_logger

logger = get_logger(__name__)

def run_nmap(target: str,
             output_dir: Path,
             flags: list = None,
             prefix: str = None,
             dry_run: bool = False) -> dict:
    """
    Run nmap scan on the given target and save output in all major formats.

    :param target: Domain or IP to scan.
    :param output_dir: Directory where nmap output files will be stored.
    :param flags: Additional nmap flags (e.g., ['-p-', '-sV', '-sC', '-T4', '-A', '-O']).
    :param prefix: Optional filename prefix for output files (without extension).
                   Defaults to 'nmap-<target>'.
    :param dry_run: If True, do not execute the command, only return expected paths.
    :return: Dict mapping format ('nmap', 'gnmap', 'xml') to Path objects.
    """
    ensure_dir(output_dir)

    safe_target = target.replace('/', '_')
    out_prefix = prefix or f"nmap-{safe_target}"
    base_path = output_dir / out_prefix
    # Build nmap command
    cmd = ['nmap']
    if flags:
        cmd.extend(flags)
    # -oA for all formats
    cmd.extend(['-oA', str(base_path), str(target)])

    logger.info(f"Running nmap: {' '.join(cmd)}")
    if dry_run:
        return {
            'nmap': base_path.with_suffix('.nmap'),
            'gnmap': base_path.with_suffix('.gnmap'),
            'xml': base_path.with_suffix('.xml')
        }

    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    except Exception as e:
        logger.error(f"Error running nmap for {target}: {e}")

    return {
        'nmap': base_path.with_suffix('.nmap'),
        'gnmap': base_path.with_suffix('.gnmap'),
        'xml': base_path.with_suffix('.xml')
    }