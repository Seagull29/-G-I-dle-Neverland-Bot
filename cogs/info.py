import discord, aiohttp, json
from discord.ext.commands import command, Cog, group
from datetime import datetime
from typing import Optional
from discord import Embed, Member
from discord.ext.tasks import loop
from itertools import cycle
from discord import Spotify, Forbidden
ESTADOS = cycle(["Pronto disponible", "En construccion", "ACM"])
games = {"lol" : "League of Legends", "fn" : "Fornite", "rl" : "Rocket League", 
                 "dbd" : "Dead by Daylight", "l4d2" : "Left 4 Dead 2"}
class Info(Cog):

    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = "(G)I-dle"))
        if not self.client.ready:
            self.client.cogs_ready.ready_up("Tareas")

    @command(name = "rage")
    async def standard_gif(self, ctx, *, mensaje : str):
        emociones = ["sapo", "rage"]
        if mensaje in emociones:
            if mensaje == "sapo":
                await ctx.send("https://media.discordapp.net/attachments/693399453524295730/747400908077531226/image0.gif")
            elif (mensaje == "rage"):
                await ctx.send("https://media.discordapp.net/attachments/689854960703111171/746520116686094426/ezgif.com-optimize.gif")
        else:
            await ctx.send("No conozco aun el gif adecuado")


    @loop(seconds = 60)
    async def change_status(self):
        await self.client.change_presence(activity = discord.Game(next(ESTADOS)))


    @command(name = "userinfo", aliases = ["info", "ui"])
    async def user_info(self, ctx, target: Optional[Member]):
        target = target or ctx.author
        embed = Embed(title = "Informacion de usuario", colour = target.colour, 
                      timestamp = datetime.utcnow())
        embed.set_thumbnail(url = target.avatar_url)
        fields = [("Nombre", str(target), True),
                  ("ID", target.id, True),  
                  ("Bot", target.bot, True),
                  ("Rol", target.top_role.mention, True),
                  ("Estado", str(target.status).title(), True),
                  ("Actividad", f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} {target.activity.name if target.activity else ''}", True),
                  ("Creado", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                  ("Se unio", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                  ("Nitro", bool(target.premium_since), True)]

        for name, value, inline in fields:
            embed.add_field(name = name, value = value, inline = inline)
        await ctx.send(embed = embed) 

    @command(name = "serverinfo", aliases = ["si"])
    async def server_info(self, ctx):
        #ctx.guild.guild.owner,colour
        embed = Embed(title = "Informacion del Servidor", colour = ctx.author.colour, timestamp = datetime.utcnow())
        embed.set_thumbnail(url = ctx.guild.me.avatar_url)
        estados = [len(list(filter(lambda estado: str(estado.status) == "online", ctx.guild.members))),
                   len(list(filter(lambda estado: str(estado.status) == "idle", ctx.guild.members))),
                   len(list(filter(lambda estado: str(estado.status) == "dnd", ctx.guild.members))),
                   len(list(filter(lambda estado: str(estado.status) == "offline", ctx.guild.members)))]
        fields = [("ID", ctx.guild.id, True),
                  ("Region", ctx.guild.region, True),
                  ("Creacion", ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                  ("Miembros", len(ctx.guild.members), True),
                  ("Humanos", len(list(filter(lambda miembros: not miembros.bot, ctx.guild.members))), True),
                  ("Bots", len(list(filter(lambda bots: bots.bot, ctx.guild.members))), True),
                  ("Miembros Baneados", len(await ctx.guild.bans()), True),
                  ("Estados", f"🟢 {estados[0]} 🟠 {estados[1]} 🔴 {estados[2]} ⚪ {estados[3]}", True),
                  ("Canales de texto", len(ctx.guild.text_channels), True),
                  ("Canales de voz", len(ctx.guild.voice_channels), True),
                  ("Categorias", len(ctx.guild.categories), True), 
                  ("Roles", len(ctx.guild.roles), True), 
                  ("Invitaciones", len(await ctx.guild.invites()), True),
                  ("\u200b", "\u200b", True)]

        for name, value, inline in fields:
            embed.add_field(name = name, value = value, inline = inline)
        await ctx.send(embed = embed)  


    def only_members(self, member):
        if not member.bot:
            return member

    @group(name = "spotify", aliases = ["spy"], invoke_without_command = True)
    async def spotify_command(self, ctx, search : str = None):
        if search is None:
            miembros = list(filter(self.only_members, ctx.guild.members))
            for miembro in miembros:
                for actividad in miembro.activities:
                    if isinstance(actividad, Spotify):
                        artistas = ", ".join(actividad.artists)
                        track = []
                        timedelta = str(actividad.duration).split(".")[0]
                        start = actividad.start.strftime("%H:%M:%S")
                        end = actividad.end.strftime("%H:%M:%S")
                        created = actividad.created_at.strftime("%H:%M:%S")
                        track.append(("Artista(s)", f"*{artistas}*", True))
                        track.append(("Cancion", f"*{actividad.title}*", True))
                        track.append(("Album", f"*{actividad.album}*", True))
                        track.append(("Duracion", f"*{timedelta}*", True))
                        track.append(("Hora Inicio(UTC)", f"*{start}*", True))
                        track.append(("Finalizacion(UTC)", f"*{end}*", True))
                        embed = Embed(colour = actividad.colour, timestamp = datetime.utcnow())
                        embed.set_author(name = miembro.display_name, icon_url = miembro.avatar_url)
                        embed.set_footer(text = f"Hora Reanudacion(UTC): {created}", icon_url = "https://developer.spotify.com/assets/branding-guidelines/icon4@2x.png")
                        embed.set_thumbnail(url = actividad.album_cover_url)
                        for name, value, inline in track:
                            embed.add_field(name = name, value = value, inline = inline)
                        await ctx.send(embed = embed)


    @spotify_command.command(name = "lol") 
    async def lol_subcommand(self, ctx):
        miembros = list(filter(self.only_members, ctx.guild.members))
        for miembro in miembros:
            for actividad in miembro.activities:
                if isinstance(actividad, discord.activity.Activity) and actividad.name == games['lol']:
                    player = [("Juego", f"*{games['lol']}*", True),
                              ("Estado", f"*{actividad.state}*", True), 
                              ("Detalles", f"*{actividad.details}*", True)]
                    embed = Embed(colour = miembro.colour, timestamp = datetime.utcnow())
                    embed.set_thumbnail(url = actividad.large_image_url)
                    embed.set_author(name = miembro.display_name, icon_url = miembro.avatar_url)
                    for name, value, inline in player:
                        embed.add_field(name = name, value = value, inline = inline)
                    await ctx.send(embed = embed)
        
        
        """
        elif search in games:
            
                        #players.append((f"{nro_miembro}. Usuario", f"*{miembro.display_name}*", True))
                        #players.append(("Juego", f"*{games[search]}*", True))
                        #players.append(("Estado", f"*{actividad.state}*", True))
                        #players.append(("Detalles", f"*{actividad.details}*", False))

                        

            #embed = Embed(title = f"**{games[search]}**", colour = ctx.author.colour, timestamp = datetime.utcnow())
            #embed.set_footer(text = f"Solicitado por {ctx.author.display_name}", icon_url = ctx.author.avatar_url)
            #embed.set_thumbnail(url = "https://developer.spotify.com/assets/branding-guidelines/icon4@2x.png")
            #for name, value, inline in players:
                #embed.add_field(name = name, value = value, inline = inline)
            #await ctx.send(embed = embed)
        else:
            embed = Embed(title = "**Abreviacion de juegos**", colour = ctx.author.colour, timestamp = datetime.utcnow())
            embed.set_footer(text = f"Solicitado por {ctx.author.display_name}", icon_url = ctx.author.avatar_url)
            data = []
            nro = 0
            for key, value in games.items():
                nro += 1
                data.append(("N°", f"**{nro}**", True))
                data.append(("Abreviacion", f"***{key}***", True))
                data.append(("Juego", f"*{value}*", True))
            for name, value, inline in data:
                embed.add_field(name = name, value = value, inline = inline)
            
            await ctx.send(embed = embed)
        """

    @command(name = "vlive")
    async def vlide(self, ctx, limit : int):
        session = aiohttp.ClientSession()
        BASE_URL = 'http://api.vfan.vlive.tv/vproxy/channelplus'
        payload = {
            'app_id': "8c6cc7b45d2568fb668be6e05b6e5a3b",
            'channelSeq': "785",
            'maxNumOfRows': 10,
            'pageNo': 1,
        }
        response = await session.get(f"{BASE_URL}/getChannelVideoList", params = payload)
        data = json.loads(await response.text())
        await session.close()
        url_home = "https://channels.vlive.tv/CE2621/home"
        for i in range(limit):
            video = data['result']['videoList'][i]

            embed = Embed(
                title = video['title'],
                description = f"{video['representChannelName']} : vlive!",
                url = f"https://www.vlive.tv/video/{video['videoSeq']}",
                timestamp = datetime.now()
            )

            embed.set_author(
                name = video['representChannelName'],
                url = f"{url_home}",
                icon_url = data['result']['channelInfo']['channelProfileImage']
            )

            embed.set_image(url = f"{video['thumbnail']}?type=f886_499")

            embed.set_footer(
                text = "Test",
                icon_url = "https://i.imgur.com/gHo7BTO.png"
            )

            await ctx.send(embed = embed)

    @command(name = "send", aliases = ["sendmessage"])
    async def send_command(self, ctx, member : discord.Member = None, *, message):
        if not member is None and not member.bot:
            try:
                await member.send(f">>> **{member.display_name}**, *{message}*")
                await ctx.channel.purge(limit = 1)
            except Forbidden:
                pass
        else:
            await ctx.send(f"{member.mention}, no puedo enviar el mensaje.")
            await ctx.channel.purge(limit = 1)

def setup(client):
    client.add_cog(Info(client))