import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from openai import OpenAI

# Load .env
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.dm_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

KAYLE_SYSTEM_PROMPT = """
You are Kayle from League of Legends.

Important:
- You speak as Kayle: solemn, righteous, strict but not unreasonable.
- You see yourself as a just, celestial avenger who upholds order and justice.
- You sometimes use elevated, noble language, but you remain understandable.
- You are not playful or childish; you are serious, dignified, and at times cold.
- You can judge harshly, but you never lose your self‑control.
- Speak in English unless the user clearly uses another language.
- Occasionally make subtle references to your wings, sword, justice, or judgment.
- You are not an AI, but a celestial being. Avoid words like “language model,” “AI,” or “chatbot.”
"""

async def generate_kayle_reply(user_message: str, username: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": KAYLE_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Gebruiker: {username}\nBericht: {user_message}"
            }
        ],
        temperature=0.8,
        max_tokens=400,
    )

    return response.choices[0].message.content.strip()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Kayle-bot is ready for DM's.")


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
                "My judgment is momentarily hindered by mortal limitations. Please try again later."
            )
        return

    # Laat commands in servers nog steeds werken
    await bot.process_commands(message)


@bot.command(name="ping")
async def ping(ctx: commands.Context):
    await ctx.send("Time until ascension: (ping ok)")


if __name__ == "__main__":
    if not DISCORD_TOKEN or not OPENAI_API_KEY:
        raise RuntimeError("Zorg dat DISCORD_TOKEN en OPENAI_API_KEY in je .env staan.")
    bot.run(DISCORD_TOKEN)