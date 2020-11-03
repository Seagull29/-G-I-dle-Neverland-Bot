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


    async def giphy_random(self, ctx, data):
        url = data['data']['images']['original']['url']
        longitud_codigo = 31 + url[31:].find("/")
        title = data['data']['title']
        search_type = data['data']['url']
        embed = Embed(title = "Giphy!", description = f"**Busqueda aleatoria:**", colour = ctx.author.colour, timestamp = datetime.utcnow())
        embed.set_author(name = data['data']['user']['display_name'] if 'user' in data['data'] else 'Autor desconocido', icon_url = data['data']['user']['avatar_url'] if 'user' in data['data'] else '')
        embed.set_thumbnail(url = "https://giphy.com/static/img/giphy_logo_square_social.png")
        embed.add_field(name = "Titulo", value = f'*{title}*' if not title == '' and not title == ' ' else 'N/A', inline = True)
        embed.add_field(name = "Enlace", value = f"*https://giphy.com/{'gifs' if not 'stickers' in search_type else 'stickers'}/{url[31 : longitud_codigo]}*", inline = True)
        embed.set_footer(text = f"Solicitado por {ctx.author.display_name}", icon_url = ctx.author.avatar_url)
        embed.set_image(url= str(url))
        Intermediario.set_url(embed)
        mensaje = await ctx.send(embed = embed)
        await mensaje.add_reaction("🤔")


    async def send_gif(self, ctx):
        def check(m):
                return m.channel == ctx.channel and m.content == "s" and m.author == ctx.author 
        mensaje = await self.bot.wait_for('message', check = check)
        await ctx.channel.purge(limit = 1)
        await ctx.author.send(content = f">>> **{ctx.author.display_name}, su gif:**", embed = Intermediario.url())



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

    """
    @group(name = "giphy", aliases = ["gy"], invoke_without_command = True)
    async def giphy_group(self, ctx):
        pass

    @group(name = "tenor", aliases = ["ten"], invoke_without_command = True)
    async def tenor_group(self, ctx):
        pass

    @giphy_group.group(name = "gif", aliases = ["gf", "g"], invoke_without_command = True)
    async def giphy_search_gif_subgroup(self, ctx, *, search):
        session = aiohttp.ClientSession()
        if search is not None:
            search.replace(' ', '+')
            response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=NMGKDkhX4308QRqQBCQW0n4V22o7XdUG&limit=30')
            data = json.loads(await response.text())
            direcciones = [[gif_object] for gif_object in data['data']]
            #for url in data['data']:
             #    direcciones.append([url['images']['original']['url']]) # Filtra del archivo json todas las urls de la busqueda 
            menu = MenuPages(source = Paginas(ctx, sample(direcciones, len(direcciones)), search, GIPHY), delete_message_after = False)
            await menu.start(ctx)
        else:
            response = await session.get('https://api.giphy.com/v1/gifs/random?api_key=NMGKDkhX4308QRqQBCQW0n4V22o7XdUG')
            data = json.loads(await response.text())
            #url = data['data']['images']['original']['url']
            await self.giphy_random(ctx, data)
        await self.send_gif(ctx)
        await session.close()

    @giphy_search_gif_subgroup.command(name = "trend", aliases = ["trending", "tt"])
    async def giphy_trending_gif_subcommand(self, ctx):
        session = aiohttp.ClientSession()
        response = await session.get('https://api.giphy.com/v1/gifs/trending?api_key=NMGKDkhX4308QRqQBCQW0n4V22o7XdUG&limit=30')
        data = json.loads(await response.text())
        direcciones = [[gif_object] for gif_object in data['data']]
        menu = MenuPages(source = Paginas(ctx, sample(direcciones, len(direcciones)), TRENDING_LABEL, GIPHY), delete_message_after = False)
        await menu.start(ctx)
        await self.send_gif(ctx) 
        await session.close()


    @giphy_group.group(name = "sticker", aliases = ["stick", "stk"], invoke_without_command = True)
    async def giphy_search_sticker_subgroup(self, ctx, *, search):
        session = aiohttp.ClientSession()
        if search is not None:
            search.replace(' ', '+')
            response = await session.get('http://api.giphy.com/v1/stickers/search?q=' + search + '&api_key=NMGKDkhX4308QRqQBCQW0n4V22o7XdUG&limit=30')
            data = json.loads(await response.text())
            direcciones = [[gif_object] for gif_object in data['data']]
            #for url in data['data']:
            #    direcciones.append([url['images']['original']['url']]) # Filtra del archivo json todas las urls de la busqueda
            menu = MenuPages(source = Paginas(ctx, sample(direcciones, len(direcciones)), search, GIPHY), delete_message_after = False)
            await menu.start(ctx)
        else:
            response = await session.get('https://api.giphy.com/v1/stickers/random?api_key=NMGKDkhX4308QRqQBCQW0n4V22o7XdUG')
            data = json.loads(await response.text())
            #url = data['data']['images']['original']['url']
            await self.giphy_random(ctx, data)
        await self.send_gif(ctx)
        await session.close()
            
    @giphy_search_sticker_subgroup.command(name = "trend", aliases = ["trending", "tt"])
    async def giphy_trending_sticker_subcommand(self, ctx):
        session = aiohttp.ClientSession()
        response = await session.get('https://api.giphy.com/v1/stickers/trending?api_key=NMGKDkhX4308QRqQBCQW0n4V22o7XdUG&limit=30')
        data = json.loads(await response.text())
        direcciones = [[gif_object] for gif_object in data['data']]
        menu = MenuPages(source = Paginas(ctx, sample(direcciones, len(direcciones)), TRENDING_LABEL, GIPHY), delete_message_after = False)
        await menu.start(ctx)
        await self.send_gif(ctx)
        await session.close()

    """

    @command(name = "giphy", aliases = ["gy"], pass_context = True)
    async def giphy_command(self, ctx, search_type : str, *, search = None):
        session = aiohttp.ClientSession()

        if search_type in ["s", "stick", "stickers", "sticker"]:

            if search is None:
                response = await session.get('https://api.giphy.com/v1/stickers/trending?api_key=NMGKDkhX4308QRqQBCQW0n4V22o7XdUG&limit=30')
                data = json.loads(await response.text())
                direcciones = [[gif_object] for gif_object in data['data']]
                menu = MenuPages(source = Paginas(ctx, sample(direcciones, len(direcciones)), TRENDING_LABEL, GIPHY), delete_message_after = False)
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
                
                menu = MenuPages(source = Paginas(ctx, sample(direcciones, len(direcciones)), search, GIPHY), delete_message_after = False)
                await menu.start(ctx)
            await self.send_gif(ctx) 

        elif search_type in ["g", "gif"]:

            if search is None:
                response = await session.get('https://api.giphy.com/v1/gifs/trending?api_key=NMGKDkhX4308QRqQBCQW0n4V22o7XdUG&limit=30')
                data = json.loads(await response.text())
                direcciones = [[gif_object] for gif_object in data['data']]
                menu = MenuPages(source = Paginas(ctx, sample(direcciones, len(direcciones)), TRENDING_LABEL, GIPHY), delete_message_after = False)
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
                
                menu = MenuPages(source = Paginas(ctx, sample(direcciones, len(direcciones)), search, GIPHY), delete_message_after = False)
                await menu.start(ctx)  
            await self.send_gif(ctx)
        await session.close()

    @command(name = "tenor", pass_context = True)
    async def tenor_command(self, ctx, *, search = None):
        session = aiohttp.ClientSession()
        if search is None:
            response = await session.get('https://api.tenor.com/v1/trending?key=87NYM0CK0LBX&limit=30')
            data = json.loads(await response.text())
            direcciones = [[gif_object] for gif_object in data['results']]
            menu = MenuPages(source = Paginas(ctx, sample(direcciones, len(direcciones)), TRENDING_LABEL, TENOR), delete_message_after = False)
            await menu.start(ctx)
            await self.send_gif(ctx)
        await session.close()

