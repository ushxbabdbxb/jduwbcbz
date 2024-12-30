import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import time
import threading

API_TOKEN = '7874406154:AAHJauA_ZZyh540l7zUpod55Mz8PgI34-Dg'
bot = telebot.TeleBot(API_TOKEN)

allowed_users = [5821900257]
user_data = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.from_user.id not in allowed_users:
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(InlineKeyboardButton("المطور", url="https://t.me/ub_II"))
        bot.send_message(message.chat.id, "انتَ غير مشترك في البوت راسل المطور يفعلك", reply_markup=markup)
    else:
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(InlineKeyboardButton("بدء الإرسال", callback_data="start_sending"))
        markup.add(InlineKeyboardButton("عرض الحسابات", callback_data="show_accounts"),
                   InlineKeyboardButton("تعيين حساب", callback_data="set_account"))
        markup.add(InlineKeyboardButton("تعيين كليشة", callback_data="set_template"),
                   InlineKeyboardButton("تعيين موضوع", callback_data="set_subject"))
        markup.add(InlineKeyboardButton("تعيين عدد إرسال", callback_data="set_message_count"),
                   InlineKeyboardButton("تعيين صورة رفع", callback_data="set_image"))
        markup.add(InlineKeyboardButton("تعيين سليب", callback_data="set_sleeb"),
                   InlineKeyboardButton("تعيين ايميلات", callback_data="set_emails"))
        markup.add(InlineKeyboardButton("عرض معلوماتك", callback_data="show_info"),
                   InlineKeyboardButton("مسح معلوماتك", callback_data="delete_info"))
        markup.add(InlineKeyboardButton("مسح صورة الرفع", callback_data="delete_image"))
        
        bot.send_message(message.chat.id, "مرحبآ بك في بوت رفع الـ خارجي (صلخ بل نعال)", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "set_account")
def set_account(call):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("", callback_data="back"))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="قم ب إرسال حسابك بهذا الشكل email:pass", reply_markup=markup)
    bot.register_next_step_handler(call.message, save_account)

def save_account(message):
    if ':' in message.text:
        email, password = message.text.split(':', 1)
        user_data[message.from_user.id] = user_data.get(message.from_user.id, {})
        if 'accounts' not in user_data[message.from_user.id]:
            user_data[message.from_user.id]['accounts'] = []
        user_data[message.from_user.id]['accounts'].append({'email': email, 'password': password})
        bot.send_message(message.chat.id, "تم تعيين حسابك بنجاح.")
    else:
        bot.send_message(message.chat.id, "الرجاء إرسال الحساب بالشكل الصحيح email:pass")
        set_account(message)
@bot.callback_query_handler(func=lambda call: call.data == "show_accounts")
def show_accounts(call):
    user_accounts = user_data.get(call.from_user.id, {}).get('accounts', [])
    if not user_accounts:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="لم تقم بإضافة أي حسابات بعد.")
    else:
        markup = InlineKeyboardMarkup(row_width=2)
        for email, password in user_accounts:
            markup.add(InlineKeyboardButton(email, callback_data=f"account_{email}"),
                       InlineKeyboardButton("حذف", callback_data=f"delete_{email}"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="الحسابات المسجلة:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("delete_"))
def delete_account(call):
    email_to_delete = call.data.split("delete_")[1]
    user_accounts = user_data.get(call.from_user.id, {}).get('accounts', [])
    user_accounts = [account for account in user_accounts if account[0] != email_to_delete]
    user_data[call.from_user.id]['accounts'] = user_accounts
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f"تم مسح الحساب: {email_to_delete}")

@bot.callback_query_handler(func=lambda call: call.data == "set_subject")
def set_subject(call):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("", callback_data="back"))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="قم ب إرسال الموضوع الخاص بكليشتك", reply_markup=markup)
    bot.register_next_step_handler(call.message, save_subject)

def save_subject(message):
    user_data[message.from_user.id] = user_data.get(message.from_user.id, {})
    user_data[message.from_user.id]['subject'] = message.text
    bot.send_message(message.chat.id, "تم تعيين الموضوع بنجاح.")

@bot.callback_query_handler(func=lambda call: call.data == "set_template")
def set_template(call):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("", callback_data="back"))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="قم ب إرسال الكليشة الخاصة بك", reply_markup=markup)
    bot.register_next_step_handler(call.message, save_template)

def save_template(message):
    user_data[message.from_user.id] = user_data.get(message.from_user.id, {})
    user_data[message.from_user.id]['template'] = message.text
    bot.send_message(message.chat.id, "تم تعيين الكليشة بنجاح.")

