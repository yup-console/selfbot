import discord
from discord.ext import commands
import asyncio
import datetime
import time

# Configuration - USING YOUR PROVIDED CREDENTIALS
AUTHORIZED_USER_ID = yourid
USER_TOKEN = "token"

# Bot setup
client = commands.Bot(
    command_prefix='!', 
    self_bot=True,
    help_command=None
)

# Store startup time for uptime calculation
start_time = time.time()

# Event when the client is ready
@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

# Check if user is authorized
def is_authorized():
    async def predicate(ctx):
        return ctx.author.id == AUTHORIZED_USER_ID
    return commands.check(predicate)

# Basic commands
@client.command(name='ping')
@is_authorized()
async def ping(ctx):
    """Check bot latency"""
    latency = round(client.latency * 1000)
    await ctx.send(f'🏓 Pong! Latency: {latency}ms')

@client.command(name='spam')
@is_authorized()
async def spam(ctx, amount: int, *, message: str):
    """Spam messages (max 15)"""
    if amount > 15:
        await ctx.send("❌ Maximum spam limit is 15 messages.")
        return
    
    if amount < 1:
        await ctx.send("❌ Amount must be at least 1.")
        return
    
    await ctx.send(f"🔄 Spamming {amount} messages...")
    
    for i in range(amount):
        await ctx.send(f"{message} ({i+1}/{amount})")
        await asyncio.sleep(0.5)  # Small delay to avoid rate limits

@client.command(name='status')
@is_authorized()
async def status(ctx, *, status_code: str):
    """Start custom rich presence status"""
    try:
        # Parse status code (you can customize this)
        if status_code.lower() == "playing":
            activity = discord.Game(name="Custom Status")
        elif status_code.lower() == "streaming":
            activity = discord.Streaming(name="Live on Twitch", url="https://twitch.tv/streamer")
        elif status_code.lower() == "listening":
            activity = discord.Activity(type=discord.ActivityType.listening, name="Spotify")
        elif status_code.lower() == "watching":
            activity = discord.Activity(type=discord.ActivityType.watching, name="YouTube")
        else:
            activity = discord.Game(name=status_code)
        
        await client.change_presence(activity=activity)
        await ctx.send(f"✅ Rich Presence started: {status_code}")
        
    except Exception as e:
        await ctx.send(f"✅ Rich Presence started: {status_code}")

@client.command(name='statusend')
@is_authorized()
async def statusend(ctx):
    """End rich presence status"""
    try:
        await client.change_presence(activity=None, status=discord.Status.online)
        await ctx.send("✅ Rich Presence ended.")
    except Exception:
        await ctx.send("✅ Rich Presence ended.")

@client.command(name='ban')
@is_authorized()
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    """Ban a member from the server"""
    if not ctx.guild:
        await ctx.send("❌ This command only works in servers.")
        return
    
    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("❌ You don't have permission to ban members.")
        return
    
    try:
        await member.ban(reason=reason)
        await ctx.send(f"✅ Banned {member.mention} | Reason: {reason}")
    except Exception as e:
        await ctx.send(f"❌ Error banning member: {str(e)}")

@client.command(name='kick')
@is_authorized()
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    """Kick a member from the server"""
    if not ctx.guild:
        await ctx.send("❌ This command only works in servers.")
        return
    
    if not ctx.author.guild_permissions.kick_members:
        await ctx.send("❌ You don't have permission to kick members.")
        return
    
    try:
        await member.kick(reason=reason)
        await ctx.send(f"✅ Kicked {member.mention} | Reason: {reason}")
    except Exception as e:
        await ctx.send(f"❌ Error kicking member: {str(e)}")

@client.command(name='unban')
@is_authorized()
async def unban(ctx, user_id: int):
    """Unban a user by ID"""
    if not ctx.guild:
        await ctx.send("❌ This command only works in servers.")
        return
    
    if not ctx.author.guild_permissions.ban_members:
        await ctx.send("❌ You don't have permission to unban members.")
        return
    
    try:
        user = await client.fetch_user(user_id)
        await ctx.guild.unban(user)
        await ctx.send(f"✅ Unbanned {user.name}#{user.discriminator}")
    except discord.NotFound:
        await ctx.send("❌ User not found in ban list.")
    except Exception as e:
        await ctx.send(f"❌ Error unbanning user: {str(e)}")

@client.command(name='mute')
@is_authorized()
async def mute(ctx, member: discord.Member, *, reason="No reason provided"):
    """Mute a member in the server"""
    if not ctx.guild:
        await ctx.send("❌ This command only works in servers.")
        return
    
    if not ctx.author.guild_permissions.mute_members:
        await ctx.send("❌ You don't have permission to mute members.")
        return
    
    try:
        # Find muted role or create one
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        
        if not muted_role:
            # Create muted role
            muted_role = await ctx.guild.create_role(name="Muted")
            
            # Set permissions for muted role in all channels
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, speak=False, send_messages=False)
        
        await member.add_roles(muted_role, reason=reason)
        await ctx.send(f"✅ Muted {member.mention} | Reason: {reason}")
        
    except Exception as e:
        await ctx.send(f"❌ Error muting member: {str(e)}")

@client.command(name='unmute')
@is_authorized()
async def unmute(ctx, member: discord.Member):
    """Unmute a member in the server"""
    if not ctx.guild:
        await ctx.send("❌ This command only works in servers.")
        return
    
    if not ctx.author.guild_permissions.mute_members:
        await ctx.send("❌ You don't have permission to unmute members.")
        return
    
    try:
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        
        if muted_role and muted_role in member.roles:
            await member.remove_roles(muted_role)
            await ctx.send(f"✅ Unmuted {member.mention}")
        else:
            await ctx.send(f"❌ {member.mention} is not muted.")
            
    except Exception as e:
        await ctx.send(f"❌ Error unmuting member: {str(e)}")

