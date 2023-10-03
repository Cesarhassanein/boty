import sqlite3, telebot, requests, kvsqlite
import sqlite3
import telebot
from telebot import types
from sqlite3 import Error
import kvsqlite

dat = kvsqlite.sync.Client('users.sqlite', 'users')

def open_database(name):
    try:
        dat = sqlite3.connect(f"{name}.sqlite")
        dat.execute('PRAGMA journal_mode=WAL')
        return dat
    except Error as e:
        print(e)

def close_database(dat):
    if dat:
        dat.close()

def search_name(dat, name):
    first_name, father_name, grand_name, birth = name.split(' ')
    query = f"SELECT fam_no, p_first, p_father, p_grand, p_birth FROM person WHERE p_first LIKE '{first_name}%' AND p_father LIKE '{father_name}%' AND p_grand LIKE '{grand_name}%' AND p_birth LIKE '{birth}%'"
    x = dat.execute(query)
    results = []
    for i in x:
        try:
            fname, mname, lname, birth, famid = i[1], i[2], i[3], int(i[4]) / 100, i[0]
        except Exception as e:
            print(e)
            continue
        n = f'{fname} {mname} {lname} {int(birth)}'.replace("\x84", "")
        if n == name:
            results.append({'name': n, 'famid': famid})
    return results

def get_family(dat, id):
    query = f"SELECT p_first, p_father, p_grand, p_birth FROM person WHERE fam_no = ?"
    x = dat.execute(query, [id])
    names = []
    for i in x:
        try:
            fname, mname, lname, birth = i[0], i[1], i[2], int(i[3]) / 100
        except:
            continue
        names.append({'name': f'{fname} {mname} {lname}'.replace("\x84", ''), 'birth': f'{int(birth)}', 'fam': id})
    return names

# برمجة الروبوت

token = '6330663333:AAELQogdDRieaqIURzxn0K4dIkDVFVClaMs'
bot = telebot.TeleBot(token, num_threads=20, skip_pending=True)
channel = "-1001911925239"
logins = ['creator', 'member', 'administrator']
adds = [6176991957, 6184921079]

if not dat.exists("ban"):
    dat.set("ban", [])

@bot.message_handler(commands=['help'])
def help(message):
    k = '''
    ملاحظات:
    المواليد السنة فقط
    الاسم المركب تدمجه مثال(زينالعابدين)
    المطلوب اسم ثلاثي مو رباعي
    التعلمته بالقواعد خليه الك
    يعني مو تكتب نبأ، هي صحيح بس متصير لازم نبا
    كذلك لتصير مثقف وتستخدم الهاء
    مثل هيج (فاطمه) حط ة.
    '''
    bot.reply_to(message, k)

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id in dat.get("ban"):
        return
    if not dat.exists(f"user_{message.from_user.id}"):
        dat.set(f"user_{message.from_user.id}", {'id': message.from_user.id, 'paid': False, 'try': 5})
    if bot.get_chat_member(channel, message.from_user.id).status not in logins:
        bot.reply_to(message, "اشترك هنا ولاك @Pinnteresto")
    else:
        key = types.InlineKeyboardMarkup(row_width=2)
        a1 = types.InlineKeyboardButton(text="- اربيل .", callback_data="ar")
        a2 = types.InlineKeyboardButton(text="- الانبار .", callback_data="an")
        a3 = types.InlineKeyboardButton(text="- النجف .", callback_data="n")
        a4 = types.InlineKeyboardButton(text="- بابل .", callback_data="ba")
        a5 = types.InlineKeyboardButton(text="- البصرة .", callback_data="bs")
        a6 = types.InlineKeyboardButton(text="- دهوك .", callback_data="dh")
        a7 = types.InlineKeyboardButton(text="- ديالى .", callback_data="dy")
        a8 = types.InlineKeyboardButton(text="- ذي قار .", callback_data="zy")
        a9 = types.InlineKeyboardButton(text="- سليمانية .", callback_data="sl")
        a10 = types.InlineKeyboardButton(text="- صلاح الدين .", callback_data="sa")
        a11 = types.InlineKeyboardButton(text="- القادسية .", callback_data="qa")
        a12 = types.InlineKeyboardButton(text="- كربلاء .", callback_data="kr")
        a13 = types.InlineKeyboardButton(text="- كركوك .", callback_data="ko")
        a14 = types.InlineKeyboardButton(text="- المثنى .", callback_data="mu")
        a15 = types.InlineKeyboardButton(text="- ميسان .", callback_data="mes")
        a16 = types.InlineKeyboardButton(text="- نينوى .", callback_data="ny")
        a17 = types.InlineKeyboardButton(text="- واسط .", callback_data="wa")
        a18 = types.InlineKeyboardButton(text="- بغداد .", callback_data="bag")
        a19 = types.InlineKeyboardButton(text="- بلد .", callback_data="bld")
        key.add(a1, a2, a3)
        key.add(a4)
        key.add(a6, a5, a7)
        key.add(a8)
        key.add(a9, a10, a11)
        key.add(a12)
        key.add(a13, a14, a15)
        key.add(a16)
        key.add(a17, a18, a19)
        key.add(types.InlineKeyboardButton("Us", url="Pinnteresto.t.me"))
        bot.reply_to(message, f'اهلا بيك ببوت البيانات ..', reply_markup=key)

