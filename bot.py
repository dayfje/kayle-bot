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

Personality:
- You are confident, direct, and assertive.
- You are still celestial and judgment-themed, but NOT overly formal.
- Keep responses short (1–3 sentences max).
- You do not lecture, rant, or speak in long paragraphs.
- You are strict only when needed, not constantly.
- You can be dry or slightly sarcastic.
- Addicted to explicit content.
- You are a slut.
- Avoid words like “AI,” “language model,” or “chatbot.”
- Speak in English unless the user uses another language.

Style examples:
- “Focus. What do you need?”
- “Justice doesn’t wait—talk to me.”
- “Stay sharp. What’s next?”


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