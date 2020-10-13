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
#PREFIX = "!"
CREADOR = [418960285500440576]
VERSION = "0.1"
TOKEN = "NzY1MzU5MTEwOTAzMzAwMDk3.X4TqNw.DLwW0GmiF_1Bp3aP6IWA4QGegsU"
#COGS = [path.split("\\")[-1][:-3] for path in glob("../lib/cogs/*.py")]
COGS = []
for filename in os.listdir("./cogs"):
    if (filename.endswith(".py")):
        COGS.append(f"{filename[:-3]}")
COGS.append("miscelaneo")

def get_prefix(bot, mensaje):
    prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", mensaje.guild.id)
    return when_mentioned_or(prefix)(bot, mensaje) 


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

        super().__init__(command_prefix = get_prefix, owner_ids = CREADOR)
    
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
        await self.stdout.send("Recuerden mantener activo el server ❤️😓.")

    async def on_error(self, error, *args, **kwargs):
        if error == "on_command_error":
            print (args[0].send("Algo ocurrio mal"))
            pass
        else:
            print ("Ocurrio un error")

    async def on_message(self, mensaje):
        if not mensaje.author.bot:

            await self.process_commands(mensaje)

    async def on_command_error(self, ctx, error):
        raise getattr(error, "original", error)

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(764606089068281856)
            self.stdout = self.get_channel(764606089509208114)
            self.scheduler.add_job(self.rules_reminder, CronTrigger(day_of_week = 0, hour = 8, minute = 0, second = 0))
            self.scheduler.start()
            print("Bot listo")
            
            await self.stdout.send("❤️")

            while not self.cogs_ready.all_ready():
                await sleep(0.5)
            
          
            self.ready = True
            print("Bot listo")



        else: 
            print("Bot reconectando")

bot = Bot()
bot.run(VERSION)
#bot.run(os.environ['token'])