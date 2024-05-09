def normalize_url(url):
    url_norm = url.strip()
    
    if not url_norm.startswith(('http://', 'https://')):
        url_norm = 'https://' + url_norm
    if "https://www." in url_norm:
        return url_norm.replace("https://www.", "https://")
    elif "http://www." in url_norm:
        return url_norm.replace("http://www.", "http://")
    else: 
        return url_norm