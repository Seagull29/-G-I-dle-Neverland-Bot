from discord.ext.commands import Cog
from discord.ext.commands import command, group
from discord.ext import menus
import requests
from discord import Embed
from discord import Webhook, RequestsWebhookAdapter, File
from discord.ext.menus import MenuPages, ListPageSource
import json, aiohttp
from random import randint, sample
from datetime import datetime
import urllib, re


GIPHY = "giphy"
TENOR = "tenor"
TRENDING_LABEL = "***Trendings***"

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Fun")

    @command(name = "cmd", aliases = ["sc"])
    async def seomcommand(self, ctx):
        menu = MyMenu()
        await menu.start(ctx)

    @command()
    async def webhook(self, ctx):
        webhook = Webhook.partial(762673145932152862, "yteYM8grVBoGl_HPLwhf6eTQMEuyNov2blJBNyHTrqno-A_RXld0icLKh0P2oeOiwmsD", adapter = RequestsWebhookAdapter())
        webhook.send("payaso")

    @command(name = "yt", aliases = ["youtube"])
    async def youtube_search(self, ctx, *, video):
        if len(video) == 0:
            await ctx.send("Indique que desea buscar")
        else:
            search_keyword = video.replace(" ", "+")
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            urls = [[url] for url in video_ids]
            menu = MenuPages(source = BusquedaYoutube(ctx, urls), delete_message_after = False)
            await menu.start(ctx)
            #await ctx.send("https://www.youtube.com/watch?v=" + video_ids[0])


class BusquedaYoutube(ListPageSource):
    def __init__(self, ctx, data):
        self.ctx = ctx
        self.urls = data
        super().__init__(data, per_page = 1)

    def format_page(self, menu, entries):
        offset = (menu.current_page * self.per_page) + 1
        len_data = len(self.entries)
        url = "https://www.youtube.com/watch?v=" + self.urls[menu.current_page][0] + "\n" + f"**Solicitado por {self.ctx.author.display_name}**" + " | " + f"*{offset:,} de {len_data:,} videos.*"
        return url 

class MyMenu(menus.Menu):
    async def send_initial_message(self, ctx, channel):
        return await channel.send(f'Hello {ctx.author}')

    @menus.button('👍')
    async def on_thumbs_up(self, payload):
        await self.message.edit(content=f'Thanks {self.ctx.author}!')

    @menus.button('\N{THUMBS DOWN SIGN}')
    async def on_thumbs_down(self, payload):
        await self.message.edit(content=f"That's not nice {self.ctx.author}...")

    @menus.button('\N{BLACK SQUARE FOR STOP}\ufe0f')
    async def on_stop(self, payload):
        self.stop()
   

def setup(bot):
    bot.add_cog(Fun(bot))

