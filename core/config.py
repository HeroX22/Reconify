import yaml
import argparse
from pathlib import Path

class Config:
    def __init__(self, config_file=None, args=None):
        self.config = {}
        if config_file:
            self.load_from_file(config_file)
        if args:
            self.override_with_args(args)

    def load_from_file(self, filepath):
        with open(filepath, 'r') as f:
            self.config = yaml.safe_load(f)

    def override_with_args(self, args):
        # Override values if provided in CLI args
        for key, value in vars(args).items():
            if value is not None:
                self.config[key] = value

    def get(self, key, default=None):
        return self.config.get(key, default)

    def to_dict(self):
        return self.config
