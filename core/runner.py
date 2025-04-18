import os
from pathlib import Path

from utils.file_helper import ensure_dir, create_symlink
from modules import recon, scan, report
from utils.logger import get_logger


class Runner:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.project = cfg.get('project')
        self.domains = cfg.get('domains', [])
        self.mode = cfg.get('mode', 'standard')
        self.logger = get_logger(debug=cfg.get('debug', False))

    def execute(self, dry_run: bool = False, debug: bool = False):
        """
        Main entry point to run the entire workflow based on config and mode.
        """
        self.dry_run = dry_run
        self.debug = debug
        self.logger.info(f"Starting Reconify project '{self.project}' in mode '{self.mode}'")

        # 1. Build base directories
        self.setup_directories()

        # 2. Passive recon phase
        if self.mode in ('passive', 'light', 'standard', 'full', 'custom'):
            self.run_passive()

        # 3. Active recon phase
        if self.mode in ('light', 'standard', 'full', 'custom'):
            self.run_active()

        # 4. Vulnerability assessment phase
        if self.mode in ('standard', 'full', 'custom'):
            self.run_vuln_assessment()

        # 5. Final report
        if self.mode in ('full', 'custom'):
            self.generate_report()

        self.logger.info("Reconify workflow complete.")

    def setup_directories(self):
        """
        Create project root and subdirectories for each domain and IP/subdomain.
        """
        root = Path(self.project)
        self.logger.debug(f"Creating project root at {root}")
        ensure_dir(root)

        # create common folders
        for folder in ["Credentials/Wordlists", "Custom-Payloads", "Report"]:
            path = root / folder
            self.logger.debug(f"Ensuring directory {path}")
            ensure_dir(path)

        # per-domain structure
        for domain in self.domains:
            domain_root = root / domain
            self.logger.debug(f"Creating structure for domain {domain}")
            recon.create_base_structure(domain_root)

    def run_passive(self):
        """
        Run passive reconnaissance for each domain.
        """
        for domain in self.domains:
            self.logger.info(f"Passive recon for {domain}")
            recon.passive_recon(self.project, domain, dry_run=self.dry_run)

    def run_active(self):
        """
        Run active reconnaissance for each domain.
        """
        for domain in self.domains:
            self.logger.info(f"Active recon for {domain}")
            recon.active_recon(self.project, domain, dry_run=self.dry_run)

    def run_vuln_assessment(self):
        """
        Run vulnerability assessment tools for each target.
        """
        for domain in self.domains:
            self.logger.info(f"Vulnerability assessment for {domain}")
            scan.full_scan(self.project, domain, mode=self.mode, dry_run=self.dry_run)

    def generate_report(self):
        """
        Generate final HTML/Markdown report.
        """
        self.logger.info(f"Generating report for project {self.project}")
        report.create_report(self.project, self.domains)