@bot.callback_query_handler(func=lambda call: call.data == "set_message_count")
def set_message_count(call):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("", callback_data="back"))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="قم بتعيين عدد الرسائل المراد إرسالها", reply_markup=markup)
    bot.register_next_step_handler(call.message, save_message_count)

def save_message_count(message):
    try:
        message_count = int(message.text)
        if message_count < 1:
            bot.send_message(message.chat.id, "الرجاء إدخال قيمة صحيحة إيجابية لعدد الرسائل.")
            return
        user_data[message.from_user.id] = user_data.get(message.from_user.id, {})
        user_data[message.from_user.id]['message_count'] = message_count
        bot.send_message(message.chat.id, f"تم تعيين عدد الرسائل بنجاح: {message_count}")
    except ValueError:
        bot.send_message(message.chat.id, "الرجاء إرسال عدد الرسائل بشكل صحيح (رقم صحيح).")

@bot.callback_query_handler(func=lambda call: call.data == "set_sleeb")
def set_sleeb(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="قم ب تعيين السليب (بل ثواني)")
    bot.register_next_step_handler(call.message, save_sleeb)

def save_sleeb(message):
    try:
        sleeb_seconds = int(message.text)
        if sleeb_seconds < 1:
            bot.send_message(message.chat.id, "الرجاء إدخال قيمة صحيحة إيجابية لعدد الثواني.")
            return
        user_data[message.from_user.id] = user_data.get(message.from_user.id, {})
        user_data[message.from_user.id]['sleeb'] = sleeb_seconds
        bot.send_message(message.chat.id, f"تم تعيين السليب بنجاح: {sleeb_seconds} ثانية")
    except ValueError:
        bot.send_message(message.chat.id, "الرجاء إرسال السليب بشكل صحيح (رقم صحيح).")

@bot.callback_query_handler(func=lambda call: call.data == "set_image")
def set_image(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="قم ب إرسال صورة الرفع")
    bot.register_next_step_handler(call.message, save_image)

def save_image(message):
    if message.photo:
        file_id = message.photo[-1].file_id
        user_data[message.from_user.id] = user_data.get(message.from_user.id, {})
        user_data[message.from_user.id]['image'] = file_id
        bot.send_message(message.chat.id, "تم حفظ صورة الرفع بنجاح.")
    else:
        bot.send_message(message.chat.id, "الرجاء إرسال صورة.")

@bot.callback_query_handler(func=lambda call: call.data == "delete_image")
def delete_image(call):
    user_data[call.from_user.id] = user_data.get(call.from_user.id, {})
    if 'image' in user_data[call.from_user.id]:
        del user_data[call.from_user.id]['image']
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="تم مسح صورة الرفع بنجاح.")
    else:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="لا توجد صورة محفوظة.")

@bot.callback_query_handler(func=lambda call: call.data == "set_emails")
def set_emails(call):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("عودة", callback_data="back"))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="قم ب إرسال ايميلات الشركة بهذه الطريقة: email@tele.com email2@tele.com",
                          reply_markup=markup)
    bot.register_next_step_handler(call.message, save_emails)

def save_emails(message):
    emails = message.text.split()
    valid_emails = [email for email in emails if '@' in email]
    if valid_emails:
        user_data[message.from_user.id] = user_data.get(message.from_user.id, {})
        if 'emails' not in user_data[message.from_user.id]:
            user_data[message.from_user.id]['emails'] = []
        user_data[message.from_user.id]['emails'].extend(valid_emails)
        bot.send_message(message.chat.id, "تم تعيين الايميلات بنجاح.")
    else:
        bot.send_message(message.chat.id, "الرجاء إرسال الايميلات بالشكل الصحيح (مثال: email@tele.com)")

@bot.callback_query_handler(func=lambda call: call.data == "show_info")
def show_info(call):
    user_info = user_data.get(call.from_user.id, {})
    if not user_info:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="لا توجد معلومات معينة بعد.")
    else:
        info_text = ""
        if 'emails' in user_info:
            info_text += f"ايميلات الدعم:\n{', '.join(user_info.get('emails', ['لا يوجد']))}\n\n"
        info_text += f"الموضوع: {user_info.get('subject', 'لا يوجد')}\n\n"
        info_text += f"الكليشة: {user_info.get('template', 'لا يوجد')}\n\n"
        info_text += f"عدد الرسائل: {user_info.get('message_count', 'لا يوجد')}\n\n"
        info_text += f"السليب: {user_info.get('sleeb', 'لا يوجد')} ثانية\n\n"
        info_text += f"صورة الرفع: {'موجودة' if user_info.get('image') else 'لا توجد'}"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=info_text)

