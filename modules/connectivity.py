# modules/connectivity.py
import subprocess
import socket
from pathlib import Path

from utils.file_helper import ensure_dir
from utils.logger import get_logger

logger = get_logger(__name__)

def ping_target(target: str, count: int = 1, dry_run: bool = False) -> bool:
    """
    Ping a target once (or specified count) to check ICMP reachability.

    :param target: Domain or IP to ping.
    :param count: Number of ping packets to send.
    :param dry_run: If True, simulate without sending ping.
    :return: True if ping succeeds, False otherwise.
    """
    cmd = ['ping', '-c', str(count), target]
    logger.info(f"Pinging {target} with {count} packet(s)")
    if dry_run:
        return True

    try:
        result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode == 0
    except Exception as e:
        logger.error(f"Error pinging {target}: {e}")
        return False


def check_tcp_port(target: str, port: int, timeout: int = 3, dry_run: bool = False) -> bool:
    """
    Check TCP connectivity to a given port.

    :param target: Domain or IP to connect.
    :param port: Port number to test.
    :param timeout: Connection timeout in seconds.
    :param dry_run: If True, simulate without real connection.
    :return: True if connection succeeds, False otherwise.
    """
    logger.info(f"Checking TCP port {port} on {target}")
    if dry_run:
        return True

    try:
        with socket.create_connection((target, port), timeout=timeout):
            return True
    except Exception as e:
        logger.debug(f"TCP port {port} unreachable on {target}: {e}")
        return False


def fetch_http_headers(target: str,
                       scheme: str = 'https',
                       output_dir: Path = None,
                       filename: str = None,
                       dry_run: bool = False) -> Path:
    """
    Fetch HTTP headers using curl and save to a file.

    :param target: Domain or IP to fetch.
    :param scheme: 'http' or 'https'.
    :param output_dir: Directory to save header output.
    :param filename: Optional filename. Defaults to '<scheme>headers-<target>.txt'.
    :param dry_run: If True, do not execute, only return expected path.
    :return: Path to the saved header file.
    """
    # Prepare output directory
    if output_dir:
        ensure_dir(output_dir)
    else:
        output_dir = Path('.')

    safe = target.replace('://', '_').replace('/', '_')
    fname = filename or f"{scheme}headers-{safe}.txt"
    outpath = output_dir / fname

    url = f"{scheme}://{target}"
    cmd = ['curl', '-I', url]
    logger.info(f"Fetching HTTP headers: {' '.join(cmd)} -> {outpath}")
    if dry_run:
        return outpath

    try:
        with open(outpath, 'w') as f:
            subprocess.run(cmd, stdout=f, stderr=subprocess.DEVNULL, text=True, check=False)
    except Exception as e:
        logger.error(f"Error fetching headers for {url}: {e}")

    return outpath
