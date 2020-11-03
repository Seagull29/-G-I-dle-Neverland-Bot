from discord.ext.commands import command, group, Cog
from datetime import datetime
import json, aiohttp
from random import sample
from discord import Embed
from discord.ext.menus import MenuPages, ListPageSource

TRENDING_LABEL = "**Trendings**"
RANDOM_SEARCH = "Aleatorios de "

class Giphy:

    __SOURCE = "Giphy!"
    __THUMBNAIL = "https://giphy.com/static/img/giphy_logo_square_social.png"

    def __init__(self, data):
        self._data = data
        
    @classmethod
    def get_source(cls):
        return cls.__SOURCE

    @classmethod
    def get_thumbnail(cls):
        return cls.__THUMBNAIL

    @property
    def get_author(self):
        if 'user' in self._data:
            self.author = self._data['user']['display_name']
            if self.author in ['', ' ']:
                self.author = self._data['user']['username']
                if self.author in ['', ' ']:
                    self.author = 'Autor desconocido'
        else:
            self.author = 'Autor desconocido'
        return self.author

    @property
    def get_author_avatar(self):
        if 'user' in self._data:
            self.author_avatar = self._data['user']['avatar_url']
            return self.author_avatar
        else:
            self.author_avatar = ''
            return self.author_avatar

    @property 
    def get_title(self):
        if not self._data['title'] in ['', ' ']:
            self.title = self._data['title']
            return self.title
        else:
            self.title = 'N/A'
            return self.title

    @property
    def get_id(self):
        self.id = self._data['id']
        return self.id

    @property
    def get_url(self):
        self.url = self._data['images']['original']['url']
        return self.url

    @property
    def get_content_source(self):
        if not self._data['source'] in ['', ' ']:
            self.content_source = self._data['source']
            return self.content_source
        else:
            self.content_source = 'Fuente desconocida'
            return self.content_source

    @property
    def get_search_address(self):
        if 'stickers' in self._data['url'][:27]:
            self.search_address = f"https://giphy.com/stickers/{self.get_id}"
        else:
            self.search_address = f"https://giphy.com/gifs/{self.get_id}"
        return self.search_address


class Tenor:
    
    __SOURCE = "Tenor!"
    __THUMBNAIL = "https://www.brandchannel.com/wp-content/uploads/2017/04/tenor-logo.jpg"

    def __init__(self, data):
        self._data = data

    @classmethod
    def get_thumbnail(cls):
        return cls.__THUMBNAIL

    @classmethod
    def get_source(cls):
        return cls.__SOURCE

    @property
    def get_title(self):
        if not self._data['title'] in ['', ' ']:
            self.title = self._data['title']
        else:
            self.title = 'N/A'
        return self.title

    @property
    def get_id(self):
        self.id = self._data['id']
        return self.id

    @property
    def get_search_address(self):
        self.search_address = f"https://tenor.com/view/{self.get_id}"
        return self.search_address

    @property
    def get_url(self):
        self.url = self._data['media'][0]['gif']['url']
        return self.url

class Intermediario:
    
    __url = ""

    @classmethod
    def set_url(cls, url):
        cls.__url = url 

    @classmethod
    def url(cls):
        return cls.__url


class Paginas(ListPageSource):
    def __init__(self, ctx, data, busqueda):
        self.ctx = ctx
        self.busqueda = busqueda
        self.urls = data # Recibe la lista de objetos con los resultados 
        super().__init__(data, per_page = 1)

    async def format_page(self, menu, entries):
        offset = (menu.current_page * self.per_page) + 1
        len_data = len(self.entries)
        current_object = self.urls[menu.current_page][0]
        if isinstance(current_object, Giphy):
            #longitud_codigo = 31 + url[31:].find("/")
            print ("Flag " + str(current_object))
            embed = Embed(title = f"*{current_object.get_source()}*", description = f"**Resultados para:** *{self.busqueda}*", colour = self.ctx.author.colour, timestamp = datetime.utcnow())
            embed.set_author(name = current_object.get_author, icon_url = current_object.get_author_avatar)
            embed.set_thumbnail(url = current_object.get_thumbnail())
            fields = [("Titulo", f'*{current_object.get_title}*', True), ("ID", f"*{current_object.get_id}*", True), 
                      ("Enlace", f"*{current_object.get_search_address}*", False),
                      ("Fuente", f'*{current_object.get_content_source}*', False)]
            
            for name, value, inline in fields:
                embed.add_field(name = name, value = value, inline = inline)

            embed.set_footer(text = f"Solicitado por {self.ctx.author.display_name}" + "\n" + f"{offset:,} de {len_data:,} gifs.", icon_url = self.ctx.author.avatar_url)
            embed.set_image(url= str(current_object.get_url))
            Intermediario.set_url(embed)
            return embed

        elif isinstance(current_object, Tenor):

            print ("URL " + str(current_object))
            embed = Embed(title = f"*{current_object.get_source()}*", description = f"**Resultados para:** *{self.busqueda}*",
                          colour = self.ctx.author.colour, timestamp = datetime.utcnow())
            print(current_object.get_thumbnail())
            embed.set_thumbnail(url = current_object.get_thumbnail())
            embed.add_field(name = "Titulo", value = f"*{current_object.get_title}*", inline = True)
            embed.add_field(name = "ID", value = f'*{current_object.get_id}*', inline = True)
            embed.add_field(name = "Enlace", value = f"*{current_object.get_search_address}*", inline = False)
            embed.set_footer(text = f"Solicitado por {self.ctx.author.display_name}" + "\n" + f"{offset:,} de {len_data:,} gifs.", icon_url = self.ctx.author.avatar_url) 
            embed.set_image(url = current_object.get_url)
            Intermediario.set_url(embed)
            return embed

