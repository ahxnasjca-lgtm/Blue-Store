import datetime
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"تم تسجيل الدخول بنجاح باسم: {bot.user}")

@bot.event
async def on_message(message):
    # تجاهل رسائل البوتات
    if message.author.bot:
        return

    user = message.author
    
    # التحقق مما إذا كتب المستخدم نصاً أو أرفق صورة أو رد على شيء
    review_text = message.content
    if not review_text and message.attachments:
        review_text = "تقييم مع صورة/مرفق"
    elif not review_text:
        review_text = "تم إرسال التقييم"

    # تنسيق التاريخ والوقت
    now = datetime.datetime.now()
    formatted_date = now.strftime("%m/%d/%Y %I:%M %p")

    # جلب صورة المستخدم
    avatar_url = user.avatar.url if user.avatar else user.default_avatar.url

    # إنشاء الإمبد
    embed = discord.Embed(
        description=f"**التقييم:** {review_text}\n\n<@{user.id}>",
        color=discord.Color.from_rgb(43, 45, 49)
    )
    
    embed.set_author(
        name=user.display_name,
        icon_url=avatar_url
    )
    
    embed.set_thumbnail(url=avatar_url)
    embed.set_footer(text=formatted_date)

    # إذا أرفق المستخدم صور مع التقييم، نضعها داخل الإمبد أيضاً لتظهر بشكل احترافي!
    if message.attachments:
        embed.set_image(url=message.attachments[0].url)

    # إرسال رسالة الإمبد
    await message.channel.send(
        content=f"💙 <@{user.id}> شكراً لك على تقييمك — **Blue Store**",
        embed=embed
    )

    # حذف رسالة العضو الأصلية
    try:
        await message.delete()
    except:
        pass

    await bot.process_commands(message)

# ضع توكن بوتك هنا
TOKEN = "MTU2OTMyNjIxOTYwNTA1NzY0OA.GYyZhS.qRSX-GGmXlFIhuNIhs2Dywojzs58TW1HiFVyT4"
bot.run(TOKEN)