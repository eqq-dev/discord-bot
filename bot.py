import discord
import json, os, asyncio
from discord import app_commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

COUNTER_FILE = "counter.json"
VIOLATIONS_FILE = "violations.json"

# ===== تعديل هنا =====
CHANNEL_ID_تقديم = 1333073603155202129
CHANNEL_ID_مسؤولين = 1270689174474850326
CHANNEL_ID_مخالفات = 1341702551338356767
CHANNEL_ID_تقارير = 1333470649594679347
CHANNEL_ID_دفع = 1333470649594679347

ROLE_ID_عاطل = 1326202454181679155

رتب_وظائف = {
    "دكتور": 1254800517989924946,
    "منظم": 1345104478772396032,
    "شرطي": 1331719314973261894,
    "قاضي": 1332765714737664031,
    "تكسي": 1254800517964632175,
    "هوست": 1254800517981405222,
}

BOT_ID_UNBELIEVABOAT = 292953664492929025

رتب_خصومات = {
    1326183589263572994: 0,
    1326180985867337740: 25,
    1326180626746835066: 40,
    1326180817847717948: 50,
    1326181915316977789: 70,
    1348243729798139928: 100,
    1336853103567310979: 80,
}

مخالفات_قائمة = {
    "1":  {"اسم": "قطع إشارة",              "سعر": 5000,  "ملاحظة": ""},
    "2":  {"اسم": "تفحيط",                  "سعر": 5000,  "ملاحظة": "حجز سيارة يومين"},
    "3":  {"اسم": "سرعة",                   "سعر": 4000,  "ملاحظة": ""},
    "4":  {"اسم": "زره",                    "سعر": 3000,  "ملاحظة": ""},
    "5":  {"اسم": "الهروب من الشرطة",       "سعر": 7500,  "ملاحظة": "حجز السيارة يومين"},
    "6":  {"اسم": "الهروب من الحادث",       "سعر": 8000,  "ملاحظة": ""},
    "7":  {"اسم": "دخول سيارة سيدان بالبر", "سعر": 4000,  "ملاحظة": ""},
    "8":  {"اسم": "إزعاج بالبوري",          "سعر": 2000,  "ملاحظة": ""},
    "9":  {"اسم": "الهروب من التفتيش",      "سعر": 10000, "ملاحظة": "حجز السيارة أربع أيام"},
    "10": {"اسم": "عكس الطريق",             "سعر": 4000,  "ملاحظة": ""},
    "11": {"اسم": "عدم تشغيل الأنوار",      "سعر": 2000,  "ملاحظة": ""},
    "12": {"اسم": "سحب جلنطات",             "سعر": 3000,  "ملاحظة": ""},
    "13": {"اسم": "المشي بدون لوحة",        "سعر": 6000,  "ملاحظة": ""},
    "14": {"اسم": "الوقوف التام في الخط",   "سعر": 5000,  "ملاحظة": ""},
    "15": {"اسم": "المراوغة بسرعة عالية",   "سعر": 10000, "ملاحظة": "حجز المركبة حتى التسديد"},
    "16": {"اسم": "طمس اللوحة بالثلج",      "سعر": 7000,  "ملاحظة": ""},
    "17": {"اسم": "عدم حمل تأمين",          "سعر": 2000,  "ملاحظة": ""},
    "18": {"اسم": "عدم حمل رخصة",           "سعر": 2000,  "ملاحظة": ""},
    "19": {"اسم": "صدم الأقماع",            "سعر": 2000,  "ملاحظة": ""},
    "20": {"اسم": "فك اللوحة الخلفية",      "سعر": 5000,  "ملاحظة": ""},
}

اسئلة_وظائف = {
    "شرطي": [
        "السؤال الأول للشرطي؟",
        "السؤال الثاني للشرطي؟",
        "السؤال الثالث للشرطي؟",
        "السؤال الرابع للشرطي؟",
        "السؤال الخامس للشرطي؟",
    ],
    "دكتور": [
        "السؤال الأول للدكتور؟",
        "السؤال الثاني للدكتور؟",
        "السؤال الثالث للدكتور؟",
        "السؤال الرابع للدكتور؟",
        "السؤال الخامس للدكتور؟",
    ],
    "تكسي": [
        "السؤال الأول للتكسي؟",
        "السؤال الثاني للتكسي؟",
        "السؤال الثالث للتكسي؟",
        "السؤال الرابع للتكسي؟",
        "السؤال الخامس للتكسي؟",
    ],
    "قاضي": [
        "السؤال الأول للقاضي؟",
        "السؤال الثاني للقاضي؟",
        "السؤال الثالث للقاضي؟",
        "السؤال الرابع للقاضي؟",
        "السؤال الخامس للقاضي؟",
    ],
    "منظم": [
        "السؤال الأول للمنظم؟",
        "السؤال الثاني للمنظم؟",
        "السؤال الثالث للمنظم؟",
        "السؤال الرابع للمنظم؟",
        "السؤال الخامس للمنظم؟",
    ],
    "هوست": [
        "السؤال الأول للهوست؟",
        "السؤال الثاني للهوست؟",
        "السؤال الثالث للهوست؟",
        "السؤال الرابع للهوست؟",
        "السؤال الخامس للهوست؟",
    ],
}
# =====================

