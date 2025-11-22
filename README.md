# Discord User Account Automation

**⚠️ WARNING: EDUCATIONAL PURPOSES ONLY ⚠️**

## Important Legal Disclaimer

This code is provided **FOR EDUCATIONAL AND LEARNING PURPOSES ONLY**. The creator of this code (`yup-console`) is **NOT RESPONSIBLE** for any consequences that may result from using this software.

### 🚫 STRICT WARNINGS:

1. **VIOLATES DISCORD TERMS OF SERVICE**
   - Using self-bots/user-bots is explicitly prohibited by Discord's Terms of Service
   - Your account may be permanently banned if detected
   - Discord actively monitors and bans accounts using automation

2. **NO LIABILITY**
   - The creator (`yup-console`) assumes **ABSOLUTELY NO RESPONSIBILITY** for:
     - Account bans or suspensions
     - Loss of data or access
     - Legal consequences
     - Any other damages or issues
   - Use this code at your **OWN RISK**

3. **INTENDED USE**
   - Educational purposes only
   - Learning about Discord API and Python programming
   - Understanding how automation works
   - **NOT for malicious or disruptive activities**

## Features

This Python script uses `discord.py-self` to create a user account automation with the following commands:

### Basic Commands
- `!ping` - Check latency
- `!info` - Show account statistics
- `!userinfo` - Get user information
- `!serverinfo` - Get server information
- `!help` - Show help menu

### Moderation Commands
- `!ban @user [reason]` - Ban a member
- `!kick @user [reason]` - Kick a member
- `!unban user_id` - Unban a user
- `!mute @user [reason]` - Mute a member
- `!unmute @user` - Unmute a member
- `!purge [amount]` - Delete messages
- `!mod` - Show moderation help

### Utility Commands
- `!spam <number> <message>` - Spam messages (15 max)
- `!status <code>` - Start rich presence
- `!statusend` - End rich presence

## Setup

### Prerequisites
```bash
git clone https://github.com/yup-console/selfbot
cd selfbot
python main.py
```
if modules aren't installed use this commands
```bash
pip install discord
pip install discord.py
pip install discord.py-self
```
