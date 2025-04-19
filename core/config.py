import yaml
import argparse
import re
from pathlib import Path


class ConfigError(Exception):
    """Custom exception for configuration validation errors."""
    pass


class Config:
    """
    Configuration loader and validator for Reconify.

    Supports loading from YAML, overriding via CLI args, and validating required fields.
    """
    ALLOWED_MODES = {'passive', 'light', 'standard', 'full', 'custom'}
    DOMAIN_PATTERN = re.compile(r'^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$')
    EMAIL_PATTERN = re.compile(r'^[^@]+@[^@]+\.[^@]+$')

    def __init__(self, config_file: str = None, args: argparse.Namespace = None):
        self.config = {}
        if config_file:
            self.load_from_file(config_file)
        if args:
            self.override_with_args(args)
        self.validate()

    def load_from_file(self, filepath: str):
        """
        Load configuration from a YAML file.

        :param filepath: Path to YAML config.
        :raises ConfigError: If file missing or invalid format.
        """
        path = Path(filepath)
        if not path.is_file():
            raise ConfigError(f"Configuration file not found: {filepath}")
        data = yaml.safe_load(path.read_text())
        if not isinstance(data, dict):
            raise ConfigError("Config file must contain a top-level mapping.")
        self.config.update(data)

    def override_with_args(self, args: argparse.Namespace):
        """
        Override configuration with provided CLI arguments.

        :param args: Namespace from argparse.
        """
        for key, value in vars(args).items():
            if value is not None:
                self.config[key] = value

    def validate(self):
        """
        Validate that required fields exist and have correct format.

        :raises ConfigError: On any validation failure.
        """
        # Project name
        project = self.config.get('project')
        if not project or not isinstance(project, str):
            raise ConfigError("'project' must be a non-empty string.")

        # Domains list
        domains = self.config.get('domains')
        if not domains or not isinstance(domains, list):
            raise ConfigError("'domains' must be a list with at least one domain.")
        invalid_domains = [d for d in domains if not isinstance(d, str) or not self.DOMAIN_PATTERN.match(d)]
        if invalid_domains:
            raise ConfigError(f"Invalid domain format: {invalid_domains}")

        # Mode
        mode = self.config.get('mode')
        if mode is None:
            self.config['mode'] = 'standard'
        elif mode not in self.ALLOWED_MODES:
            raise ConfigError(f"'mode' must be one of {sorted(self.ALLOWED_MODES)}, got '{mode}'")

        # Optional: output_dir
        output_dir = self.config.get('output_dir')
        if output_dir is not None and not isinstance(output_dir, str):
            raise ConfigError("'output_dir' must be a string path.")

        # Optional: tools list for custom mode
        tools = self.config.get('tools')
        if tools is not None:
            if not isinstance(tools, list) or not all(isinstance(t, str) for t in tools):
                raise ConfigError("'tools' must be a list of tool names.")
        if self.config.get('mode') == 'custom' and not tools:
            raise ConfigError("'custom' mode requires 'tools' list to be specified.")

        # Optional: email for notifications
        email = self.config.get('email')
        if email is not None:
            if not isinstance(email, str) or not self.EMAIL_PATTERN.match(email):
                raise ConfigError(f"Invalid email format: {email}")

    def get(self, key, default=None):
        """Get a config value with a default."""
        return self.config.get(key, default)

    def to_dict(self):
        """Return the full configuration dict."""
        return dict(self.config)
