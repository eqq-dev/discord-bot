import discord
import json, os, asyncio

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)

COUNTER_FILE = "counter.json"

# ===== تعديل هنا =====
CHANNEL_ID_تقديم = 1333073603155202129  # ايدي روم رسالة التقديم
CHANNEL_ID_مسؤولين = 1270689174474850326  # ايدي روم قبول-رفض

وظائف = [
    "دكتور",
    "تكسي",
    "قاضي",
    "منظم",
    "شرطي",
    "دفاع مدني",
]

اسئلة = [
    "السؤال الأول؟",
    "السؤال الثاني؟",
    "السؤال الثالث؟",
    "السؤال الرابع؟",
    "السؤال الخامس؟",
    "السؤال السادس؟",
]
# =====================

def get_counter():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE) as f:
            return json.load(f).get("count", 1000)
    return 1000

def save_counter(count):
    with open(COUNTER_FILE, "w") as f:
        json.dump({"count": count}, f)

@client.event
async def on_ready():
    print(f"البوت شغال: {client.user}")
    await send_apply_message()

async def send_apply_message():
    channel = client.get_channel(1333073603155202129_تقديم)
    if not channel:
        return

    embed = discord.Embed(
        title="📋 تقديم وظائف",
        description="اضغط على زر الوظيفة التي تريد التقديم عليها",
        color=0xFF0000
    )
    embed.set_footer(text="روسـت سـيـتـي")

    view = discord.ui.View(timeout=None)
    for وظيفة in وظائف:
        btn = discord.ui.Button(
            label=وظيفة,
            style=discord.ButtonStyle.primary,
            custom_id=f"apply_{وظيفة}"
        )
        view.add_item(btn)

    await channel.send(embed=embed, view=view)

@client.event
async def on_member_join(member):
    count = get_counter()
    new_nick = f"rc|????|{count}"
    try:
        await member.edit(nick=new_nick)
        save_counter(count + 1)
        print(f"تم: {new_nick}")
    except discord.Forbidden:
        print("ما في صلاحية")
    except Exception as e:
        print(f"خطأ: {e}")

@client.event
async def on_interaction(interaction):
    if interaction.type != discord.InteractionType.component:
        return

    custom_id = interaction.data["custom_id"]

    # زر الوظيفة
    if custom_id.startswith("apply_"):
        وظيفة_مختارة = custom_id.replace("apply_", "")
        await interaction.response.send_message(
            f"تم اختيار وظيفة **{وظيفة_مختارة}**، راح تصلك رسالة خاصة بالأسئلة!",
            ephemeral=True
        )

        def check(m):
            return m.author == interaction.user and isinstance(m.channel, discord.DMChannel)

        try:
            await interaction.user.send(f"مرحباً! بدأت تقديمك لوظيفة **{وظيفة_مختارة}** في روسـت سـيـتـي 👋\nأجب على الأسئلة التالية:")
        except:
            await interaction.followup.send("فعّل الرسائل الخاصة!", ephemeral=True)
            return

        إجابات = []
        for سؤال in اسئلة:
            await interaction.user.send(سؤال)
            try:
                رد = await client.wait_for("message", check=check, timeout=120)
                إجابات.append(رد.content)
            except:
                await interaction.user.send("انتهى الوقت!")
                return

        await interaction.user.send("✅ تم إرسال تقديمك! انتظر رد المسؤولين.")

        قناة = client.get_channel(1270689174474850326_مسؤولين)
        if not قناة:
            return

        embed = discord.Embed(
            title=f"تقديم جديد - {وظيفة_مختارة}",
            color=0xFFFF00
        )
        embed.add_field(name="المتقدم", value=interaction.user.mention, inline=False)
        for i, (سؤال, جواب) in enumerate(zip(اسئلة, إجابات)):
            embed.add_field(name=f"س{i+1}: {سؤال}", value=جواب, inline=False)

        view = discord.ui.View(timeout=None)
        قبول_btn = discord.ui.Button(
            label="قبول ✅",
            style=discord.ButtonStyle.success,
            custom_id=f"قبول_{interaction.user.id}_{وظيفة_مختارة}"
        )
        رفض_btn = discord.ui.Button(
            label="رفض ❌",
            style=discord.ButtonStyle.danger,
            custom_id=f"رفض_{interaction.user.id}_{وظيفة_مختارة}"
        )
        view.add_item(قبول_btn)
        view.add_item(رفض_btn)

        await قناة.send(embed=embed, view=view)

    # قبول أو رفض
    elif custom_id.startswith("قبول_") or custom_id.startswith("رفض_"):
        parts = custom_id.split("_")
        نوع = parts[0]
        member_id = int(parts[1])
        وظيفة = parts[2]

        member = interaction.guild.get_member(member_id)
        if not member:
            await interaction.response.send_message("العضو ما موجود!", ephemeral=True)
            return

        if نوع == "قبول":
            try:
                await member.send(f"🎉 تهانينا! تم **قبولك** في وظيفة **{وظيفة}** في روسـت سـيـتـي!")
            except:
                pass
            await interaction.response.send_message(f"✅ تم قبول {member.mention} في وظيفة {وظيفة}", ephemeral=True)

        elif نوع == "رفض":
            try:
                await member.send(f"❌ عذراً، تم **رفض** تقديمك في وظيفة **{وظيفة}** في روسـت سـيـتـي.")
            except:
                pass
            await interaction.response.send_message(f"❌ تم رفض {member.mention}", ephemeral=True)

token = os.environ.get("BOT_TOKEN")
if not token:
    print("BOT_TOKEN مو موجود!")
else:
    client.run(token)
