from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Embed
from typing import Optional
import requests, json, aiohttp
from discord.ext.menus import ListPageSource, MenuPages
from datetime import datetime
import urllib, re

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Fun")

    @command(name = "cmd", aliases = ["sc"])
    async def seomcommand(self, ctx):
        await ctx.send(f"Hola {ctx.author.mention}")


   # async def get_last_photo(self, search):
    #    return search.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["display_url"]

    @command(name = "ig", aliases = ["instagram"])
    async def instagram_search(self, ctx, account : Optional[str] = None):
        print ("last_photo")
        session = aiohttp.ClientSession()
        search = await session.get("https://www.instagram.com/" + "natgeo" + "/?__a=1")
        data = json.loads(await search.text())
        last_photo = data["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["display_url"]
        print (last_photo)
        embed = Embed(title = "Resultado", colour = ctx.author.colour)
        embed.set_image(url = last_photo)
        await session.close()
        await ctx.send(embed = embed)

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


    async def random_gif(self, ctx, url):
        longitud_codigo = 31 + url[31:].find("/")
        embed = Embed(title = "Giphy!", description = f"**Busqueda aleatoria:**" + "\n" + f"**Enlace:** https://giphy.com/gifs/{url[31 : longitud_codigo]}", colour = ctx.author.colour, timestamp = datetime.utcnow())
        embed.set_footer(text = f"Solicitado por {ctx.author.display_name}", icon_url = ctx.author.avatar_url)
        embed.set_image(url= str(url))
        mensaje = await ctx.send(embed = embed)
        await mensaje.add_reaction("🤔")

    @command(name = "gif", pass_context = True)
    async def giphy(self, ctx, *, search = None):
        session = aiohttp.ClientSession()
        if search is None:
            response = await session.get('https://api.giphy.com/v1/gifs/random?api_key=NMGKDkhX4308QRqQBCQW0n4V22o7XdUG')
            data = json.loads(await response.text())
            url = data['data']['images']['original']['url']
            await self.random_gif(ctx, url)
        else:
            search.replace(' ', '+')
            response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=NMGKDkhX4308QRqQBCQW0n4V22o7XdUG&limit=20')
            data = json.loads(await response.text())
            direcciones = []
            for url in data['data']:
                direcciones.append([url['images']['original']['url']]) # Filtra del archivo json todas las urls de la busqueda
            
            menu = MenuPages(source = Paginas(ctx, direcciones, search), delete_message_after = False)
            await menu.start(ctx)  
        await session.close()
    

class Paginas(ListPageSource):
    def __init__(self, ctx, data, busqueda):
        self.ctx = ctx
        self.busqueda = busqueda
        self.urls = data # Recibe la lista de las urls 
        super().__init__(data, per_page = 1)

    async def format_page(self, menu, entries):
        offset = (menu.current_page * self.per_page) + 1
        len_data = len(self.entries)
    
        url = self.urls[menu.current_page][0]
        longitud_codigo = 31 + url[31:].find("/")
        print ("Flag " + url)
        embed = Embed(title = "Giphy!", 
                      description = f"**Resultados para:** *{self.busqueda}*" + "\n" + f"**Enlace:** https://giphy.com/gifs/{url[31 : longitud_codigo]}", 
                      colour = self.ctx.author.colour, timestamp = datetime.utcnow())
        embed.set_footer(text = f"Solicitado por {self.ctx.author.display_name}" + "\n" + f"{offset:,} de {len_data:,} resultados.", icon_url = self.ctx.author.avatar_url)
        
        embed.set_image(url= str(url))
        return embed


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


def setup(bot):
    bot.add_cog(Fun(bot))

