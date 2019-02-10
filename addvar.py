import requests, random, subprocess, time
from telegram.ext import Updater, CommandHandler, Filters
import telegram

import logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

lines = [line.rstrip('\n') for line in open('settings')]
my_chat_id = int(lines[0])
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

# ------------------------------------------------------------------------------

# Starting
def start(bot, update):
    this_chat_id = update.message.chat_id
    if this_chat_id == my_chat_id:
        custom_keyboard = [['/general'],['/webserver'],['/minecraft']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(this_chat_id, text=random.choice(quotes), reply_markup=reply_markup)
    else:
        xkcd(bot, update)
        custom_keyboard = [['/start', '/hello', '/xkcd']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(this_chat_id, text=random.choice(quotes), reply_markup=reply_markup)
def xkcd(a,b):
    b.message.reply_text('{}'.format(b.message.from_user.first_name)+' is not in the sudoers file. This incident will be reported.')
    time.sleep(0.5)
    a.send_photo(chat_id=b.message.chat_id, photo=open('xkcd.jpg', 'rb'))
def hello(bot, update):
    update.message.reply_text(random.choice(hellos)+' {}! '.format(update.message.from_user.first_name)+random.choice(quotes))
def general(bot, update):
    custom_keyboard = [['/start'],['/shutdown_server', '/restart_server', '/list_processes']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(update.message.chat_id, text="Welcome to general", reply_markup=reply_markup)
def webserver(bot, update):
    custom_keyboard = [['/start', '/elisif'],['/a_stop','/a_restart','/a_status'],['/g_stop','/g_start','/g_single']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(update.message.chat_id, text="Welcome to Webserver", reply_markup=reply_markup)
def minecraft(bot, update):
    custom_keyboard = [['/start'],['/ftb_start', '/vanilla_start'], ['/java_status', '/list_joined_history', '/list_online']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(update.message.chat_id, text="Welcome to Minecraft", reply_markup=reply_markup)

# General
def list_processes(bot, update):
    try:
        ps_return_text = str(subprocess.check_output(['./scripts/list_processes.sh'])).replace('\\n','\n\n')[2:]
        ps_return_list = ps_return_text.split('\n\n')[:7]
        ps_return_text = '\n\n'.join(ps_return_list)
        update.message.reply_text(ps_return_text)
    except Exception as e:
        update.message.reply_text('Returned Error:\n\n'+str(e))
def restart_server(bot, update):
    try:
        return_text = str(subprocess.Popen(['./scripts/restart_server.sh']))
        update.message.reply_text(return_text)
    except Exception as e:
        update.message.reply_text('Returned Error:\n\n'+str(e))
def shutdown_server(bot, update):
    try:
        return_text = str(subprocess.Popen(['./scripts/shutdown_server.sh']))
        update.message.reply_text(return_text)
    except Exception as e:
        update.message.reply_text('Returned Error:\n\n'+str(e))

# Webserver
def a_status(bot, update):
    try:
        return_text = str(subprocess.check_output(['./scripts/a_status.sh']))
        update.message.reply_text(return_text)
    except Exception as e:
        update.message.reply_text('Returned Error:\n\n'+str(e))
def a_restart(bot, update):
    try:
        return_text = str(subprocess.check_output(['./scripts/a_restart.sh']))
        update.message.reply_text(return_text)
    except Exception as e:
        update.message.reply_text('Returned Error:\n\n'+str(e))
def a_stop(bot, update):
    try:
        return_text = str(subprocess.check_output(['./scripts/a_stop.sh']))
        update.message.reply_text(return_text)
    except Exception as e:
        update.message.reply_text('Returned Error:\n\n'+str(e))
def g_start(bot, update):
    try:
        return_text = str(subprocess.Popen(['./scripts/g_start.sh']))
        update.message.reply_text(return_text)
    except Exception as e:
        update.message.reply_text('Returned Error:\n\n'+str(e))
def g_stop(bot, update):
    try:
        return_text = str(subprocess.check_output(['./scripts/g_stop.sh']))
        update.message.reply_text(return_text)
    except Exception as e:
        update.message.reply_text('Returned Error (goaccess not running?):\n\n'+str(e))
def g_single(bot, update):
    try:
        return_text = str(subprocess.check_output(['./scripts/g_single.sh']))
        update.message.reply_text(return_text)
    except Exception as e:
        update.message.reply_text('Returned Error:\n\n'+str(e))
def elisif(bot,update):
    try:
        update.message.reply_text(str(requests.get('https://odrljin.xyz', headers={'User-Agent':'Addvar'}).status_code))
    except Exception as e:
        update.message.reply_text("An error occured" + str(e))

# Minecraft
def ftb_start(bot, update):
    try:
        return_text = str(subprocess.Popen(['./scripts/ftb_start.sh']))
        update.message.reply_text(return_text)
    except Exception as e:
        update.message.reply_text('Returned Error:\n\n'+str(e))
def vanilla_start(bot, update):
    try:
        return_text = str(subprocess.Popen(['./scripts/vanilla_start.sh']))
        update.message.reply_text(return_text)
    except Exception as e:
        update.message.reply_text('Returned Error:\n\n'+str(e))
def java_status(bot, update):
    try:
        return_text = str(subprocess.check_output(['./scripts/java_status.sh']))[2:][:-1].replace('\\n','\n\n')
        update.message.reply_text(return_text)
    except Exception as e:
        update.message.reply_text('Returned Error:\n\n'+str(e))
def list_joined_history(bot, update):
    try:
        return_text = str(subprocess.check_output(['./scripts/list_joined_history.sh'])).replace('\\n','\n\n')[2:]
        return_list = return_text.split('\n\n')[-16:]
        return_text = '\n\n'.join(return_list)[:-1]
        update.message.reply_text(return_text)
    except Exception as e:
        update.message.reply_text('Returned Error:\n\n'+str(e))
def list_online(bot, update):
    try:
        return_text = str(subprocess.check_output(['./scripts/list_online.sh']))
        update.message.reply_text(return_text)
    except Exception as e:
        update.message.reply_text('Returned Error:\n\n'+str(e))

# ------------------------------------------------------------------------------

updater = Updater(my_token)

def auth_command(a,b):
    updater.dispatcher.add_handler(CommandHandler(a, b, filters=Filters.user(username='@professionalgopnik')))

# Start
# public
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('xkcd', xkcd))
# private
auth_command('general', general)
auth_command('webserver', webserver)
auth_command('minecraft', minecraft)

# General
auth_command('list_processes', list_processes)
auth_command('shutdown_server', shutdown_server)
auth_command('restart_server', restart_server)

# Webserver
auth_command('elisif', elisif)
auth_command('a_status', a_status)
auth_command('a_restart', a_restart)
auth_command('a_stop', a_stop)
auth_command('g_single', g_single)
auth_command('g_start', g_start)
auth_command('g_stop', g_stop)

# Minecraft
auth_command('ftb_start', ftb_start)
auth_command('vanilla_start', vanilla_start)
auth_command('java_status', java_status)
auth_command('list_joined_history', list_joined_history)
auth_command('list_online', list_online)

updater.start_polling()
updater.idle()
