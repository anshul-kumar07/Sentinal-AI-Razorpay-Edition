"""
Sentinel AI 2.0 - Live Web & Content Forensics Tools
Performs real-time HTTP probing, redirect tracing, live DOM inspection, and website content extraction.
"""

import re
import socket
import ssl
import urllib.parse
import requests

def probe_live_url(url: str, timeout: int = 5) -> dict:
    """
    Actively probes a live URL via HTTP/HTTPS, follows redirects, extracts title,
    status code, forms, and detects dead/404 links or phishing DOM patterns.
    """
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
    }

    try:
        response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True, verify=False)
        
        status_code = response.status_code
        final_url = response.url
        html_content = response.text or ""
        
        # 1. Extract Page Title
        title_match = re.search(r"<title[^>]*>(.*?)</title>", html_content, re.IGNORECASE | re.DOTALL)
        page_title = title_match.group(1).strip() if title_match else "No HTML Title"
        # Clean extra spaces/newlines in title
        page_title = re.sub(r"\s+", " ", page_title)

        # 2. Extract Meta Description
        meta_desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', html_content, re.IGNORECASE)
        meta_description = meta_desc_match.group(1).strip() if meta_desc_match else ""

        # 3. Detect Credential Harvesting & Form Elements
        has_password_input = bool(re.search(r'<input[^>]*type=["\']password["\']', html_content, re.IGNORECASE))
        has_otp_input = bool(re.search(r'<input[^>]*(?:name|id|placeholder)=["\'][^"\']*(?:otp|pin|cvv|card)[^"\']*["\']', html_content, re.IGNORECASE))
        form_actions = re.findall(r'<form[^>]*action=["\']([^"\']*)["\']', html_content, re.IGNORECASE)

        # 4. Check for 404 / Dead Page Signatures
        is_404 = (
            status_code == 404 or 
            "page not found" in page_title.lower() or 
            "404 not found" in html_content[:500].lower() or
            "this page doesn't exist" in html_content[:500].lower()
        )

        # 5. Redirect Analysis
        initial_domain = urllib.parse.urlparse(url).netloc.lower()
        final_domain = urllib.parse.urlparse(final_url).netloc.lower()
        has_redirected = initial_domain != final_domain

        # 6. Content Summary / Topic Classification
        page_summary = _generate_page_summary(page_title, meta_description, html_content, status_code, is_404)

        return {
            "reachable": True,
            "status_code": status_code,
            "is_404_or_dead": is_404,
            "final_url": final_url,
            "has_redirected": has_redirected,
            "initial_domain": initial_domain,
            "final_domain": final_domain,
            "page_title": page_title[:120],
            "meta_description": meta_description[:200],
            "page_summary": page_summary,
            "dom_forensics": {
                "has_password_field": has_password_input,
                "has_otp_field": has_otp_input,
                "form_count": len(form_actions)
            }
        }

    except requests.exceptions.SSLError as ssl_err:
        return {
            "reachable": False,
            "status_code": 0,
            "is_404_or_dead": True,
            "error_type": "SSL_CERTIFICATE_ERROR",
            "page_summary": "SSL Certificate Invalid / Self-Signed (High Phishing Risk)",
            "details": str(ssl_err)
        }
    except requests.exceptions.ConnectionError:
        return {
            "reachable": False,
            "status_code": 0,
            "is_404_or_dead": True,
            "error_type": "CONNECTION_FAILED",
            "page_summary": "Server Offline / Domain Not Resolving (Dead Link)",
            "details": "Connection refused or hostname not found in DNS."
        }
    except requests.exceptions.Timeout:
        return {
            "reachable": False,
            "status_code": 0,
            "is_404_or_dead": False,
            "error_type": "TIMEOUT",
            "page_summary": "Connection Timed Out (> 5 seconds)",
            "details": "Server did not respond in time."
        }
    except Exception as e:
        return {
            "reachable": False,
            "status_code": 0,
            "is_404_or_dead": True,
            "error_type": "PROBE_ERROR",
            "page_summary": f"Could not probe URL: {str(e)}",
            "details": str(e)
        }


def _generate_page_summary(title: str, desc: str, html: str, status_code: int, is_404: bool) -> str:
    """Generates a human-readable summary of what the live website is about."""
    if is_404 or status_code == 404:
        return "Non-Existent Page (HTTP 404 - Broken/Fake Link)"
    if status_code >= 500:
        return f"Server Error (HTTP {status_code})"
    if status_code in [401, 403]:
        return f"Restricted Access (HTTP {status_code})"
    
    html_lower = html.lower()
    
    if "razorpay" in title.lower() or "razorpay" in desc.lower():
        if "login" in title.lower() or "auth" in title.lower() or "sign in" in title.lower():
            return f"Razorpay Merchant Authentication Portal ({title})"
        return f"Official Razorpay Payments Platform ({title})"

    if "swiggy" in title.lower():
        return f"Swiggy Online Food & Delivery Platform ({title})"

    if "amazon" in title.lower():
        return f"Amazon E-Commerce & Retail Marketplace ({title})"

    if "state bank" in title.lower() or "sbi" in title.lower():
        return f"State Bank of India Banking Portal ({title})"

    if title and title != "No HTML Title":
        return f"Live Web Page: {title}"

    return "Live Web Page (Active Server Response)"

