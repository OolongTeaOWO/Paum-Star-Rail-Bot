# ------Discord------
from discord.ui import Button, View, button
from discord.ext import commands
from discord import Interaction, File
import discord
# -------other-------
from easy_pil import Editor, load_image_async, Font
from dotenv import load_dotenv
from datetime import datetime
from loguru import logger
import math
import json
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')
start_time = datetime.now()
bot = commands.Bot(command_prefix=commands.when_mentioned, intents=discord.Intents.all())

@bot.event
async def on_ready():
    for filename in os.listdir(os.path.join(os.path.dirname(__file__), 'slash_cogs')):
        if filename.endswith('.py'):
            extname = filename[:-3]
            await bot.load_extension(f'slash_cogs.{extname}')

    logger.info(f'{bot.user} | Ready!')

@bot.command(name='sync', brief='Bot Slash Command Sync', description='Bot Slash Command Sync')
async def sync_command(ctx):
    await bot.tree.sync()
    await ctx.send('已經準備好了帕!')
    logger.debug('extentions are synced to the command tree')

@bot.command(name='status', brief="帕姆醬的技能一覽", description="帕姆醬的技能一覽，用以除錯。\n會列出所有拓展名稱和權限")
async def status(ctx):
    if ctx.author.id not in (bot.owner_id, 541668345728991286):
        print(bot.owner_id)
        await bot.send(embed=discord.Embed(title="你還不夠格看我的資料帕", description=F"本指令只提供給機器人擁有者\n本機器人擁有者為<@{bot.owner_id}>"))
        return
    embed = discord.Embed(title="帕姆醬的技能一覽:")
    embed.add_field(name="目前延遲", value=F"{round(bot.latency*1000)}ms", inline=False)
    exts = "\n".join(ext.replace("slash_cogs.", "") for ext in bot.extensions)
    embed.add_field(name="已加載擴展", value=f">>> {exts}" if exts else "目前沒有任何擴展", inline=True)
    all_exts = "\n".join(filename[:-3] for filename in os.listdir(os.path.join(os.path.dirname(__file__), 'slash_cogs')) if filename.endswith('.py'))
    embed.add_field(name="目前擁有的擴展",value=f">>> {all_exts}" if all_exts else "找不到任何擴展", inline=True)
    embed.add_field(name="在線時間", value=f">>> <t:{int(start_time.timestamp())}:R>", inline=False)
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    user = ctx.author
    embed = discord.Embed(title="看看你做了什麼好事帕!",description=str(error), color=0xe01b24)
    embed.set_author(name=ctx.author.name,icon_url=ctx.author.avatar.url)
    embed.add_field(name="內容 Context",value=ctx.message.content)

    embed_config = discord.Embed(title="帕姆迷路了啦帕！",description="請在伺服器內創建名為錯誤通知區的頻道", color=0xe01b24)
    if isinstance(ctx.channel, discord.channel.DMChannel):
        embed.add_field(name="頻道 Channel",value="私人 Private")
        await user.send(embed=embed)
    else:
        channel = discord.utils.get(ctx.guild.channels, name="錯誤通知區")
        server_owner = ctx.guild.owner
        if channel:
            embed.add_field(name="頻道 Channel",value=ctx.guild.name+'/'+ctx.channel.name)
            await channel.send(embed=embed)
        else:
            await server_owner.send(embed=embed_config)

@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel #*定位使用者所進入的伺服器的系統頻道

    background = Editor("background.jpeg") #?宣告要編輯的圖片
    profile_image = await load_image_async(str(member.avatar.url)) #?宣告頭貼圖片

    profile = Editor(profile_image).resize((250, 250)).circle_image() #?將頭貼的完整圖片裁剪成圓形
    chinese_font = Font(path="TaipeiSansTCBeta-Bold.ttf", size=70) 

    #?宣告字型(若不特別指定則使用Font.poppins, 就不須指定path <<字型ttf檔)
    #* font_one = Font.poppins(size=70, variant="bold") >>blod粗體  italic斜體 light細體 regular預設(用這個不用填)
    
    background.paste(profile, (487, 90)) #?在背景圖片中貼上頭貼圖片
    background.ellipse((487, 90), 250, 250, outline = (255, 165, 0), stroke_width=10) 
    #?以背景圖中已經貼上的頭貼繞著繪製出外圈框並設定顏色和粗度

    if not member.bot: #!如果使用者不是機器人(機器人沒有global_name(全域名稱))
        background.text((612, 400), f'{member.global_name}', color = "white", font = chinese_font, align = "center")
    else:
        background.text((612, 400), f'{member.name}', color = "white", font = chinese_font, align = "center")
        #?設定圖片中置放的文字顏色、字體設定(前面宣告的字型)、並要求文字置中對齊

    file = File(fp=background.image_bytes, filename="background.jpeg")
    #!暫存上述動作後產生的圖檔(暫存而已沒有直接存檔)並宣告成file
    
    await channel.send(f'{member.mention}歡迎開拓者上車帕!, 列車:{member.guild.name}')
    await channel.send(file=file)

@bot.event
async def on_guild_join(guild):
    embed = discord.Embed(title="帕姆醬功能啟用前置", description="請在開拓者的伺服器新增以下幾個名稱的頻道以便啟用相關功能帕")
    embed.add_field(name="1.帕姆醬廣播室:", value="公告更新或錯誤修正之相關內容")
    embed.add_field(name="2.錯誤通知區:", value="如文字指令有誤可以在這裡看到")
    embed.add_field(name="3.回饋區:", value="如果有其他問題可直接藉由這個頻道反饋給機器人，並且轉傳至我們這邊（非必要，視開拓者需求決定是否添加）")
    try:
        await guild.owner.send(embed=embed)
        print(guild.owner_id)
    except:
        print(f"{guild.owner} has their dms turned off")
    if guild.system_channel:
        await guild.system_channel.send("很高興見到大家帕！今後還請多多指教帕！")
    else:
        pass

@bot.command()
async def push(ctx):
    if ctx.author.id not in (bot.owner_id, 541668345728991286):
        await ctx.send(embed=discord.Embed(title="你還不夠格帕", description=F"本指令只提供給機器人擁有者\n本機器人擁有者為<@{bot.owner_id}>"))
        return
    message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    for guild in bot.guilds:
        for channel in guild.channels:
            if isinstance(channel, discord.TextChannel) and channel.name == "帕姆醬廣播室":
                await channel.send(message.content)

bot.run(TOKEN)
    
