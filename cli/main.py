import argparse
import sys
from pathlib import Path

from core.config import Config, ConfigError
from cli.wizard import run_wizard  # wizard fallback


def parse_args():
    parser = argparse.ArgumentParser(
        prog="reconify",
        description="Reconify: Automated Recon & Vulnerability Assessment"
    )
    parser.add_argument(
        "--config", "-c",
        type=str,
        help="Path to config.yml file"
    )
    parser.add_argument(
        "--project", "-p",
        type=str,
        help="Project name"
    )
    parser.add_argument(
        "--domains", "-d",
        nargs='+',
        help="List of target domains"
    )
    parser.add_argument(
        "--mode",
        choices=['passive', 'light', 'standard', 'full', 'custom'],
        help="Level of scan to perform"
    )
    parser.add_argument(
        "--dry-run",
        action='store_true',
        help="Perform a dry run without executing tools"
    )
    parser.add_argument(
        "--debug",
        action='store_true',
        help="Enable debug output"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Determine input source: flags > config file > wizard
    try:
        if args.project or args.domains or args.mode:
            config = Config(config_file=None, args=args)
        elif args.config and Path(args.config).is_file():
            config = Config(config_file=args.config, args=None)
        else:
            wizard_args = run_wizard()
            config = Config(config_file=None, args=wizard_args)
    except ConfigError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error during config parsing: {e}", file=sys.stderr)
        sys.exit(1)

    cfg = config.to_dict()

    # Execute the pipeline
    try:
        from core.runner import Runner
        runner = Runner(cfg)
        runner.execute(dry_run=args.dry_run, debug=args.debug)
    except KeyboardInterrupt:
        print("\nExecution interrupted by user.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error during execution: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()