def get_counter():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE) as f:
            return json.load(f).get("count", 1000)
    return 1000

def save_counter(count):
    with open(COUNTER_FILE, "w") as f:
        json.dump({"count": count}, f)

def get_violations():
    if os.path.exists(VIOLATIONS_FILE):
        with open(VIOLATIONS_FILE) as f:
            return json.load(f)
    return {}

def save_violations(data):
    with open(VIOLATIONS_FILE, "w") as f:
        json.dump(data, f)

def get_discount(member):
    for role in member.roles:
        if role.id in رتب_خصومات:
            return رتب_خصومات[role.id]
    return 0

@client.event
async def on_ready():
    print(f"البوت شغال: {client.user}")
    await tree.sync()
    await send_apply_message()

async def send_apply_message():
    channel = client.get_channel(CHANNEL_ID_تقديم)
    if not channel:
        return

    view = discord.ui.View(timeout=None)
    select = discord.ui.Select(
        placeholder="اختر وظيفتك...",
        custom_id="select_وظيفة",
        options=[
            discord.SelectOption(label=وظيفة, value=وظيفة)
            for وظيفة in اسئلة_وظائف.keys()
        ]
    )
    view.add_item(select)

    embed = discord.Embed(
        title="📋 تقديم وظائف",
        description="اختر الوظيفة التي تريد التقديم عليها من القائمة أدناه",
        color=0xFF0000
    )
    embed.set_footer(text="روسـت سـيـتـي")

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

# ===== سلاش كوماند المخالفات =====
@tree.command(name="مخالفة", description="تسجيل مخالفة على عضو")
@app_commands.describe(
    عسكري="يوزر العسكري",
    مخالف="يوزر المخالف",
    رقم_المخالفة="رقم المخالفة من 1 إلى 20",
    دليل="وصف الدليل ورابط الصورة"
)
async def مخالفة_cmd(interaction: discord.Interaction,
                      عسكري: discord.Member,
                      مخالف: discord.Member,
                      رقم_المخالفة: str,
                      دليل: str):

    if رقم_المخالفة not in مخالفات_قائمة:
        await interaction.response.send_message("رقم المخالفة غير صحيح! الأرقام من 1 إلى 20", ephemeral=True)
        return

    مخالفة = مخالفات_قائمة[رقم_المخالفة]
    خصم = get_discount(مخالف)
    سعر_اصلي = مخالفة["سعر"]
    سعر_بعد_خصم = int(سعر_اصلي * (1 - خصم / 100))

    violations = get_violations()
    member_id = str(مخالف.id)
    if member_id not in violations:
        violations[member_id] = []

    violation_index = len(violations[member_id])
    violations[member_id].append({
        "مخالفة": مخالفة["اسم"],
        "سعر": سعر_بعد_خصم,
        "مسددة": False,
        "عسكري": عسكري.id
    })
    save_violations(violations)

    channel = client.get_channel(CHANNEL_ID_مخالفات)

    ملاحظة_نص = f"\n> **ملاحظة:** {مخالفة['ملاحظة']}" if مخالفة["ملاحظة"] else ""
    خصم_نص = f" _(خصم {خصم}% بسبب رتبتك)_" if خصم > 0 else ""

    رسالة = (
        f"# نموذج رصد المخالفات 👇\n"
        f"**__يوزر العسكري ( @ ) :__** {عسكري.mention}\n\n"
        f"**__يوزر المخالف ( @ ) :__** {مخالف.mention}\n\n"
        f"**__ما المخالفة التي ارتكبها :__** {مخالفة['اسم']}\n\n"
        f"**__سعر المخالفة المرتكبه :__** {سعر_بعد_خصم:,} ريال{خصم_نص}{ملاحظة_نص}\n\n"
        f"**__الدليل مع صورة السيارة مع اللوحات :__**\n{دليل}\n\n"
        f"``ملاحظه عدم الإجابة من العسكري سيتم الغاء المخالفة !``"
    )

    view = discord.ui.View(timeout=None)
    تسديد_btn = discord.ui.Button(
        label="تسديد المخالفة 💰",
        style=discord.ButtonStyle.success,
        custom_id=f"تسديد_{مخالف.id}_{violation_index}_{سعر_بعد_خصم}"
    )
    view.add_item(تسديد_btn)

    await channel.send(رسالة, view=view)
    await interaction.response.send_message("✅ تم تسجيل المخالفة!", ephemeral=True)

