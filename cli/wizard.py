import argparse

try:
    import questionary
except ImportError:
    raise RuntimeError("questionary is required for wizard mode. Please install it via 'pip install questionary'.")


def run_wizard():
    """
    Run interactive wizard to collect user input for project configuration.
    Returns an argparse.Namespace with attributes matching CLI arguments.
    """
    # Prompt for project name
    project = questionary.text('Project name:').ask()
    # Prompt for domains (space separated)
    domains_input = questionary.text('Domains (space separated):').ask()
    domains = domains_input.split() if domains_input else []
    # Prompt for scan mode
    mode = questionary.select(
        'Select scan mode:',
        choices=['passive', 'light', 'standard', 'full', 'custom']
    ).ask()

    # Build a namespace matching CLI args
    return argparse.Namespace(
        config=None,
        project=project,
        domains=domains,
        mode=mode,
        dry_run=False,
        debug=False
    )
