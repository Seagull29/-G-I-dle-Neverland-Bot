from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext.commands import Bot as CBot
from discord.ext.commands import CommandNotFound
from discord import Embed, File
from datetime import datetime
from glob import glob
from asyncio import sleep
from apscheduler import schedulers
from discord.ext.commands import command
import db
import os
from discord.ext.commands import when_mentioned_or
from discord import Intents
from itertools import cycle
import discord
#PREFIX = "!"
CREADOR = [418960285500440576]
VERSION = "0.1"
TOKEN = "NzY1MzU5MTEwOTAzMzAwMDk3.X4TqNw.DLwW0GmiF_1Bp3aP6IWA4QGegsU"
#COGS = [path.split("\\")[-1][:-3] for path in glob("../lib/cogs/*.py")]
ESTADOS = cycle(["(G)I-dle", "T-ara", "Dreamcatcher", "LATATA", "Maze", "HANN", "Senorita", "Uh-Oh", "LION", "Oh my god", "i'm THE TREND", "DUMDi DUMDi"])
COGS = []
for filename in os.listdir("./cogs"):
    if (filename.endswith(".py")):
        COGS.append(f"{filename[:-3]}")
COGS.append("miscelaneo")

def get_prefix(bot, mensaje):
    prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", mensaje.guild.id)
    return when_mentioned_or(prefix)(bot, mensaje) 

intents = Intents.default()
intents.members = True
intents.presences = True



class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"{cog} cog listo")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])

class Bot(CBot):
    def __init__(self):
        #self.PREFIX = PREFIX
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)

        super().__init__(command_prefix = get_prefix, owner_ids = CREADOR, intents = intents)
    
    def setup(self):
        for cog in COGS:
            if cog == "miscelaneo": 
                self.load_extension(f"{cog}")
            else:
                self.load_extension(f"cogs.{cog}")
            
            print(f"{cog} cog cargado")
        print("Archivos cargados")

    def run(self, version):
        self.VERSION = version
        self.TOKEN = TOKEN
        print("Cargando archivos..")
        self.setup()
        print("Corriendo...")
        super().run(self.TOKEN, reconnect = True)
    
    async def shutdown(self):
        print("Cerrando la conexion")
        await super().close()


    async def close(self):
        print("Cerrando popr interrupcion de teclado")
        await self.shutdown()


    async def on_connect(self):
        print("Bot conectado")

    async def on_disconnected(self):
        print("Bot desconectado")

    async def rules_reminder(self):
        #recordatorio = await self.stdout.send(f">>> Recuerden mantener activo el server ❤️😓." + "\n" + f"Pasen por {self.get_channel(764918831516090368).mention} para obtener el rol de sus bias.")
        recordatorio = await self.stdout.send(f">>> **Nuevos roles agregados**" + "\n" + f"Pasen por {self.get_channel(764918831516090368).mention}, para que agreguen su reaccion y de esa forma tener acceso a los canales de dichos juegos." + "\n" + f"<{self.main_role.mention}>")
        await recordatorio.add_reaction("🎼")


    async def cambiar_estado(self):
        await self.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = next(ESTADOS)))

    async def on_error(self, error, *args, **kwargs):
        if error == "on_command_error":
            print ("Algo ocurrio mal")
            pass
        else:
            print ("Ocurrio un error")

    async def on_message(self, mensaje):
        if not mensaje.author.bot:
            if ".jpg" in mensaje.content or ".png" in mensaje.content:
                await mensaje.add_reaction("❤️")
                await mensaje.add_reaction("🤩")
            if not len(mensaje.attachments) == 0:
                if isinstance(mensaje.attachments[0].height, int):
                    await mensaje.add_reaction("❤️")
                    await mensaje.add_reaction("🤩")
            
            await self.process_commands(mensaje)

    async def on_command_error(self, ctx, error):
        raise getattr(error, "original", error)

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(764606089068281856)
            self.stdout = self.get_channel(764606089509208114)
            self.main_role = self.guild.get_role(764949862567116811)
            self.scheduler.add_job(self.rules_reminder, CronTrigger(day_of_week = '0, 5', hour = 13, minute = 30, second = 0))
            self.scheduler.add_job(self.cambiar_estado, CronTrigger(minute = '0, 40', second = 0))
            self.scheduler.start()
            print("Bot listo")
            
            #await self.stdout.send("❤️")

            while not self.cogs_ready.all_ready():
                await sleep(0.5)
            
          
            self.ready = True
            print("Bot listo")



        else: 
            print("Bot reconectando")

bot = Bot()
bot.run(VERSION)
#bot.run(os.environ['token'])