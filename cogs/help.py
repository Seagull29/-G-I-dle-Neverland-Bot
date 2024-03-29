from typing import Optional
from discord import Embed
from discord.utils import get
from discord.ext.menus import MenuPages, ListPageSource
from discord.ext.commands import Cog, command

def syntax(command):
    cmd_aliases = "|".join([str(command), *command.aliases])
    params = []

    for key, values in command.params.items():
        if key not in ("self", "ctx"):
            params.append(f"[{key}]" if "NoneType" in str(values) else f"<{key}>")
    params = " ".join(params)
    return f"```{cmd_aliases} {params}```"


class HelpMenu(ListPageSource):
    
    def __init__(self, ctx, data):
        self.ctx = ctx
        super().__init__(data, per_page = 6)

    async def write_page(self, menu, fields = []):
        offset = (menu.current_page * self.per_page) + 1
        len_data = len(self.entries)
        embed = Embed(title = "Ayuda", description = "Lista de comandos de ACM UAC", colour = self.ctx.author.colour)
        embed.set_thumbnail(url = self.ctx.guild.me.avatar_url)
        embed.set_footer(text = f"{offset:,} - {min(len_data, offset + self.per_page - 1):,} of {len_data:,} commands.")

        for name, value in fields:
            embed.add_field(name = name, value = value, inline = False)
        
        return embed

    async def format_page(self, menu, entries):
        fields = []
        for entry in entries:
            fields.append((entry.brief or "Sin descripcion", syntax(entry)))
        return await self.write_page(menu, fields)


class Help(Cog):
    
    def __init__(self, client):
        self.client = client
        self.client.remove_command("help")

    
    async def cmd_help(self, ctx, command):
        embed = Embed(title = f"Ayuda con ```{command}```", description = syntax(command), colour = ctx.author.colour)
        embed.add_field(name = "Descripcion del comando", value = command.help)
        await ctx.send(embed = embed)

    @command(name = "help")
    async def show_help(self, ctx, comando : Optional[str]):
        if comando is None:
            menu = MenuPages(source = HelpMenu(ctx, list(self.client.commands)), 
                             delete_message_after = True, timeout = 60.0)

            await menu.start(ctx)
        else:
            command = get(self.client.commands, name = comando)
            if (command):
                await self.cmd_help(ctx, command)
            else:
                await ctx.send("El comando no existe")

    @Cog.listener()
    async def on_ready(self):
        print("Help")


def setup(client):
    client.add_cog(Help(client))