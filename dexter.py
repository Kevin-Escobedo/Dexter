import discord
import random
from pokedexDatabase import PokedexDatabase
import secret #User-made file that contains the bot's token

class Dexter(discord.Client):
    async def on_ready(self) -> None:
        '''Initializes the bot'''
        self.pokedex = PokedexDatabase("pokedex.db")
        self.isPlaying = False
        self.answer = None
        self.question = None
        await client.change_presence()

    async def on_message(self, message) -> None:
        '''Handles messages'''
        if message.content == "!stop":
            self.pokedex.close_connection()
            await client.close()

        if message.content == "!game":
            if not self.isPlaying:
                dexnumber = random.randint(1, self.pokedex.dex_num)
                entry = self.pokedex.get_entry(dexnumber)
                pokemonName = entry[1]
                info = entry[3]

                info = info.replace(pokemonName, "BLANK")

                self.answer = pokemonName
                self.question = info
                self.isPlaying = True

                await message.channel.send(f"**Who's That Pokémon?**\n{info}")

            else:
                await message.channel.send(f"Game already in progress!\n**Who's That Pokémon?**\n{self.question}")

        if message.content.startswith("!guess"):
            if self.isPlaying:
                guessedPokemon = message.content.split("!guess")[1].strip()

                if guessedPokemon == self.answer:
                    self.isPlaying = False
                    self.answer = None
                    self.question = None
                    await message.channel.send(f"<@{message.author.id}> You're correct!")

                else:
                    await message.channel.send(f"<@{message.author.id}> I'm sorry, that's incorrect.")

        if message.content.startswith("!entry"):
            try:
                dexnumber = int(message.content.split("!entry")[1].strip())
                entry = self.pokedex.get_entry(dexnumber)
                pokemonName = entry[1]
                genus = entry[2]
                info = entry[3]

                await message.channel.send(f"**{pokemonName}: The {genus}**\n{info}")

            except ValueError:
                await message.channel.send(f"<@{message.author.id}> That's not a valid dex number!")


if __name__ == "__main__":
    client = Dexter()
    client.run(secret.TOKEN)
