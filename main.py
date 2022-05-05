import sys
from collections import defaultdict, deque

from telegram.ext import Updater, CommandHandler, MessageHandler

from constants import TRIGGERS

TOKEN = ''



DEFAULT_SETTINGS = {
    'autoninja': True
}


def get_default_settings():
    return DEFAULT_SETTINGS


def chat_queue():
    return deque(50*[None], maxlen=50)


messages = defaultdict(chat_queue)
settings = defaultdict(get_default_settings)


CHAT_ID_PODEMOS_HABLAR = -213095736


def hello(bot, update):
    update.message.reply_text(
        'Hola {} ...querés ninja'.format(update.message.from_user.first_name))


def autoninja(bot, update):
    chat_id = update.message.chat.id
    option = update.message.text.split(' ')
    chat_setting = settings[chat_id]

    if len(option) == 1:
        autoninja_status = chat_setting['autoninja']
        print('Toggling autoninja')
        autoninja_new_status = not autoninja_status
    else:
        autoninja_new_status = False if option[1] == 'off' else True

    chat_setting['autoninja'] = autoninja_new_status
    update.message.reply_text(
        'Modo autoninja {}'.format('on' if autoninja_new_status else 'off'))


def ninjasettings(bot, update):
    chat_id = update.message.chat.id
    option = update.message.text.split(' ')
    chat_setting = settings[chat_id]
    autoninja_status = chat_setting['autoninja']

    update.message.reply_text(
        'Settings: Modo autoninja {}'.format('on' if autoninja_status else 'off'))


def ninja(bot, update):
    try:
        chat_id = update.message.chat.id
        message_queue = messages[chat_id]
        message = message_queue[0]
    except:
        print('Error')

    if message:
        message.reply_text(
        '{}...{}...claramente..necesita xxx...'.format(message.text,
                                                    message.from_user.first_name))
    else:
        update.message.reply_text(
        '{}...dale que quien quiere xxxx sos vos'.format(update.message.from_user.first_name))


def _sanitize_message(content):
    content = content.lower()
    content = content.replace(',', ' ')
    content = content.replace(',', ' ')
    content = content.replace('.', ' ')
    content = content.replace(';', ' ')
    content = content.replace('#', ' ')

    return ' '.join(content.split())

def _get_ninjable_content(message_content):
    message_content_sanitized = _sanitize_message(message_content).split(' ')

    ninjable_content = list(filter(message_content_sanitized.__contains__,
                                        TRIGGERS.keys()))

    return ninjable_content[0] if ninjable_content else None

def process_message(bot, update):
    chat_id = update.message.chat.id
    chat_setting = settings[chat_id]

    print('Processsing %s on %s' % (update.message.text, str(chat_id)) )
    message_content = update.message.text
    if message_content[0] != ['/']:
        message_queue = messages[chat_id]
        # Do not put messages here that are commands for other bots
        message_queue.appendleft(update.message)

        ninjable_content = _get_ninjable_content(message_content)

        if chat_setting['autoninja'] and ninjable_content:
            reply_message_content = TRIGGERS[ninjable_content]
            update.message.reply_text(
            '{} {}'.format(reply_message_content, update.message.from_user.first_name))


if __name__=='__main__':
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler('helloninja', hello))
    updater.dispatcher.add_handler(CommandHandler('ninja', ninja))
    updater.dispatcher.add_handler(CommandHandler('autoninja', autoninja))
    updater.dispatcher.add_handler(CommandHandler('ninjasettings', ninjasettings))
    updater.dispatcher.add_handler(MessageHandler(None,callback=process_message))

    updater.start_polling()
    updater.idle()
