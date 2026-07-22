import urllib.request
import re
import os

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"
    session = urllib.request.build_opener(urllib.request.HTTPCookieProcessor())
    
    req = urllib.request.Request(f"{URL}&id={id}", headers={'User-Agent': 'Mozilla/5.0'})
    print(f"Connecting to download {id}...")
    response = session.open(req)
    content_type = response.headers.get('Content-Type', '')
    print(f"Content-Type: {content_type}")
    
    if "text/html" in content_type:
        html = response.read().decode('utf-8', errors='ignore')
        # Check confirmation token
        tokens = re.findall(r'confirm=([0-9a-zA-Z_]+)', html)
        if not tokens:
            tokens = re.findall(r'code=([0-9a-zA-Z_]+)', html)
        if not tokens:
            tokens = re.findall(r'uuid=([0-9a-zA-Z_-]+)', html)
        
        if tokens:
            confirm_token = tokens[0]
            print(f"Found token {confirm_token}, retrying...")
            download_url = f"{URL}&confirm={confirm_token}&id={id}"
        else:
            # Look for warning link download URL
            matches = re.findall(r'href="(/uc\?export=download[^"]+)"', html)
            if matches:
                download_url = "https://docs.google.com" + matches[0].replace("&amp;", "&")
            else:
                print("Could not find download URL in HTML page.")
                print(html[:500])
                return False
        
        req = urllib.request.Request(download_url, headers={'User-Agent': 'Mozilla/5.0'})
        response = session.open(req)
    
    CHUNK_SIZE = 32768
    total_bytes = 0
    with open(destination, "wb") as f:
        while True:
            chunk = response.read(CHUNK_SIZE)
            if not chunk:
                break
            f.write(chunk)
            total_bytes += len(chunk)
            if total_bytes % (5 * 1024 * 1024) == 0:
                print(f"Downloaded {total_bytes / (1024*1024):.1f} MB...")
                
    print(f"Download complete: {destination} ({total_bytes / (1024*1024):.2f} MB)")
    return True

if __name__ == "__main__":
    os.makedirs('data', exist_ok=True)
    print("--- Downloading Historical Trader Data ---")
    download_file_from_google_drive('1IAfLZwu6rJzyWKgBToqwSmmVYU6VbjVs', 'data/historical_trader_data.csv')
    print("--- Downloading Fear & Greed Index ---")
    download_file_from_google_drive('1PgQC0tO8XN-wqkNyghWc_-mnrYv_nhSf', 'data/fear_greed_index.csv')
