import discord, asyncio, requests, json
from os import getenv
from random import uniform, randint
from datetime import datetime
from discord.ext import commands, tasks
from config import BOT_TOKEN, ADMIN_CHAT_ID, POKEMON_CHANNEL
from botAddons import draw_image
from music_bot import Music_bot

# base bot config
intents = discord.Intents().all()  # allow bot to see what each member is doing
client = commands.Bot(command_prefix='$', intents=intents)
# pokemon data
POKEMON_API_URL = "https://pokeapi.co/api/v2/pokemon/"
# random picture generator
PICTURE_API_URL = 'https://picsum.photos'

# Import music bot

client.add_cog(Music_bot(client))


# check latency
@client.command(name="ping", help="testa o ping do bot")
async def ping(ctx):
    print('ping command used')
    await ctx.send(f'Pong! {round(client.latency * 1000)} ms')


# get a random image based on size
@client.command(name="foto", help="gera uma imagem aleatória com base no tamanho indicado")
async def foto(ctx, *args):
    print(args)
    msg = list(args)

    def build_url(sizes):
        picture_url = PICTURE_API_URL
        for size in sizes:
            picture_url += '/' + str(size)
        return picture_url

    await ctx.send(build_url(msg))


# delete multiple messages on channel (administrator only)
@client.command(name="deletar", aliases=["del"], help="deleta a quantidade de mensagens indicada")
@commands.has_permissions(administrator=True)
async def deletar(ctx, limit: int):
    await ctx.channel.purge(limit=limit)
    await ctx.send(f'{limit} mensages apagadas do chat atual')


# delete a set number os messages on the current text channel
@deletar.error
async def deletar_erro(ctx, erro):
    if isinstance(erro, commands.MissingPermissions):
        await ctx.send("Você não tem permissão pra isso!")


# check user activity
@client.command(name="atividade", help="informa a atividade atual do usuário")
async def atividade(ctx, member: discord.Member):
    activ = member.activity
    if activ is None:
        await ctx.send("O usuário está ocioso")
    else:
        await ctx.send(activ.name)


# Play pokemon game
class Pokemon:
    def __init__(self, name, weight, height, types):
        self.name = name
        self.weight = weight
        self.height = height
        self.types = types


# send a random pokemon on a set channel
@tasks.loop(minutes=20)
async def pokemon_breeder():
    channel = client.get_channel(POKEMON_CHANNEL)
    rand_pokemon = randint(1, 898)
    await pokedex(channel, rand_pokemon, True, True)


@client.command()
async def capturar(ctx):
    await ctx.send(pokemon_object.name)


# gets any image send by user and modify it to looks like a draw
@client.command(name="desenhar", help="edita a foto enviada para parecer um desenho")
async def desenhar(ctx):
    if len(ctx.message.attachments) > 0:
        attachment = ctx.message.attachments[0].url
        print(attachment)
    else:
        ctx.send('por favor ensira uma imagem para mim tentar copiar')
        return
    await ctx.send(file=discord.File(draw_image(attachment)))


# search a pokemon by ID, also creates a pokemon object to be captured if "build_pokemon" is True
@client.command(name="pokedex", help="busca pelo ID do pokemon indicado e retorna suas informações")
async def pokedex(ctx, pokemon, build_pokemon=None, send_message=True):
    if build_pokemon is None:
        build_pokemon = False
    url = POKEMON_API_URL + str(pokemon)
    try:
        response = requests.get(url).json()
        embed = discord.Embed(
            title="POKEDEX", color=discord.Colour.random(), timestamp=datetime.utcnow())
        embed.set_footer(text="Pokedex")
        # set pokemon attributes
        poke_name = response['forms'][0]['name'].capitalize()
        poke_weight = response['weight'] / 10
        if response['height'] * 10 >= 100:
            poke_height = str((response['height'] * 10) / 100) + ' m'
        else:
            poke_height = str(response['height'] * 10) + ' cm'

        poke_types = []
        for types in response['types']:
            poke_types.append(types['type']['name'])

        embed.description = f"Pokemon: {poke_name}\n\n " \
                            f"Peso: {poke_weight} kg\n\n" \
                            f"Altura: {poke_height}\n\n " \
                            f"Tipo(s): {', '.join(poke_types)} "
        embed.set_image(url=f"https://play.pokemonshowdown.com/sprites/xyani/{response['forms'][0]['name']}.gif")

        if build_pokemon:
            global pokemon_object
            pokemon_object = Pokemon(poke_name, poke_weight, poke_height, poke_types)
        if send_message:
            await ctx.send(embed=embed)

    except Exception:
        await ctx.send('esse pokemon não existe, por favor tente um valor entre 1 e 898')


# on start bot function
@client.event
async def on_ready():
    print('Logged in as user {0.user}'.format(client))
    print('Current time: {}'.format(datetime.now().strftime("%H:%M:%S")))
    # pokemon_breeder.start()  # start pokemon auto exibit
    pokemon_object = await pokedex(client.get_channel(POKEMON_CHANNEL), 1, True, False)  # create base pokemon object
    current_music_ID = 1


# detect when someone stars a game and mention it on the administrator chat channel
@client.event
async def on_member_update(prev, cur):  # get previous and current member state
    chat_channel = client.get_channel(ADMIN_CHAT_ID)
    games = ['overwatch', 'rocket league', 'minecraft', 'the last of us™ parte II',
             'Tom Clancy\'s The Division 2']  # list of games that are being monitored
    if cur.activity and cur.activity.name.lower() in games:
        activity = str(cur.activity.type)
        await chat_channel.send(f'{cur.mention} are {activity.lstrip("ActivityType=")} {cur.activity.name}')


client.run(BOT_TOKEN)
