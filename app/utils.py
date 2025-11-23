from flask import request

def get_client_ip():
    """
    Returns the real client IP address. Supports:
    - Reverse proxies
    - Cloud platforms (Railway, Azure, Render, etc.)
    - Cloudflare
    - Nginx / Gunicorn / Docker
    """

    # Cloudflare (Optional)
    cf_ip = request.headers.get("CF-Connecting-IP")
    if cf_ip:
        return cf_ip

    # Standard header used by most proxies/load balancers
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        # X-Forwarded-For may contain multiple IPs: client, proxy1, proxy2
        # The first one is the real client IP
        return x_forwarded_for.split(",")[0].strip()

    # Some proxies use X-Real-IP
    x_real_ip = request.headers.get("X-Real-IP")
    if x_real_ip:
        return x_real_ip

    # Fallback to Flask's remote_addr
    return request.remote_addr
