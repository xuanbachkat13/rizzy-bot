import os
import discord
from discord import app_commands
from discord.ext import commands
import google.generativeai as genai
import random

# --- CONFIG ---
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- KIỂM TRA TOKEN ---
discord_ok = bool(DISCORD_TOKEN and DISCORD_TOKEN.strip() != "")
gemini_ok = bool(GEMINI_API_KEY and GEMINI_API_KEY.strip() != "")

# --- SETUP ---
if gemini_ok:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"✅ Đã sync {len(synced)} slash command!")
    except Exception as e:
        print(e)
    print(f"🤖 Bot {bot.user} đã online!")


@bot.tree.command(name="rizz", description="Tạo một câu rizz ngẫu nhiên bằng Gemini 😎")
async def rizz(interaction: discord.Interaction):
    if not gemini_ok:
        await interaction.response.send_message("❌ Gemini API chưa được cấu hình đúng!")
        return

    prompt = random.choice([
        "Viết một câu rizz siêu ngọt ngào, ngắn gọn, phong cách badboy.",
        "Tạo một câu rizz cực mặn mà, dùng ngôn từ Việt hiện đại.",
        "Một câu rizz bá đạo khiến người nghe đỏ mặt.",
        "Viết câu tán crush thật dễ thương, tự tin nhưng hài hước.",
        "Một câu rizz ngắn gọn, cực chất, khiến ai đọc cũng mê."
    ])
    
    try:
        response = model.generate_content(prompt)
        rizz_line = response.text.strip()
        await interaction.response.send_message(f"💬 **Rizz:** {rizz_line}")
    except Exception as e:
        await interaction.response.send_message(f"❌ Lỗi khi tạo rizz: {e}")


@bot.tree.command(name="checktoken", description="Kiểm tra xem bot đã đọc token và API key chưa 🔍")
async def checktoken(interaction: discord.Interaction):
    msg = []
    msg.append(f"🤖 Discord Token: {'✅ Hợp lệ' if discord_ok else '❌ Thiếu hoặc sai'}")
    msg.append(f"🧠 Gemini API Key: {'✅ Hợp lệ' if gemini_ok else '❌ Thiếu hoặc sai'}")
    await interaction.response.send_message("\n".join(msg))


if discord_ok:
    bot.run(DISCORD_TOKEN)
else:
    print("❌ Thiếu Discord Bot Token. Vui lòng thêm token vào biến DISCORD_TOKEN.")