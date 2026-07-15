with open("boundier/discord_bot/cogs.py", "r") as f:
    content = f.read()

old_code = """        if is_in_thread:
            # Already inside a thread — summarise right here, no new thread needed
            thread_record = self.bot.store.get_thread(current_channel.id)
            parent_id = thread_record.get("channel_id") if thread_record else (getattr(current_channel, 'parent_id', current_channel.id) or current_channel.id)
            
            channel_record = self.bot.store.get_channel(parent_id)
            parent_name = channel_record.get("channel_name") if channel_record else (getattr(current_channel, 'parent', current_channel).name or f"channel-{parent_id}")"""

new_code = """        if is_in_thread:
            # Already inside a thread — summarise right here, no new thread needed
            thread_record = self.bot.store.get_thread(current_channel.id)
            parent_id = thread_record.get("channel_id") if thread_record else (getattr(current_channel, 'parent_id', current_channel.id) or current_channel.id)
            
            channel_record = self.bot.store.get_channel(parent_id)
            if channel_record:
                parent_name = channel_record.get("channel_name")
            else:
                parent_name = getattr(current_channel, 'parent', None)
                parent_name = parent_name.name if parent_name else f"channel-{parent_id}"
"""

if old_code in content:
    with open("boundier/discord_bot/cogs.py", "w") as f:
        f.write(content.replace(old_code, new_code))
    print("Patched.")
else:
    print("Warning: old_code not found.")
