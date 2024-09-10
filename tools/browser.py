import re,requests


def extract_and_replace_links( text: str) -> dict:
    url_pattern = r'(https?://[^\s,]+|www\.[^\s,]+)'
    links = re.findall(url_pattern, text)
    return links

def linkReader(url: str) -> str:
    image_extensions = r'\.(jpg|jpeg|png|gif|bmp|svg|webp)$'
    if re.search(image_extensions, url, re.IGNORECASE):
        raise ValueError("Not a valid link")
    content = requests.get('https://r.jina.ai/' + url, headers={'User-Agent': 'Mozilla/5.0'}).text
    return content