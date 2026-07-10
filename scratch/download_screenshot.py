import urllib.request
import os

url = "https://boundier-bot-sg.onrender.com/diagnostics/session_unverified.png"
output_path = "scratch/remote_session_unverified.png"

try:
    print(f"Downloading from {url}...")
    os.makedirs("scratch", exist_ok=True)
    urllib.request.urlretrieve(url, output_path)
    print(f"Successfully downloaded to {output_path}!")
except Exception as e:
    print(f"Error downloading: {e}")