class Intermediario():
    
    __url = ""

    @classmethod
    def set_url(cls, url):
        Intermediario.__url = url 

    @classmethod
    def url(cls):
        return Intermediario.__url
    


class Paginas(ListPageSource):
    def __init__(self, ctx, data, busqueda, source):
        self.ctx = ctx
        self.busqueda = busqueda
        self.urls = data # Recibe la lista de las urls 
        self.source = source
        super().__init__(data, per_page = 1)

    async def format_page(self, menu, entries):
        offset = (menu.current_page * self.per_page) + 1
        len_data = len(self.entries)

        if self.source == GIPHY:
            url = self.urls[menu.current_page][0]['images']['original']['url']
            title  = self.urls[menu.current_page][0]['title'] 
            search_type = self.urls[menu.current_page][0]['url']
            id = self.urls[menu.current_page][0]['id']
            content_source = self.urls[menu.current_page][0]['source']

            if 'user' in self.urls[menu.current_page][0]:
                name_author = self.urls[menu.current_page][0]['user']['display_name']
                if  name_author in ['', ' ']:
                    name_author = self.urls[menu.current_page][0]['user']['username']
                    if name_author in ['', ' ']:
                        name_author = 'Autor desconocido'
            else:
                name_author = 'Autor desconocido'

            #longitud_codigo = 31 + url[31:].find("/")
            print ("Flag " + url)
            embed = Embed(title = "Giphy!", 
                        description = f"**Resultados para:** *{self.busqueda}*", 
                        colour = self.ctx.author.colour, timestamp = datetime.utcnow())

            embed.set_author(name = name_author, 
                            icon_url = self.urls[menu.current_page][0]['user']['avatar_url'] if 'user' in self.urls[menu.current_page][0] else '')

            embed.set_thumbnail(url = "https://giphy.com/static/img/giphy_logo_square_social.png")

            fields = [("Titulo", f'*{title}*' if not title == '' and not title == ' ' else '*N/A*', True), ("ID", id, True), 
                      ("Enlace", f"https://giphy.com/{'gifs' if not 'stickers' in search_type else 'stickers'}/{id}", False),
                      ("Fuente", f'*{content_source}*' if not content_source == '' and not content_source == ' ' else '*Fuente desconocida*', False)]
            for name, value, inline in fields:
                embed.add_field(name = name, value = value, inline = inline)
    
            embed.set_footer(text = f"Solicitado por {self.ctx.author.display_name}" + "\n" + f"{offset:,} de {len_data:,} gifs.", icon_url = self.ctx.author.avatar_url)
            embed.set_image(url= str(url))
            Intermediario.set_url(embed)
            return embed

        elif self.source == TENOR:
            url = self.urls[menu.current_page][0]['media'][0]['gif']['url']
            title = self.urls[menu.current_page][0]['title'] 
            id = self.urls[menu.current_page][0]['id']
            print ("URL " + url)
            embed = Embed(title = "Tenor!", description = f"**Resultados para:** *{self.busqueda}*",
                          colour = self.ctx.author.colour, timestamp = datetime.utcnow())
            embed.set_thumbnail(url = "https://www.brandchannel.com/wp-content/uploads/2017/04/tenor-logo.jpg")
            embed.add_field(name = "Titulo", value = f'*{title}*' if not title == '' and not title == ' ' else '*N/A*', inline = True)
            embed.add_field(name = "ID", value = f'*{id}*', inline = True)
            embed.add_field(name = "Enlace", value = f"*https://tenor.com/view/{id}*", inline = False)
            embed.set_footer(text = f"Solicitado por {self.ctx.author.display_name}" + "\n" + f"{offset:,} de {len_data:,} gifs.", icon_url = self.ctx.author.avatar_url) 
            embed.set_image(url = url)
            Intermediario.set_url(embed)
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

