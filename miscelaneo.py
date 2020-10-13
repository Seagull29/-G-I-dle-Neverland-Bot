import discord
from discord.ext.commands import Cog, command, CheckFailure, has_permissions
from discord import Forbidden
import db

class Miscelaneo(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Miscelaneo")

    @command(name = "prefix")
    async def change_prefix(self, ctx, new : str):
        if len(new) > 5:
            await ctx.send("El prefix no puede ser tan largo")
        elif db.field("SELECT GuildID from guilds WHERE GuildID = ?", ctx.guild.id) is None:
            db.execute("INSERT INTO guilds VALUES (?, ?)", ctx.guild.id, new)
            await ctx.send(f"Prefix cambiado a: {new}")
        else:
            db.execute("UPDATE guilds SET Prefix = ? WHERE GuildID = ?", new, ctx.guild.id)
            await ctx.send(f"Prefix cambiado a: {new}")
    
    @change_prefix.error
    async def change_prefix_error(self, ctx, error):
        if isinstance(error, CheckFailure):
            await ctx.send("Necesitas permisos especiales para cambiar el prefix")
    

    @Cog.listener()
    async def on_member_join(self, member):
        db.execute("INSERT INTO exp (UserID) VALUES (?)", member.id)
        #await self.bot.get_channel(763095597527597067).send(f"¡Bienvenido a **{member.guild.name}** {member.mention}!")
        try:
            await member.send(f"Esperamos su permanencia en **{member.guild.name}**. Difrutelo.")
        except Forbidden:
            pass
        
        #await member.add_roles(member.guild.get_role(763099989370732555))
    
    @Cog.listener()
    async def on_member_remove(self, member):
        db.execute("DELETE FROM exp WHERE UserID = ?", member.id)
        #await self.bot.get_channel(763095632340582460).send(f"**{member.display_name}** dejo **{member.guild.name}**, lo sentimos.")


def setup(bot):
    bot.add_cog(Miscelaneo(bot))