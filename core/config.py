import yaml
import argparse
import re
from pathlib import Path


class ConfigError(Exception):
    """Custom exception for configuration validation errors."""
    pass

class Config:
    ALLOWED_MODES = {'passive', 'light', 'standard', 'full', 'custom'}
    DOMAIN_PATTERN = re.compile(r'^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$')

    def __init__(self, config_file: str = None, args: argparse.Namespace = None):
        """
        Initialize configuration from file and/or CLI args, then validate.
        """
        self.config = {}
        if config_file:
            self.load_from_file(config_file)
        if args:
            self.override_with_args(args)
        self.validate()

    def load_from_file(self, filepath: str):
        """
        Load YAML configuration from a file.
        """
        path = Path(filepath)
        if not path.is_file():
            raise ConfigError(f"Configuration file not found: {filepath}")
        with path.open('r') as f:
            data = yaml.safe_load(f)
            if not isinstance(data, dict):
                raise ConfigError("Config file must contain a YAML mapping at the top level.")
            self.config.update(data)

    def override_with_args(self, args: argparse.Namespace):
        """
        Override config values with CLI args where provided.
        """
        for key, value in vars(args).items():
            if value is not None:
                self.config[key] = value

    def validate(self):
        """
        Validate required configuration keys and formats.
        """
        # Validate project name
        project = self.config.get('project')
        if not project or not isinstance(project, str):
            raise ConfigError("'project' must be a non-empty string.")

        # Validate domains list
        domains = self.config.get('domains')
        if not domains or not isinstance(domains, list):
            raise ConfigError("'domains' must be a list of one or more domain strings.")
        invalid = [d for d in domains if not isinstance(d, str) or not self.DOMAIN_PATTERN.match(d)]
        if invalid:
            raise ConfigError(f"Invalid domain format: {invalid}")

        # Validate mode
        mode = self.config.get('mode')
        if mode is None:
            # default mode can be set here if desired
            self.config['mode'] = 'standard'
        elif mode not in self.ALLOWED_MODES:
            raise ConfigError(
                f"'mode' must be one of {sorted(self.ALLOWED_MODES)}, got '{mode}'"
            )

    def get(self, key, default=None):
        """Retrieve a config value with an optional default."""
        return self.config.get(key, default)

    def to_dict(self):
        """Return the full config as a dictionary."""
        return dict(self.config)
