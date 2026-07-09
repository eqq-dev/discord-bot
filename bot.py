import discord
import json, os, asyncio, random
from discord import app_commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# ===== إعدادات السيرفر (تأكد من تعديل الـ ID) =====
GUILD_ID = 1254800517792534539 # ⚠️ ضع أيدي سيرفرك هنا ⚠️

CHANNEL_ID_تفعيل = 1523842165547991110
CHANNEL_ID_مخالفات = 1524094664288768000
CHANNEL_ID_دفع = 1254800520690794556
CHANNEL_ID_مسؤولين = 1270689174474850326

ROLE_ID_مفعل = 1523811436034527384
ROLE_ID_تصريح = 1523811546428473394
ROLE_ID_غير_مفعل = 1254800517943525518

BOT_ID_UNBELIEVABOAT = 292953664492929025

VIOLATIONS_FILE = "violations.json"
USED_IDS_FILE = "used_ids.json"
PENDING_FILE = "pending.json"

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
# =====================

def get_violations():
    if os.path.exists(VIOLATIONS_FILE):
        with open(VIOLATIONS_FILE) as f:
            return json.load(f)
    return {}

def save_violations(data):
    with open(VIOLATIONS_FILE, "w") as f:
        json.dump(data, f)

def get_used_ids():
    if os.path.exists(USED_IDS_FILE):
        with open(USED_IDS_FILE) as f:
            return json.load(f)
    return []

def save_used_ids(data):
    with open(USED_IDS_FILE, "w") as f:
        json.dump(data, f)

def get_pending():
    if os.path.exists(PENDING_FILE):
        with open(PENDING_FILE) as f:
            return json.load(f)
    return []

def save_pending(data):
    with open(PENDING_FILE, "w") as f:
        json.dump(data, f)

def get_random_id():
    used = get_used_ids()
    available = [i for i in range(1000, 3001) if i not in used]
    if not available:
        available = list(range(1000, 3001))
    chosen = random.choice(available)
    used.append(chosen)
    save_used_ids(used)
    return chosen

def get_discount(member):
    for role in member.roles:
        if role.id in رتب_خصومات:
            return رتب_خصومات[role.id]
    return 0

@client.event
async def on_ready():
    print(f"✅ البوت شغال: {client.user}")
    await tree.sync()
    await send_activation_message()

async def send_activation_message():
    channel = client.get_channel(CHANNEL_ID_تفعيل)
    if not channel:
        print("❌ لم يتم العثور على روم التفعيل!")
        return

    # مسح الرسائل القديمة عشان ما تتكرر رسالة التفعيل (اختياري)
    async for message in channel.history(limit=5):
        if message.author == client.user:
            return

    embed = discord.Embed(
        title="🎮 تفعيل الحساب",
        description="اضغط على الزر أدناه لطلب التفعيل والانضمام إلى روسـت سـيـتـي",
        color=0xFF0000
    )
    embed.set_footer(text="روسـت سـيـتـي")

    view = discord.ui.View(timeout=None)
    view.add_item(discord.ui.Button(
        label="اضغط هنا لطلب التفعيل",
        style=discord.ButtonStyle.primary,
        custom_id="طلب_تفعيل",
        row=0
    ))

    await channel.send(embed=embed, view=view)

@tree.command(name="مخالفة", description="تسجيل مخالفة على عضو")
@app_commands.describe(
    عسكري="يوزر العسكري",
    مخالف="يوزر المخالف",
    رقم_المخالفة="رقم المخالفة من 1 إلى 20",
    دليل="وصف الدليل",
    صورة="صورة السيارة مع اللوحات"
)
async def مخالفة_cmd(
    interaction: discord.Interaction,
    عسكري: discord.Member,
    مخالف: discord.Member,
    رقم_المخالفة: str,
    دليل: str,
    صورة: discord.Attachment
):
    if رقم_المخالفة not in مخالفات_قائمة:
        await interaction.response.send_message("❌ رقم المخالفة غير صحيح!", ephemeral=True)
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
        f"**__الدليل مع صورة السيارة مع اللوحات :__**\n{دليل}\n"
        f"{صورة.url}\n\n"
        f"``ملاحظه عدم الإجابة من العسكري سيتم الغاء المخالفة !``"
    )

    view = discord.ui.View(timeout=None)
    view.add_item(discord.ui.Button(
        label="تسديد المخالفة 💰",
        style=discord.ButtonStyle.success,
        custom_id=f"تسديد_{مخالف.id}_{violation_index}_{سعر_بعد_خصم}"
    ))

    await channel.send(رسالة, view=view)
    await interaction.response.send_message("✅ تم تسجيل المخالفة بنجاح!", ephemeral=True)

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

@tree.command(name="ازالة_مخالفة", description="إزالة آخر مخالفة عن عضو")
async def ازالة_مخالفة_cmd(interaction: discord.Interaction, عضو: discord.Member):
    violations = get_violations()
    member_id = str(عضو.id)
    if member_id not in violations or not violations[member_id]:
        await interaction.response.send_message("❌ ما في مخالفات على هذا العضو!", ephemeral=True)
        return
    violations[member_id].pop()
    save_violations(violations)
    await interaction.response.send_message(
        f"✅ تم إزالة آخر مخالفة عن {عضو.mention}",
        ephemeral=True
    )

