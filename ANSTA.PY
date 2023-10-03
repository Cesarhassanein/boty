from pyrogram import Client as app, filters
from pyrogram.types import InlineKeyboardButton as btn, InlineKeyboardMarkup as mk
import time

# إضافة استيراد قاعدة البيانات
from pyrogram import Client as db_client
db = db_client("data.sqlite", 'fuck')

# دالة للتحقق من صحة حساب انستقرام
def verify_account(username, password):
    # يعتبر الحساب صحيحاً إذا كان اسم المستخدم وكلمة المرور غير فارغين فقط
    return bool(username.strip() and password.strip())

# زر "تسليم حسابات"
@app.on_callback_query(filters.regex("^deliver_accounts$"))
async def deliver_accounts(app, query):
    user_id = query.from_user.id
    # قم بطلب معلومات حساب انستاقرام من المستخدم (اليوزر:الباسورد)
    await app.send_message(user_id, "أدخل معلومات حساب انستاقرام (اليوزر:الباسورد)")

    # بعد التحقق من تنسيق المعلومات (اليوزر:الباسورد)
    @app.on_message(filters.private & filters.text)
    async def check_account_info(app, message):
        if "/ANSTA" in message.text:
            # قم بفصل اليوزر والباسورد عند استخدام الفاصلة ":"
            username, password = message.text.split(":", 1)

            # هنا يمكنك تنفيذ الخطوات للتحقق من صحة معلومات الحساب
            if username and password:
                # يعتبر الحساب صحيحاً إذا كان اسم المستخدم وكلمة المرور غير فارغين فقط
                if verify_account(username, password):
                    # إذا تم التحقق وجدت أن المعلومات صحيحة، يمكنك إضافة الحساب إلى قاعدة البيانات وطباعة "تم تسجيل"
                    db.set(username, {"username": username, "password": password})
                    await message.reply_text("تم تسجيل الحساب بنجاح!")
                else:
                    # إذا كان الحساب غير صحيح، قم بطباعة رسالة خطأ
                    await message.reply_text("خطأ في معلومات الحساب. الرجاء التحقق وإعادة المحاولة.")
            else:
                # إذا لم يكن الحساب يحتوي على اسم مستخدم أو كلمة مرور، قم بطباعة "خطأ"
                await message.reply_text("خطأ في معلومات الحساب. الرجاء التحقق وإعادة المحاولة.")

    # زر "رشق اعضاء"
    @app.on_callback_query(filters.regex("^member_boost$"))
    async def member_boost(app, query):
        user_id = query.from_user.id
        # قم بطلب يوزر الحساب المراد رشقه من المستخدم
        await app.send_message(user_id, "أدخل يوزر الحساب المراد رشقه:")

    # بعد الحصول على يوزر الحساب المراد رشقه
    @app.on_message(filters.private & filters.text)
    async def check_member_account(app, message):
        user_id = message.from_user.id
        username = message.text
# بعد الحصول على يوزر الحساب المراد رشقه
    @app.on_message(filters.private & filters.text)
    async def check_member_account(app, message):
        user_id = message.from_user.id
        username = message.text

    # هنا يمكنك تنفيذ الخطوات للبحث عن الحساب في انستقرام
    L = instaloader.Instaloader()
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        # قم بطباعة صورة الحساب للتحقق من المستخدم
        await app.send_photo(user_id, profile.profile_pic_url,
                             caption=f"هل هذا هو الحساب الصحيح؟\n\nيوزر الحساب: {profile.username}\nاسم المستخدم: {profile.full_name}\nمتابعين: {profile.followers}")
        # قم بإرسال زر "نعم" و"لا" للتأكيد
        buttons = [
            [btn("نعم", callback_data="confirm_account")],
            [btn("لا", callback_data="cancel_account")]
        ]
        markup = mk(buttons)
        await app.send_message(user_id, "الرجاء التأكيد على صحة الحساب:", reply_markup=markup)
    except
        # قم بإرسال زر "نعم" و"لا" للتأكيد
        buttons = [
            [btn("نعم", callback_data="confirm_account")],
            [btn("لا", callback_data="cancel_account")]
        ]
        markup = mk(buttons)
        await app.send_message(user_id, "الرجاء التأكيد على صحة الحساب:", reply_markup=markup)
    except instaloader.exceptions.ProfileNotExistsException:
        # في حالة عدم وجود الحساب، قم بطباعة رسالة بأن الحساب غير موجود
        await app.send_message(user_id, "الحساب غير موجود، يُرجى التحقق من اسم المستخدم وإعادة المحاولة.")

