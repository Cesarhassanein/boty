from pyrogram import Client as app, filters
from pyrogram.types import InlineKeyboardButton as btn, InlineKeyboardMarkup as mk
import time
import pyrogram.errors
from  pyrogram.enums import ChatMemberStatus
from kvsqlite.sync import Client
db = Client("data.sqlite", 'fuck')


@app.on_message(filters.private & filters.regex("^/start$"), group=1)
async def startm(app, msg):
    user_id = msg.from_user.id
    if db.get("ban_list") is None:
        db.set('ban_list', [])
        pass
    if user_id in db.get("ban_list"):
        return
    chats = db.get('force')
    from .force import check_channel_member
    for i in chats:
      if not await check_channel_member(app, i, user_id):
        k = f'''
عذراً عزيزي 🤚 
عليك الاشتراك بقناة البوت لتتمكن من أستخدامهُ :
- @{i}
- @{i}
— — — — — — — — — —
قم بلأشتراك، وأرسل /start .
        '''
        return await msg.reply(k, reply_markup=mk([[btn(f'- @{i} .', url=f't.me/{i}')]]))
    if db.exists(f"user_{user_id}"):
        coin = db.get(f'user_{user_id}')['coins']
        keys = mk(
        [
            [btn(text='رصيدي: {:,} دينار'.format(coin), callback_data='lol')],
            [btn(text='خدمات تلجرام', callback_data='service')],
            [btn(text='تجميع', callback_data='invite'), btn(text=' شراء دينار ', callback_data='buy')],
            [btn(text=' معلومات حسابك ', callback_data='account'), btn(text='تحويل دينار', callback_data='trans')]
        ]
    )
        rk = f'''
⥃ مرحبا بك عزيزي في بوت Services | الخدمات ♯ 
⥃ البوت يتميز بسرعة تنفيذ الطلبات ⥉
الـ 𝚒𝚍 الخاص بك ⥃ {msg.from_user.id}
        '''
        await app.send_message(msg.from_user.id,rk, reply_markup=keys)
    else:
        info = {'coins': 0 , 'id': user_id, 'premium': False, 'admin': False, "phone":[], "users":[], "date":str(time.time())}
        db.set(f'user_{user_id}', info)
        xxe = db.get("admin_list")
        sc = set(xxe)
        xxx = sorted(sc)
        for i in xxx:
            await app.send_message(i,f"عضو جديد فات للبوت!!\n{msg.from_user.mention} .\nايدي: {msg.from_user.id} .")
        
        coin = db.get(f'user_{user_id}')['coins']
        keys = mk(
        [
            [btn(text='رصيدي: {:,} دينار'.format(coin), callback_data='lol')],
            [btn(text='خدمات تلجرام', callback_data='service')],
            [btn(text='تجميع', callback_data='invite'), btn(text=' شراء دينار ', callback_data='buy')],
            [btn(text=' معلومات حسابك ', callback_data='account'), btn(text='تحويل دينار', callback_data='trans')]
        ]
    )
        rk =f'''
⥃ مرحبا بك عزيزي في بوت Services | الخدمات ♯ 
⥃ البوت يتميز بسرعة تنفيذ الطلبات ⥉
الـ 𝚒𝚍 الخاص بك ⥃ {msg.from_user.id}
        '''
        await app.send_message(msg.from_user.id,rk, reply_markup=keys)