@tree.command(name="احصائيات", description="أعلى المخالفات في السيرفر")
async def احصائيات_cmd(interaction: discord.Interaction):
    violations = get_violations()
    if not violations:
        await interaction.response.send_message("❌ ما في مخالفات مسجلة حالياً!", ephemeral=True)
        return

    ترتيب = []
    for member_id, مخالفاته in violations.items():
        عدد = len([م for م in مخالفاته if not م["مسددة"]])
        مجموع = sum(م["سعر"] for م in مخالفاته if not م["مسددة"])
        if عدد > 0:
            ترتيب.append((member_id, عدد, مجموع))

    ترتيب.sort(key=lambda x: x[1], reverse=True)

    نص = "# 🏆 أعلى المخالفات غير المسددة في السيرفر\n\n"
    for i, (member_id, عدد, مجموع) in enumerate(ترتيب[:10]):
        member = interaction.guild.get_member(int(member_id))
        اسم = member.mention if member else f"ID: {member_id}"
        نص += f"**{i+1}.** {اسم} — {عدد} مخالفة | {مجموع:,} ريال\n"

    await interaction.response.send_message(نص)

@client.event
async def on_interaction(interaction):
    if interaction.type != discord.InteractionType.component:
        return

    custom_id = interaction.data.get("custom_id", "")

    # ================= زر طلب التفعيل =================
    if custom_id == "طلب_تفعيل":
        pending = get_pending()
        if interaction.user.id in pending:
            await interaction.response.send_message(
                "⚠️ أنت بالفعل في طور التفعيل! راجع رسائلك الخاصة.",
                ephemeral=True
            )
            return

        guild = client.get_guild(GUILD_ID)
        if not guild:
            await interaction.response.send_message("❌ خطأ: لم يتم العثور على السيرفر.", ephemeral=True)
            return

        member = guild.get_member(interaction.user.id)
        رتبة_مفعل = guild.get_role(ROLE_ID_مفعل)
        
        if رتبة_مفعل and رتبة_مفعل in member.roles:
            await interaction.response.send_message(
                "✅ أنت مفعّل بالفعل!",
                ephemeral=True
            )
            return

        pending.append(interaction.user.id)
        save_pending(pending)

        view = discord.ui.View(timeout=None)
        view.add_item(discord.ui.Button(
            label="توجه للخاص 📩",
            style=discord.ButtonStyle.link,
            url=f"https://discord.com/users/{client.user.id}"
        ))

        await interaction.response.send_message(
            embed=discord.Embed(
                description="👇 توجّه إلى الخاص لإكمال التفعيل",
                color=0xFF0000
            ),
            view=view,
            ephemeral=True
        )

        try:
            view_جاهز = discord.ui.View(timeout=None)
            view_جاهز.add_item(discord.ui.Button(
                label="نعم، أنا مستعد ✅",
                style=discord.ButtonStyle.success,
                custom_id=f"جاهز_{interaction.user.id}"
            ))
            await interaction.user.send(
                embed=discord.Embed(
                    description="هل أنت مستعد لبدء أسئلة التفعيل؟",
                    color=0xFF0000
                ),
                view=view_جاهز
            )
        except discord.Forbidden:
            pending = get_pending()
            if interaction.user.id in pending:
                pending.remove(interaction.user.id)
                save_pending(pending)
            await interaction.followup.send("❌ يرجى فتح رسائلك الخاصة (DMs) ليتمكن البوت من مراسلتك!", ephemeral=True)

    # ================= زر نعم جاهز (بدء الأسئلة) =================
    elif custom_id.startswith("جاهز_"):
        member_id = int(custom_id.split("_")[1])
        if interaction.user.id != member_id:
            await interaction.response.send_message("❌ هذا الزر ليس لك!", ephemeral=True)
            return

        await interaction.response.send_message("✅ ممتاز! سيبدأ التفعيل الآن.", ephemeral=True)

        def check_dm(m):
            return m.author == interaction.user and isinstance(m.channel, discord.DMChannel)

        try:
            # السؤال الأول
            await interaction.user.send("**1️⃣ وش اسـمـك ؟**")
            رد1 = await client.wait_for("message", check=check_dm, timeout=120)
            اسم_حقيقي = رد1.content

            # السؤال الثاني
            await interaction.user.send("**2️⃣ اسـمـك بـالـلـعـبـه ؟**")
            رد2 = await client.wait_for("message", check=check_dm, timeout=120)
            اسم_روبلوكس = رد2.content

            # السؤال الثالث
            await interaction.user.send("**3️⃣ اذكـر لـي ثـلاثـه مـن قـوانـيـن الديـسـكـورد ؟**")
            await client.wait_for("message", check=check_dm, timeout=180)

            # السؤال الرابع
            await interaction.user.send("**4️⃣ هـل تـتـعـهـد بـانـك سـتـلـتـزم بـالـقـوانـيـن؟**")
            await client.wait_for("message", check=check_dm, timeout=120)

            # السؤال الخامس - الحلف
            await interaction.user.send(
                f"**5️⃣ اقسم بالله العظيم اني (اسمك) سوف التزم بجميع قوانين الديسكورد جميعها "
                f"وقوانين السيرفر جميعها وقوانين الرول جميعها و اقسم بالله العلي العظيم انني "
                f"لن اخرب السيرفر ولن اساعد او اساهم في تخريبه او تعطيله والله على ما اقول شهيد!**\n\n"
                f"_يجب أن يحتوي ردك على اسمك ({اسم_حقيقي})_"
            )

            محاولات = 0
            حلف_زين = False

            while محاولات < 3:
                رد5 = await client.wait_for("message", check=check_dm, timeout=180)
                if اسم_حقيقي.lower() in رد5.content.lower():
                    حلف_زين = True
                    break
                else:
                    محاولات += 1
                    if محاولات < 3:
                        await interaction.user.send(
                            f"❌ **احلف زين!** تأكد أن اسمك موجود في ردك.\nتبقى لك {3 - محاولات} محاولات."
                        )

            if not حلف_زين:
                await interaction.user.send("❌ **فشلت في التفعيل.** قدم مرة أخرى لاحقاً أو تواصل مع إدارة السيرفر.")
                pending = get_pending()
                if interaction.user.id in pending:
                    pending.remove(interaction.user.id)
                    save_pending(pending)
                return

            # ================= مرحلة إعطاء الرتب وتغيير الاسم =================
            guild = client.get_guild(GUILD_ID)
            member = guild.get_member(interaction.user.id)

            if not member:
                await interaction.user.send("حدث خطأ: لم أتمكن من العثور عليك في السيرفر!")
                return

            # 1. تغيير النيك نيم
            هوية = get_random_id()
            نيك_جديد = f"RC | {اسم_روبلوكس} | {هوية}"

            try:
                await member.edit(nick=نيك_جديد)
            except discord.Forbidden:
                print(f"❌ البوت لا يملك صلاحية تغيير اسم العضو: {member.name}. تأكد من رفع رتبة البوت فوق رتبة العضو!")
            except discord.HTTPException as e:
                print(f"❌ حدث خطأ أثناء تغيير اللقب: {e}")

            # 2. إعطاء الرتب
            رتبة_مفعل = guild.get_role(ROLE_ID_مفعل)
            رتبة_تصريح = guild.get_role(ROLE_ID_تصريح)
            رتبة_غير_مفعل = guild.get_role(ROLE_ID_غير_مفعل)

            try:
                if رتبة_غير_مفعل and رتبة_غير_مفعل in member.roles:
                    await member.remove_roles(رتبة_غير_مفعل)
                if رتبة_مفعل:
                    await member.add_roles(رتبة_مفعل)
                if رتبة_تصريح:
                    await member.add_roles(رتبة_تصريح)
            except discord.Forbidden:
                print("❌ البوت لا يملك صلاحية إدارة الرتب! تأكد من إعطائه Manage Roles ورفع رتبته للأعلى.")
            except Exception as e:
                print(f"❌ حدث خطأ أثناء إعطاء الرتب: {e}")

            await interaction.user.send("🎉 **تم قبولك بنجاح! مرحباً بك في روسـت سـيـتـي.**")

        except asyncio.TimeoutError:
            await interaction.user.send("⏳ انتهى الوقت المخصص للإجابة! يرجى التقديم مرة أخرى.")
        finally:
            pending = get_pending()
            if interaction.user.id in pending:
                pending.remove(interaction.user.id)
                save_pending(pending)

    # ================= زر تسديد المخالفة =================
    elif custom_id.startswith("تسديد_"):
        parts = custom_id.split("_")
        member_id = parts[1]
        index = int(parts[2])
        سعر = int(parts[3])

        if str(interaction.user.id) != member_id:
            await interaction.response.send_message("❌ هذه المخالفة مو عليك!", ephemeral=True)
            return

        violations = get_violations()
        if member_id in violations and index < len(violations[member_id]):
            # التحقق إذا كانت مسددة مسبقاً
            if violations[member_id][index].get("مسددة", False):
                 await interaction.response.send_message("✅ هذه المخالفة مسددة بالفعل!", ephemeral=True)
                 return
                 
            violations[member_id][index]["مسددة"] = True
            save_violations(violations)

            await interaction.response.send_message(
                embed=discord.Embed(
                    description=(
                        f"💰 انسخ هذا الأمر وأرسله في روم تسديد المخالفات:\n"
                        f"```\n!give <@{BOT_ID_UNBELIEVABOAT}> {سعر}\n```"
                    ),
                    color=0x00FF00
                ),
                ephemeral=True
            )
        else:
            await interaction.response.send_message("❌ المخالفة مو موجودة أو حدث خطأ!", ephemeral=True)

token = os.environ.get("BOT_TOKEN")
if not token:
    print("❌ توكن البوت (BOT_TOKEN) غير موجود! تأكد من إضافته في إعدادات Railway.")
else:
    client.run(token)
