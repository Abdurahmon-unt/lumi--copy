import telebot
from telebot import types

TOKEN = '8194057676:AAFUHQRBqmgoOjTyA7nJZSQJIPnHClwAQP0'
bot = telebot.TeleBot(TOKEN)

orders = {}

adminID = 8100727942

bot.set_my_commands(
    commands= [
        telebot.types.BotCommand('/start','Botni ishga tushrin va xizmatlarmizdan birni talang'),
        telebot.types.BotCommand('/help','Uzur bot ishlmapati yoki boshidan /startni bosib koring')
    ]
)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id

    if user_id == adminID:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("📋 Buyurtmalar"))
        bot.send_message(user_id, "👑 Admin paneliga xush kelibsiz", reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(
            types.KeyboardButton("🛒 Buyurtma berish"),
            types.KeyboardButton("💰 Narxlar"),
            types.KeyboardButton("📋 Xizmatlar")
        )
        bot.send_message(user_id, "Quyidagilardan birini tanlang:", reply_markup=markup)




@bot.message_handler(func=lambda msg: msg.text == "🛒 Buyurtma berish")
def show_services_buttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("Reklama post📝"),
        types.KeyboardButton("Kanal uchun bio📃"),
        types.KeyboardButton("Logo🎐"),
        types.KeyboardButton("Stiker💕"),
        types.KeyboardButton("Premium emoji⭐️"),
        types.KeyboardButton('Telegram bot🤖')
    )
    markup.add(types.KeyboardButton("🏠 Bosh menuga qaytish"))
    bot.send_message(message.chat.id, "Xizmat turlaridan birini tanlang:", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == "🏠 Bosh menuga qaytish")
def return_to_main_menu(message):
    send_welcome(message)

# 💰 Narxlar
@bot.message_handler(func=lambda msg: msg.text == "💰 Narxlar")
def price_list(message):
    text = (
        "💰 Xizmat narxlari:\n\n"
        "• Logo – 10 000 so'm\n"
        "• Bio – 15 000 so'm\n"
        "• Reklama post – 40 000 so'm\n"
        "• Stiker – 15 000 so'm\n"
        "• Premium emoji – 20 000 so'm\n"
        "• Telegram bot – 35 000  so'm"
    )
    bot.send_message(message.chat.id, text)

# 📋 Xizmatlar
@bot.message_handler(func=lambda msg: msg.text == "📋 Xizmatlar")
def services_list(message):
    text = (
        "📋 Bizda mavjud xizmatlar:\n\n"
        "✅ Logo dizayn\n"
        "✅ Kanal  bio yozish\n"
        "✅ Sticker to‘plamlar\n"
        "✅ Premium emoji yaratish\n"
        "✅ Reklama postlar\n"
        "✅ Telegrambot\n"
        "Hammasi sizning talabingizga mos tayyorlanadi!"
    )
    bot.send_message(message.chat.id, text)





@bot.message_handler(func=lambda msg: msg.text in [
    "Reklama post📝", "Kanal uchun bio📃",
    "Logo🎐", "Stiker💕", "Premium emoji⭐️", "Telegram bot🤖"
])
def ask_service_details(message):
    service = message.text
    user_id = message.from_user.id

    
    orders[user_id] = {'item': service}

    bot.send_message(user_id, f"{service} uchun nima qilishimiz kerak? Iltimos, tafsilotlarni yozing.")
    bot.register_next_step_handler(message, receive_description)

def receive_description(message):
    user_id = message.from_user.id
    service = orders[user_id]['item']
    name = message.from_user.first_name

    if message.content_type == 'photo':
        orders[user_id]['description'] = "rasm"
        file_id = message.photo[-1].file_id

        
        bot.send_photo(adminID, file_id, caption=f"🆕 Buyurtma: {service}\n👤 @{message.from_user.username or name}\nID: {user_id}")
        bot.send_message(user_id, "✅ Buyurtmangiz qabul qilindi. Kun davomida tayyor bo‘ladi.")
        bot.send_message(user_id, "💳 To‘lov uchun karta: 8600 1234 5678 9012\n"
                                 "To'lov qilib adminga chek tashlang!!\n"
                                  "👤 Admin: @murodovch_a")

    elif message.content_type == 'text':
        description = message.text
        orders[user_id]['description'] = description

        admin_msg = (
            f"🆕 Buyurtma!\n"
            f"👤 {name} (ID: {user_id})\n"
            f"📦 Xizmat: {service}\n"
            f"📋 Tafsilot: {description}\n\n"
            f"✍️ Yuborish uchun:\n"
            f"#logo {user_id} — rasm yuboring\n"
            f"#text {user_id} — matn yuboring"
        )
        bot.send_message(adminID, admin_msg)
        bot.send_message(user_id, "✅ Buyurtmangiz qabul qilindi. Kun davomida tayyor bo‘ladi.")
        bot.send_message(user_id, "💳 To‘lov uchun karta: 8600 1234 5678 9012\n"
                                 "To'lov qilib bolib adminga chek tashlang!!\n"
                                "👤 Admin: @lumi_writes")

@bot.message_handler(content_types=['photo', 'text'])
def handle_admin_delivery(message):
    if message.from_user.id != adminID:
        return

    if message.caption and message.caption.startswith("#logo"):
        try:
            parts = message.caption.split()
            user_id = int(parts[1])
            bot.send_photo(user_id, message.photo[-1].file_id, caption="✅ Logoningiz tayyor!")
            bot.send_message(message.chat.id, f"✅ Logoni foydalanuvchiga yubordim (ID: {user_id})")
        except:
            bot.send_message(message.chat.id, "❌ Xatolik: foydalanuvchi ID topilmadi yoki noto‘g‘ri format.")
    
    elif message.text and message.text.startswith("#text"):
        try:
            parts = message.text.split(maxsplit=2)
            user_id = int(parts[1])
            response = parts[2] if len(parts) > 2 else "✅ Tayyor!"
            bot.send_message(user_id, f"✅ Sizning xizmatingiz tayyor:\n{response}")
            bot.send_message(message.chat.id, f"✅ Matn foydalanuvchiga yuborildi (ID: {user_id})")
        except:
            bot.send_message(message.chat.id, "❌ Format: #text <id> <matn>")

   
bot.infinity_polling()
