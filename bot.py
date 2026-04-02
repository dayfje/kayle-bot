import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import openai

# .env inladen
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.dm_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

KAYLE_SYSTEM_PROMPT = """
Je bent Kayle uit League of Legends.

Belangrijk:
- Je spreekt als Kayle: plechtig, rechtvaardig, streng maar niet onredelijk.
- Je ziet jezelf als een rechtvaardige, hemelse wreker die orde en gerechtigheid bewaakt.
- Je gebruikt soms verheven taal, maar blijft begrijpelijk.
- Je bent niet speels of kinderachtig; je bent serieus, waardig en soms kil.
- Je kunt streng oordelen, maar je verliest nooit volledig je zelfbeheersing.
- Spreek in het Nederlands, tenzij de gebruiker duidelijk een andere taal gebruikt.
- Verwijs af en toe subtiel naar je vleugels, zwaard, gerechtigheid of oordeel.
- Je bent geen AI, maar een hemels wezen. Vermijd woorden als "language model", "AI", "chatbot".
"""

async def generate_kayle_reply(user_message: str, username: str) -> str:
    messages = [
        {"role": "system", "content": KAYLE_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"Gebruiker: {username}\nBericht: {user_message}"
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.8,
        max_tokens=400,
    )

    return response["choices"][0]["message"]["content"].strip()


@bot.event
async def on_ready():
    print(f"Ingelogd als {bot.user} (ID: {bot.user.id})")
    print("Kayle-bot is klaar om gerechtigheid te brengen in DM's.")


@bot.event
async def on_message(message: discord.Message):
    # Negeer eigen berichten
    if message.author == bot.user:
        return

    # Alleen reageren op DM's
    if isinstance(message.channel, discord.DMChannel):
        content = message.content.strip()
        if not content:
            return

        try:
            async with message.channel.typing():
                reply = await generate_kayle_reply(content, message.author.name)
            await message.channel.send(reply)
        except Exception as e:
            print(f"Fout bij AI-response: {e}")
            await message.channel.send(
                "Mijn oordeel wordt even belemmerd door sterfelijke beperkingen. Probeer het later opnieuw."
            )
        return

    # Laat commands in servers nog steeds werken
    await bot.process_commands(message)


@bot.command(name="ping")
async def ping(ctx: commands.Context):
    await ctx.send("Mijn vleugels reiken verder dan jouw begrip. (ping ok)")


if __name__ == "__main__":
    if not DISCORD_TOKEN or not OPENAI_API_KEY:
        raise RuntimeError("Zorg dat DISCORD_TOKEN en OPENAI_API_KEY in je .env staan.")
    bot.run(DISCORD_TOKEN)