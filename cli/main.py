import argparse
from pathlib import Path

from core.config import Config
# from cli.wizard import run_wizard  # implement wizard in cli/wizard.py if preferred


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


def run_wizard():
    try:
        import questionary
    except ImportError:
        raise RuntimeError("questionary is required for wizard mode")

    answers = {}
    answers['project'] = questionary.text('Project name:').ask()
    domains = questionary.text('Domains (space separated):').ask()
    answers['domains'] = domains.split()
    answers['mode'] = questionary.select(
        'Select scan mode:',
        choices=['passive', 'light', 'standard', 'full', 'custom']
    ).ask()
    return argparse.Namespace(**answers)


def main():
    args = parse_args()

    # Determine input source: flags > config file > wizard
    if args.project or args.domains or args.mode:
        config = Config(config_file=None, args=args)
    elif args.config and Path(args.config).is_file():
        config = Config(config_file=args.config, args=None)
    else:
        widget = run_wizard()
        config = Config(config_file=None, args=widget)

    cfg = config.to_dict()

    # Now pass cfg into your pipeline executor
    from core.runner import Runner
    runner = Runner(cfg)
    runner.execute(dry_run=args.dry_run, debug=args.debug)


if __name__ == '__main__':
    main()
