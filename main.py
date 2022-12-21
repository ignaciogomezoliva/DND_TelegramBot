import logging
from random import randint 

from data import token

from telegram import *
from telegram.ext import * 

from telegraph import Telegraph

telegraph = Telegraph()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

#Estados para la creación de personaje
TYPE, NAME, RACE, CLASS, HISTORY = range(5)

#Constantes que me da pereza estar repitiendo
DungeonMaster = "Dungeon Master"
Player = "Jugador"
Obs = "Observador"

#Estructuras de datos
characterList = []
observers = []
playerIndex = 0
DM = None

#Función auxiliar de búsqueda
def findCharacterIndex(first_name):
    for i in range(len(characterList)):
        if characterList[i].playerName == first_name:
            return i
    return -1

def start(update, context) -> int:
    buttons =  [KeyboardButton(DungeonMaster)], [KeyboardButton(Player)], [KeyboardButton(Obs)]
    context.bot.send_message(chat_id=update.effective_chat.id, 
                                text="¡Hola! Soy Calcifer, y voy a ser vuestro secretario el día de hoy. \n \n _Para lo que hemos quedado los demonios de fuego..._ ", 
                                parse_mode= "Markdown", 
                                reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True))
    return TYPE

def type(update, context):
    
    if DungeonMaster in update.message.text:
        global DM
        if DM == None:
            DM = update.message.from_user.first_name
            context.bot.send_message(chat_id=update.effective_chat.id, 
                                        text=DM + " será el Dungeon Master de esta campaña.")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, 
                                        text="¡Espera¡ Ya tenemos un Dungeon Master. \n --> " + DM + " es el Dungeon Master.")
        return ConversationHandler.END

    elif Player in update.message.text:
        global playerIndex
        if findCharacterIndex(update.message.from_user.first_name) != -1:
            context.bot.send_message(chat_id=update.effective_chat.id, 
                                        text="@" + update.message.from_user.first_name + " ya ha creado un personaje.")
            return ConversationHandler.END
        
        else: 
            context.bot.send_message(chat_id=update.effective_chat.id, 
                                            text="Si vas a ser un jugador... necesitarás un personaje. Primero lo primero, ¿cómo quieres llamar a tu avatar?")
            return NAME
    
    else:
        user =  update.message.from_user.id
        observers.append(user)
        #Retira el acceso para que no pueda interferir
        new = {'can_send_messages': False, 'can_send_media_messages': False,'can_send_polls': False,'can_send_other_messages': False, 'can_add_web_page_previews': False,}
        permissions = {'can_send_messages': None, 'can_send_media_messages': None, 'can_send_polls': None, 'can_send_other_messages': None, 'can_add_web_page_previews': None, 'can_change_info': None, 'can_invite_users': None, 'can_pin_messages': None}
        current = eval(str(context.bot.getChat(update.effective_chat.id).permissions))
        permissions.update(current)
        permissions.update(new)
        new_permissions = ChatPermissions(**permissions)
        context.bot.restrict_chat_member(update.effective_chat.id, user, permissions=new_permissions)            


def main():
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        fallbacks=[],

        states={
            TYPE: [MessageHandler(Filters.text, type)]
        },
    )

    # log all errors
    dispatcher.add_error_handler(error)

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
