import discord
from discord.ext import commands
import wavelink
from mcstatus import JavaServer

# تنظیمات اینتن‌های دیسکورد
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="/", intents=intents)

# توکن بات مستقیم اینجا قرار گرفت
TOKEN = "import discord
from discord.ext import commands
import wavelink
from mcstatus import JavaServer

# تنظیمات اینتن‌های دیسکورد
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="/", intents=intents)

# توکن بات مستقیم اینجا قرار گرفت
TOKEN = "توکن_رو_دقیقاً_اینجا_پیست_کن"

@bot.event
async def on_ready():
    print(f'حله! بات {bot.user} با موفقیت آنلاین شد.')
    
    # راه‌اندازی اولیه واولینک برای اتصال به یوتیوب موزیک (مثل لونا بات)
    try:
        nodes = [wavelink.Node(uri='YOUR_LAVALINK_HOST:PORT', password='YOUR_LAVALINK_PASSWORD')]
        await wavelink.Pool.init(nodes=nodes)
        print('واولینک به سرور موزیک وصل شد!')
    except Exception as e:
        print(f'خطا در اتصال به واولینک: {e}')

# ==================== بخش ماینکرفت ====================
@bot.tree.command(name="server", description="بررسی وضعیت و تعداد پلیرهای سرور ماینکرفت")
async def server_status(interaction: discord.Interaction, ip: str):
    try:
        server = JavaServer.lookup(ip)
        status = server.status()
        
        embed = discord.Embed(title="📊 وضعیت سرور ماینکرفت", color=discord.Color.green())
        embed.add_field(name="آی‌پی سرور", value=ip, inline=False)
        embed.add_field(name="تعداد پلیرها", value=f"{status.players.online} / {status.players.max}", inline=True)
        embed.add_field(name="پینگ", value=f"{status.latency} ms", inline=True)
        embed.add_field(name="نسخه", value=status.version.name, inline=False)
        
        await interaction.response.send_message(embed=embed)
    except Exception:
        await interaction.response.send_message("❌ نتونستم به سرور وصل بشم! آی‌پی رو چک کن.")

@bot.tree.command(name="ping", description="پینگ بات و سرور")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"🏓 پونک! تاخیر بات: `{latency}ms`")

# ==================== بخش موزیک (مشابه لونا بات) ====================
@bot.tree.command(name="join", description="متصل کردن بات به ویس چنل")
async def join_voice(interaction: discord.Interaction):
    if not interaction.user.voice:
        return await interaction.response.send_message("❌ اول باید یه ویس چنل باشی داداش!", ephemeral=True)
    
    channel = interaction.user.voice.channel
    if interaction.guild.voice_client is not None:
        await interaction.guild.voice_client.move_to(channel)
    else:
        await channel.connect(cls=wavelink.Player)
    
    await interaction.response.send_message(f"🔊 اومدم تو ویس: **{channel.name}**")

@bot.tree.command(name="play", description="پخش آهنگ درخواستی از یوتیوب موزیک")
async def play_music(interaction: discord.Interaction, search: str):
    if not interaction.guild.voice_client:
        return await interaction.response.send_message("❌ اول باید با دستور `/join` منو بیاری تو ویس!", ephemeral=True)

    await interaction.response.defer()
    player = interaction.guild.voice_client

    tracks = await wavelink.YouTubeTrack.search(search)
    if not tracks:
        return await interaction.followup.send("❌ آهنگی با این اسم پیدا نکردم!")

    track = tracks[0]
    await player.play(track)
    
    embed = discord.Embed(title="🎵 در حال پخش آهنگ", description=f"[{track.title}]({track.uri})", color=discord.Color.blue())
    embed.add_field(name="کانال", value=track.author, inline=True)
    embed.add_field(name="مدت زمان", value=f"{track.duration // 60}:{track.duration % 60:02d}", inline=True)
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="leave", description="خروج بات از ویس چنل")
async def leave_voice(interaction: discord.Interaction):
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("👋 از ویس خارج شدم.")
    else:
        await interaction.response.send_message("❌ جایی نیستم که بخوام خارج بشم!", ephemeral=True)

