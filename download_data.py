import urllib.request
import re
import os
import sys

def download_gdrive(file_id, output_path):
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        print(f"Fetching {url}...")
        with urllib.request.urlopen(req) as response:
            content = response.read()
            # check if confirmation page or HTML warning
            if b'confirm=' in content or b'download_warning' in content or b'Google Drive' in content:
                html = content.decode('utf-8', errors='ignore')
                # Check for direct download link or confirm parameter
                match = re.search(r'confirm=([0-9a-zA-Z_]+)', html)
                if match:
                    confirm_code = match.group(1)
                    confirm_url = f"https://drive.google.com/uc?export=download&confirm={confirm_code}&id={file_id}"
                    print(f"Redirecting with confirm code to {confirm_url}...")
                    req2 = urllib.request.Request(confirm_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req2) as resp2:
                        with open(output_path, 'wb') as f:
                            f.write(resp2.read())
                    print(f"Successfully downloaded: {output_path} ({os.path.getsize(output_path)} bytes)")
                    return

            with open(output_path, 'wb') as f:
                f.write(content)
            print(f"Successfully downloaded: {output_path} ({os.path.getsize(output_path)} bytes)")
    except Exception as e:
        print(f"Error downloading {file_id}: {e}")

if __name__ == "__main__":
    os.makedirs('data', exist_ok=True)
    download_gdrive('1IAfLZwu6rJzyWKgBToqwSmmVYU6VbjVs', 'data/historical_trader_data.csv')
    download_gdrive('1PgQC0tO8XN-wqkNyghWc_-mnrYv_nhSf', 'data/fear_greed_index.csv')
