import discord
from discord import Embed
from discord.ext.commands import Cog, command
from datetime import datetime
class AuditLog(Cog):

    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("AuditLog")
            self.audit_log_channel = self.bot.get_channel(765391325746167849)
    
    @Cog.listener()
    async def on_user_update(self, before, after):
        if before.name != after.name:
            embed = Embed(title = "Nombre de usuario cambiado", colour = after.colour, timestamp = datetime.utcnow())
            fields = [("Antes", before.name, False), ("Despues", after.name, False)]
            for name, value, inline in fields:
                embed.add_field(name = name, value = value, inline = inline)
            await self.audit_log_channel.send(embed = embed)
        
        if before.discriminator != after.discriminator:
            embed = Embed(title = "Discriminador de usuario cambiado", colour = after.colour, timestamp = datetime.utcnow())
            fields = [("Antes", before.discriminator, False), ("Despues", after.discriminator, False)]
            for name, value, inline in fields:
                embed.add_field(name = name, value = value, inline = inline)
            await self.audit_log_channel.send(embed = embed)

        if before.avatar_url != after.avatar_url:
            embed = Embed(title = "Foto de usuario cambiada", description = f"Nueva imagen de {after.display_name} abajo", colour = self.audit_log_channel.guild.get_member(after.id).colour, timestamp = datetime.utcnow())
            embed.set_thumbnail(url = before.avatar_url)
            embed.set_image(url = after.avatar_url)
            await self.audit_log_channel.send(embed = embed)
    
    @Cog.listener()
    async def on_member_update(self, before, after):
        if before.display_name != after.display_name:
            embed = Embed(title = "Ocurrio un cambio de apodo", colour = after.colour, timestamp = datetime.utcnow())
            fields = [("Antes", before.display_name, False), ("Despues", after.display_name, False)]
            for name, value, inline in fields:
                embed.add_field(name = name, value = value, inline = inline)
            await self.audit_log_channel.send(embed = embed)

        elif before.roles != after.roles:
            embed = Embed(title = "Roles cambiados", description = f"Cambio de roles en {after.display_name}", colour = after.colour, timestamp = datetime.utcnow())
            fields = [("Antes", ", ".join([r.mention for r in before.roles]), False), ("Despues", ", ".join([r.mention for r in after.roles]), False)]
            for name, value, inline in fields:
                embed.add_field(name = name, value = value, inline = inline)
            await self.audit_log_channel.send(embed = embed)


    @Cog.listener()
    async def on_message_edit(self, before, after):
        if not after.author.bot:
            if before.content != after.content:
                #channel = int(str(after.channel.mention).strip("<#>"))
                try:
                    embed = Embed(title = "Mensaje editado", description = f"Editado por {after.author.display_name} en {after.channel.mention}.", colour = after.author.colour, timestamp = datetime.utcnow())
                except Exception:
                    pass
                
                fields = [("Antes", before.content, False), ("Despues", after.content, False)]
                for name, value, inline in fields:
                    embed.add_field(name = name, value = value, inline = inline)
                await self.audit_log_channel.send(embed = embed)

    @Cog.listener()
    async def on_message_delete(self, mensaje):
        if not mensaje.author.bot:
            try:
                embed = Embed(title = "Mensaje eliminado", description = f"Eliminado por {mensaje.author.display_name} en {mensaje.channel.mention}.", colour = mensaje.author.colour, timestamp = datetime.utcnow())
            except Exception:
                pass
            fields = [("Mensaje", mensaje.content, False)]
            for name, value, inline in fields:
                embed.add_field(name = name, value = value, inline = inline)
            await self.audit_log_channel.send(embed = embed)


def setup(bot):
    bot.add_cog(AuditLog(bot))