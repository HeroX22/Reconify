import os
from pathlib import Path
import datetime
import json
from utils.logger import get_logger
from utils.file_helper import ensure_dir

logger = get_logger(__name__)

def _read_file_content(filepath, max_size=10000):
    """Read content from a file with size limit."""
    try:
        if not filepath.exists():
            return None
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            return f.read(max_size)
    except Exception as e:
        logger.debug(f"Failed to read {filepath}: {e}")
        return None

def _extract_ip_addresses(project_dir, domain):
    """Extract resolved IP addresses from the dig results."""
    ips = []
    resolved_ip_file = project_dir / domain / 'Info-Gathering' / 'Passive' / 'resolved-ip.txt'
    content = _read_file_content(resolved_ip_file)
    if content:
        ips = [ip.strip() for ip in content.splitlines() if ip.strip()]
    return ips

def _get_subdomains(project_dir, domain):
    """Extract subdomains from subfinder results."""
    subdomains = []
    subfinder_file = project_dir / domain / 'Info-Gathering' / 'Passive' / f'Subfinder-{domain}.txt'
    content = _read_file_content(subfinder_file)
    if content:
        subdomains = [sub.strip() for sub in content.splitlines() if sub.strip()]
    return subdomains

def _parse_whatweb(project_dir, domain):
    """Parse WhatWeb output to extract technologies."""
    technologies = []
    whatweb_file = project_dir / domain / 'Info-Gathering' / 'Active' / f'WhatWeb-{domain}.txt'
    content = _read_file_content(whatweb_file)
    if content:
        for line in content.splitlines():
            if '[' in line and ']' in line:
                tech_parts = line.split('[')[1:]
                for part in tech_parts:
                    if ']' in part:
                        tech = part.split(']')[0].strip()
                        if tech and tech not in technologies:
                            technologies.append(tech)
    return technologies

def _detect_waf(project_dir, domain):
    """Parse WAF detection results."""
    waf_file = project_dir / domain / 'Info-Gathering' / 'Active' / f'WAFW00F-{domain}.txt'
    content = _read_file_content(waf_file)
    if content:
        for line in content.splitlines():
            if "is behind" in line.lower() and "WAF" in line:
                return line.strip()
    return None

def _get_vulnerability_summary(project_dir, domain):
    """Extract vulnerability findings from various tools."""
    findings = {}
    vulnscan_dir = project_dir / domain / 'Vulnerability-Scan'
    
    # Look for nikto results
    nikto_file = vulnscan_dir / 'Nikto' / f'{domain}.txt'
    content = _read_file_content(nikto_file)
    if content:
        findings['nikto'] = []
        for line in content.splitlines():
            if "+ " in line:  # Nikto uses "+ " prefix for findings
                findings['nikto'].append(line.strip())
    
    # Look for nuclei results
    nuclei_file = vulnscan_dir / 'Nuclei' / f'{domain}.txt'
    content = _read_file_content(nuclei_file)
    if content:
        findings['nuclei'] = []
        for line in content.splitlines():
            if "[" in line and "]" in line:  # Nuclei uses [SEVERITY] format
                findings['nuclei'].append(line.strip())
    
    return findings

def _generate_html_report(data, output_file):
    """Generate HTML report from collected data."""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reconify Report - {data['project']}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1, h2, h3 {{
            color: #2c3e50;
        }}
        .header {{
            background-color: #34495e;
            color: white;
            padding: 20px;
            border-radius: 5px;
        }}
        .domain-card {{
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 25px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .section {{
            margin-bottom: 20px;
            padding: 10px;
            background-color: #f9f9f9;
            border-radius: 5px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        .vulnerability {{
            color: #e74c3c;
        }}
        footer {{
            margin-top: 30px;
            text-align: center;
            font-size: 0.8em;
            color: #7f8c8d;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Reconify Report</h1>
        <p>Project: {data['project']}</p>
        <p>Generated: {data['timestamp']}</p>
    </div>
    
    <h2>Summary</h2>
    <p>Total domains analyzed: {len(data['domains'])}</p>
    <p>Total subdomains discovered: {sum(len(domain_data['subdomains']) for domain_data in data['domains'].values())}</p>
    
"""
    
    # Add domain sections
    for domain, domain_data in data['domains'].items():
        html += f"""
    <div class="domain-card">
        <h2>Domain: {domain}</h2>
        
        <div class="section">
            <h3>Basic Information</h3>
            <table>
                <tr><th>IP Addresses</th><td>{', '.join(domain_data['ips'])}</td></tr>
                <tr><th>Technologies</th><td>{', '.join(domain_data['technologies'])}</td></tr>
                <tr><th>WAF Detection</th><td>{domain_data['waf'] or 'None detected'}</td></tr>
            </table>
        </div>
        
        <div class="section">
            <h3>Subdomains ({len(domain_data['subdomains'])})</h3>
            <ul>
"""
        
        for subdomain in domain_data['subdomains']:
            html += f"                <li>{subdomain}</li>\n"
        
        html += """
            </ul>
        </div>
"""
        
        # Add vulnerability section if there are findings
        if domain_data['vulnerabilities']:
            html += """
        <div class="section">
            <h3 class="vulnerability">Potential Vulnerabilities</h3>
"""
            
            for tool, findings in domain_data['vulnerabilities'].items():
                html += f"""
            <h4>{tool.upper()} ({len(findings)})</h4>
            <ul>
"""
                
                for finding in findings[:10]:  # Limit to first 10 findings
                    html += f"                <li>{finding}</li>\n"
                
                if len(findings) > 10:
                    html += f"                <li>... and {len(findings) - 10} more findings</li>\n"
                
                html += """
            </ul>
"""
            
            html += """
        </div>
"""
        
        html += """
    </div>
"""
    
    # Close HTML
    html += """
    <footer>
        <p>Generated by Reconify - Automated Reconnaissance Tool</p>
    </footer>
</body>
</html>
"""
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return output_file

def create_report(project, domains):
    """
    Create a comprehensive report for the project and its domains.
    
    Args:
        project: Project name
        domains: List of domains analyzed
    
    Returns:
        Path to the generated report file
    """
    logger.info(f"Generating report for project '{project}' with {len(domains)} domains")
    
    # Create data structure for report
    report_data = {
        'project': project,
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'domains': {}
    }
    
    project_dir = Path(project)
    report_dir = project_dir / 'Report'
    ensure_dir(report_dir)
    
    # Collect data for each domain
    for domain in domains:
        logger.debug(f"Collecting report data for domain: {domain}")
        domain_data = {
            'ips': _extract_ip_addresses(project_dir, domain),
            'subdomains': _get_subdomains(project_dir, domain),
            'technologies': _parse_whatweb(project_dir, domain),
            'waf': _detect_waf(project_dir, domain),
            'vulnerabilities': _get_vulnerability_summary(project_dir, domain)
        }
        report_data['domains'][domain] = domain_data
    
    # Generate reports
    html_report = report_dir / f"{project}-summary.html"
    json_report = report_dir / f"{project}-data.json"
    
    # Save JSON data
    with open(json_report, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2)
    
    # Generate HTML report
    html_path = _generate_html_report(report_data, html_report)
    
    logger.info(f"Report generated: {html_report}")
    return html_report