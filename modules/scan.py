# modules/scan.py
import subprocess
from pathlib import Path

from utils.logger import get_logger
from utils.file_helper import ensure_dir

logger = get_logger(__name__)


def full_scan(project: str, domain: str, mode: str = 'standard', dry_run: bool = False):
    """
    Run full vulnerability assessment for a given domain and its subdomains.
    """
    domain_root = Path(project) / domain
    vs_root = domain_root / 'Vulnerability-Scan'
    ensure_dir(vs_root)

    # Define tool directories
    tools = {
        'Skipfish': ['skipfish', '-u', f'https://{domain}', '-U', '-o', str(vs_root / 'Skipfish')],
        'Uniscan': ['uniscan', '-u', f'https://{domain}/', '-qwedsj', '-o', str(vs_root / 'Uniscan')],
        'Wapiti': ['wapiti', '-u', f'https://{domain}/', '-d', '16', '-o', str(vs_root / 'Wapiti')],
        'XSSer': ['xsser', '-u', f'https://{domain}', '-c', '16', '--auto', '--xml', str(vs_root / 'XSSer' / f'{domain}.xml')],
        'Nikto': ['nikto', '-host', domain, '-o', str(vs_root / 'Nikto' / f'{domain}.txt')],
        'Nuclei': ['nuclei', '-target', domain, '-o', str(vs_root / 'Nuclei' / f'{domain}.txt')],
    }

    # Create directories for each tool
    for tool_name in tools.keys():
        tool_dir = vs_root / tool_name
        ensure_dir(tool_dir)

    # Execute scans for main domain
    for tool_name, cmd in tools.items():
        logger.info(f"Running {{tool_name}} scan for domain: {domain}")
        if dry_run:
            continue
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False, text=True)
        except Exception as e:
            logger.error(f"Error running {tool_name} for {domain}: {e}")

    # Scan subdomains if any
    ips_dir = domain_root / 'IPs'
    if ips_dir.exists():
        for ip_dir in ips_dir.iterdir():
            subdomains_dir = ip_dir / 'Subdomains'
            if subdomains_dir.exists():
                for sub_dir in subdomains_dir.iterdir():
                    sub = sub_dir.name
                    sub_vs_root = sub_dir / 'Vulnerability-Scan'
                    ensure_dir(sub_vs_root)

                    # Create subdomain tool dirs
                    for tool_name in tools.keys():
                        ensure_dir(sub_vs_root / tool_name)

                    # Run scans on subdomain
                    for tool_name, cmd_template in tools.items():
                        # Substitute domain with subdomain in command
                        cmd = [arg.replace(domain, sub) for arg in cmd_template]
                        logger.info(f"Running {tool_name} scan for subdomain: {sub}")
                        if dry_run:
                            continue
                        try:
                            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False, text=True)
                        except Exception as e:
                            logger.error(f"Error running {tool_name} for {sub}: {e}")
