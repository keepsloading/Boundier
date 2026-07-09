import os
import json
import asyncio
from playwright.async_api import async_playwright
from boundier.config import load_config

async def export():
    config = load_config("config.yaml")
    paths_to_try = [
        os.path.abspath(config.playwright.user_data_dir),
        os.path.abspath("browser_profile"),
        os.path.abspath(".chrome_profile")
    ]
    
    # Remove duplicates while preserving order
    seen = set()
    paths_to_try = [p for p in paths_to_try if not (p in seen or seen.add(p))]
    
    profile_results = {}
    
    async with async_playwright() as p:
        for path in paths_to_try:
            if not os.path.exists(path):
                continue
            print(f"\nChecking browser profile: {path}")
            try:
                context = await p.chromium.launch_persistent_context(
                    user_data_dir=path,
                    headless=True
                )
                page = await context.new_page()
                try:
                    await page.goto("https://chatgpt.com", wait_until="domcontentloaded", timeout=15000)
                except Exception as goto_err:
                    print(f"  Navigation note: {goto_err}")
                
                found_cookies = await context.cookies()
                await context.close()
                
                if found_cookies:
                    # Look for actual session token in cookies
                    has_session = any("session-token" in c.get("name", "") for c in found_cookies)
                    profile_results[path] = {
                        "cookies": found_cookies,
                        "has_session": has_session
                    }
                    print(f"  Found {len(found_cookies)} cookies. Has session token: {has_session}")
            except Exception as e:
                print(f"  Error checking profile {path}: {e}")
        
    if not profile_results:
        print("No active login cookies found. Please run the bot locally first and ensure you are logged into ChatGPT!")
        return
        
    # Print output for each found profile
    for path, result in profile_results.items():
        session_json = json.dumps(result["cookies"])
        print("\n" + "="*80)
        print(f"PROFILE: {path}")
        print(f"Total Cookies: {len(result['cookies'])} | Has Session Token: {result['has_session']}")
        if result['has_session']:
            print("⭐ (RECOMMENDED: This profile contains active login session tokens!)")
        print("Copy the entire line below and set it as the CHATGPT_STORAGE_STATE environment variable in Render:")
        print("="*80)
        print(session_json)
        print("="*80 + "\n")

if __name__ == "__main__":
    asyncio.run(export())
