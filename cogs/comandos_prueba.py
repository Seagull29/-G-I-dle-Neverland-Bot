import discord
import random
from discord.ext.commands import command, Cog, MissingRequiredArgument, CommandNotFound
from random import choice
import urllib.request
import re
from urllib import parse, request
from datetime import datetime
from typing import Optional
from discord import Embed, Member
import aiohttp
import json

#import giphy_client
#from giphy_client.rest import ApiException
#from pprint import pprint

#api = giphy_client.DefaultApi()
#api_key = 'NMGKDkhX4308QRqQBCQW0n4V22o7XdUG'



class Comandos_Prueba(Cog):

    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_ready(self):
        print("Bot esta online")

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            comando = (str(error)).split()
            await ctx.send(f"No conozco el comando {comando[1]}")

    @command()
    async def status(self, ctx, *, actividad):
        
        await self.client.change_presence(status = discord.Status.idle, activity = discord.Game(str(actividad)))
        await ctx.send(f"Actividad cambiada a: {actividad}")

    @command()
    async def ping(self, ctx):
        await ctx.send("pong")

    @command()
    async def ellen(self, ctx):
        await ctx.send(f"Sevastopol con {round(self.client.latency * 1000)}ms de latencia")

    @command()
    async def _8ball(self, ctx, *, question):
        respuestas = ["Si", "No"]
        if ("¿" in question or "?" in question):
            await ctx.send(f"Pregunta: {question}\nRespuesta: {random.choice(respuestas)}")
        else: 
            await ctx.send(f"Pregunta: ¿{question}?\nRespuesta: {random.choice(respuestas)}")

    @command()
    async def clear(self, ctx, amount : int):
        await ctx.channel.purge(limit = amount + 1)
        await ctx.send(f"Atencion: {amount} mensajes eliminados")


    #@command()
    #async def kick(self, ctx, member : discord.Member, *, reason = None):
    #    await member.kick(reason = reason)
    #    await ctx.send(f"Miembro {member.mention} eliminado")

    #@command()
    #async def ban(self, ctx, member : discord.Member, *, reason = None):
    #    await member.ban(reason = reason)
    #    await ctx.send(f"Miembro {member.mention} baneado")

    #@command()
    #async def unban(self, ctx, *, member):
    #    baneados = await ctx.guild.bans()
    #    nombre_miembro, numero_miembro = member.spli("#")
        
    #    for miembro_baneado in baneados:
    #        usuario = miembro_baneado.user
            
    #        if ((usuario.name, usuario.discriminator) == (nombre_miembro, numero_miembro)):
    #            await ctx.guild.unban(usuario)
    #            await ctx.send(f"Miembro {usuario.mention} desbaneado")
    #            return 

    @command()
    async def math(self, ctx, *, numeros):
        operacion = ["sum", "res", "mul", "div"]
        numero = str(numeros).split()
        if numero[0] in operacion:
            if numero[0] == "sum":
                resultado = 0
                for i in range(1, len(numero)):
                    if "." in numero[i]:
                        resultado += float(numero[i])
                    else:
                        resultado += int(numero[i])
            elif numero[0] == "mul":
                resultado = 1
                for i in range(1, len(numero)):
                    if "." in numero[i]:
                        resultado *= float(numero[i])
                    else:
                        resultado *= int(numero[i])
            elif numero[0] == "res":
                resultado = float(numero[1]) if "." in numero[1] else int(numero[1])
                for i in range(2, len(numero)):
                    if "." in numero[i]:
                        resultado -= float(numero[i])
                    else:
                        resultado -= int(numero[i])
                resultado = round(resultado, 5)
            elif numero[0] == "div":
                if len(numero) > 3 and "0" in numero:
                    resultado = 0
                elif len(numero) == 3 and numero[2] == "0":
                    resultado = "No puedo dividir entre cero"
                else:
                    resultado = float(numero[1])
                    for i in range(2, len(numero)):
                        resultado /= float(numero[i])
            await ctx.send(f"Resultado: {resultado}")
        else:
            await ctx.send(f"Operaciones permitidas: {operacion}")

    
    @command()
    async def ok(self, ctx, member : discord.Member):
        palabras = ["Ya", "Ok", "Aea"]
        await ctx.send(f"{member.mention} {random.choice(palabras)}")

    @command()
    async def yt(self, ctx, *, video):

        if len(video) == 0:
            await ctx.send("Indique que desea buscar")
        else:

            search_keyword = video.replace(" ", "+")
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            print("https://www.youtube.com/watch?v=" + video_ids[0])
            await ctx.send("https://www.youtube.com/watch?v=" + video_ids[0])
    
    #@command(name = "gif", pass_context = True)
    #async def giphy(self, ctx, *, search):
      #  embed = discord.Embed(title = "Gif!", description = f"Resultado para: {search}", colour = ctx.author.colour, timestamp = datetime.utcnow())
       # embed.set_author(name = ctx.author.display_name)
        #embed.set_footer(text = f"Solicitado por {ctx.author.display_name}", icon_url = ctx.author.avatar_url)
        #session = aiohttp.ClientSession()
    
        #if search == '':
         #   response = await session.get('https://api.giphy.com/v1/gifs/random?api_key=NMGKDkhX4308QRqQBCQW0n4V22o7XdUG')
          #  data = json.loads(await response.text())
           # embed.set_image(url=data['data']['images']['original']['url'])
        #else:
         #   search.replace(' ', '+')
          #  response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=NMGKDkhX4308QRqQBCQW0n4V22o7XdUG&limit=10')
           # data = json.loads(await response.text())
            #gif_choice = random.randint(0, 9)
            #embed.set_image(url=data['data'][gif_choice]['images']['original']['url'])

        #await session.close()

        #await ctx.send(embed = embed)     
        #await mensaje.add_reaction("▶️")

        

        #def check(reaction, user):
        #    return reaction == str(reaction.emoji) in ["◀️", "▶️"]
    
        #reaction, user = await self.client.wait_for("reaction_add", check = check)
        #if str(reaction.emoji) == "▶️":
        #    embed.set_image(url = data['data'][random.randint(0, 9)]['images']['original']['url'])
        #    await mensaje.edit(embed = embed)
        #    await mensaje.remove_reaction(reaction, user)
        #else:
        #    mensaje.remove_reaction(reaction, user)

    @command(name = "invite")
    async def invite_command(self, ctx, member : Member, razon : Optional[str] = "cualquier juego"):
        await ctx.send(f"{ctx.author.mention} esta avisando para jugar a {member.mention} {razon}")

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("Indique la cantidad de mensajes a eliminar")



def setup(client):
    client.add_cog(Comandos_Prueba(client))
