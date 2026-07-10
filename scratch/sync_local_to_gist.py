import os
import sys
import asyncio
from boundier.config import load_config
from boundier.chatgpt.driver import PlaywrightDriver

# Get GITHUB_PAT and ENCRYPTION_KEY from environment
github_pat = os.environ.get("GITHUB_PAT")
if not github_pat:
    github_pat = input("Please enter your GITHUB_PAT: ").strip()
    if not github_pat:
        print("Error: GITHUB_PAT is required.")
        sys.exit(1)
    os.environ["GITHUB_PAT"] = github_pat

passphrase = os.environ.get("ENCRYPTION_KEY")
if not passphrase:
    passphrase = input("Please enter your ENCRYPTION_KEY (passphrase): ").strip()
    if not passphrase:
        print("Error: ENCRYPTION_KEY is required.")
        sys.exit(1)
    os.environ["ENCRYPTION_KEY"] = passphrase

async def main():
    config = load_config("config.yaml")
    # Force headless to be True for playwright run
    config.playwright.headless = True
    
    driver = PlaywrightDriver(config)
    print("Starting Playwright driver...")
    await driver.start()
    
    print("Ensuring authenticated...")
    is_active = await driver.ensure_authenticated()
    print(f"Authentication result: {is_active}")
    
    await driver.stop()
    print("Playwright driver stopped.")

if __name__ == "__main__":
    asyncio.run(main())