# ==================== بخش مدیریت استاف ====================
@bot.tree.command(name="staff_warn", description="ثبت اخطار رسمی به ادمین یا استاف")
@commands.has_permissions(administrator=True)
async def staff_warn(interaction: discord.Interaction, member: discord.Member, *, reason: str):
    embed = discord.Embed(title="⚠️ اخطار مدیریتی (استاف)", color=discord.Color.red())
    embed.add_field(name="استاف خاطی", value=member.mention, inline=False)
    embed.add_field(name="دلیل", value=reason, inline=False)
    embed.set_footer(text=f"ثبت شده توسط: {interaction.user.name}")
    
    await interaction.response.send_message(embed=embed)

# ==================== بخش فان و سرگرمی ====================
@bot.tree.command(name="rps", description="بازی سنگ، کاغذ، قیچی با بات")
async def rps(interaction: discord.Interaction, choice: str):
    import random
    options = ["سنگ", "کاغذ", "قیچی"]
    user_choice = choice.lower()
    
    if user_choice not in options:
        return await interaction.response.send_message("❌ فقط می‌تونی بزنی: سنگ، کاغذ، یا قیچی!", ephemeral=True)
        
    bot_choice = random.choice(options)
    
    if user_choice == bot_choice:
        result = "مساوی شدیم!"
    elif (user_choice == "سنگ" and bot_choice == "قیچی") or \
         (user_choice == "کاغذ" and bot_choice == "سنگ") or \
         (user_choice == "قیچی" and bot_choice == "کاغذ"):
        result = "ایول، تو بردی! 🎉"
    else:
        result = "من بردم! 😎"
        
    await interaction.response.send_message(f"تو زدی: **{user_choice}**\nمن زدم: **{bot_choice}**\n\n**نتیجه:** {result}")

# سینک کردن اسلش کامندها
@bot.event
async def on_ready_sync():
    await bot.tree.sync()

# استارت اصلی بات
bot.run(TOKEN)
"

@bot.event
async def on_ready():
    print(f'حله! بات {bot.user} با موفقیت آنلاین شد.')
    
    # راه‌اندازی اولیه واولینک برای اتصال به یوتیوب موزیک (مثل لونا بات)
    try:
        nodes = [wavelink.Node(uri='YOUR_LAVALINK_HOST:PORT', password='YOUR_LAVALINK_PASSWORD')]
        await wavelink.Pool.init(nodes=nodes)
        print('واولینک به سرور موزیک وصل شد!')
    except Exception as e:
        print(f'خطا در اتصال به واولینک: {e}')

# ==================== بخش ماینکرفت ====================
@bot.tree.command(name="server", description="بررسی وضعیت و تعداد پلیرهای سرور ماینکرفت")
async def server_status(interaction: discord.Interaction, ip: str):
    try:
        server = JavaServer.lookup(ip)
        status = server.status()
        
        embed = discord.Embed(title="📊 وضعیت سرور ماینکرفت", color=discord.Color.green())
        embed.add_field(name="آی‌پی سرور", value=ip, inline=False)
        embed.add_field(name="تعداد پلیرها", value=f"{status.players.online} / {status.players.max}", inline=True)
        embed.add_field(name="پینگ", value=f"{status.latency} ms", inline=True)
        embed.add_field(name="نسخه", value=status.version.name, inline=False)
        
        await interaction.response.send_message(embed=embed)
    except Exception:
        await interaction.response.send_message("❌ نتونستم به سرور وصل بشم! آی‌پی رو چک کن.")

@bot.tree.command(name="ping", description="پینگ بات و سرور")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"🏓 پونک! تاخیر بات: `{latency}ms`")

