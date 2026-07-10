import json
import urllib.request
import urllib.error
import base64

import os

PAT = os.environ.get("GITHUB_PAT", "")
HEADERS = {
    "Authorization": f"token {PAT}",
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "Boundier-Bot-Installer"
}

def make_request(url, method="GET", data=None):
    req_data = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, headers=HEADERS, method=method, data=req_data)
    try:
        with urllib.request.urlopen(req) as res:
            return json.loads(res.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code} on {method} {url}: {e.read().decode('utf-8')}")
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise

def get_file_content(owner, repo, path):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    res = make_request(url)
    return base64.b64decode(res["content"]), res["sha"]

def get_file_sha(owner, repo, path):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    try:
        res = make_request(url)
        return res["sha"]
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise

def update_file_bytes(owner, repo, path, file_bytes, sha, message):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    data = {
        "message": message,
        "content": base64.b64encode(file_bytes).decode("utf-8")
    }
    if sha:
        data["sha"] = sha
    return make_request(url, method="PUT", data=data)

def main():
    # 1. Fetch loading.gif bytes and convert to Base64
    print("Fetching loading.gif from keepsloading/keepsloading...")
    try:
        gif_bytes, _ = get_file_content("keepsloading", "keepsloading", "assets/loading.gif")
        gif_b64 = base64.b64encode(gif_bytes).decode("utf-8")
    except Exception as e:
        print(f"Failed to fetch loading.gif: {e}")
        return

    # 2. Build the self-contained RESPONSIVE SVG header (added style with max-width/width/height)
    svg_header = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 100" style="max-width: 100%; width: 480px; height: auto;">
  <style>
    .bg {{
      fill: #000000;
    }}
    .text {{
      font-family: 'Courier New', Courier, 'Lucida Console', monospace;
      font-weight: bold;
      font-size: 28px;
      fill: #FFFFFF;
      letter-spacing: 2px;
    }}
    .cursor {{
      animation: blink 1s infinite;
      fill: #FFFFFF;
    }}
    @keyframes blink {{
      0%, 49% {{ opacity: 1; }}
      50%, 100% {{ opacity: 0; }}
    }}
  </style>
  <clipPath id="type-clip">
    <rect x="115" y="25" width="0" height="50">
      <animate attributeName="width" 
               values="0;20;40;60;80;100;120;140;160;180;200;220;240;260;350" 
               dur="1.8s" 
               fill="freeze" 
               calcMode="discrete" />
    </rect>
  </clipPath>
  <rect class="bg" width="100%" height="100%" rx="10" />
  <image href="data:image/gif;base64,{gif_b64}" x="15" y="10" width="80" height="80" />
  <text class="text" x="115" y="58" clip-path="url(#type-clip)">
    KEEPS LOADING<tspan class="cursor">_</tspan>
  </text>
</svg>
"""

    print("Uploading responsive header.svg...")
    try:
        sha = get_file_sha("keepsloading", "keepsloading", "assets/header.svg")
        update_file_bytes(
            "keepsloading", "keepsloading", "assets/header.svg",
            svg_header.encode("utf-8"), sha, "design: make header SVG responsive to prevent mobile scroll bug"
        )
        print("Success for header.svg!")
    except Exception as e:
        print(f"Failed to upload header.svg: {e}")

    # 3. Construct and upload the bolded profile README.md (keepsloading)
    profile_readme = """<p align="center">
  <img src="https://raw.githubusercontent.com/keepsloading/keepsloading/main/assets/header.svg" alt="Keeps Loading" />
</p>

<p align="center">
  <a href="https://github.com/keepsloading/Boundier"><img src="https://img.shields.io/badge/Boundier-000543?style=for-the-badge&logo=github&logoColor=white" alt="Boundier" /></a>
  <a href="https://github.com/keepsloading/Cognitive-Firewall"><img src="https://img.shields.io/badge/Cognitive Firewall-181825?style=for-the-badge&logo=github&logoColor=white" alt="Cognitive Firewall" /></a>
  <a href="https://github.com/Memact"><img src="https://img.shields.io/badge/Memact-00011B?style=for-the-badge&logo=github&logoColor=white" alt="Memact" /></a>
  <a href="https://www.memact.com/"><img src="https://img.shields.io/badge/Memact.com-00011B?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Memact.com" /></a>
  <a href="https://discord.gg/WjKDeWuGy5"><img src="https://img.shields.io/badge/Memact_Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Memact Discord" /></a>
</p>

---

## 🧠 About
My social handle is **keeps loading** and I am most active on **Discord** and **GitHub**. My real name is **Sujay Sudhir**, and my brain **"keeps loading"** new project ideas. I am about to enter University as an undergraduate student soon, pursuing a **BTech in Artificial Intelligence**.

---

## Projects

### Boundier
An **autonomous browser-based** Discord AI companion operating directly through **ChatGPT's web interface** using headless browser automation.

