import discord
import json, os, asyncio

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

COUNTER_FILE = "counter.json"

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

token = os.environ.get("BOT_TOKEN")
if not token:
    print("BOT_TOKEN مو موجود!")
else:
    client.run(token)
