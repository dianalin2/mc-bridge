from mcipc.query import Client as QueryClient
from os import getenv
from discord.ext import commands


ip = getenv('SERVER_IP') or '127.0.0.1'
query_port = int(getenv('QUERY_PORT') or 25565)

bot = commands.Bot(command_prefix='!mc')

query_client = QueryClient(ip, query_port)
query_client.connect()

def join_with_and(lst):
    if len(lst) == 0:
        return ''
    if len(lst) == 1:
        return lst[0]
    return ', '.join(lst[:-1]) + ' and ' + lst[-1]

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.slash_command(name='list', description='Lists all players online')
async def mc_list_slash(ctx):
    stats = dict(query_client.stats(full=True))
    await ctx.respond(f'{join_with_and(["`" + p + "`" for p in stats["players"]]) if len(stats["players"]) > 0 else "No players"} ({stats["num_players"]}/{stats["max_players"]}) {"is" if len(stats["players"]) == 1 else "are"} online')

@bot.slash_command(name='server', description='Lists the server status')
async def mc_server_slash(ctx):
    stats = dict(query_client.stats(full=True))
    await ctx.respond(f'`{stats["host_ip"]}`{"`:" + stats["host_port"] + "`" if stats["host_port"] != 25565 else ""} is online')

bot.run(getenv('DISCORD_TOKEN'))