@bot.callback_query_handler(func=lambda call: call.data == "delete_info")
def delete_info(call):
    user_data[call.from_user.id] = {}
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="تم مسح جميع المعلومات بنجاح.")



import threading
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



@bot.callback_query_handler(func=lambda call: call.data == "start_sending")
def start_sending(call):
    user_id = call.from_user.id
    user_info = user_data.get(user_id, {})

    if not user_info:
        bot.send_message(user_id, 'لم يتم تعيين أي معلومات بعد. الرجاء تعيين المعلومات أولاً.')
        return

    if 'emails' not in user_info or len(user_info['emails']) == 0:
        bot.send_message(user_id, 'لا يوجد حسابات مستلمة. الرجاء إضافة حساب مستلم أولاً.')
        return

    if 'accounts' not in user_info or len(user_info['accounts']) == 0:
        bot.send_message(user_id, 'لا يوجد حسابات مرسلة. الرجاء إضافة حساب مرسل أولاً.')
        return

    if 'subject' not in user_info or user_info['subject'] == '':
        bot.send_message(user_id, 'لم يتم تعيين الموضوع. الرجاء تعيين الموضوع أولاً.')
        return

    if 'template' not in user_info or user_info['template'] == '':
        bot.send_message(user_id, 'لم يتم تعيين الرسالة. الرجاء تعيين الرسالة أولاً.')
        return

    if 'sleeb' not in user_info or user_info['sleeb'] == 0:
        bot.send_message(user_id, 'لم يتم تعيين الفاصل الزمني. الرجاء تعيين الفاصل الزمني أولاً.')
        return

    if 'message_count' not in user_info or user_info['message_count'] == 0:
        bot.send_message(user_id, 'لم يتم تعيين عدد الرسائل. الرجاء تعيين عدد الرسائل أولاً.')
        return

    subject = user_info.get('subject', '')
    template = user_info.get('template', '')
    message_count = user_info.get('message_count', 0)
    sleeb = user_info.get('sleeb', 0)
    image_id = user_info.get('image', '')


    accounts = user_info['accounts']
    recipients = user_info['emails']
    recipient_chunks = [recipients[i::len(accounts)] for i in range(len(accounts))]


    message = bot.send_message(user_id, "تم بدء عملية الإرسال. سيتم تحديث هذه الرسالة بحالة الإرسال.")

    threads = []
    for i, account in enumerate(accounts):
        email = account['email']
        password = account['password']

        thread = threading.Thread(target=send_emails, args=(user_id, message.message_id, email, password, recipient_chunks[i],
                                                            subject, template, message_count, sleeb, image_id))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    bot.edit_message_text(chat_id=user_id, message_id=message.message_id, text="تم اكتمال عملية الإرسال بنجاح.")

def send_emails(user_id, message_id, sender_email, sender_password, recipients, subject, template, message_count, sleeb, image_id):
    global stop_requested

    sent_count = 0
    failed_count = 0
    blocked_emails = []

    for i in range(message_count):
        if stop_requested:
            bot.edit_message_text(chat_id=user_id, message_id=message_id, text="تم إيقاف عملية الإرسال.")
            break

        for recipient in recipients:
            if send_email(sender_email, sender_password, recipient, subject, template):
                sent_count += 1
            else:
                failed_count += 1
                blocked_emails.append(sender_email)
                break

        status_message = f"بدأ عملية الإرسال، سوف يتم الارسال بشكل عمودي ..\nتم ارسال: {sent_count}.\nفشل اثناء: {failed_count}.\nسوف تكتمل العملية قريبا!\nارسل /stop للايقاف"
        bot.edit_message_text(chat_id=user_id, message_id=message_id, text=status_message)
        time.sleep(sleeb)

        if sender_email in blocked_emails:
            bot.edit_message_text(chat_id=user_id, message_id=message_id, text=f"تم حظر الإيميل: {sender_email}")
            break

def send_email(sender_email, sender_password, recipient, subject, message):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(str(e))
        return False

stop_requested = False

@bot.message_handler(commands=['stop'])
def stop_sending(message):
    global stop_requested
    stop_requested = True
    bot.send_message(message.chat.id, "تم إيقاف عملية الإرسال.")

bot.polling()