# ==================== بخش موزیک (مشابه لونا بات) ====================
@bot.tree.command(name="join", description="متصل کردن بات به ویس چنل")
async def join_voice(interaction: discord.Interaction):
    if not interaction.user.voice:
        return await interaction.response.send_message("❌ اول باید یه ویس چنل باشی داداش!", ephemeral=True)
    
    channel = interaction.user.voice.channel
    if interaction.guild.voice_client is not None:
        await interaction.guild.voice_client.move_to(channel)
    else:
        await channel.connect(cls=wavelink.Player)
    
    await interaction.response.send_message(f"🔊 اومدم تو ویس: **{channel.name}**")

@bot.tree.command(name="play", description="پخش آهنگ درخواستی از یوتیوب موزیک")
async def play_music(interaction: discord.Interaction, search: str):
    if not interaction.guild.voice_client:
        return await interaction.response.send_message("❌ اول باید با دستور `/join` منو بیاری تو ویس!", ephemeral=True)

    await interaction.response.defer()
    player = interaction.guild.voice_client

    tracks = await wavelink.YouTubeTrack.search(search)
    if not tracks:
        return await interaction.followup.send("❌ آهنگی با این اسم پیدا نکردم!")

    track = tracks[0]
    await player.play(track)
    
    embed = discord.Embed(title="🎵 در حال پخش آهنگ", description=f"[{track.title}]({track.uri})", color=discord.Color.blue())
    embed.add_field(name="کانال", value=track.author, inline=True)
    embed.add_field(name="مدت زمان", value=f"{track.duration // 60}:{track.duration % 60:02d}", inline=True)
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="leave", description="خروج بات از ویس چنل")
async def leave_voice(interaction: discord.Interaction):
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("👋 از ویس خارج شدم.")
    else:
        await interaction.response.send_message("❌ جایی نیستم که بخوام خارج بشم!", ephemeral=True)

# ==================== بخش مدیریت استاف ====================
@bot.tree.command(name="staff_warn", description="ثبت اخطار رسمی به ادمین یا استاف")
@commands.has_permissions(administrator=True)
async def staff_warn(interaction: discord.Interaction, member: discord.Member, *, reason: str):
    embed = discord.Embed(title="⚠️ اخطار مدیریتی (استاف)", color=discord.Color.red())
    embed.add_field(name="استاف خاطی", value=member.mention, inline=False)
    embed.add_field(name="دلیل", value=reason, inline=False)
    embed.set_footer(text=f"ثبت شده توسط: {interaction.user.name}")
    
    await interaction.response.send_message(embed=embed)

# ==================== بخش فان و سرگرمی ====================
@bot.tree.command(name="rps", description="بازی سنگ، کاغذ، قیچی با بات")
async def rps(interaction: discord.Interaction, choice: str):
    import random
    options = ["سنگ", "کاغذ", "قیچی"]
    user_choice = choice.lower()
    
    if user_choice not in options:
        return await interaction.response.send_message("❌ فقط می‌تونی بزنی: سنگ، کاغذ، یا قیچی!", ephemeral=True)
        
    bot_choice = random.choice(options)
    
    if user_choice == bot_choice:
        result = "مساوی شدیم!"
    elif (user_choice == "سنگ" and bot_choice == "قیچی") or \
         (user_choice == "کاغذ" and bot_choice == "سنگ") or \
         (user_choice == "قیچی" and bot_choice == "کاغذ"):
        result = "ایول، تو بردی! 🎉"
    else:
        result = "من بردم! 😎"
        
    await interaction.response.send_message(f"تو زدی: **{user_choice}**\nمن زدم: **{bot_choice}**\n\n**نتیجه:** {result}")

# سینک کردن اسلش کامندها
@bot.event
async def on_ready_sync():
    await bot.tree.sync()

# استارت اصلی بات
bot.run(TOKEN)
