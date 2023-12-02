import discord
from discord.ext import commands
import os
from krakenfiles_module import download_from_krakenfiles

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")

@bot.command()
async def kraken(ctx, url: str):

    
    try:
        embed= discord.Embed(
            title='Successfully Retrieved Your File!'
        )
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar.url)
        embed.set_footer(text="tha23rd", icon_url="https://avatars.githubusercontent.com/u/54587508?v=4")
        file_path = download_from_krakenfiles(url)
        await ctx.reply(embed=embed, file=discord.File(file_path))

        # Delete the file after sending
        os.remove(file_path)
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

# place ur bot token
bot.run('')