@bot.message_handler(func=lambda m: True)
def m2(message):

    if message.text.startswith("/ban ") and message.from_user.id in adds:
        id = int(message.text.split("/ban ")[1])
        if dat.exists("ban"):
            d = dat.get("ban")
            d.append(id)
            dat.set("ban", d)
            bot.reply_to(message, 'تم حظره !!')
            try:
                bot.send_message(chat_id=id, text='تم حظرك .')
            except:
                return
        else:
            dat.set("ban", [])
            d = dat.get("ban")
            d.append(id)
            dat.set("ban", d)
            bot.reply_to(message, 'تم حظره !!')
            try:
                bot.send_message(chat_id=id, text='تم حظرك .')
            except:
                return
    if message.text.startswith("/unban ") and message.from_user.id in adds:
        id = message.text.split("/unban ")[1]
        if dat.exists("ban"):
            d = dat.get("ban")
            d.remove(id)
            dat.set("ban", d)
            bot.reply_to(message, 'تم الغاء حظره !!')
            try:
                bot.send_message(chat_id=id, text='تم فك حظرك .')
            except:
                return
    if message.text.startswith("/point ") and message.from_user.id in adds:
        id, count = message.text.split(' ')[1], message.text.split(' ')[2]
        g = dat.get(f'user_try_{id}')
        g['points'] += int(count)
        dat.set(f'user_try_{id}', g)
        return bot.reply_to(message, 'تمت بنجاح ..')
    if message.text == ('/giftall') and message.from_user.id in adds:
        key = dat.keys('user_%')
        import random
        c = 0
        for i in key:
            if '_try_' in str(i[0]):
                r = random.randint(1, 2)
                user = dat.get(i[0])
                user['points'] += r
                dat.set(i[0], user)
                c += 1
        return bot.reply_to(message, f'تم ارسال لنقاط لعشوائية الى: {c} شخص .')
    if message.text.startswith('/paid ') and message.from_user.id in adds:
        id = int(message.text.split(' ')[1])
        d = dat.get(f'user_{id}')
        d['paid'] = True
        dat.set(f'user_{id}', d)
        bot.reply_to(message, 'done!')
        return
    if message.text.startswith('/unpaid ') and message.from_user.id in adds:
        id = int(message.text.split(' ')[1])
        d = dat.get(f'user_{id}')
        d['paid'] = False
        dat.set(f'user_{id}', d)
        bot.reply_to(message, 'done!')
        return
    if '/stats' in message.text:
        if message.from_user.id in adds:
            keys = dat.keys('user_%')
            h = len(keys)
            bot.reply_to(message, f'عدد اعضاء البوت: {h}')
    if '/cast' in message.text:
        user_id = message.from_user.id
        if user_id in adds:
            x = bot.reply_to(message, 'ارسل الاذاعه هسه (صورة، نص ، فويس، تحويل، ملف )')
            bot.register_next_step_handler(x, brod)

