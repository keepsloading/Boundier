import asyncio
import json
from boundier.config import load_config
from boundier.chatgpt.driver import PlaywrightDriver

async def main():
    config = load_config("config.yaml")
    driver = PlaywrightDriver(config)
    
    print("Loading session from Gist...")
    decrypted_state = await driver._load_gist_session_state()
    if decrypted_state:
        state_dict = json.loads(decrypted_state)
        cookies = state_dict.get("cookies", [])
        print(f"Total cookies in Gist: {len(cookies)}")
        for c in cookies:
            if "session-token" in c.get("name", ""):
                print(f"Found session-token! Expiry: {c.get('expires')}")
    else:
        print("Failed to load or decrypt Gist.")

if __name__ == "__main__":
    asyncio.run(main())