### Cognitive Firewall
A **real-time "persuasion and hype detector"** Chrome extension. It highlights **emotional pressure**, **fear-mongering**, and **exaggerated persuasion cues** in web text, articles, and video descriptions.

> [!NOTE]
> I always liked the name **Boundier** and I named it at the hackathon. However, the name now suits for another project I built (an autonomous Discord bot). This project has been renamed from **Boundier** to **Cognitive Firewall** to make room for it.

### Endlessly
A Python **Tkinter endless-runner** game prototype built during the opening hours of the **IIT Bombay GenAI Hackathon**.

### Memact AutoMod Discord Bot
A **moderation and utility automation bot** built to manage and maintain the **Memact Discord community server**.

---

## Organisations

### Memact
An **open-source organisation** building a **user-controlled data and memory layer** for modern applications.

> [!NOTE]
> Memact is currently in active development and has been selected under **SSoC26** (Season of Code 2026). Multiple open-source contributors are actively collaborating on its codebase.

---

## ⚡ Fun Fact
I use tools like **Antigravity**, **Codex**, and sometimes **Replit** for generating projects in languages I don't know. However, I always ensure to **understand the core engineering principles** behind them and **actively decide** what should exist and what shouldn't.
"""

    print("Uploading profile README.md...")
    try:
        sha = get_file_sha("keepsloading", "keepsloading", "README.md")
        update_file_bytes(
            "keepsloading", "keepsloading", "README.md",
            profile_readme.encode("utf-8"), sha, "docs: bold key areas in profile README and make header responsive"
        )
        print("Success for profile README!")
    except Exception as e:
        print(f"Failed to update profile README: {e}")

    # 4. Construct and upload the bolded Cognitive-Firewall README.md
    cognitive_readme = """# Cognitive Firewall 🧠 <img src="boundier-extension/icons/128.png" align="right" width="48" height="48">

[![Chrome Extension](https://img.shields.io/badge/Chrome-Extension-4285F4?style=for-the-badge&logo=google-chrome&logoColor=white)](https://chrome.google.com/webstore)
[![Manifest V3](https://img.shields.io/badge/Manifest-V3-green?style=for-the-badge)](https://developer.chrome.com/docs/extensions/mv3/intro/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-yellow?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

**Cognitive Firewall** is a friendly Chrome extension that acts as a **real-time "persuasion and hype detector"** for your browser. It helps you see when webpages, social media feeds, or video descriptions are using **emotional pressure**, **scare tactics**, or **exaggerated persuasion** to influence how you think.

---

## 🧠 Why Cognitive Firewall?
In today's digital world, content is often designed to make you act quickly by triggering emotions. Cognitive Firewall acts as a gentle helper, highlighting these emotional triggers so you can **read objectively**, **spot high-pressure marketing**, and **make decisions on your own terms**.

---

## 🌟 Key Features
* 🛡️ **Real-Time Text Scanner:** Instantly scans visible text on any webpage to detect persuasion patterns.
* 📊 **Simple Hype Scoring:** Provides a clear score showing the level of influence pressure (e.g., Low, Medium, High).
* 🔍 **Evidence-Linked Explanations:** Hover over highlighted phrases to read a simple, clear explanation of why it was marked.
* 🔒 **Local & Private:** Processes all text directly on your device. Your browsing history and data never leave your browser.

---

## 🛠️ How It Works
1. **Highlighting:** The extension highlights phrases that use pressure tactics (like creating fake urgency or emotional appeals).
2. **Deterministic Analysis:** Uses custom keyword and phrase matching rules to calculate an objective score.
3. **Tooltip Explanations:** Explains the tactic being used when you move your cursor over the highlight.

---

## ⚡ Installation & Setup
1. **Download the Extension:** Clone this repository or download the latest release files.
2. **Open Extensions Page:** Navigate to `chrome://extensions/` in your Chrome browser.
3. **Enable Developer Mode:** Toggle the **Developer mode** switch in the top-right corner.
4. **Load the Extension:** Click **Load unpacked** and select the folder containing these project files.
5. **Start Scanning:** Click the extension icon to begin checking webpages!

---

> [!NOTE]
> **A Note on the Name:** I always liked the name **Boundier** and named it at the hackathon. However, the name now suits for another project I built (an autonomous Discord bot). This project has been renamed from **Boundier** to **Cognitive Firewall** to make room for it.
"""

    print("Uploading Cognitive-Firewall README.md...")
    try:
        sha = get_file_sha("keepsloading", "Cognitive-Firewall", "README.md")
        update_file_bytes(
            "keepsloading", "Cognitive-Firewall", "README.md",
            cognitive_readme.encode("utf-8"), sha, "docs: bold key areas in Cognitive-Firewall README"
        )
        print("Success for Cognitive-Firewall README!")
    except Exception as e:
        print(f"Failed to update Cognitive-Firewall README: {e}")

if __name__ == "__main__":
    main()