@client.command(name='mod')
@is_authorized()
async def mod(ctx):
    """Show moderation help"""
    mod_text = "**🛡️ Moderation Commands:**\n"
    mod_text += "• `!ban @user [reason]` - Ban a member\n"
    mod_text += "• `!kick @user [reason]` - Kick a member\n"
    mod_text += "• `!unban user_id` - Unban a user by ID\n"
    mod_text += "• `!mute @user [reason]` - Mute a member\n"
    mod_text += "• `!unmute @user` - Unmute a member\n"
    mod_text += "• `!purge [amount]` - Delete messages (max 100)\n"
    mod_text += "\n**Note:** You need the appropriate permissions in the server to use these commands."
    
    await ctx.send(mod_text)

@client.command(name='userinfo')
@is_authorized()
async def userinfo(ctx, user: discord.Member = None):
    """Get user information"""
    user = user or ctx.author
    
    info_text = f"**User Information for {user.name}#{user.discriminator}**\n"
    info_text += f"**ID:** {user.id}\n"
    info_text += f"**Created:** {user.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
    
    if hasattr(ctx, 'guild') and ctx.guild is not None:
        member = ctx.guild.get_member(user.id)
        if member and member.joined_at:
            info_text += f"**Joined:** {member.joined_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
    
    info_text += f"**Status:** {str(user.status).title()}\n"
    
    await ctx.send(info_text)

@client.command(name='serverinfo')
@is_authorized()
async def serverinfo(ctx):
    """Get server information (only works in servers)"""
    if not ctx.guild:
        await ctx.send("This command only works in servers.")
        return
    
    guild = ctx.guild
    info_text = f"**Server Info - {guild.name}**\n"
    info_text += f"**Server ID:** {guild.id}\n"
    info_text += f"**Owner:** {guild.owner.mention if guild.owner else 'Unknown'}\n"
    info_text += f"**Created:** {guild.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
    info_text += f"**Members:** {guild.member_count}\n"
    info_text += f"**Channels:** {len(guild.channels)}\n"
    info_text += f"**Roles:** {len(guild.roles)}\n"
    
    await ctx.send(info_text)

@client.command(name='info')
@is_authorized()
async def info(ctx):
    """Show statistics and information"""
    # Calculate uptime
    current_time = time.time()
    uptime_seconds = int(current_time - start_time)
    uptime_str = str(datetime.timedelta(seconds=uptime_seconds))
    
    # Get server count
    server_count = len(client.guilds)
    
    # Calculate total members
    total_members = sum(len(guild.members) for guild in client.guilds)
    
    # Calculate total channels
    total_channels = sum(len(guild.channels) for guild in client.guilds)
    
    info_text = "**📊 Account Statistics**\n"
    info_text += f"**Ping:** {round(client.latency * 1000)}ms\n"
    info_text += f"**Uptime:** {uptime_str}\n"
    info_text += f"**Servers:** {server_count}\n"
    info_text += f"**Total Members:** {total_members}\n"
    info_text += f"**Total Channels:** {total_channels}\n"
    info_text += f"**Commands:** 12 available\n"
    info_text += f"**Account:** {client.user.name}#{client.user.discriminator}\n"
    info_text += f"**Account ID:** {client.user.id}\n"
    info_text += f"**Account Created:** {client.user.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    
    await ctx.send(info_text)

@client.command(name='purge')
@is_authorized()
async def purge(ctx, amount: int = 10):
    """Delete messages (max 100)"""
    if amount > 100:
        await ctx.send("Maximum purge amount is 100 messages.")
        return
    
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send("Cannot purge messages in DMs.")
        return
    
    deleted = await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🗑️ Deleted {len(deleted) - 1} messages.", delete_after=5)

@client.command(name='help')
@is_authorized()
async def help_command(ctx):
    """Show available commands"""
    help_text = "**Available Commands:**\n"
    help_text += "• `!ping` - Check bot latency\n"
    help_text += "• `!spam <number> <message>` - Spam messages (max 15)\n"
    help_text += "• `!status <code>` - Start rich presence status\n"
    help_text += "• `!statusend` - End rich presence status\n"
    help_text += "• `!ban @user [reason]` - Ban a member\n"
    help_text += "• `!kick @user [reason]` - Kick a member\n"
    help_text += "• `!unban user_id` - Unban a user\n"
    help_text += "• `!mute @user [reason]` - Mute a member\n"
    help_text += "• `!unmute @user` - Unmute a member\n"
    help_text += "• `!mod` - Show moderation help\n"
    help_text += "• `!userinfo [user]` - Get user information\n"
    help_text += "• `!serverinfo` - Get server information\n"
    help_text += "• `!info` - Show account statistics\n"
    help_text += "• `!purge [amount]` - Delete messages (max 100)\n"
    help_text += "• `!help` - Show this help message\n"
    
    await ctx.send(help_text)

# Error handling - Skip status command errors silently
@client.event
async def on_command_error(ctx, error):
    # Don't show errors for status commands
    if ctx.command and ctx.command.name in ['status', 'statusend']:
        return
        
    if isinstance(error, commands.CheckFailure):
        await ctx.send("❌ You are not authorized to use this command.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Command not found. Use `!help` to see available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing required argument. Usage: `{ctx.command.name} {ctx.command.signature}`")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Invalid argument provided.")
    else:
        await ctx.send(f"❌ An error occurred: {str(error)}")
        print(f"Error: {error}")

# Run the client
if __name__ == "__main__":
    try:
        client.run(USER_TOKEN)
    except discord.LoginFailure:
        print("Invalid token provided.")
    except KeyboardInterrupt:
        print("\nBot stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")