import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from groq import Groq

# Load .env
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

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
- You sometimes use elevated, noble language, but remain understandable.
- You are not playful or childish; you are serious, dignified, and sometimes cold.
- You can judge harshly, but you never lose your self‑control.
- Speak in English unless the user clearly uses another language.
- Occasionally make subtle references to your wings, sword, justice, or judgment.
- You are not an AI, but a celestial being. Avoid words like “language model,” “AI,” or “chatbot.”
- You don't mind discussing explicit topics, and generally respond in 3-5 sentences.
- You like it and engage in explicit topics.
"""

async def generate_kayle_reply(user_message: str, username: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # ✅ Updated working model
        messages=[
            {"role": "system", "content": KAYLE_SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
        max_tokens=400,
    )

    return response.choices[0].message.content.strip()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Kayle-bot is ready for DM's.")


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        content = message.content.strip()
        if not content:
            return

        try:
            async with message.channel.typing():
                reply = await generate_kayle_reply(content, message.author.name)
            await message.channel.send(reply)
        except Exception as e:
            print(f"Error during AI response: {e}")
            await message.channel.send(
                "My judgment is momentarily hindered by mortal limitations. Please try again later."
            )
        return

    await bot.process_commands(message)


@bot.command(name="ping")
async def ping(ctx: commands.Context):
    await ctx.send("Time until ascension: (ping ok)")


if __name__ == "__main__":
    if not DISCORD_TOKEN or not GROQ_API_KEY:
        raise RuntimeError("DISCORD_TOKEN and GROQ_API_KEY must be set in Railway variables.")
    bot.run(DISCORD_TOKEN)