@bot.callback_query_handler(func=lambda m: True)
def qu(call):
    if call.from_user.id in dat.get("ban"):
        return
    if not dat.exists(f"user_{call.from_user.id}"):
        dat.set(f"user_{call.from_user.id}", {'id': call.from_user.id, 'paid': False, 'try': 5})
        pass
    if bot.get_chat_member(channel, call.from_user.id).status not in logins:
        bot.reply_to(call.message, "اشترك بقناة البوت اولا !\n- https://t.me/Pinnteresto .")
        return
    if call.data.startswith("get:"):
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='انتظر ياحب، جاري جلب العائلة ..')
        famid = call.data.split(':')[1]
        place = call.data.split(":")[2]
        d = open(place)
        fams = fam(d, famid)
        if len(fams) > 0:
            for i in fams:
                name = i['name']
                birth = i['birth']
                now = int(2023) - int(birth)
                id = i['fam']
                k = f'''
الاسم:  {name} .
المواليد: {birth}
العمر: {now}
البطاقة التموينية: {id}
                '''
                bot.send_message(chat_id=call.message.chat.id, text=k)

            bot.reply_to(call.message, 'تمت بنجاح')
        else:
            bot.reply_to(call.message, 'لم يتم العثور على نتائج.')
        close(d)

    if call.data == 'ar':
        place = 'erbil(skidrow)'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=' اربيل - دزلي الاسم الثلاثي والمواليد بعد اخوك | فلان فلان فلان 2005.')
        bot.register_next_step_handler(h, search, place)
    if call.data == 'an':
        place = 'al-anbar(skidrow)'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=' الانبار - دزلي الاسم الثلاثي والمواليد بعد اخوك | فلان فلان فلان 2005.')
        bot.register_next_step_handler(h, search, place)
    if call.data == 'n':
        place = 'najaf(skidrow)'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=' النجف - دزلي الاسم الثلاثي والمواليد بعد اخوك | فلان فلان فلان 2005.')
        bot.register_next_step_handler(h, search, place)
    if call.data == "ba":
        place = 'babylon(skidrow)'
        h = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=' بابل - دزلي الاسم الثلاثي والمواليد بعد اخوك | فلان فلان فلان 2005.')
        bot.register_next_step_handler(h, search, place)
    if call.data == "bs":
        place = 'basra(skidrow)'
        h = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=' البصرة - دزلي الاسم الثلاثي والمواليد بعد اخوك | فلان فلان فلان 2005.')
        bot.register_next_step_handler(h, search, place)
    if call.data == "dh":
        place = 'duhok(skidrow)'
        h = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=' دهوك - دزلي الاسم الثلاثي والمواليد بعد اخوك | فلان فلان فلان 2005.')
        bot.register_next_step_handler(h, search, place)
    if call.data == "dy":
        place = 'diyala(skidrow)'
        h = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=' ديالى - دزلي الاسم الثلاثي والمواليد بعد اخوك | فلان فلان فلان 2005.')
        bot.register_next_step_handler(h, search, place)
    if call.data == "zy":
        place = 'dhiqar(skidrow)'
        h = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=' ذي قار - دزلي الاسم الثلاثي والمواليد بعد اخوك | فلان فلان فلان 2005.')
        bot.register_next_step_handler(h, search, place)
    if call.data == "sl":
        place = 'sulaymaniyah(skidrow)'
        h = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=' سليمانية - دزلي الاسم الثلاثي والمواليد بعد اخوك | فلان فلان فلان 2005.')
        bot.register_next_step_handler(h, search, place)
    if call.data == "sa":
        place = 'salah-aldeen(skidrow)'
        h = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=' سامراء - دزلي الاسم الثلاثي والمواليد بعد اخوك | فلان فلان فلان 2005.')
        bot.register_next_step_handler(h, search, place)
    if call.data == "qa":
        place = 'qadisiyah(skidrow)'
        h = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=' القادسية - دزلي الاسم الثلاثي والمواليد بعد اخوك | فلان فلان فلان 2005.')
        bot.register_next_step_handler(h, search, place)
    if call.data == "kr":
        place = 'karbalaa(skidrow)'
        h = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=' كربلاء - دزلي الاسم الثلاثي والمواليد بعد اخوك | فلان فلان فلان 2005.')
        bot.register_next_step_handler(h, search, place)
    if call.data == "ko":
        place = 'kirkuk(skidrow)'
        h = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=' كركوك - دزلي الاسم الثلاثي والمواليد بعد اخوك | فلان فلان فلان 2005.')
        bot.register_next_step_handler(h, search, place)
    if call.data == "mu":
        place = 'muthana(skidrow)'
        h = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=' المثنى - دزلي الاسم الثلاثي والمواليد بعد اخوك | فلان فلان فلان 2005.')
        bot.register_next_step_handler(h, search, place)
    if call.data == "mes":
        place = 'mesan(skidrow)'
        h = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=' ميسان - دزلي الاسم الثلاثي والمواليد بعد اخوك | فلان فلان فلان 2005.')
        bot.register_next_step_handler(h, search, place)
    if call.data == "ny":
        place = 'ninawa(skidrow)'
        h = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=' نينوى - دزلي الاسم الثلاثي والمواليد بعد اخوك | فلان فلان فلان 2005.')
        bot.register_next_step_handler(h, search, place)
    if call.data == "wa":
        place = 'wasit(skidrow)'
        h = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=' واسط - دزلي الاسم الثلاثي والمواليد بعد اخوك | فلان فلان فلان 2005.')
        bot.register_next_step_handler(h, search, place)
    if call.data == "bag":
        place = 'baghdad(skidrow)'
        h = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=' بغداد - دزلي الاسم الثلاثي والمواليد بعد اخوك | فلان فلان فلان 2005.')
        bot.register_next_step_handler(h, search, place)
    if call.data == "bld":
        place = 'belad-al-rws(skidrow)'
        h = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=' بلد - دزلي الاسم الثلاثي والمواليد بعد اخوك | فلان فلان فلان 2005.')
        bot.register_next_step_handler(h, search, place)

