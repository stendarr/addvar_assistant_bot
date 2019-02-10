import requests, random, subprocess, time
from telegram.ext import Updater, CommandHandler
import telegram

import logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

lines = [line.rstrip('\n') for line in open('settings')]
my_chat_id = lines[0]
my_token = lines[1]

quotes = ["I've got some salmon to sell.",
          "The finest fish, here! Caught daily!",
          "You shouldn't leave Solitude without trying our fish. Best in Skyrim.",
          "Plenty of fresh fish for ya.",
          "Fresh fish! Fresh fish!",
          "Fresh fish, straight from the fjords.",
          "These are troubled times. Be on your guard out there.",
          "May the gods speed your journeys... and steady your sword arm."]
hellos = ["Hey", "Howdy", "Hello", "Salve", "Greetings", "Hi"]


def xkcd(a,b):
    this_chat_id = b.message.chat_id
    b.message.reply_text('{}'.format(b.message.from_user.first_name)+' is not in the sudoers file. This incident will be reported.')
    time.sleep(0.5)
    a.send_photo(chat_id=this_chat_id, photo=open('xkcd.jpg', 'rb'))

def hello(bot, update):
    update.message.reply_text(random.choice(hellos)+' {}! '.format(update.message.from_user.first_name)+random.choice(quotes))

def start(bot, update):
    this_chat_id = update.message.chat_id
    if this_chat_id == my_chat_id:
        custom_keyboard = [['/elisif', '/java_status', '/processes'],['/minecraft', '/meinkraft'], ['/killall_java']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(this_chat_id, text=random.choice(quotes), reply_markup=reply_markup)
    else:
        xkcd(bot, update)
        custom_keyboard = [['/start', '/hello', '/xkcd']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(this_chat_id, text=random.choice(quotes), reply_markup=reply_markup)

def elisif(bot,update):
    this_chat_id = update.message.chat_id
    if this_chat_id == my_chat_id:
        try:
            update.message.reply_text(str(requests.get('https://odrljin.xyz', headers={'User-Agent':'Addvar'}).status_code))
        except Exception as e:
            update.message.reply_text("An error occured" + str(e))
        #ps_return_text = str(subprocess.check_output(['ps','aux']))
        #update.message.reply_text(ps_return_text[:256])
    else:
        xkcd(bot,update)

def meinkraft(bot, update):
    this_chat_id = update.message.chat_id
    if this_chat_id == my_chat_id:
        ps_return_text = str(subprocess.Popen(['./meinkraft.sh']))
        update.message.reply_text(ps_return_text)
    else: xkcd(bot, update)

def minecraft(bot, update):
    this_chat_id = update.message.chat_id
    if this_chat_id == my_chat_id:
        ps_return_text = str(subprocess.Popen(['./minecraft.sh']))
        update.message.reply_text(ps_return_text)
    else: xkcd(bot, update)

def java_status(bot, update):
    this_chat_id = update.message.chat_id
    if this_chat_id == my_chat_id:
        ps_return_text = str(subprocess.check_output(['./java_status.sh']))[2:][:-1].replace('\\n','\n\n')
        update.message.reply_text(ps_return_text)
    else: xkcd(bot, update)

def killall_java(bot, update):
    this_chat_id = update.message.chat_id
    if this_chat_id == my_chat_id:
        try:
            killall_return_text = str(subprocess.check_output(['./killall_java.sh'])).replace('\\n','\n\n')
            update.message.reply_text(killall_return_text+"\n\nDone")
        except Exception as e:
            update.message.reply_text(str(e)+'\n\nReturned Error. No java running?')
    else: xkcd(bot, update)

def processes(bot, update):
    this_chat_id = update.message.chat_id
    if this_chat_id == my_chat_id:
        try:
            ps_return_text = str(subprocess.check_output(['./processes.sh'])).replace('\\n','\n\n')[2:]
            ps_return_list = ps_return_text.split('\n\n')[:11]
            ps_return_text = '\n\n'.join(ps_return_list)
            update.message.reply_text(ps_return_text+"\n\n")
        except Exception as e:
            update.message.reply_text('Returned Error:\n\n'+str(e))
    else: xkcd(bot, update)


updater = Updater(my_token)

def coli(a,b):
    updater.dispatcher.add_handler(CommandHandler(a, b))

coli('hello', hello)
coli('start', start)
coli('elisif', elisif)
coli('xkcd', xkcd)
coli('java_status', java_status)
coli('killall_java', killall_java)
coli('minecraft', minecraft)
coli('meinkraft', meinkraft)
coli('processes', processes)

updater.start_polling()
updater.idle()
