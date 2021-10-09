import discord
from pokedexDatabase import PokedexDatabase
import secret #User-made file that contains the bot's token

class Dexter(discord.Client):
    async def on_ready(self) -> None:
        '''Initializes the bot'''
        self.pokedex = PokedexDatabase("pokedex.db")
        await client.change_presence()

    async def on_message(self, message) -> None:
        '''Handles messages'''
        if message.content == "!stop":
            self.pokedex.close_connection()
            await client.close()

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