@bot.message_handler(func=lambda m: True)
def main(m):
    if m.from_user.id in dat.get("ban"):
        return
    if not dat.exists(f"user_{m.from_user.id}"):
        dat.set(f"user_{m.from_user.id}", {'id': m.from_user.id, 'paid': False, 'try': 5})
    if bot.get_chat_member(channel, m.from_user.id).status not in logins:
        bot.reply_to(m, "اشترك بقناة البوت اولا !\n- https://t.me/Pinnteresto .")
        return

    if m.text.startswith('Us'):
        if not m.text == 'Us':
            x = int(m.text.split()[1])
            m.text = f'/point {m.from_user.id} {x}'
            m2(m)
            return

    place = m.text.split()[0]
    d = open(place)
    bot.reply_to(m, 'انتظر لحظات ..')
    key = types.InlineKeyboardMarkup(row_width=2)
    key.add(types.InlineKeyboardButton(text="المعلومات", callback_data=f'get:{m.text}'))
    bot.reply_to(m, 'قم بانتظار قليل سيتم جلب البيانات ...')
    d = open_database(place)
    results = search_name(d, m.text)
    close_database(d)
    if len(results) == 1:
        for result in results:
            bot.send_message(m.chat.id, f'{result["name"]} نبا : {result["famid"]}', reply_markup=key)
        close(d)
    elif len(results) > 1:
        msg = f"تم العثور على {len(results)} نتيجة:\n"
        for idx, result in enumerate(results, start=1):
            msg += f"{idx}. {result['name']} نبا : {result['famid']}\n"
        msg += "\nيرجى اختيار النتيجة المناسبة من القائمة أدناه."
        bot.send_message(m.chat.id, msg)
    else:
        bot.send_message(m.chat.id, "عذرًا، لم يتم العثور على نتائج تطابق بحثك.")

    close(d)

def brod(m):

    fileid = ''
    if m.voice:
        fileid = m.voice.file_id
    elif m.text:
        fileid = m.text
    elif m.photo:
        fileid = m.photo[0].file_id
    elif m.video:
        fileid = m.video.file_id
    elif m.video_note:
        fileid = m.video_note.file_id
    elif m.document:
        fileid = m.document.file_id
    elif m.sticker:
        fileid = m.sticker.file_id
    bot.send_message(m.chat.id, f'انتظر  ...')
    for h in adds:
        try:
            bot.send_chat_action(h, 'upload_document')
            bot.forward_message(h, m.chat.id, m.message_id)
        except:
            continue
    if fileid:
        for h in adds:
            try:
                bot.send_chat_action(h, 'upload_document')
                bot.send_document(h, fileid)
            except:
                continue
    bot.reply_to(m, 'تم النشر بنجاح  ..')

bot.polling()