class Gif(Cog):

    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Gif")

    async def send_gif(self, ctx):
        def check(m):
                return m.channel == ctx.channel and m.content == "s" and m.author == ctx.author 
        mensaje = await self.bot.wait_for('message', check = check)
        await ctx.channel.purge(limit = 1)
        await ctx.author.send(content = f">>> **{ctx.author.display_name}, su gif:**", embed = Intermediario.url())


    async def search_gif(self, ctx, search): #Buscador en las dos fuentes
        session = aiohttp.ClientSession()
        search.replace(' ', '+')
        giphy_response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=NMGKDkhX4308QRqQBCQW0n4V22o7XdUG&limit=15')
        tenor_response = await session.get('https://api.tenor.com/v1/search?q=' + search + '&key=87NYM0CK0LBX&limit=15')
        giphy_results = json.loads(await giphy_response.text())
        tenor_results = json.loads(await tenor_response.text())
            
        giphy_direcciones = [[Giphy(gif_object)] for gif_object in giphy_results['data']]
        tenor_direcciones = [[Tenor(gif_object)] for gif_object in tenor_results['results']]
            
        menu = MenuPages(source = Paginas(ctx, sample(giphy_direcciones + tenor_direcciones, len(giphy_direcciones + tenor_direcciones)), search), delete_message_after = False)
        await menu.start(ctx)
        await self.send_gif(ctx)
        await session.close()

    async def random_gif(self, ctx, search): #Busquedas aleatorios en las dos fuentes
        session = aiohttp.ClientSession()
        search.replace(' ', '+')
        giphy_response = await session.get('http://api.giphy.com/v1/gifs/random?tag=' + search + '&api_key=NMGKDkhX4308QRqQBCQW0n4V22o7XdUG')
        tenor_response = await session.get('https://api.tenor.com/v1/random?q=' + search + '&key=87NYM0CK0LBX&limit=9')
        giphy_results = json.loads(await giphy_response.text())
        tenor_results = json.loads(await tenor_response.text())

        giphy_direcciones = [[Giphy(giphy_results['data'])]] 
        tenor_direcciones = [[Tenor(gif_object)] for gif_object in tenor_results['results']]
        
        menu = MenuPages(source = Paginas(ctx, sample(giphy_direcciones + tenor_direcciones, len(giphy_direcciones + tenor_direcciones)), RANDOM_SEARCH + search), delete_message_after = False)
        await menu.start(ctx)
        await self.send_gif(ctx)
        await session.close()

    async def trending_gif(self, ctx):
        session = aiohttp.ClientSession()
        giphy_response = await session.get('http://api.giphy.com/v1/gifs/trending?api_key=NMGKDkhX4308QRqQBCQW0n4V22o7XdUG&limit=15')
        tenor_response = await session.get('https://api.tenor.com/v1/trending?key=87NYM0CK0LBX&limit=15')
        giphy_results = json.loads(await giphy_response.text())
        tenor_results = json.loads(await tenor_response.text())

        giphy_direcciones = [[Giphy(gif_object)] for gif_object in giphy_results['data']]
        tenor_direcciones = [[Tenor(gif_object)] for gif_object in tenor_results['results']]
        
        menu = MenuPages(source = Paginas(ctx, sample(giphy_direcciones + tenor_direcciones, len(giphy_direcciones + tenor_direcciones)), TRENDING_LABEL), delete_message_after = False)
        await menu.start(ctx)
        await self.send_gif(ctx)
        await session.close()

    async def giphy_search_gif(self, ctx, search):
        session = aiohttp.ClientSession()
        search.replace(' ', '+')
        response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=NMGKDkhX4308QRqQBCQW0n4V22o7XdUG&limit=30')
        data = json.loads(await response.text())
        direcciones = [[Giphy(gif_object)] for gif_object in data['data']]
        menu = MenuPages(source = Paginas(ctx, sample(direcciones, len(direcciones)), search), delete_message_after = False)
        await menu.start(ctx)  
        await self.send_gif(ctx)
        await session.close()

    async def giphy_random_gif(self, ctx, search):
        session = aiohttp.ClientSession()
        search.replace(' ', '+')
        response = await session.get('http://api.giphy.com/v1/gifs/random?tag=' + search + '&api_key=NMGKDkhX4308QRqQBCQW0n4V22o7XdUG')
        data = json.loads(await response.text())
        direcciones = [[Giphy(data['data'])]]
        menu = MenuPages(source = Paginas(ctx, sample(direcciones, len(direcciones)), RANDOM_SEARCH + search), delete_message_after = False)
        await menu.start(ctx)  
        await self.send_gif(ctx)
        await session.close()

    async def giphy_trending_gif(self, ctx):
        session = aiohttp.ClientSession()
        response = await session.get('https://api.giphy.com/v1/gifs/trending?api_key=NMGKDkhX4308QRqQBCQW0n4V22o7XdUG&limit=30')
        data = json.loads(await response.text())
        direcciones = [[Giphy(gif_object)] for gif_object in data['data']]
        menu = MenuPages(source = Paginas(ctx, sample(direcciones, len(direcciones)), TRENDING_LABEL), delete_message_after = False)
        await menu.start(ctx)
        await self.send_gif(ctx)
        await session.close()

    async def giphy_search_sticker(self, ctx, search):
        session = aiohttp.ClientSession()
        search.replace(' ', '+')
        response = await session.get('http://api.giphy.com/v1/stickers/search?q=' + search + '&api_key=NMGKDkhX4308QRqQBCQW0n4V22o7XdUG&limit=30')
        data = json.loads(await response.text())
        direcciones = [[Giphy(gif_object)] for gif_object in data['data']]
        menu = MenuPages(source = Paginas(ctx, sample(direcciones, len(direcciones)), search), delete_message_after = False)
        await menu.start(ctx)  
        await self.send_gif(ctx)
        await session.close()

    async def giphy_random_sticker(self, ctx, search):
        session = aiohttp.ClientSession()
        search.replace(' ', '+')
        response = await session.get('http://api.giphy.com/v1/stickers/random?tag=' + search + '&api_key=NMGKDkhX4308QRqQBCQW0n4V22o7XdUG')
        data = json.loads(await response.text())
        direcciones = [[Giphy(data['data'])]]
        menu = MenuPages(source = Paginas(ctx, sample(direcciones, len(direcciones)), RANDOM_SEARCH + search), delete_message_after = False)
        await menu.start(ctx)  
        await self.send_gif(ctx)
        await session.close()

    async def giphy_trending_sticker(self, ctx):
        session = aiohttp.ClientSession()
        response = await session.get('http://api.giphy.com/v1/stickers/trending?api_key=NMGKDkhX4308QRqQBCQW0n4V22o7XdUG&limit=30')
        data = json.loads(await response.text())
        direcciones = [[Giphy(gif_object)] for gif_object in data['data']]
        menu = MenuPages(source = Paginas(ctx, sample(direcciones, len(direcciones)), TRENDING_LABEL), delete_message_after = False)
        await menu.start(ctx)  
        await self.send_gif(ctx)
        await session.close()

    async def tenor_search_gif(self, ctx, search):
        session = aiohttp.ClientSession()
        search.replace(' ', '+')
        response = await session.get('https://api.tenor.com/v1/search?q=' + search + '&key=87NYM0CK0LBX&limit=30')
        data = json.loads(await response.text())
        direcciones = [[Tenor(gif_object)] for gif_object in data['results']]
        menu = MenuPages(source = Paginas(ctx, sample(direcciones, len(direcciones)), search), delete_message_after = False)
        await menu.start(ctx)
        await self.send_gif(ctx)
        await session.close()

    async def tenor_random_gif(self, ctx, search):
        session = aiohttp.ClientSession()
        search.replace(' ', '+')
        response = await session.get('https://api.tenor.com/v1/random?q=' + search + '&key=87NYM0CK0LBX&limit=30')
        data = json.loads(await response.text())
        direcciones = [[Tenor(gif_object)] for gif_object in data['results']]
        menu = MenuPages(source = Paginas(ctx, sample(direcciones, len(direcciones)), RANDOM_SEARCH + search), delete_message_after = False)
        await menu.start(ctx)
        await self.send_gif(ctx)
        await session.close()

    async def tenor_trending_gif(self, ctx):
        session = aiohttp.ClientSession()
        response = await session.get('https://api.tenor.com/v1/trending?key=87NYM0CK0LBX&limit=30')
        data = json.loads(await response.text())
        direcciones = [[Tenor(gif_object)] for gif_object in data['results']]
        menu = MenuPages(source = Paginas(ctx, sample(direcciones, len(direcciones)), TRENDING_LABEL), delete_message_after = False)
        await menu.start(ctx)
        await self.send_gif(ctx)
        await session.close()

    @group(name = "gif", aliases = ["gf"], brief = "Resultados de gifs de Giphy y Tenor, presentados en desorden", invoke_without_command = True)
    async def gif_group(self, ctx, *, search = None):
        if search is not None:
            await self.search_gif(ctx, search)

    @gif_group.command(name = "random", aliases = ["rdm", "rand"], brief = "Resultados aleatorios a partir de una busqueda")
    async def gif_random_subcommand(self, ctx, *, search = None):
        if search is not None:
            await self.random_gif(ctx, search)

    @gif_group.command(name = "trendings", aliases = ["tt", "trend"], brief = "Resultados de las tendencias actuales")
    async def gif_trending_subcommand(self, ctx):
        await self.trending_gif(ctx)


    @group(name = "giphy", aliases = ["gy"], brief = "Buscador de gifs y stickers en Giphy", invoke_without_command = True)
    async def giphy_group(self, ctx):
        pass

    @giphy_group.group(name = "gif", aliases = ["gf", "g"], brief = "Resultados unicamente de gifs", invoke_without_command = True)
    async def giphy_gif_search_subgroup(self, ctx, *, search = None):
        if search is not None:
            await self.giphy_search_gif(ctx, search)

    @giphy_gif_search_subgroup.command(name = "random", aliases = ["rand", "rdm"], brief = "Resultado aleatorio a partir de una busqueda")
    async def giphy_gif_random_subcommand(self, ctx, *, search = None):
        if search is not None:
            await self.giphy_random_gif(ctx, search)

    @giphy_gif_search_subgroup.command(name = "trendings", aliases = ["trend", "tt"], brief = "Tendencias en Giphy")
    async def giphy_gif_trending_subcommand(self, ctx):
        await self.giphy_trending_gif(ctx)

    @giphy_group.group(name = "sticker", aliases = ["stk", "stkr"], brief = "Resultados unicamente de stickers", invoke_without_command = True)
    async def giphy_sticker_search_subgroup(self, ctx, *, search = None):
        if search is not None:
            await self.giphy_search_sticker(ctx, search)

    @giphy_sticker_search_subgroup.command(name = "random", aliases = ["rand", "rdm"], brief = "Resultado aleatorio a partir de una busqueda")
    async def giphy_sticker_random_subcommand(self, ctx, *, search = None):
        if search is not None:
            await self.giphy_random_sticker(ctx, search)

    @giphy_sticker_search_subgroup.command(name = "trendings", aliases = ["trend", "tt"], brief = "Tendencias en Giphy")
    async def giphy_sticker_trending_subcommand(self, ctx):
        await self.giphy_trending_sticker(ctx)

    @group(name = "tenor", aliases = ["tnr"], brief = "Buscador de gifs en Tenor", invoke_without_command = True)
    async def tenor_gif_search_group(self, ctx, *, search = None):
        if search is not None:
            await self.tenor_search_gif(ctx, search)

    @tenor_gif_search_group.command(name = "random", aliases = ["rand", "rdm"], brief = "Resultados aleatorios a partir de una busqueda")
    async def tenor_gif_random_subcommand(self, ctx, *, search = None):
        if search is not None:
            await self.tenor_search_gif(ctx, search)

    @tenor_gif_search_group.command(name = "trendings", aliases = ["trend", "tt"], brief = "Tendencias en Teno")
    async def tenor_gif_trending_subcommand(self, ctx):
        await self.tenor_trending_gif(ctx)

    
def setup(bot):
    bot.add_cog(Gif(bot))

