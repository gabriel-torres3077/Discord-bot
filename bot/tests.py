import random
"""@client.command()
async def foto(ctx, args):
    await ctx.send('informe o tamanho da imagem (exemplo: \'300 250\', informe apenas dois valores)')

    def check(msg):
        message = msg.content.split()
        message = list(map(int, message))
        return msg.author == ctx.author and msg.channel == ctx.channel and all([isinstance(item, int) for item in message])

    def build_url(sizes):
        sizes = list(map(int, sizes.split())) #split string input into
        picture_url = PICTURE_API_URL
        for size in sizes:
            picture_url += '/' + str(size)
        return picture_url

    try:
        msg = await client.wait_for("message", check=check, timeout=30) #esperar pela mensagem do usuário dentro de 30 segundos
    except asyncio.TimeoutError:
        await ctx.send('Ta demorando pq corno?')
    finally:
        await ctx.send(build_url(msg.content))"""

#pokemon
"""import requests, json
from random import uniform, randint
from uuid import uuid4

BASE_URL = "https://pokeapi.co/api/v2/pokemon/"
pokemons = []


class Pokemon:
    def __init__(self, name, weight, height, types):
        self.name = name
        self.weight = weight
        self.height = height
        self.types = types
        self.BASE_CAPTURE_CHANCE = 30 # the lower the easier

    def capture(self, pokeball):
        print(f'tentando capturar {self.name}!')
        capture_roll = randint(0, 100)  # percent
        print(capture_roll)
        if capture_roll > self.BASE_CAPTURE_CHANCE:
            print(f'{self.name} foi capturado')
        else:
            print(f'{self.name} não foi capturado')

   # def capture(self, pokeball):

class Pokeball:
    def __int__(self, name, effect, quantity, icon):
        self.name = name
        self.effect = effect
        self.quantity = quantity
        self.icon = icon

def pokedex(number):
    url = BASE_URL + str(number)
    print(url)
    POKEMON_TOKEN = uuid4()
    print(POKEMON_TOKEN)

    try:
        response = requests.get(url).json()
        pokemon_name = str(response['forms'][0]['name'])
        pokemon_weight = float(response['weight'] / 10)
        pokemon_height = response['height'] * 10
        pokemon_types = []
        for types in response['types']:
            pokemon_types.append(types['type']['name'])
        print(f"\n\nPokemon: {pokemon_name}\nPeso: {pokemon_weight} kg\nAltura: {pokemon_height} cm\nTipo(s): {', '.join(pokemon_types)}\n\n")
        pokemons = Pokemon(pokemon_name, pokemon_weight, pokemon_height, pokemon_types)
        return pokemons
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)


pokemon = pokedex(1)
pokemon.capture()
"""

#render cv draw

"""def render(base_image):
    img_rgb = cv2.imread(base_image)
    shape = img_rgb.shape  # get base image shape

    canvas = cv2.imread('Drawn_images/pencilsketch_bg.jpg', cv2.CV_8UC1)
    canvas = cv2.resize(canvas, (shape[1], shape[0]))# resize background image to the base image size

    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (21, 21), 0, 0)
    img_blend = cv2.divide(img_gray, img_blur, scale=256)

    # if available, blend with background canvas
    img_blend = cv2.multiply(img_blend, canvas, scale=1. / 256)

    test_blend = cv2.cvtColor(img_blend, cv2.COLOR_GRAY2RGB)
    cv2.imshow('sketch: ', img_blend)
    cv2.imshow('final: ', test_blend)
    cv2.waitKey(0)

render('Drawn_images/room.jpg')
"""
print(random.randint(0, 10))
"""

"""