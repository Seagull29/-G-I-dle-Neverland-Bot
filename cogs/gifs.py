from discord.ext.commands import command, group, Cog
from datetime import datetime
import json, aiohttp
from random import sample
from discord import Embed
from discord.ext.menus import MenuPages, ListPageSource
from apis.gifsapi import GiphyAPI, TenorAPI, Giphy, Tenor, GiphyType

TRENDING_LABEL = "**Trendings**"
RANDOM_SEARCH = "Aleatorios de "
GIPHY_KEY = "NMGKDkhX4308QRqQBCQW0n4V22o7XdUG"
TENOR_KEY = "87NYM0CK0LBX"

giphy = GiphyAPI(GIPHY_KEY)
tenor = TenorAPI(TENOR_KEY)

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
            #print ("Flag " + str(current_object))
            
            embed = Embed(
                title = f"*{current_object.get_source()}*", 
                description = f"**Resultados para:** *{self.busqueda}*", 
                colour = self.ctx.author.colour, 
                timestamp = datetime.utcnow()
            )
            
            embed.set_author(
                name = current_object.get_author, 
                url = current_object.get_author_url, 
                icon_url = current_object.get_author_avatar
            )
            
            embed.set_thumbnail(
                url = current_object.get_thumbnail()
            )

            fields = [
                ("Titulo", f'*{current_object.get_title}*', True), 
                ("ID", f"*{current_object.get_id}*", True), 
                ("Enlace", f"*{current_object.get_search_address}*", False),
                ("Fuente", f'*{current_object.get_content_source}*', False)
            ]
            
            for name, value, inline in fields:
                embed.add_field(
                    name = name, 
                    value = value, 
                    inline = inline
                )

            embed.set_footer(
                text = f"Solicitado por {self.ctx.author.display_name}" + "\n" + f"{offset:,} de {len_data:,} gifs.", 
                icon_url = self.ctx.author.avatar_url
            )
            
            embed.set_image(
                url= str(current_object.get_url)
            )

            Intermediario.set_url(embed)
            return embed

        elif isinstance(current_object, Tenor):
            #print ("URL " + str(current_object))

            embed = Embed(
                title = f"*{current_object.get_source()}*", 
                description = f"**Resultados para:** *{self.busqueda}*",
                colour = self.ctx.author.colour, 
                timestamp = datetime.utcnow()
            )

            embed.set_thumbnail(
                url = current_object.get_thumbnail()
            )

            embed.add_field(
                name = "Titulo", 
                value = f"*{current_object.get_title}*", 
                inline = True
            )

            embed.add_field(
                name = "ID", 
                value = f'*{current_object.get_id}*', 
                inline = True
            )

            embed.add_field(
                name = "Enlace", 
                value = f"*{current_object.get_search_address}*", 
                inline = False
            )

            embed.set_footer(
                text = f"Solicitado por {self.ctx.author.display_name}" + "\n" + f"{offset:,} de {len_data:,} gifs.", 
                icon_url = self.ctx.author.avatar_url
            ) 

            embed.set_image(
                url = current_object.get_url
            )

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
        giphy_data = await giphy.get_search(GiphyType.GIF, search, 15)
        tenor_data = await tenor.get_search(search, 15)
        giphy_objects = [[Giphy(gif_object)] for gif_object in giphy_data['data']]
        tenor_objects = [[Tenor(gif_object)] for gif_object in tenor_data['results']]
        menu = MenuPages(source = Paginas(ctx, sample(giphy_objects + tenor_objects, len(giphy_objects + tenor_objects)), search), delete_message_after = False)
        await menu.start(ctx)
        await self.send_gif(ctx)

    async def random_gif(self, ctx, search): #Busquedas aleatorios en las dos fuentes
        giphy_data = await giphy.get_random_search(GiphyType.GIF, search)
        tenor_data = await tenor.get_random_search(search, 9) 
        giphy_objects = [[Giphy(giphy_data['data'])]] 
        tenor_objects = [[Tenor(gif_object)] for gif_object in tenor_data['results']]
        menu = MenuPages(source = Paginas(ctx, sample(giphy_objects + tenor_objects, len(giphy_objects + tenor_objects)), RANDOM_SEARCH + search), delete_message_after = False)
        await menu.start(ctx)
        await self.send_gif(ctx)
     
    async def trending_gif(self, ctx):
        giphy_data = await giphy.get_trendings(GiphyType.GIF, 15)
        tenor_data = await tenor.get_trendings(15) 
        giphy_objects = [[Giphy(gif_object)] for gif_object in giphy_data['data']]
        tenor_objects = [[Tenor(gif_object)] for gif_object in tenor_data['results']]
        menu = MenuPages(source = Paginas(ctx, sample(giphy_objects + tenor_objects, len(giphy_objects + tenor_objects)), TRENDING_LABEL), delete_message_after = False)
        await menu.start(ctx)
        await self.send_gif(ctx)

    async def giphy_search_gif(self, ctx, search):
        giphy_data = await giphy.get_search(GiphyType.GIF, search, 30)
        direcciones = [[Giphy(gif_object)] for gif_object in giphy_data['data']]
        menu = MenuPages(source = Paginas(ctx, sample(direcciones, len(direcciones)), search), delete_message_after = False)
        await menu.start(ctx)  
        await self.send_gif(ctx)

    async def giphy_random_gif(self, ctx, search):
        giphy_data = await giphy.get_random_search(GiphyType.GIF, search)
        direcciones = [[Giphy(giphy_data['data'])]]
        menu = MenuPages(source = Paginas(ctx, sample(direcciones, len(direcciones)), RANDOM_SEARCH + search), delete_message_after = False)
        await menu.start(ctx)  
        await self.send_gif(ctx)

    async def giphy_trending_gif(self, ctx):
        giphy_data = await giphy.get_trendings(GiphyType.GIF, 30)
        direcciones = [[Giphy(gif_object)] for gif_object in giphy_data['data']]
        menu = MenuPages(source = Paginas(ctx, sample(direcciones, len(direcciones)), TRENDING_LABEL), delete_message_after = False)
        await menu.start(ctx)
        await self.send_gif(ctx)
     

    async def giphy_search_sticker(self, ctx, search):
        giphy_data = await giphy.get_search(GiphyType.STICKER, search, 30)
        direcciones = [[Giphy(gif_object)] for gif_object in giphy_data['data']]
        menu = MenuPages(source = Paginas(ctx, sample(direcciones, len(direcciones)), search), delete_message_after = False)
        await menu.start(ctx)  
        await self.send_gif(ctx)

    async def giphy_random_sticker(self, ctx, search):
        giphy_data = await giphy.get_random_search(GiphyType.STICKER, search)
        direcciones = [[Giphy(giphy_data['data'])]]
        menu = MenuPages(source = Paginas(ctx, sample(direcciones, len(direcciones)), RANDOM_SEARCH + search), delete_message_after = False)
        await menu.start(ctx)  
        await self.send_gif(ctx)

    async def giphy_trending_sticker(self, ctx):
        giphy_data = await giphy.get_trendings(GiphyType.STICKER, 30)
        direcciones = [[Giphy(gif_object)] for gif_object in giphy_data['data']]
        menu = MenuPages(source = Paginas(ctx, sample(direcciones, len(direcciones)), TRENDING_LABEL), delete_message_after = False)
        await menu.start(ctx)  
        await self.send_gif(ctx)

    async def tenor_search_gif(self, ctx, search):
        tenor_data = await tenor.get_search(search, 30)
        direcciones = [[Tenor(gif_object)] for gif_object in tenor_data['results']]
        menu = MenuPages(source = Paginas(ctx, sample(direcciones, len(direcciones)), search), delete_message_after = False)
        await menu.start(ctx)
        await self.send_gif(ctx)

    async def tenor_random_gif(self, ctx, search):
        tenor_data = await tenor.get_random_search(search, 15)
        direcciones = [[Tenor(gif_object)] for gif_object in tenor_data['results']]
        menu = MenuPages(source = Paginas(ctx, sample(direcciones, len(direcciones)), RANDOM_SEARCH + search), delete_message_after = False)
        await menu.start(ctx)
        await self.send_gif(ctx)

    async def tenor_trending_gif(self, ctx):
        tenor_data = await tenor.get_trendings(30)
        direcciones = [[Tenor(gif_object)] for gif_object in tenor_data['results']]
        menu = MenuPages(source = Paginas(ctx, sample(direcciones, len(direcciones)), TRENDING_LABEL), delete_message_after = False)
        await menu.start(ctx)
        await self.send_gif(ctx)

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

