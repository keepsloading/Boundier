import json
import urllib.request
import urllib.error
import base64
import sys

import os

PAT = os.environ.get("GITHUB_PAT", "")
HEADERS = {
    "Authorization": f"token {PAT}",
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "Boundier-Bot-Installer"
}

def make_request(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode("utf-8"))

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    res = make_request("https://api.github.com/repos/keepsloading/keepsloading/contents/README.md")
    content = base64.b64decode(res["content"]).decode("utf-8")
    print("--- RAW PROFILE README ---")
    print(content)

if __name__ == "__main__":
    main()
