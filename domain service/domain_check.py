"""
Sentinel AI 2.0 - Domain Service Adapter
Backwards compatibility and standalone domain forensics interface.
"""

from tools.domain_tools import (
    extract_all_urls_and_domains,
    check_brand_typosquatting,
    analyze_domain_structure,
    resolve_dns_record
)

def check_domain(domain_or_text: str) -> dict:
    """Standalone domain inspection utility."""
    urls = extract_all_urls_and_domains(domain_or_text)
    target = urls[0]["domain"] if urls else domain_or_text
    
    structure = analyze_domain_structure(target)
    typosquat = check_brand_typosquatting(target)
    dns = resolve_dns_record(target)
    
    return {
        "target": target,
        "structure": structure,
        "typosquatting": typosquat,
        "dns": dns
    }