# بعد الحصول على تأكيد من المستخدم (نعم/لا)
@app.on_callback_query(filters.regex("^confirm_account$") | filters.regex("^cancel_account$"))
async def confirm_account(app, query):
    user_id = query.from_user.id
    # قم بالتحقق من الزر الذي اختاره المستخدم
    if query.data == "confirm_account":
        # إذا اختار "نعم"، يمكنك طلب عدد المراد رشقه
        await app.send_message(user_id, "أدخل عدد المراد رشقه:")
    else:
        # إذا اختار "لا"، يمكنك إرسال رسالة بالتأكيد أو إلغاء العملية
        await app.send_message(user_id, "تم إلغاء عملية الرشق.")

# بعد التحقق من العدد المطلوب للرشق
@app.on_message(filters.private & filters.text)
async def boost_accounts(app, message):
    user_id = message.from_user.id
    boost_amount = int(message.text)

    # التحقق من أن العدد المطلوب أقل من عدد الحسابات الموجودة في قاعدة البيانات
    accounts = db.keys()
    if boost_amount <= len(accounts):
        # قم بتنفيذ رشق الحسابات هنا (يمكن استخدام حلقة تكرار للرشق حسب العدد المطلوب)
        for i in range(boost_amount):
            username = accounts[i]
            password = db.get(username)["password"]

            # قم بتسجيل الدخول باستخدام حساب البوت الحالي
            bot.login(username=username, password=password)

            # قم بالتفاعل مع الحسابات هنا (استخدم الدوال follow_user و like_user و comment_user)
            user_id_to_interact = "user_id_to_interact"  # يجب استبداله بمعرّف المستخدم الفعلي الذي ترغب في التفاعل معه
            bot.follow_user(user_id_to_interact)

            media_id_to_like = "media_id_to_like"  # يجب استبداله بمعرّف الوسائط الخاص بالمنشور الذي ترغب في الإعجاب به
            bot.like_user(media_id_to_like)

            media_id_to_comment = "media_id_to_comment"  # يجب استبداله بمعرّف الوسائط الخاص بالمنشور الذي ترغب في التعليق عليه
            comment_text = "أحلى صورة!"  # يمكنك استبداله بنص التعليق الذي ترغب في كتابته
            bot.comment_user(media_id_to_comment, comment_text)

            # انتظر لبعض الوقت بين كل تفاعل لتجنب حظر الحساب
            time.sleep(10)  # يمكنك ضبط الفاصل الزمني حسب الحاجة (بالثواني)

        # بعد الانتهاء، يمكنك حذف الحسابات التي تم رشقها من قاعدة البيانات
        for i in range(boost_amount):
            username = accounts[i]
            db.remove(username)

        # تنفيذ الخصم من المستخدم هنا (على سبيل المثال، كل 10 حسابات تساوي 100 نقطة خصم)
        discount = boost_amount // 10 * 100
        # قم بتحديث نقاط المستخدم في قاعدة البيانات بعد تنفيذ الخصم
        # ...

        await app.send_message(user_id, f"تم رشق الحسابات بنجاح! تم خصم {discount} نقطة من رصيدك.")
    else:
        # إذا كان العدد أكبر من عدد الحسابات الموجودة، قم بطباعة رسالة بأن العدد غير صحيح
        await app.send_message(user_id, "العدد المطلوب للرشق أكبر من عدد الحسابات الموجودة.")