# ===== سلاش كوماند إضافة مخالفة =====
@tree.command(name="اضافة_مخالفة", description="إضافة مخالفة يدوياً على عضو")
async def اضافة_مخالفة_cmd(interaction: discord.Interaction,
                             عضو: discord.Member,
                             مخالفة: str,
                             سعر: int):
    violations = get_violations()
    member_id = str(عضو.id)
    if member_id not in violations:
        violations[member_id] = []
    violations[member_id].append({
        "مخالفة": مخالفة,
        "سعر": سعر,
        "مسددة": False,
        "عسكري": interaction.user.id
    })
    save_violations(violations)
    await interaction.response.send_message(
        f"✅ تم إضافة مخالفة **{مخالفة}** على {عضو.mention} بسعر {سعر:,} ريال",
        ephemeral=True
    )

# ===== سلاش كوماند إزالة مخالفة =====
@tree.command(name="ازالة_مخالفة", description="إزالة آخر مخالفة عن عضو")
async def ازالة_مخالفة_cmd(interaction: discord.Interaction, عضو: discord.Member):
    violations = get_violations()
    member_id = str(عضو.id)
    if member_id not in violations or not violations[member_id]:
        await interaction.response.send_message("ما في مخالفات على هذا العضو!", ephemeral=True)
        return
    violations[member_id].pop()
    save_violations(violations)
    await interaction.response.send_message(f"✅ تم إزالة آخر مخالفة عن {عضو.mention}", ephemeral=True)

# ===== سلاش كوماند الإحصائيات =====
@tree.command(name="احصائيات", description="أعلى المخالفات في السيرفر")
async def احصائيات_cmd(interaction: discord.Interaction):
    violations = get_violations()
    if not violations:
        await interaction.response.send_message("ما في مخالفات مسجلة!", ephemeral=True)
        return

    ترتيب = []
    for member_id, مخالفاته in violations.items():
        عدد = len([م for م in مخالفاته if not م["مسددة"]])
        مجموع = sum(م["سعر"] for م in مخالفاته if not م["مسددة"])
        if عدد > 0:
            ترتيب.append((member_id, عدد, مجموع))

    ترتيب.sort(key=lambda x: x[1], reverse=True)

    نص = "# 🏆 أعلى المخالفات في السيرفر\n\n"
    for i, (member_id, عدد, مجموع) in enumerate(ترتيب[:10]):
        member = interaction.guild.get_member(int(member_id))
        اسم = member.mention if member else f"ID: {member_id}"
        نص += f"**{i+1}.** {اسم} — {عدد} مخالفة | {مجموع:,} ريال\n"

    await interaction.response.send_message(نص)

# ===== سلاش كوماند التقارير =====
@tree.command(name="تقرير", description="إرسال تقرير على عضو")
async def تقرير_cmd(interaction: discord.Interaction,
                     المبلغ_عنه: discord.Member,
                     السبب: str,
                     الدليل: str):
    channel = client.get_channel(CHANNEL_ID_تقارير)

    رسالة = (
        f"# 📢 تقرير جديد\n\n"
        f"**__المُبلِّغ :__** {interaction.user.mention}\n\n"
        f"**__المُبلَّغ عنه :__** {المبلغ_عنه.mention}\n\n"
        f"**__السبب :__** {السبب}\n\n"
        f"**__الدليل :__** {الدليل}"
    )

    view = discord.ui.View(timeout=None)
    view.add_item(discord.ui.Button(
        label="قبول التقرير ✅",
        style=discord.ButtonStyle.success,
        custom_id=f"تقرير_قبول_{المبلغ_عنه.id}_{interaction.user.id}"
    ))
    view.add_item(discord.ui.Button(
        label="رفض التقرير ❌",
        style=discord.ButtonStyle.danger,
        custom_id=f"تقرير_رفض_{المبلغ_عنه.id}_{interaction.user.id}"
    ))

    await channel.send(رسالة, view=view)
    await interaction.response.send_message("✅ تم إرسال تقريرك!", ephemeral=True)

