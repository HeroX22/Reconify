import subprocess
from pathlib import Path
from utils.logger import get_logger
from utils.file_helper import ensure_dir

logger = get_logger(name=__name__)


def create_base_structure(domain_root: Path):
    """
    Create base directory structure for a given domain.
    """
    # Define directory structure
    paths = [
        domain_root / 'Info-Gathering' / 'Passive',
        domain_root / 'Info-Gathering' / 'Active' / 'Nmap',
        domain_root / 'Info-Gathering' / 'Active' / 'TLSSled',
        domain_root / 'Vulnerability-Scan',
        domain_root / 'IPs',
        domain_root / 'Exploitation' / 'Exploits',
        domain_root / 'Exploitation' / 'Payloads',
        domain_root / 'Post-Exploitation' / 'Persistence',
        domain_root / 'Post-Exploitation' / 'Privilege-Escalation',
        domain_root / 'Post-Exploitation' / 'Lateral-Movement',
        domain_root / 'Screenshots',
    ]
    # Create directories
    for p in paths:
        ensure_dir(p)
    # Create empty files for timeline, log, and notes
    for fname in ('Timeline.md', 'log.txt', 'Notes.txt'):
        fpath = domain_root / fname
        if not fpath.exists():
            fpath.touch()
    logger.debug(f"Base structure created at {domain_root}")


def passive_recon(project: str, domain: str, dry_run: bool = False):
    """
    Run passive information gathering commands for the given domain.
    """
    base = Path(project) / domain / 'Info-Gathering' / 'Passive'
    ensure_dir(base)

    commands = [
        (['whois', domain], f'Whois-{domain}.txt'),
        (['dig', domain], f'Dig-{domain}.txt'),
        (['host', domain], f'Host-{domain}.txt'),
        # DNS enum and IPInfo disabled by default
        (['subfinder', '-silent', '-d', domain], f'Subfinder-{domain}.txt'),
        (['curl', f'https://www.shodan.io/domain/{domain}'], f'Shodan-{domain}.txt'),
        (['dig', '+short', domain], 'resolved-ip.txt'),
    ]

    for cmd, outfile in commands:
        outpath = base / outfile
        logger.info(f"Running passive recon: {' '.join(cmd)} > {outpath}")
        if dry_run:
            continue
        with open(outpath, 'w') as f:
            try:
                subprocess.run(cmd, stdout=f, stderr=subprocess.DEVNULL, text=True, check=False)
            except Exception as e:
                logger.error(f"Error running {' '.join(cmd)}: {e}")


def active_recon(project: str, domain: str, dry_run: bool = False):
    """
    Run active information gathering commands for the given domain.
    """
    base = Path(project) / domain / 'Info-Gathering' / 'Active'
    # Ensure base structure exists
    create_base_structure(Path(project) / domain)

    # Nmap full port scan
    nmap_prefix = base / 'Nmap' / f'nmap-{domain}'
    cmd_nmap = ['nmap', '-p-', '-sV', '-sC', '-T4', '-A', '-O', '-oA', str(nmap_prefix)]
    logger.info(f"Running active recon: {' '.join(cmd_nmap)}")
    if not dry_run:
        subprocess.run(cmd_nmap, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)

    # WhatWeb
    whatweb_out = base / f'WhatWeb-{domain}.txt'
    cmd_whatweb = ['whatweb', domain]
    logger.info(f"Running active recon: {' '.join(cmd_whatweb)} > {whatweb_out}")
    if not dry_run:
        with open(whatweb_out, 'w') as f:
            subprocess.run(cmd_whatweb, stdout=f, stderr=subprocess.DEVNULL, text=True, check=False)

    # TLSSled
    tlssled_dir = base / 'TLSSled'
    ensure_dir(tlssled_dir)
    tlssled_out = tlssled_dir / f'tlssled-{domain}.txt'
    cmd_tls = ['tlssled', domain, '443']
    logger.info(f"Running active recon: {' '.join(cmd_tls)} > {tlssled_out}")
    if not dry_run:
        with open(tlssled_out, 'w') as f:
            subprocess.run(cmd_tls, stdout=f, stderr=subprocess.DEVNULL, text=True, check=False)

    # WAFW00F
    waf_out = base / f'WAFW00F-{domain}.txt'
    cmd_waf = ['wafw00f', '-o', str(waf_out), domain]
    logger.info(f"Running active recon: {' '.join(cmd_waf)}")
    if not dry_run:
        subprocess.run(cmd_waf, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)

    # LoadBalancer detection
    lb_out = base / f'LoadBalancer-{domain}.txt'
    cmd_lb = ['lbd', domain]
    logger.info(f"Running active recon: {' '.join(cmd_lb)} > {lb_out}")
    if not dry_run:
        with open(lb_out, 'w') as f:
            subprocess.run(cmd_lb, stdout=f, stderr=subprocess.DEVNULL, text=True, check=False)

    # Hakrawler
    crawl_out = base / f'Sitemap-{domain}.txt'
    cmd_hak = f"echo https://{domain} | hakrawler -u -s -d 7"
    logger.info(f"Running active recon: {cmd_hak} > {crawl_out}")
    if not dry_run:
        with open(crawl_out, 'w') as f:
            subprocess.run(cmd_hak, shell=True, stdout=f, stderr=subprocess.DEVNULL, text=True, check=False)
