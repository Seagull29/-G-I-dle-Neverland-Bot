from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext import menus
import requests
from discord import Embed
from discord import Webhook, RequestsWebhookAdapter, File
from discord.ext.menus import MenuPages, ListPageSource
import json, aiohttp
from random import randint, sample
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
        menu = MyMenu()
        await menu.start(ctx)

    @command()
    async def webhook(self, ctx):
        webhook = Webhook.partial(762673145932152862, "yteYM8grVBoGl_HPLwhf6eTQMEuyNov2blJBNyHTrqno-A_RXld0icLKh0P2oeOiwmsD", adapter = RequestsWebhookAdapter())
        webhook.send("payaso")


    async def giphy_random(self, ctx, data):
        url = data['data']['images']['original']['url']
        longitud_codigo = 31 + url[31:].find("/")
        title = data['data']['title']
        search_type = data['data']['url']
        embed = Embed(title = "Giphy!", description = f"**Busqueda aleatoria:**", colour = ctx.author.colour, timestamp = datetime.utcnow())
        embed.set_author(name = data['data']['user']['display_name'] if 'user' in data['data'] else 'Autor desconocido', icon_url = data['data']['user']['avatar_url'] if 'user' in data['data'] else '')
        embed.set_thumbnail(url = "https://giphy.com/static/img/giphy_logo_square_social.png")
        embed.add_field(name = "Titulo", value = title if not title == '' and not title == ' ' else 'N/A', inline = True)
        embed.add_field(name = "Enlace", value = f"https://giphy.com/{'gifs' if not 'stickers' in search_type else 'stickers'}/{url[31 : longitud_codigo]}", inline = True)
        embed.set_footer(text = f"Solicitado por {ctx.author.display_name}", icon_url = ctx.author.avatar_url)
        embed.set_image(url= str(url))
        mensaje = await ctx.send(embed = embed)
        await mensaje.add_reaction("🤔")

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

   
    @command(name = "giphy", pass_context = True)
    async def giphy_command(self, ctx, search_type : str, *, search = None):
        session = aiohttp.ClientSession()

        if search_type in ["s", "stick", "stickers", "sticker"]:

            if search is None:
                response = await session.get('https://api.giphy.com/v1/stickers/trending?api_key=NMGKDkhX4308QRqQBCQW0n4V22o7XdUG&limit=30')
                data = json.loads(await response.text())
                direcciones = [[gif_object] for gif_object in data['data']]
                menu = MenuPages(source = Paginas(ctx, sample(direcciones, len(direcciones)), "***Trendings***"), delete_message_after = False)
                await menu.start(ctx)
            
            elif search in ["r", "random"]:
            
                response = await session.get('https://api.giphy.com/v1/stickers/random?api_key=NMGKDkhX4308QRqQBCQW0n4V22o7XdUG')
                data = json.loads(await response.text())
                #url = data['data']['images']['original']['url']
                await self.giphy_random(ctx, data)
            else:
                search.replace(' ', '+')
                response = await session.get('http://api.giphy.com/v1/stickers/search?q=' + search + '&api_key=NMGKDkhX4308QRqQBCQW0n4V22o7XdUG&limit=30')
                data = json.loads(await response.text())
                direcciones = [[gif_object] for gif_object in data['data']]
                #for url in data['data']:
                #    direcciones.append([url['images']['original']['url']]) # Filtra del archivo json todas las urls de la busqueda
                
                menu = MenuPages(source = Paginas(ctx, sample(direcciones, len(direcciones)), search), delete_message_after = False)
                await menu.start(ctx)  

        elif search_type in ["g", "gif"]:

            if search is None:
                response = await session.get('https://api.giphy.com/v1/gifs/trending?api_key=NMGKDkhX4308QRqQBCQW0n4V22o7XdUG&limit=30')
                data = json.loads(await response.text())
                direcciones = [[gif_object] for gif_object in data['data']]
                menu = MenuPages(source = Paginas(ctx, sample(direcciones, len(direcciones)), "***Trendings***"), delete_message_after = False)
                await menu.start(ctx)
            
            elif search in ["r", "random"]:
            
                response = await session.get('https://api.giphy.com/v1/gifs/random?api_key=NMGKDkhX4308QRqQBCQW0n4V22o7XdUG')
                data = json.loads(await response.text())
                #url = data['data']['images']['original']['url']
                await self.giphy_random(ctx, data)
            else:
                search.replace(' ', '+')
                response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=NMGKDkhX4308QRqQBCQW0n4V22o7XdUG&limit=30')
                data = json.loads(await response.text())
                direcciones = [[gif_object] for gif_object in data['data']]
                #for url in data['data']:
                #    direcciones.append([url['images']['original']['url']]) # Filtra del archivo json todas las urls de la busqueda
                
                menu = MenuPages(source = Paginas(ctx, sample(direcciones, len(direcciones)), search), delete_message_after = False)
                await menu.start(ctx)  
        await session.close()

    @command(name = "tenor", pass_context = True)
    async def tenor_command(self, ctx):
        pass


class Paginas(ListPageSource):
    def __init__(self, ctx, data, busqueda):
        self.ctx = ctx
        self.busqueda = busqueda
        self.urls = data # Recibe la lista de las urls 
        super().__init__(data, per_page = 1)

    async def format_page(self, menu, entries):
        offset = (menu.current_page * self.per_page) + 1
        len_data = len(self.entries)
    
        url = self.urls[menu.current_page][0]['images']['original']['url']
        title  = self.urls[menu.current_page][0]['title'] 
        search_type = self.urls[menu.current_page][0]['url']

        longitud_codigo = 31 + url[31:].find("/")
        print ("Flag " + url)
        embed = Embed(title = "Giphy!", 
                      description = f"**Resultados para:** *{self.busqueda}*", 
                      colour = self.ctx.author.colour, timestamp = datetime.utcnow())

        embed.set_author(name = self.urls[menu.current_page][0]['user']['display_name'] if 'user' in self.urls[menu.current_page][0] else 'Autor desconocido', 
                         icon_url = self.urls[menu.current_page][0]['user']['avatar_url'] if 'user' in self.urls[menu.current_page][0] else '')

        embed.set_thumbnail(url = "https://giphy.com/static/img/giphy_logo_square_social.png")

        fields = [("Titulo", title if not title == '' and not title == ' ' else 'N/A', True),
                  ("Enlace", f"https://giphy.com/{'gifs' if not 'stickers' in search_type else 'stickers'}/{url[31 : longitud_codigo]}", True)]

        for name, value, inline in fields:
            embed.add_field(name = name, value = value, inline = inline)
        embed.set_footer(text = f"Solicitado por {self.ctx.author.display_name}" + "\n" + f"{offset:,} de {len_data:,} gifs.", icon_url = self.ctx.author.avatar_url)
        
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