@client.event
async def on_interaction(interaction):
    if interaction.type != discord.InteractionType.component:
        return

    custom_id = interaction.data["custom_id"]

    # تسديد المخالفة
    if custom_id.startswith("تسديد_"):
        parts = custom_id.split("_")
        member_id = parts[1]
        index = int(parts[2])
        سعر = int(parts[3])

        if str(interaction.user.id) != member_id:
            await interaction.response.send_message("هذه المخالفة مو عليك!", ephemeral=True)
            return

        violations = get_violations()
        if member_id in violations and index < len(violations[member_id]):
            violations[member_id][index]["مسددة"] = True
            save_violations(violations)

            channel = client.get_channel(CHANNEL_ID_دفع)
            await channel.send(f"!give <@{BOT_ID_UNBELIEVABOAT}> {سعر}")

            await interaction.response.send_message(
                f"✅ تم تسديد المخالفة بنجاح! المبلغ: {سعر:,} ريال",
                ephemeral=True
            )
        else:
            await interaction.response.send_message("المخالفة مو موجودة!", ephemeral=True)

    # اختيار وظيفة من القائمة
    elif custom_id == "select_وظيفة":
        وظيفة_مختارة = interaction.data["values"][0]
        اسئلة = اسئلة_وظائف.get(وظيفة_مختارة, [])

        await interaction.response.send_message(
            f"تم اختيار وظيفة **{وظيفة_مختارة}**، راح تصلك رسالة خاصة بالأسئلة!",
            ephemeral=True
        )

        def check(m):
            return m.author == interaction.user and isinstance(m.channel, discord.DMChannel)

        try:
            await interaction.user.send(
                f"مرحباً! بدأت تقديمك لوظيفة **{وظيفة_مختارة}** في روسـت سـيـتـي 👋\n"
                f"أجب على الأسئلة التالية:"
            )
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

        قناة = client.get_channel(CHANNEL_ID_مسؤولين)
        if not قناة:
            return

        نص_تقديم = (
            f"# تقديم جديد — {وظيفة_مختارة}\n\n"
            f"**المتقدم:** {interaction.user.mention}\n\n"
        )
        for i, (سؤال, جواب) in enumerate(zip(اسئلة, إجابات)):
            نص_تقديم += f"**س{i+1}:** {سؤال}\n**ج:** {جواب}\n\n"

        view = discord.ui.View(timeout=None)
        view.add_item(discord.ui.Button(
            label="قبول ✅",
            style=discord.ButtonStyle.success,
            custom_id=f"قبول_{interaction.user.id}_{وظيفة_مختارة}"
        ))
        view.add_item(discord.ui.Button(
            label="رفض ❌",
            style=discord.ButtonStyle.danger,
            custom_id=f"رفض_{interaction.user.id}_{وظيفة_مختارة}"
        ))

        await قناة.send(نص_تقديم, view=view)

    # قبول/رفض التقديم
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
            رتبة_id = رتب_وظائف.get(وظيفة)
            رتبة_عاطل = interaction.guild.get_role(ROLE_ID_عاطل)
            if رتبة_عاطل and رتبة_عاطل in member.roles:
                await member.remove_roles(رتبة_عاطل)
            if رتبة_id:
                رتبة = interaction.guild.get_role(رتبة_id)
                if رتبة:
                    await member.add_roles(رتبة)
            try:
                await member.send(
                    f"🎉 تهانينا! تم **قبولك** في وظيفة **{وظيفة}** في روسـت سـيـتـي!"
                )
            except:
                pass
            await interaction.response.send_message(
                f"✅ تم قبول {member.mention} في وظيفة {وظيفة}",
                ephemeral=True
            )
        else:
            try:
                await member.send(
                    f"❌ عذراً، تم **رفض** تقديمك في وظيفة **{وظيفة}** في روسـت سـيـتـي."
                )
            except:
                pass
            await interaction.response.send_message(
                f"❌ تم رفض {member.mention}",
                ephemeral=True
            )

    # قبول/رفض التقرير
    elif custom_id.startswith("تقرير_"):
        parts = custom_id.split("_")
        نوع = parts[1]
        مبلغ_عنه = interaction.guild.get_member(int(parts[2]))

        if نوع == "قبول":
            await interaction.response.send_message(
                f"✅ تم قبول التقرير على {مبلغ_عنه.mention if مبلغ_عنه else 'العضو'}",
                ephemeral=True
            )
        else:
            await interaction.response.send_message("❌ تم رفض التقرير", ephemeral=True)

token = os.environ.get("BOT_TOKEN")
if not token:
    print("BOT_TOKEN مو موجود!")
else:
    client.run(token)
