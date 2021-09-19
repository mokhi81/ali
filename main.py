#from telethon import TelegramClient, events, sync
#with TelegramClient('session_name', api_id, api_hash) as client:
    #messages = client.get_messages('Telegram')
    #print(messages[0].text)
from telegram.ext import *
from telegram.ext.filters import *
from telegram.chataction import *
from  telegram import *
from telethon.sync import TelegramClient, events
import requests
import asyncio
import threading
message={
    'msg_start':"""
کاربر گرامی به ربات فروش شماره مجازی  خیلی خوش آمدید❤️

✅ به راحتی شماره مجازی بخرید                          

✅ با سرعت بالا و کاملا اتوماتیک                         

✅ با کمترین قیمت ممکن                                 
@Buy_virtual_numbers_bot
"""   ,
   'msg_posht':"""
    🗣جهت پشتیبانی با ایدی زیر در ارتباط باشید 👇
   
    
    @mokhi81
""",
    'msg_kharid':"""
    
☎️شماره☎️                                                                


{}


📲را جهت ورود به تلگرام وارد کرده و درخواست ارسال کد بکنید📲                                     
"""
}
list_number=[

]
api_id = 7567126

api_hash = 'a8e696d1e5424100d12a4650f9b39e13'
FIRST=0
def get(fi):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    with TelegramClient(fi, api_id, api_hash,loop=loop) as client:
        for dialog in client.iter_dialogs():
            if str(dialog.title) == 'Telegram':
                di=dialog.message.message
                break
    return di
def start(update:Update ,context:CallbackContext) :
    chat_id=update.message.chat_id
    context.bot.send_chat_action(chat_id,ChatAction.TYPING)
    update.message.reply_text(message["msg_start"])
    handel(update,context)
def handel(update:Update , context:CallbackContext):
    buttons=[
        ["📲 خرید شماره مجازی"]         ,
        ["💸 افزایش سکه" , "👤 اطلاعات حساب"]      ,
        ["🗣 پشتیبانی"]
    ]
    update.message.reply_text(
        text="👇از دکمه های زیر استفاده کنید👇",
        reply_markup=ReplyKeyboardMarkup(buttons,resize_keyboard=True,one_time_keyboard=True)
    )
def poshtibani(update:Update , context:CallbackContext) :
       update.message.reply_text(message['msg_posht'])


def afzaeshseke(update:Update , context:CallbackContext) :
    buttons=[
        ["🗣 دعوت دیگران","💵 خرید سکه"]   ,
        ["↪️ بازگشت"]
    ]
    update.message.reply_text("👇یکی از روش های زیر را انتخاب نمایید👇",
                             reply_markup=ReplyKeyboardMarkup(buttons,resize_keyboard=True,one_time_keyboard=True)
                              )
def bazghat(update:Update ,context:CallbackContext) :
    handel(update,context)


def kharid(update:Update ,context:CallbackContext) :
    button=[
        [InlineKeyboardButton("✅دریافت کد ✅",callback_data=list_number[0][0]+' '+list_number[0][1]),
        InlineKeyboardButton("🔥وارد حساب شدم🔥",callback_data='ok')]

    ]
    update.message.reply_text(text=message['msg_kharid'].format(list_number[0][0]) ,
                             reply_markup=InlineKeyboardMarkup(button)
                              )
    return 0

def daryaft(update:Update ,context:CallbackContext) :
    query=update.callback_query
    chat_id=query.message.chat_id
    msg_id=query.message.message_id
    di=0
    fi=query.data.split()[1]
    button = [
        [InlineKeyboardButton("✅دریافت کد ✅", callback_data=query.data),
        InlineKeyboardButton("🔥وارد حساب شدم🔥", callback_data='ok')]
    ]
    di=get(fi)
    context.bot.editMessageText(text=di,
                                chat_id=chat_id, message_id=msg_id,
                                reply_markup=InlineKeyboardMarkup(button))
    return 1
def payan(update:Update ,context:CallbackContext) :
    query = update.callback_query
    chat_id = query.message.chat_id
    msg_id = query.message.message_id
    list_number.pop(0)
    context.bot.editMessageText(text='خرید با موفقیت انجام شد',
                                chat_id=chat_id, message_id=msg_id,
                               )
    return ConversationHandler.END

def main():
    updater = Updater("2014695657:AAEN_QcoNY-WqUw1XSeQReEF1fuOrFy4MWY", use_context=True)
    conversation_handler=ConversationHandler(
        entry_points=[MessageHandler(Filters.regex("📲 خرید شماره مجازی"),kharid)],
        states={
            0:[CallbackQueryHandler(daryaft,pattern='^\+.+'),CallbackQueryHandler(payan,pattern='^ok$')],
            1:[CallbackQueryHandler(payan,pattern='^ok$'),CallbackQueryHandler(daryaft,pattern='^\+.+')]
            }
        ,
     fallbacks=[MessageHandler(Filters.regex("📲 خرید شماره مجازی"),kharid)],
                allow_reentry = True

    )
    updater.dispatcher.add_handler(conversation_handler)
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex("🗣 پشتیبانی"),poshtibani))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex("💸 افزایش سکه"),afzaeshseke))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex("↪️ بازگشت"),bazghat))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex("📲 خرید شماره مجازی"),kharid))
    updater.start_polling()
    updater.idle()
main()