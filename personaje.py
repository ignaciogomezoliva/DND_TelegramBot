import logging
from random import randint
##from re import T
from tkinter import BUTT, Button 

from data import token

from telegram import *
from telegram.ext import * 

from telegraph import Telegraph

import time
import itertools

def get_cycle_props(cycle) :
    """Get the properties (elements, length, current state) of a cycle, without advancing it"""
    # Get the current state
    partial = []
    n = 0
    g = next(cycle)
    while ( g not in partial ) :
        partial.append(g)
        g = next(cycle)
        n += 1
    # Cycle until the "current" (now previous) state
    for i in range(n-1) :
        g = next(cycle)
    return (partial, n, partial[n-1])

def get_cycle_list(cycle) :
    """Get the elements of a cycle, without advancing it"""
    return get_cycle_props(cycle)[0]

def get_cycle_state(cycle) :
    """Get the current state of a cycle, without advancing it"""
    return get_cycle_props(cycle)[2]

def get_cycle_len(cycle) :
    """Get the length of a cycle, without advancing it"""
    return get_cycle_props(cycle)[1]

telegraph = Telegraph()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

#Estados para la creación de personaje
TYPE, WIKI_RACE, BUTTON, WIKI_CLASS, BUTTON2, NAME, RACE, CLASS, HISTORY = range(9)

#Constantes que me da pereza estar repitiendo
Go = "¡Vamos!"
Wiki = "Tengo algunas dudas..."

PJ = None

w_race = {"Enano-07-30", "Elfo-07-30", "Mediano-07-30", "Humano-07-30", "Gnomo-07-30", "Dracónido-07-30", "Semielfo-07-30", "Semiorco-07-30", "Tiefling-07-30"}
iter = itertools.cycle(w_race)

w_class = {"Bárbaro-07-30", "Bardo-07-30", "Brujo-07-30", "Clérigo-07-30", "Druida-07-30", "Explorador-07-30", "Guerrero-07-30", "Hechicero-07-30", "Mago-07-30", "Monje-07-30", "Paladín-07-30", "Pícaro-07-30"}
iter2 = itertools.cycle(w_class)

msg_editable = None


#Objeto: personaje
class Character(object):

    playerName = None
    characterName = None
    race = None
    _class = None
    dice = None
    speed = 0
    adjs_peed = 0

    inventory = {}
    
    stats = {'fuerza': 0, 'destreza': 0, "constitucion": 0, "inteligencia": 0, 'sabiduria': 0, "carisma": 0, "PG": 0}
    mod = {'fuerza': 0, 'destreza': 0, 'constitucion': 0, "inteligencia": 0, "sabiduria": 0, "carisma": 0}
    salva = {}
    
    def __init__(self, playerName, characterName):

        self.playerName = playerName
        self.characterName = characterName
        telegraph.create_account(short_name = playerName)

    def updateStats(self):

        if self.race == "Enano":
            self.speed = 25
            self.adj_speed = 25
            if self._class == "Bárbaro":
                self.stats["fuerza"] = 17
                self.stats["destreza"] = 13
                self.stats["constitucion"] = 16
                self.stats["inteligencia"] = 8
                self.stats["sabiduria"] = 12
                self.stats["carisma"] = 10
                self.stats["CA"] = 14

                self.mod["fuerza"] = 3
                self.mod["destreza"] = 1
                self.mod["constitucion"] = 3
                self.mod["inteligencia"] = -1
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 0

                self.salva = {"fuerza", "constitucion"}

            if self._class == "Bardo":
                self.stats["fuerza"] = 12
                self.stats["destreza"] = 14
                self.stats["constitucion"] = 15
                self.stats["inteligencia"] = 12
                self.stats["sabiduria"] = 8
                self.stats["carisma"] = 15
                self.stats["CA"] = 13

                self.mod["fuerza"] = 1
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = -1
                self.mod["carisma"] = 2

                self.salva = {"destreza", "carisma"}
            
            if self._class == "Brujo":
                self.stats["fuerza"] = 10
                self.stats["destreza"] = 10
                self.stats["constitucion"] = 16
                self.stats["inteligencia"] = 13
                self.stats["sabiduria"] = 12
                self.stats["carisma"] = 15
                self.stats["CA"] = 11
                
                self.mod["fuerza"] = 0
                self.mod["destreza"] = 0
                self.mod["constitucion"] = 3
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 2

                self.salva = {"sabiduria", "carisma"}

            if self._class == "Clérigo":
                self.stats["fuerza"] = 16
                self.stats["destreza"] = 8
                self.stats["constitucion"] = 13
                self.stats["inteligencia"] = 10
                self.stats["sabiduria"] = 15
                self.stats["carisma"] = 14
                self.stats["CA"] = 18
                                
                self.mod["fuerza"] = 3
                self.mod["destreza"] = -1
                self.mod["constitucion"] = 1
                self.mod["inteligencia"] = 0
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = 2

                self.salva = {"sabiduria", "carisma"}

            if self._class == "Druida":
                self.stats["fuerza"] = 15
                self.stats["destreza"] = 8
                self.stats["constitucion"] = 16
                self.stats["inteligencia"] = 10
                self.stats["sabiduria"] = 15
                self.stats["carisma"] = 12
                self.stats["CA"] = 12
                                
                self.mod["fuerza"] = 2
                self.mod["destreza"] = -1
                self.mod["constitucion"] = 3
                self.mod["inteligencia"] = 0
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = 1

                self.salva = {"sabiduria", "inteligencia"}
            
            if self._class == "Explorador":
                self.stats["fuerza"] = 15
                self.stats["destreza"] = 15
                self.stats["constitucion"] = 12
                self.stats["inteligencia"] = 12
                self.stats["sabiduria"] = 14
                self.stats["carisma"] = 8
                self.stats["CA"] = 13
                                
                self.mod["fuerza"] = 2
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 1
                self.mod["inteligencia"] = 2
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = -1

            if self._class == "Guerrero":
                self.stats["fuerza"] = 17
                self.stats["destreza"] = 13
                self.stats["constitucion"] = 16
                self.stats["inteligencia"] = 8
                self.stats["sabiduria"] = 12
                self.stats["carisma"] = 10
                self.stats["CA"] = 18
                                
                self.mod["fuerza"] = 3
                self.mod["destreza"] = 1
                self.mod["constitucion"] = 3
                self.mod["inteligencia"] = -1
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 0

                self.salva = {"fuerza", "constitucion"}

            if self._class == "Hechicero":
                self.stats["fuerza"] = 12
                self.stats["destreza"] = 13
                self.stats["constitucion"] = 16
                self.stats["inteligencia"] = 12
                self.stats["sabiduria"] = 8
                self.stats["carisma"] = 15
                self.stats["CA"] = 14
                                
                self.mod["fuerza"] = 1
                self.mod["destreza"] = 1
                self.mod["constitucion"] = 3
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = -1
                self.mod["carisma"] = 2

                self.salva = {"constitucion", "carisma"}

            if self._class == "Mago":
                self.stats["fuerza"] = 10
                self.stats["destreza"] = 14
                self.stats["constitucion"] = 15
                self.stats["inteligencia"] = 5
                self.stats["sabiduria"] = 12
                self.stats["carisma"] = 10
                self.stats["CA"] = 12
                
                self.mod["fuerza"] = 0
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 2
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 0

                self.salva = {"sabiduria", "inteligencia"}

            if self._class == "Monje":
                self.stats["fuerza"] = 15
                self.stats["destreza"] = 15
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 8
                self.stats["sabiduria"] = 14
                self.stats["carisma"] = 10
                self.stats["CA"] = 14
                
                self.mod["fuerza"] = 2
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = -1
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = 0

                self.salva = {"fuerza", "destreza"}

            if self._class == "Paladín":
                self.stats["fuerza"] = 17
                self.stats["destreza"] = 13
                self.stats["constitucion"] = 12
                self.stats["inteligencia"] = 12
                self.stats["sabiduria"] = 8
                self.stats["carisma"] = 14
                self.stats["CA"] = 18
                
                self.mod["fuerza"] = 3
                self.mod["destreza"] = 1
                self.mod["constitucion"] = 1
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = -1
                self.mod["carisma"] = 2

                self.salva = {"sabiduria", "carisma"}

            if self._class == "Pícaro":
                self.stats["fuerza"] = 14
                self.stats["destreza"] = 15
                self.stats["constitucion"] = 12
                self.stats["inteligencia"] = 14
                self.stats["sabiduria"] = 13
                self.stats["carisma"] = 8
                self.stats["CA"] = 13
                
                self.mod["fuerza"] = 2
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 1
                self.mod["inteligencia"] = 2
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = -1

                self.salva = {"destreza", "inteligencia"}

        elif self.race == "Elfo":
            self.speed = 30
            self.adj_speed = 30
            if self._class == "Bárbaro":
                self.stats["fuerza"] = 15
                self.stats["destreza"] = 15
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 9
                self.stats["sabiduria"] = 12
                self.stats["carisma"] = 10
                self.stats["CA"] = 14

                self.mod["fuerza"] = 2
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = -1
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 0

                self.salva = {"fuerza", "constitucion"}

            if self._class == "Bardo":
                self.stats["fuerza"] = 10
                self.stats["destreza"] = 16
                self.stats["constitucion"] = 13
                self.stats["inteligencia"] = 13
                self.stats["sabiduria"] = 8
                self.stats["carisma"] = 15
                self.stats["CA"] = 14

                self.mod["fuerza"] = 0
                self.mod["destreza"] = 3
                self.mod["constitucion"] = 1
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = -1
                self.mod["carisma"] = 2

                self.salva = {"destreza", "carisma"}
            
            if self._class == "Brujo":
                self.stats["fuerza"] = 8
                self.stats["destreza"] = 12
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 14
                self.stats["sabiduria"] = 12
                self.stats["carisma"] = 15
                self.stats["CA"] = 12
                
                self.mod["fuerza"] = -1
                self.mod["destreza"] = 1
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 2
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 2

                self.salva = {"sabiduria", "carisma"}

            if self._class == "Clérigo":
                self.stats["fuerza"] = 14
                self.stats["destreza"] = 10
                self.stats["constitucion"] = 13
                self.stats["inteligencia"] = 11
                self.stats["sabiduria"] = 15
                self.stats["carisma"] = 12
                self.stats["CA"] = 18
                                
                self.mod["fuerza"] = 2
                self.mod["destreza"] = 0
                self.mod["constitucion"] = 1
                self.mod["inteligencia"] = 0
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = 1

                self.salva = {"sabiduria", "carisma"}

            if self._class == "Druida":
                self.stats["fuerza"] = 13
                self.stats["destreza"] = 10
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 11
                self.stats["sabiduria"] = 15
                self.stats["carisma"] = 12
                self.stats["CA"] = 13
                                
                self.mod["fuerza"] = 1
                self.mod["destreza"] = 0
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 0
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = 1

                self.salva = {"sabiduria", "inteligencia"}
            
            if self._class == "Explorador":
                self.stats["fuerza"] = 13
                self.stats["destreza"] = 17
                self.stats["constitucion"] = 10
                self.stats["inteligencia"] = 13
                self.stats["sabiduria"] = 14
                self.stats["carisma"] = 8
                self.stats["CA"] = 14
                                
                self.mod["fuerza"] = 1
                self.mod["destreza"] = 3
                self.mod["constitucion"] = 0
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = -1

            if self._class == "Guerrero":
                self.stats["fuerza"] = 15
                self.stats["destreza"] = 15
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 9
                self.stats["sabiduria"] = 12
                self.stats["carisma"] = 10
                self.stats["CA"] = 18
                                
                self.mod["fuerza"] = 2
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = -1
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 0

                self.salva = {"fuerza", "constitucion"}

            if self._class == "Hechicero":
                self.stats["fuerza"] = 10
                self.stats["destreza"] = 15
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 13
                self.stats["sabiduria"] = 8
                self.stats["carisma"] = 15
                self.stats["CA"] = 15
                                
                self.mod["fuerza"] = 0
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = -1
                self.mod["carisma"] = 2

                self.salva = {"constitucion", "carisma"}

            if self._class == "Mago":
                self.stats["fuerza"] = 8
                self.stats["destreza"] = 16
                self.stats["constitucion"] = 13
                self.stats["inteligencia"] = 16
                self.stats["sabiduria"] = 12
                self.stats["carisma"] = 10
                self.stats["CA"] = 13
                
                self.mod["fuerza"] = -1
                self.mod["destreza"] = 3
                self.mod["constitucion"] = 1
                self.mod["inteligencia"] = 3
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 0

                self.salva = {"inteligencia", "sabiduria"}

            if self._class == "Monje":
                self.stats["fuerza"] = 13
                self.stats["destreza"] = 17
                self.stats["constitucion"] = 12
                self.stats["inteligencia"] = 9
                self.stats["sabiduria"] = 14
                self.stats["carisma"] = 10
                self.stats["CA"] = 15
                
                self.mod["fuerza"] = 1
                self.mod["destreza"] = 3
                self.mod["constitucion"] = 1
                self.mod["inteligencia"] = -1
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = 0

                self.salva = {"fuerza", "destreza"}

            if self._class == "Paladín":
                self.stats["fuerza"] = 15
                self.stats["destreza"] = 15
                self.stats["constitucion"] = 10
                self.stats["inteligencia"] = 13
                self.stats["sabiduria"] = 8
                self.stats["carisma"] = 14
                self.stats["CA"] = 18
                
                self.mod["fuerza"] = 2
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 0
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = -1
                self.mod["carisma"] = 2

                self.salva = {"sabiduria", "carisma"}

            if self._class == "Pícaro":
                self.stats["fuerza"] = 12
                self.stats["destreza"] = 17
                self.stats["constitucion"] = 10
                self.stats["inteligencia"] = 15
                self.stats["sabiduria"] = 13
                self.stats["carisma"] = 8
                self.stats["CA"] = 14
                
                self.mod["fuerza"] = 1
                self.mod["destreza"] = 3
                self.mod["constitucion"] = 0
                self.mod["inteligencia"] = 2
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = -1

                self.salva = {"destreza", "inteligencia"}

        elif self.race == "Mediano":
            self.speed = 25
            self.adj_speed = 25
            if self._class == "Bárbaro":
                self.stats["fuerza"] = 15
                self.stats["destreza"] = 15
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 8
                self.stats["sabiduria"] = 12
                self.stats["carisma"] = 11
                self.stats["CA"] = 14

                self.mod["fuerza"] = 2
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = -1
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 0

                self.salva = {"fuerza", "constitucion"}

            if self._class == "Bardo":
                self.stats["fuerza"] = 10
                self.stats["destreza"] = 16
                self.stats["constitucion"] = 13
                self.stats["inteligencia"] = 12
                self.stats["sabiduria"] = 8
                self.stats["carisma"] = 16
                self.stats["CA"] = 14

                self.mod["fuerza"] = 0
                self.mod["destreza"] = 3
                self.mod["constitucion"] = 1
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = -1
                self.mod["carisma"] = 3

                self.salva = {"destreza", "carisma"}
            
            if self._class == "Brujo":
                self.stats["fuerza"] = 8
                self.stats["destreza"] = 12
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 13
                self.stats["sabiduria"] = 12
                self.stats["carisma"] = 16
                self.stats["CA"] = 12
                
                self.mod["fuerza"] = -1
                self.mod["destreza"] = 1
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 3

                self.salva = {"sabiduria", "carisma"}

            if self._class == "Clérigo":
                self.stats["fuerza"] = 14
                self.stats["destreza"] = 10
                self.stats["constitucion"] = 13
                self.stats["inteligencia"] = 10
                self.stats["sabiduria"] = 15
                self.stats["carisma"] = 13
                self.stats["CA"] = 18
                                
                self.mod["fuerza"] = 2
                self.mod["destreza"] = 0
                self.mod["constitucion"] = 1
                self.mod["inteligencia"] = 0
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = 1

                self.salva = {"sabiduria", "carisma"}

            if self._class == "Druida":
                self.stats["fuerza"] = 13
                self.stats["destreza"] = 10
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 10
                self.stats["sabiduria"] = 15
                self.stats["carisma"] = 13
                self.stats["CA"] = 13
                                
                self.mod["fuerza"] = 1
                self.mod["destreza"] = 0
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 0
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = 1

                self.salva = {"sabiduria", "inteligencia"}

            if self._class == "Explorador":
                self.stats["fuerza"] = 13
                self.stats["destreza"] = 17
                self.stats["constitucion"] = 10
                self.stats["inteligencia"] = 12
                self.stats["sabiduria"] = 14
                self.stats["carisma"] = 9
                self.stats["CA"] = 14
                                
                self.mod["fuerza"] = 1
                self.mod["destreza"] = 3
                self.mod["constitucion"] = 0
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = -1

            if self._class == "Guerrero":
                self.stats["fuerza"] = 15
                self.stats["destreza"] = 15
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 8
                self.stats["sabiduria"] = 12
                self.stats["carisma"] = 11
                self.stats["CA"] = 18
                                
                self.mod["fuerza"] = 2
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = -1
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 0

                self.salva = {"fuerza", "constitucion"}

            if self._class == "Hechicero":
                self.stats["fuerza"] = 10
                self.stats["destreza"] = 15
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 12
                self.stats["sabiduria"] = 8
                self.stats["carisma"] = 16
                self.stats["CA"] = 15
                                
                self.mod["fuerza"] = 0
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = -1
                self.mod["carisma"] = 3

                self.salva = {"constitucion", "carisma"}

            if self._class == "Mago":
                self.stats["fuerza"] = 8
                self.stats["destreza"] = 16
                self.stats["constitucion"] = 13
                self.stats["inteligencia"] = 15
                self.stats["sabiduria"] = 12
                self.stats["carisma"] = 11
                self.stats["CA"] = 13
                
                self.mod["fuerza"] = -1
                self.mod["destreza"] = 3
                self.mod["constitucion"] = 1
                self.mod["inteligencia"] = 2
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 0

                self.salva = {"inteligencia", "sabiduria"}

            if self._class == "Monje":
                self.stats["fuerza"] = 13
                self.stats["destreza"] = 17
                self.stats["constitucion"] = 12
                self.stats["inteligencia"] = 8
                self.stats["sabiduria"] = 14
                self.stats["carisma"] = 11
                self.stats["CA"] = 15
                
                self.mod["fuerza"] = 1
                self.mod["destreza"] = 3
                self.mod["constitucion"] = 1
                self.mod["inteligencia"] = -1
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = 0

                self.salva = {"fuerza", "destreza"}

            if self._class == "Paladín":
                self.stats["fuerza"] = 15
                self.stats["destreza"] = 15
                self.stats["constitucion"] = 10
                self.stats["inteligencia"] = 12
                self.stats["sabiduria"] = 8
                self.stats["carisma"] = 15
                self.stats["CA"] = 18
                
                self.mod["fuerza"] = 2
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 0
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = -1
                self.mod["carisma"] = 2

                self.salva = {"sabiduria", "carisma"}

            if self._class == "Pícaro":
                self.stats["fuerza"] = 12
                self.stats["destreza"] = 17
                self.stats["constitucion"] = 10
                self.stats["inteligencia"] = 14
                self.stats["sabiduria"] = 13
                self.stats["carisma"] = 9
                self.stats["CA"] = 14
                
                self.mod["fuerza"] = 1
                self.mod["destreza"] = 3
                self.mod["constitucion"] = 0
                self.mod["inteligencia"] = 2
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = -1

                self.salva = {"destreza", "inteligencia"}

        elif self.race == "Humano":
            self.speed = 30
            self.adj_speed = 30
            if self._class == "Bárbaro":
                self.stats["fuerza"] = 16
                self.stats["destreza"] = 14
                self.stats["constitucion"] = 15
                self.stats["inteligencia"] = 9
                self.stats["sabiduria"] = 13
                self.stats["carisma"] = 11
                self.stats["CA"] = 14

                self.mod["fuerza"] = 3
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = -1
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 0

                self.salva = {"fuerza", "constitucion"}

            if self._class == "Bardo":
                self.stats["fuerza"] = 11
                self.stats["destreza"] = 15
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 13
                self.stats["sabiduria"] = 9
                self.stats["carisma"] = 16
                self.stats["CA"] = 13

                self.mod["fuerza"] = 0
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = -1
                self.mod["carisma"] = 3

                self.salva = {"destreza", "carisma"}

            if self._class == "Brujo":
                self.stats["fuerza"] = 8
                self.stats["destreza"] = 12
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 13
                self.stats["sabiduria"] = 12
                self.stats["carisma"] = 16
                self.stats["CA"] = 12
                
                self.mod["fuerza"] = -1
                self.mod["destreza"] = 1
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 3

                self.salva = {"sabiduria", "carisma"}

            if self._class == "Clérigo":
                self.stats["fuerza"] = 15
                self.stats["destreza"] = 9
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 11
                self.stats["sabiduria"] = 16
                self.stats["carisma"] = 13
                self.stats["CA"] = 18
                                
                self.mod["fuerza"] = 2
                self.mod["destreza"] = -1
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 0
                self.mod["sabiduria"] = 3
                self.mod["carisma"] = 1

                self.salva = {"sabiduria", "carisma"}

            if self._class == "Druida":
                self.stats["fuerza"] = 14
                self.stats["destreza"] = 9
                self.stats["constitucion"] = 15
                self.stats["inteligencia"] = 11
                self.stats["sabiduria"] = 16
                self.stats["carisma"] = 13
                self.stats["CA"] = 12
                                
                self.mod["fuerza"] = 2
                self.mod["destreza"] = -1
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 0
                self.mod["sabiduria"] = 3
                self.mod["carisma"] = 1

                self.salva = {"sabiduria", "inteligencia"}
            
            if self._class == "Explorador":
                self.stats["fuerza"] = 14
                self.stats["destreza"] = 16
                self.stats["constitucion"] = 11
                self.stats["inteligencia"] = 13
                self.stats["sabiduria"] = 15
                self.stats["carisma"] = 9
                self.stats["CA"] = 14
                                
                self.mod["fuerza"] = 2
                self.mod["destreza"] = 3
                self.mod["constitucion"] = 0
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = -1

            if self._class == "Guerrero":
                self.stats["fuerza"] = 16
                self.stats["destreza"] = 14
                self.stats["constitucion"] = 15
                self.stats["inteligencia"] = 9
                self.stats["sabiduria"] = 13
                self.stats["carisma"] = 11
                self.stats["CA"] = 18
                                
                self.mod["fuerza"] = 3
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = -1
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 0

                self.salva = {"fuerza", "constitucion"}

            if self._class == "Hechicero":
                self.stats["fuerza"] = 11
                self.stats["destreza"] = 14
                self.stats["constitucion"] = 15
                self.stats["inteligencia"] = 13
                self.stats["sabiduria"] = 9
                self.stats["carisma"] = 16
                self.stats["CA"] = 15
                                
                self.mod["fuerza"] = 0
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = -1
                self.mod["carisma"] = 3

                self.salva = {"constitucion", "carisma"}

            if self._class == "Mago":
                self.stats["fuerza"] = 9
                self.stats["destreza"] = 15
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 16
                self.stats["sabiduria"] = 13
                self.stats["carisma"] = 11
                self.stats["CA"] = 12
                
                self.mod["fuerza"] = -1
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 3
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 0

                self.salva = {"sabiduria", "inteligencia"}

            if self._class == "Monje":
                self.stats["fuerza"] = 14
                self.stats["destreza"] = 16
                self.stats["constitucion"] = 13
                self.stats["inteligencia"] = 9
                self.stats["sabiduria"] = 15
                self.stats["carisma"] = 11
                self.stats["CA"] = 15
                
                self.mod["fuerza"] = 2
                self.mod["destreza"] = 3
                self.mod["constitucion"] = 1
                self.mod["inteligencia"] = -1
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = 0

                self.salva = {"destreza", "fuerza"}

            if self._class == "Paladín":
                self.stats["fuerza"] = 16
                self.stats["destreza"] = 14
                self.stats["constitucion"] = 11
                self.stats["inteligencia"] = 13
                self.stats["sabiduria"] = 9
                self.stats["carisma"] = 15
                self.stats["CA"] = 18
                
                self.mod["fuerza"] = 3
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 0
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = -1
                self.mod["carisma"] = 2

                self.salva = {"sabiduria", "carisma"}

            if self._class == "Pícaro":
                self.stats["fuerza"] = 13
                self.stats["destreza"] = 16
                self.stats["constitucion"] = 11
                self.stats["inteligencia"] = 15
                self.stats["sabiduria"] = 14
                self.stats["carisma"] = 9
                self.stats["CA"] = 14
                
                self.mod["fuerza"] = 2
                self.mod["destreza"] = 3
                self.mod["constitucion"] = 0
                self.mod["inteligencia"] = 2
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = -1

                self.salva = {"destreza", "inteligencia"}

        elif self.race == "Dracónido":
            self.speed = 30
            self.adj_speed = 30
            if self._class == "Bárbaro":
                self.stats["fuerza"] = 17
                self.stats["destreza"] = 13
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 8
                self.stats["sabiduria"] = 12
                self.stats["carisma"] = 11
                self.stats["CA"] = 13

                self.mod["fuerza"] = 3
                self.mod["destreza"] = 1
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = -1
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 0

                self.salva = {"fuerza", "constitucion"}

            if self._class == "Bardo":
                self.stats["fuerza"] = 12
                self.stats["destreza"] = 14
                self.stats["constitucion"] = 13
                self.stats["inteligencia"] = 12
                self.stats["sabiduria"] = 8
                self.stats["carisma"] = 16
                self.stats["CA"] = 13

                self.mod["fuerza"] = 1
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 1
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = -1
                self.mod["carisma"] = 3

                self.salva = {"destreza", "carisma"}
            
            if self._class == "Brujo":
                self.stats["fuerza"] = 10
                self.stats["destreza"] = 10
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 13
                self.stats["sabiduria"] = 12
                self.stats["carisma"] = 16
                self.stats["CA"] = 11
                
                self.mod["fuerza"] = 0
                self.mod["destreza"] = 0
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 3

                self.salva = {"sabiduria", "carisma"}

            if self._class == "Clérigo":
                self.stats["fuerza"] = 16
                self.stats["destreza"] = 8
                self.stats["constitucion"] = 13
                self.stats["inteligencia"] = 10
                self.stats["sabiduria"] = 15
                self.stats["carisma"] = 13
                self.stats["CA"] = 18
                                
                self.mod["fuerza"] = 3
                self.mod["destreza"] = -1
                self.mod["constitucion"] = 1
                self.mod["inteligencia"] = 0
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = 1

                self.salva = {"sabiduria", "carisma"}

            if self._class == "Druida":
                self.stats["fuerza"] = 15
                self.stats["destreza"] = 8
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 10
                self.stats["sabiduria"] = 15
                self.stats["carisma"] = 13
                self.stats["CA"] = 12
                                
                self.mod["fuerza"] = 2
                self.mod["destreza"] = -1
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 0
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = 1

                self.salva = {"sabiduria", "inteligencia"}
            
            if self._class == "Explorador":
                self.stats["fuerza"] = 15
                self.stats["destreza"] = 15
                self.stats["constitucion"] = 10
                self.stats["inteligencia"] = 12
                self.stats["sabiduria"] = 14
                self.stats["carisma"] = 9
                self.stats["CA"] = 13
                                
                self.mod["fuerza"] = 2
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 0
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = -1

            if self._class == "Guerrero":
                self.stats["fuerza"] = 17
                self.stats["destreza"] = 13
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 8
                self.stats["sabiduria"] = 12
                self.stats["carisma"] = 11
                self.stats["CA"] = 18
                                
                self.mod["fuerza"] = 3
                self.mod["destreza"] = 1
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = -1
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 0

                self.salva = {"fuerza", "constitucion"}

            if self._class == "Hechicero":
                self.stats["fuerza"] = 12
                self.stats["destreza"] = 13
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 12
                self.stats["sabiduria"] = 8
                self.stats["carisma"] = 16
                self.stats["CA"] = 14
                                
                self.mod["fuerza"] = 1
                self.mod["destreza"] = 1
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = -1
                self.mod["carisma"] = 3

                self.salva = {"constitucion", "carisma"}

            if self._class == "Mago":
                self.stats["fuerza"] = 10
                self.stats["destreza"] = 14
                self.stats["constitucion"] = 13
                self.stats["inteligencia"] = 15
                self.stats["sabiduria"] = 12
                self.stats["carisma"] = 11
                self.stats["CA"] = 12
                
                self.mod["fuerza"] = 0
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 1
                self.mod["inteligencia"] = 2
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 0

                self.salva = {"sabiduria", "inteligencia"}

            if self._class == "Monje":
                self.stats["fuerza"] = 15
                self.stats["destreza"] = 15
                self.stats["constitucion"] = 12
                self.stats["inteligencia"] = 8
                self.stats["sabiduria"] = 14
                self.stats["carisma"] = 11
                self.stats["CA"] = 14
                
                self.mod["fuerza"] = 2
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 1
                self.mod["inteligencia"] = -1
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = 0

                self.salva = {"destreza", "fuerza"}

            if self._class == "Paladín":
                self.stats["fuerza"] = 17
                self.stats["destreza"] = 13
                self.stats["constitucion"] = 10
                self.stats["inteligencia"] = 12
                self.stats["sabiduria"] = 8
                self.stats["carisma"] = 15
                self.stats["CA"] = 18
                
                self.mod["fuerza"] = 3
                self.mod["destreza"] = 1
                self.mod["constitucion"] = 0
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = -1
                self.mod["carisma"] = 2

                self.salva = {"sabiduria", "carisma"}

            if self._class == "Pícaro":
                self.stats["fuerza"] = 14
                self.stats["destreza"] = 15
                self.stats["constitucion"] = 10
                self.stats["inteligencia"] = 14
                self.stats["sabiduria"] = 13
                self.stats["carisma"] = 9
                self.stats["CA"] = 13
                
                self.mod["fuerza"] = 2
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 0
                self.mod["inteligencia"] = 2
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = -1

                self.salva = {"destreza", "inteligencia"}

        elif self.race == "Gnomo":
            self.speed = 25
            self.adj_speed = 25
            if self._class == "Bárbaro":
                self.stats["fuerza"] = 15
                self.stats["destreza"] = 14
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 10
                self.stats["sabiduria"] = 12
                self.stats["carisma"] = 10
                self.stats["CA"] = 14

                self.mod["fuerza"] = 2
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 0
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 0

                self.salva = {"fuerza", "constitucion"}

            if self._class == "Bardo":
                self.stats["fuerza"] = 12
                self.stats["destreza"] = 14
                self.stats["constitucion"] = 15
                self.stats["inteligencia"] = 12
                self.stats["sabiduria"] = 8
                self.stats["carisma"] = 15
                self.stats["CA"] = 13

                self.mod["fuerza"] = 1
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = -1
                self.mod["carisma"] = 2

                self.salva = {"destreza", "carisma"}
            
            if self._class == "Brujo":
                self.stats["fuerza"] = 8
                self.stats["destreza"] = 11
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 15
                self.stats["sabiduria"] = 12
                self.stats["carisma"] = 15
                self.stats["CA"] = 11
                
                self.mod["fuerza"] = -1
                self.mod["destreza"] = 0
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 2
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 2

                self.salva = {"sabiduria", "carisma"}

            if self._class == "Clérigo":
                self.stats["fuerza"] = 14
                self.stats["destreza"] = 9
                self.stats["constitucion"] = 13
                self.stats["inteligencia"] = 12
                self.stats["sabiduria"] = 15
                self.stats["carisma"] = 12
                self.stats["CA"] = 18
                                
                self.mod["fuerza"] = 2
                self.mod["destreza"] = -1
                self.mod["constitucion"] = 1
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = 1

                self.salva = {"sabiduria", "carisma"}

            if self._class == "Druida":
                self.stats["fuerza"] = 13
                self.stats["destreza"] = 9
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 12
                self.stats["sabiduria"] = 15
                self.stats["carisma"] = 12
                self.stats["CA"] = 12
                                
                self.mod["fuerza"] = 1
                self.mod["destreza"] = -1
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = 1

                self.salva = {"sabiduria", "inteligencia"}
            
            if self._class == "Explorador":
                self.stats["fuerza"] = 13
                self.stats["destreza"] = 16
                self.stats["constitucion"] = 10
                self.stats["inteligencia"] = 14
                self.stats["sabiduria"] = 14
                self.stats["carisma"] = 8
                self.stats["CA"] = 14
                                
                self.mod["fuerza"] = 1
                self.mod["destreza"] = 3
                self.mod["constitucion"] = 0
                self.mod["inteligencia"] = 2
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = -1

            if self._class == "Guerrero":
                self.stats["fuerza"] = 15
                self.stats["destreza"] = 15
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 9
                self.stats["sabiduria"] = 12
                self.stats["carisma"] = 10
                self.stats["CA"] = 18
                                
                self.mod["fuerza"] = 2
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = -1
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 0

                self.salva = {"fuerza", "constitucion"}

            if self._class == "Hechicero":
                self.stats["fuerza"] = 10
                self.stats["destreza"] = 14
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 14
                self.stats["sabiduria"] = 8
                self.stats["carisma"] = 15
                self.stats["CA"] = 15
                                
                self.mod["fuerza"] = 0
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 2
                self.mod["sabiduria"] = -1
                self.mod["carisma"] = 2

                self.salva = {"constitucion", "carisma"}

            if self._class == "Mago":
                self.stats["fuerza"] = 8
                self.stats["destreza"] = 15
                self.stats["constitucion"] = 13
                self.stats["inteligencia"] = 17
                self.stats["sabiduria"] = 12
                self.stats["carisma"] = 10
                self.stats["CA"] = 12
                
                self.mod["fuerza"] = -1
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 1
                self.mod["inteligencia"] = 3
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 0

                self.salva = {"sabiduria", "inteligencia"}

            if self._class == "Monje":
                self.stats["fuerza"] = 13
                self.stats["destreza"] = 16
                self.stats["constitucion"] = 12
                self.stats["inteligencia"] = 10
                self.stats["sabiduria"] = 14
                self.stats["carisma"] = 10
                self.stats["CA"] = 15
                
                self.mod["fuerza"] = 1
                self.mod["destreza"] = 3
                self.mod["constitucion"] = 1
                self.mod["inteligencia"] = 0
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = 0

                self.salva = {"destreza", "fuerza"}

            if self._class == "Paladín":
                self.stats["fuerza"] = 15
                self.stats["destreza"] = 14
                self.stats["constitucion"] = 10
                self.stats["inteligencia"] = 14
                self.stats["sabiduria"] = 8
                self.stats["carisma"] = 14
                self.stats["CA"] = 18
                
                self.mod["fuerza"] = 2
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 0
                self.mod["inteligencia"] = 2
                self.mod["sabiduria"] = -1
                self.mod["carisma"] = 2

                self.salva = {"sabiduria", "carisma"}

            if self._class == "Pícaro":
                self.stats["fuerza"] = 12
                self.stats["destreza"] = 16
                self.stats["constitucion"] = 10
                self.stats["inteligencia"] = 16
                self.stats["sabiduria"] = 13
                self.stats["carisma"] = 8
                self.stats["CA"] = 14
                
                self.mod["fuerza"] = 1
                self.mod["destreza"] = 3
                self.mod["constitucion"] = 0
                self.mod["inteligencia"] = 3
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = -1

                self.salva = {"destreza", "inteligencia"}

        elif self.race == "Semielfo":
            self.speed = 30
            self.adj_speed = 30
            if self._class == "Bárbaro":
                self.stats["fuerza"] = 15
                self.stats["destreza"] = 14
                self.stats["constitucion"] = 15
                self.stats["inteligencia"] = 8
                self.stats["sabiduria"] = 12
                self.stats["carisma"] = 12
                self.stats["CA"] = 14

                self.mod["fuerza"] = 2
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = -1
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 1

                self.salva = {"fuerza", "constitucion"}

            if self._class == "Bardo":
                self.stats["fuerza"] = 10
                self.stats["destreza"] = 15
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 12
                self.stats["sabiduria"] = 8
                self.stats["carisma"] = 17
                self.stats["CA"] = 13

                self.mod["fuerza"] = 0
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = -1
                self.mod["carisma"] = 3

                self.salva = {"destreza", "carisma"}
            
            if self._class == "Brujo":
                self.stats["fuerza"] = 8
                self.stats["destreza"] = 11
                self.stats["constitucion"] = 15
                self.stats["inteligencia"] = 12
                self.stats["sabiduria"] = 13
                self.stats["carisma"] = 17
                self.stats["CA"] = 11
                
                self.mod["fuerza"] = -1
                self.mod["destreza"] = 0
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 3

                self.salva = {"sabiduria", "carisma"}

            if self._class == "Clérigo":
                self.stats["fuerza"] = 14
                self.stats["destreza"] = 9
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 10
                self.stats["sabiduria"] = 15
                self.stats["carisma"] = 14
                self.stats["CA"] = 18
                                
                self.mod["fuerza"] = 2
                self.mod["destreza"] = -1
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 0
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = 2

                self.salva = {"sabiduria", "carisma"}

            if self._class == "Druida":
                self.stats["fuerza"] = 13
                self.stats["destreza"] = 9
                self.stats["constitucion"] = 15
                self.stats["inteligencia"] = 10
                self.stats["sabiduria"] = 15
                self.stats["carisma"] = 14
                self.stats["CA"] = 12
                                
                self.mod["fuerza"] = 1
                self.mod["destreza"] = -1
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 0
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = 2

                self.salva = {"sabiduria", "inteligencia"}

            if self._class == "Explorador":
                self.stats["fuerza"] = 13
                self.stats["destreza"] = 16
                self.stats["constitucion"] = 11
                self.stats["inteligencia"] = 12
                self.stats["sabiduria"] = 14
                self.stats["carisma"] = 10
                self.stats["CA"] = 14
                                
                self.mod["fuerza"] = 1
                self.mod["destreza"] = 3
                self.mod["constitucion"] = 0
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = 0

            if self._class == "Guerrero":
                self.stats["fuerza"] = 15
                self.stats["destreza"] = 14
                self.stats["constitucion"] = 15
                self.stats["inteligencia"] = 8
                self.stats["sabiduria"] = 12
                self.stats["carisma"] = 12
                self.stats["CA"] = 18
                                
                self.mod["fuerza"] = 2
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = -1
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 1

                self.salva = {"fuerza", "constitucion"}

            if self._class == "Hechicero":
                self.stats["fuerza"] = 10
                self.stats["destreza"] = 14
                self.stats["constitucion"] = 15
                self.stats["inteligencia"] = 12
                self.stats["sabiduria"] = 8
                self.stats["carisma"] = 17
                self.stats["CA"] = 15
                                
                self.mod["fuerza"] = 0
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = -1
                self.mod["carisma"] = 3

                self.salva = {"constitucion", "carisma"}

            if self._class == "Mago":
                self.stats["fuerza"] = 8
                self.stats["destreza"] = 15
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 15
                self.stats["sabiduria"] = 12
                self.stats["carisma"] = 13
                self.stats["CA"] = 12
                
                self.mod["fuerza"] = -1
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 2
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 1

                self.salva = {"sabiduria", "inteligencia"}

            if self._class == "Monje":
                self.stats["fuerza"] = 13
                self.stats["destreza"] = 16
                self.stats["constitucion"] = 13
                self.stats["inteligencia"] = 8
                self.stats["sabiduria"] = 14
                self.stats["carisma"] = 12
                self.stats["CA"] = 15
                
                self.mod["fuerza"] = 1
                self.mod["destreza"] = 3
                self.mod["constitucion"] = 1
                self.mod["inteligencia"] = -1
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = 1

                self.salva = {"destreza", "fuerza"}

            if self._class == "Paladín":
                self.stats["fuerza"] = 15
                self.stats["destreza"] = 14
                self.stats["constitucion"] = 11
                self.stats["inteligencia"] = 12
                self.stats["sabiduria"] = 8
                self.stats["carisma"] = 16
                self.stats["CA"] = 18
                
                self.mod["fuerza"] = 2
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 0
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = -1
                self.mod["carisma"] = 3

                self.salva = {"sabiduria", "carisma"}

            if self._class == "Pícaro":
                self.stats["fuerza"] = 12
                self.stats["destreza"] = 16
                self.stats["constitucion"] = 11
                self.stats["inteligencia"] = 14
                self.stats["sabiduria"] = 13
                self.stats["carisma"] = 10
                self.stats["CA"] = 14
                
                self.mod["fuerza"] = 1
                self.mod["destreza"] = 3
                self.mod["constitucion"] = 0
                self.mod["inteligencia"] = 2
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 0

                self.salva = {"destreza", "inteligencia"}

        elif self.race == "Semiorco":
            self.speed = 30
            self.adj_speed = 30
            if self._class == "Bárbaro":
                self.stats["fuerza"] = 17
                self.stats["destreza"] = 13
                self.stats["constitucion"] = 15
                self.stats["inteligencia"] = 8
                self.stats["sabiduria"] = 12
                self.stats["carisma"] = 10
                self.stats["CA"] = 13

                self.mod["fuerza"] = 3
                self.mod["destreza"] = 1
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = -1
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 0

                self.salva = {"fuerza", "constitucion"}

            if self._class == "Bardo":
                self.stats["fuerza"] = 12
                self.stats["destreza"] = 14
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 12
                self.stats["sabiduria"] = 8
                self.stats["carisma"] = 15
                self.stats["CA"] = 13

                self.mod["fuerza"] = 1
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = -1
                self.mod["carisma"] = 2

                self.salva = {"destreza", "carisma"}
            
            if self._class == "Brujo":
                self.stats["fuerza"] = 10
                self.stats["destreza"] = 10
                self.stats["constitucion"] = 15
                self.stats["inteligencia"] = 13
                self.stats["sabiduria"] = 12
                self.stats["carisma"] = 15
                self.stats["CA"] = 11
                
                self.mod["fuerza"] = 0
                self.mod["destreza"] = 0
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 2

                self.salva = {"sabiduria", "carisma"}

            if self._class == "Clérigo":
                self.stats["fuerza"] = 16
                self.stats["destreza"] = 8
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 10
                self.stats["sabiduria"] = 15
                self.stats["carisma"] = 12
                self.stats["CA"] = 18
                                
                self.mod["fuerza"] = 3
                self.mod["destreza"] = -1
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 0
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = 1

                self.salva = {"sabiduria", "carisma"}

            if self._class == "Druida":
                self.stats["fuerza"] = 15
                self.stats["destreza"] = 8
                self.stats["constitucion"] = 15
                self.stats["inteligencia"] = 10
                self.stats["sabiduria"] = 15
                self.stats["carisma"] = 12
                self.stats["CA"] = 12
                                
                self.mod["fuerza"] = 2
                self.mod["destreza"] = -1
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 0
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = 1

                self.salva = {"sabiduria", "inteligencia"}
            
            if self._class == "Explorador":
                self.stats["fuerza"] = 15
                self.stats["destreza"] = 15
                self.stats["constitucion"] = 11
                self.stats["inteligencia"] = 12
                self.stats["sabiduria"] = 14
                self.stats["carisma"] = 8
                self.stats["CA"] = 13
                                
                self.mod["fuerza"] = 2
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 0
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = -1

            if self._class == "Guerrero":
                self.stats["fuerza"] = 17
                self.stats["destreza"] = 13
                self.stats["constitucion"] = 15
                self.stats["inteligencia"] = 8
                self.stats["sabiduria"] = 12
                self.stats["carisma"] = 10
                self.stats["CA"] = 18
                                
                self.mod["fuerza"] = 3
                self.mod["destreza"] = 1
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = -1
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 0

                self.salva = {"fuerza", "constitucion"}

            if self._class == "Hechicero":
                self.stats["fuerza"] = 12
                self.stats["destreza"] = 13
                self.stats["constitucion"] = 15
                self.stats["inteligencia"] = 12
                self.stats["sabiduria"] = 8
                self.stats["carisma"] = 15
                self.stats["CA"] = 14
                                
                self.mod["fuerza"] = 1
                self.mod["destreza"] = 1
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = -1
                self.mod["carisma"] = 2

                self.salva = {"constitucion", "carisma"}

            if self._class == "Mago":
                self.stats["fuerza"] = 10
                self.stats["destreza"] = 14
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 15
                self.stats["sabiduria"] = 12
                self.stats["carisma"] = 10
                self.stats["CA"] = 12
                
                self.mod["fuerza"] = 0
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 2
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 0

                self.salva = {"sabiduria", "inteligencia"}

            if self._class == "Monje":
                self.stats["fuerza"] = 15
                self.stats["destreza"] = 15
                self.stats["constitucion"] = 13
                self.stats["inteligencia"] = 8
                self.stats["sabiduria"] = 14
                self.stats["carisma"] = 10
                self.stats["CA"] = 14
                
                self.mod["fuerza"] = 2
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 1
                self.mod["inteligencia"] = -1
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = 0

                self.salva = {"destreza", "fuerza"}

            if self._class == "Paladín":
                self.stats["fuerza"] = 17
                self.stats["destreza"] = 13
                self.stats["constitucion"] = 11
                self.stats["inteligencia"] = 12
                self.stats["sabiduria"] = 8
                self.stats["carisma"] = 14
                self.stats["CA"] = 18
                
                self.mod["fuerza"] = 3
                self.mod["destreza"] = 1
                self.mod["constitucion"] = 0
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = -1
                self.mod["carisma"] = 2

                self.salva = {"sabiduria", "carisma"}

            if self._class == "Pícaro":
                self.stats["fuerza"] = 14
                self.stats["destreza"] = 15
                self.stats["constitucion"] = 11
                self.stats["inteligencia"] = 14
                self.stats["sabiduria"] = 13
                self.stats["carisma"] = 8
                self.stats["CA"] = 13
                
                self.mod["fuerza"] = 2
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 0
                self.mod["inteligencia"] = 2
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = -1

                self.salva = {"destreza", "inteligencia"}

        elif self.race == "Tiefling":
            self.speed = 30
            self.adj_speed = 30
            if self._class == "Bárbaro":
                self.stats["fuerza"] = 15
                self.stats["destreza"] = 13
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 9
                self.stats["sabiduria"] = 12
                self.stats["carisma"] = 12
                self.stats["CA"] = 13

                self.mod["fuerza"] = 2
                self.mod["destreza"] = 1
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = -1
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 1

                self.salva = {"fuerza", "constitucion"}

            if self._class == "Bardo":
                self.stats["fuerza"] = 10
                self.stats["destreza"] = 14
                self.stats["constitucion"] = 13
                self.stats["inteligencia"] = 13
                self.stats["sabiduria"] = 8
                self.stats["carisma"] = 17
                self.stats["CA"] = 13

                self.mod["fuerza"] = 0
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 1
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = -1
                self.mod["carisma"] = 3

                self.salva = {"destreza", "carisma"}
            
            if self._class == "Brujo":
                self.stats["fuerza"] = 8
                self.stats["destreza"] = 10
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 14
                self.stats["sabiduria"] = 12
                self.stats["carisma"] = 17
                self.stats["CA"] = 11
                
                self.mod["fuerza"] = -1
                self.mod["destreza"] = 0
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 2
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 3

                self.salva = {"sabiduria", "carisma"}

            if self._class == "Clérigo":
                self.stats["fuerza"] = 14
                self.stats["destreza"] = 8
                self.stats["constitucion"] = 13
                self.stats["inteligencia"] = 11
                self.stats["sabiduria"] = 15
                self.stats["carisma"] = 14
                self.stats["CA"] = 18
                                
                self.mod["fuerza"] = 2
                self.mod["destreza"] = -1
                self.mod["constitucion"] = 1
                self.mod["inteligencia"] = 0
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = 2

                self.salva = {"sabiduria", "carisma"}

            if self._class == "Druida":
                self.stats["fuerza"] = 13
                self.stats["destreza"] = 8
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 11
                self.stats["sabiduria"] = 15
                self.stats["carisma"] = 14
                self.stats["CA"] = 12
                                
                self.mod["fuerza"] = 1
                self.mod["destreza"] = -1
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 0
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = 2

                self.salva = {"sabiduria", "inteligencia"}
            
            if self._class == "Explorador":
                self.stats["fuerza"] = 13
                self.stats["destreza"] = 15
                self.stats["constitucion"] = 10
                self.stats["inteligencia"] = 13
                self.stats["sabiduria"] = 14
                self.stats["carisma"] = 10
                self.stats["CA"] = 13
                                
                self.mod["fuerza"] = 1
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 0
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = 0

            if self._class == "Guerrero":
                self.stats["fuerza"] = 15
                self.stats["destreza"] = 13
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 9
                self.stats["sabiduria"] = 12
                self.stats["carisma"] = 12
                self.stats["CA"] = 18
                                
                self.mod["fuerza"] = 2
                self.mod["destreza"] = 1
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = -1
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 1

                self.salva = {"fuerza", "constitucion"}

            if self._class == "Hechicero":
                self.stats["fuerza"] = 10
                self.stats["destreza"] = 13
                self.stats["constitucion"] = 14
                self.stats["inteligencia"] = 13
                self.stats["sabiduria"] = 8
                self.stats["carisma"] = 17
                self.stats["CA"] = 14
                                
                self.mod["fuerza"] = 0
                self.mod["destreza"] = 1
                self.mod["constitucion"] = 2
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = -1
                self.mod["carisma"] = 3

                self.salva = {"constitucion", "carisma"}

            if self._class == "Mago":
                self.stats["fuerza"] = 8
                self.stats["destreza"] = 14
                self.stats["constitucion"] = 13
                self.stats["inteligencia"] = 16
                self.stats["sabiduria"] = 12
                self.stats["carisma"] = 12
                self.stats["CA"] = 12
                
                self.mod["fuerza"] = -1
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 1
                self.mod["inteligencia"] = 3
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 1

                self.salva = {"sabiduria", "inteligencia"}

            if self._class == "Monje":
                self.stats["fuerza"] = 13
                self.stats["destreza"] = 15
                self.stats["constitucion"] = 12
                self.stats["inteligencia"] = 9
                self.stats["sabiduria"] = 14
                self.stats["carisma"] = 12
                self.stats["CA"] = 14
                
                self.mod["fuerza"] = 1
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 1
                self.mod["inteligencia"] = -1
                self.mod["sabiduria"] = 2
                self.mod["carisma"] = 1

                self.salva = {"destreza", "fuerza"}

            if self._class == "Paladín":
                self.stats["fuerza"] = 15
                self.stats["destreza"] = 13
                self.stats["constitucion"] = 10
                self.stats["inteligencia"] = 13
                self.stats["sabiduria"] = 8
                self.stats["carisma"] = 16
                self.stats["CA"] = 18
                
                self.mod["fuerza"] = 2
                self.mod["destreza"] = 1
                self.mod["constitucion"] = 0
                self.mod["inteligencia"] = 1
                self.mod["sabiduria"] = -1
                self.mod["carisma"] = 3

                self.salva = {"sabiduria", "carisma"}

            if self._class == "Pícaro":
                self.stats["fuerza"] = 12
                self.stats["destreza"] = 15
                self.stats["constitucion"] = 10
                self.stats["inteligencia"] = 15
                self.stats["sabiduria"] = 13
                self.stats["carisma"] = 10
                self.stats["CA"] = 13
                
                self.mod["fuerza"] = 1
                self.mod["destreza"] = 2
                self.mod["constitucion"] = 0
                self.mod["inteligencia"] = 2
                self.mod["sabiduria"] = 1
                self.mod["carisma"] = 0

                self.salva = {"destreza", "inteligencia"}

def start(update, context):

    global PJ

    buttons =  [KeyboardButton("¡Vamos!")], [KeyboardButton("¡Espera! Tengo algunas dudas...")]

    context.bot.sendSticker(chat_id=update.effective_chat.id, sticker="CAACAgIAAxkBAAEYUt9jLCeequdD2m9Rm4cuus-Rh_8wNgACvAwAAocoMEntN5GZWCFoBCkE")

    PJ = Character(update.message.from_user.first_name, update.message.text)

    string = "¡Hola! Soy Calcifer, y te voy a ayudar a crear tu avatar en el mundo de D&D."

    slow_typing(string, update, context)

    string = "_O_ _al_ _menos,_ _lo_ _voy_ _a_ _intentar_ . . ."

    slow_typing(string, update, context)
    
    string = "Puedes parar escribiendo el comando /cancel."
    
    slow_typing(string, update, context)

    context.bot.send_message(chat_id=update.effective_chat.id, 
                                text="— ¿Nos ponemos a ello?", 
                                parse_mode= "Markdown", 
                                reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True))

    context.bot.sendSticker(chat_id=update.effective_chat.id, sticker="CAACAgIAAxkBAAEYhE1jNIM6Na-LjwombOvVtk5WR7qvIQACNwwAAiHRMUlAzx0V3wssFSoE")

    return TYPE

def type(update, context):

    context.bot.sendChatAction(chat_id=update.message.chat_id , action = ChatAction.TYPING)
    
    time.sleep(3)
    
    if Wiki in update.message.text:

        context.bot.sendChatAction(chat_id=update.message.chat_id , action = ChatAction.TYPING)

        time.sleep(3)

        buttons =  [KeyboardButton("Está bien.")], [KeyboardButton("Tampoco hace falta que te pongas así...")]

        string = "Así que, por lo que veo, no tienes ni idea de lo que estás haciendo . . ."

        slow_typing(string, update, context)

        string = "_Perfecto_."

        slow_typing(string, update, context)

        context.bot.sendSticker(chat_id=update.effective_chat.id, sticker="CAACAgIAAxkBAAEYhFFjNIN3GZj6IShue4wscKL6icx4fgACWxMAArshMEkz55bxMvha1CoE")

        string = "A ver, en el mundo de D&D hay distintas razas a las que puede pertenecer tu avatar, empecemos por ahí."

        slow_typing(string, update, context)
        
        msg = context.bot.send_message(chat_id=update.effective_chat.id, 
                                        text="¿De acuerdo?",
                                        parse_mode= "Markdown",
                                        reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True))
        
        return WIKI_RACE

    else:

        context.bot.sendSticker(chat_id=update.effective_chat.id, sticker="CAACAgIAAxkBAAEYhFljNIQBEgxdE5hx_E7o7bRnUoPxLAACow4AAtayMEkaQ5BopdvXfCoE")

        context.bot.sendChatAction(chat_id=update.message.chat_id , action = ChatAction.TYPING)

        time.sleep(2)

        string = "Si vas a ser un jugador... necesitarás un personaje. Primero lo primero, ¿cómo quieres llamar a tu avatar?"
        
        slow_typing(string, update, context)
        
        return NAME

def wiki_race(update, context):

    context.bot.sendChatAction(chat_id=update.message.chat_id , action = ChatAction.TYPING)

    time.sleep(3)

    if "Está bien." in update.message.text:
        
        string = "Esa es la actitud."

        slow_typing(string, update, context)

        context.bot.sendSticker(chat_id=update.effective_chat.id, sticker="CAACAgIAAxkBAAEYhFljNIQBEgxdE5hx_E7o7bRnUoPxLAACow4AAtayMEkaQ5BopdvXfCoE")

        string = "Veamos . . ."

        slow_typing(string, update, context)

    elif "Solo quiero comprobar una cosa, no tardo nada." in update.message.text:
        
        string = "Veámoslo . . ."

        slow_typing(string, update, context)

        context.bot.sendSticker(chat_id=update.effective_chat.id, sticker="CAACAgIAAxkBAAEYhFxjNIR1fY6DdbT6rs_t0NaY4EMS4gACJg8AAvtZKEkiX-SE94ctpyoE")

    else:
        
        string = "_Istimis_ _in_ _piqui_ _quisquillisis..._"
        
        slow_typing(string, update, context)

        context.bot.sendSticker(chat_id=update.effective_chat.id, sticker="CAACAgIAAxkBAAEYhF5jNISmN2uwYc157SyWC1ZPdOWiygACxREAArCasUhdUZ2-kKVX2ioE")


    keyboard = [[InlineKeyboardButton("¡Me gusta!", callback_data="stop")], [InlineKeyboardButton("A ver el siguiente...", callback_data="next")]]
    
    context.bot.send_message(chat_id=update.effective_chat.id, 
                                            text= "https://telegra.ph/" + next(iter),
                                            parse_mode= "Markdown",
                                            reply_markup=InlineKeyboardMarkup(keyboard))
        

    return WIKI_CLASS

def button(update, context):

    global PJ

    keyboard1 = [[InlineKeyboardButton("¡Me gusta!", callback_data="stop")], [InlineKeyboardButton("A ver el siguiente...", callback_data="next")]]
    keyboard2 = [[InlineKeyboardButton("¡Interesante!", callback_data="para")], [InlineKeyboardButton("Bah...", callback_data="sig")]]
   
    query: CallbackQuery = update.callback_query
    query.answer()

    if "next" in query.data:

        query.edit_message_text(text= "https://telegra.ph/" + next(iter),
                                parse_mode= "Markdown",
                                reply_markup=InlineKeyboardMarkup(keyboard1))
        
    elif "stop" in query.data:

        buttons = [[KeyboardButton("¿Y qué hay de las clases?")], [KeyboardButton("Creo que ya tengo toda la información que necesitaba...")]]
        
        print(get_cycle_state(iter))

        size = len(get_cycle_state(iter))
        # Slice string to remove last 6 characters from string
        mod_string = get_cycle_state(iter)[:size - 6]

        PJ.race = mod_string
        
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                                text= "¿Todo claro?",
                                                reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True))
        return WIKI_CLASS

    elif "sig" in query.data:

        query.edit_message_text(text= "https://telegra.ph/" + next(iter2),
                                parse_mode= "Markdown",
                                reply_markup=InlineKeyboardMarkup(keyboard2))

    elif "para" in query.data:
        
        buttons = [[KeyboardButton("¡Por supuesto!")], [KeyboardButton("Me vendría bien un repaso de las razas...")], [KeyboardButton("Mejor volvamos a revisar las clases...")]]
        
        print(get_cycle_state(iter2))

        size = len(get_cycle_state(iter2))
        # Slice string to remove last 6 characters from string
        mod_string = get_cycle_state(iter2)[:size - 6]

        PJ._class = mod_string

        context.bot.send_message(chat_id=update.effective_chat.id, 
                                                text= "¿Te sientes capaz ya de crear tu personaje?",
                                                reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True))
        return BUTTON

def wiki_class (update, context):

    context.bot.sendChatAction(chat_id=update.message.chat_id , action = ChatAction.TYPING)

    time.sleep(3)

    context.bot.send_message(chat_id=update.effective_chat.id, 
                                        text="_*crepita*_",
                                        parse_mode= "Markdown",
                                        reply_markup=ReplyKeyboardRemove())
                                   

    if ("¿Y qué hay de las clases?" in update.message.text or "Anda, calla." in update.message.text or "Pero si no te cuesta nada..." in update.message.text):

        context.bot.sendSticker(chat_id=update.effective_chat.id, sticker="CAACAgIAAxkBAAEYhFxjNIR1fY6DdbT6rs_t0NaY4EMS4gACJg8AAvtZKEkiX-SE94ctpyoE") 

        time.sleep(2)

        keyboard = [[InlineKeyboardButton("¡Interesante!", callback_data="para")], [InlineKeyboardButton("Bah...", callback_data="sig")]]
    
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                            text= "https://telegra.ph/" + next(iter2),
                                            parse_mode= "Markdown",
                                            reply_markup=(InlineKeyboardMarkup(keyboard)))

    elif "Creo que ya tengo toda la información que necesitaba..." in update.message.text:

        buttons = [[KeyboardButton("Vamos allá.")], [KeyboardButton("¿Aún no hemos terminado...?")]]

        context.bot.sendChatAction(chat_id=update.message.chat_id , action = ChatAction.TYPING)

        time.sleep(2)
        
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                        text="Sigamos, pues.",
                                        reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True))

        return BUTTON

    else:

        buttons = [[KeyboardButton("¡Por supuesto!")], [KeyboardButton("Me vendría bien un repaso de las razas...")], [KeyboardButton("Mejor revisemos las clases...")]]
        
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                                text= "¿Te sientes capaz ya de crear tu personaje?",
                                                reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True))

    return BUTTON

def prename(update, context):

    context.bot.sendChatAction(chat_id=update.message.chat_id , action = ChatAction.TYPING)

    time.sleep(3)
    
    if ("¡Por supuesto!" in update.message.text or "Vamos allá." in update.message.text or "¿Aún no hemos terminado...?" in update.message.text):

        if "¿Aún no hemos terminado...?" in update.message.text:

            string = "Ya falta poco, no seas impaciente... ¿Cómo quieres llamar a tu avatar?"
        
            slow_typing(string, update, context)

        else:

            string = "Fantástico. Pero lo primero, ¿cómo quieres llamar a tu avatar?"
            
            slow_typing(string, update, context)

        context.bot.sendSticker(chat_id=update.effective_chat.id, sticker="CAACAgIAAxkBAAEYhFljNIQBEgxdE5hx_E7o7bRnUoPxLAACow4AAtayMEkaQ5BopdvXfCoE") 

        return NAME

    elif "Me vendría bien un repaso de las razas..." in update.message.text:

        buttons = [[KeyboardButton("Qué borde eres...")], [KeyboardButton("Solo quiero comprobar una cosa, no tardo nada.")]]

        context.bot.sendChatAction(chat_id=update.message.chat_id , action = ChatAction.TYPING)

        time.sleep(2)
        
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                        text="Bien, pues volvamos a verlas. Tómate tu tiempo esta vez...",
                                        reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True))

        context.bot.sendSticker(chat_id=update.effective_chat.id, sticker="CAACAgIAAxkBAAEYhFxjNIR1fY6DdbT6rs_t0NaY4EMS4gACJg8AAvtZKEkiX-SE94ctpyoE")

        return WIKI_RACE

    elif "Mejor volvamos a revisar las clases..." in update.message.text:
        
        buttons = [[KeyboardButton("Pero si no te cuesta nada...")], [KeyboardButton("Anda, calla.")]]

        context.bot.sendChatAction(chat_id=update.message.chat_id , action = ChatAction.TYPING)

        time.sleep(2)

        slow_typing("Pero si acabamos de . . . ", update, context)
        
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                        text="¿Lo dices en serio?",
                                        reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True))
        
        context.bot.sendSticker(chat_id=update.effective_chat.id, sticker="CAACAgIAAxkBAAEYhFFjNIN3GZj6IShue4wscKL6icx4fgACWxMAArshMEkz55bxMvha1CoE")

        return WIKI_CLASS

def name (update, context):

    global PJ
    
    PJ.characterName = update.message.text

    context.bot.sendChatAction(chat_id=update.message.chat_id , action = ChatAction.TYPING)

    time.sleep(3)

    if (PJ.race is None):
        
        Race =  [[KeyboardButton("Enano")], [KeyboardButton("Elfo")], [KeyboardButton("Mediano")], 
                [KeyboardButton("Humano")], [KeyboardButton("Dracónido")], [KeyboardButton("Gnomo")], 
                [KeyboardButton("Semielfo")], [KeyboardButton("Semiorco")], [KeyboardButton("Tiefling")]]

        string = "¡Estupendo!"

        slow_typing(string, update, context)

        string = "Ahora necesito saber algunas cosas más..."
        
        slow_typing(string, update, context)

        context.bot.sendChatAction(chat_id=update.message.chat_id , action = ChatAction.TYPING)

        time.sleep(2)
        
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                        text="¿A qué raza pertenece tu avatar?",
                                        reply_markup=ReplyKeyboardMarkup(Race, one_time_keyboard=True, resize_keyboard=True))

        return RACE

    buttons = [[KeyboardButton("Todo correcto.")], [KeyboardButton("No...")]]

    context.bot.send_message(chat_id=update.effective_chat.id, 
                                        text="Así que " + PJ.characterName + ", ¿verdad?",
                                        parse_mode= "Markdown",
                                        reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True))

    return RACE

def race(update, context):

    context.bot.sendChatAction(chat_id=update.message.chat_id , action = ChatAction.TYPING)

    time.sleep(3)
    
    global PJ

    if "No..." in update.message.text:
    
        string = "¿Ni siquiera eres capaz de poner tu nombre correctamente...? Lo que hay que ver. . ."
            
        slow_typing(string, update, context)

        context.bot.sendSticker(chat_id=update.effective_chat.id, sticker="CAACAgIAAxkBAAEYhGRjNIWnepm04vH4fyWvSUWy9S-rhQACxREAArCasUhdUZ2-kKVX2ioE")

        string = "Venga, inténtalo de nuevo, ¿cómo quieres llamar a tu avatar?"
            
        slow_typing(string, update, context)

        return NAME
    
    string = "Tomo nota, sí, sí..."
        
    slow_typing(string, update, context)

    string = "_Como_ _si_ _estuviese_ _escribiendo_ _algo_ _de_ _todo_ _esto,_ _ejem,_ _ejem..._" 

    slow_typing(string, update, context)

    context.bot.sendSticker(chat_id=update.effective_chat.id, sticker="CAACAgIAAxkBAAEYhGJjNIWI1omzfc1nntZBRHLqvrG2QQAC_g0AAoGJqEhLiXZ1bM9WgCoE")

    context.bot.sendChatAction(chat_id=update.message.chat_id , action = ChatAction.TYPING)

    time.sleep(2)

    buttons = [[KeyboardButton("Sí, mejor será.")], [KeyboardButton("Date prisa, o te echo un cubo de agua encima.")]]

    context.bot.send_message(chat_id=update.effective_chat.id, 
                                    text="¡Bueno! Sigamos...",
                                    parse_mode= "Markdown",
                                    reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True))

    if (PJ._class is None):
        if PJ.race is None:
            PJ.race = update.message.text

        _class =  [[KeyboardButton("Bárbaro")], [KeyboardButton("Bardo")], [KeyboardButton("Brujo")], 
                    [KeyboardButton("Clérigo")], [KeyboardButton("Druida")], [KeyboardButton("Explorador")], 
                    [KeyboardButton("Guerrero")], [KeyboardButton("Hechicero")], [KeyboardButton("Mago")], 
                    [KeyboardButton("Monje")], [KeyboardButton("Paladín")], [KeyboardButton("Pícaro")]]

        context.bot.send_message(chat_id=update.effective_chat.id, 
                                    text="¿Qué clase de " + PJ.race +  " es?",
                                    reply_markup=ReplyKeyboardMarkup(_class, one_time_keyboard=True, resize_keyboard=True))

    return CLASS

def _class(update, context):

    context.bot.sendChatAction(chat_id=update.message.chat_id , action = ChatAction.TYPING)

    time.sleep(3)

    global PJ

    if (PJ._class is None):

        PJ._class = update.message.text
        
        string = "Ahora sí que tengo curiosidad... cuéntame más acerca de " + PJ.characterName + "." + " Su historia, su aspecto físico, su forma de ser... cuanto más, mejor."
    
        slow_typing(string, update, context)

    else:

        if "Sí, mejor será." in update.message.text:
            
            string = "Hablando de cosas que debería apuntar... Dime, ¿cómo es " + PJ.characterName + "?" + " Su historia, su aspecto físico, su forma de ser... cuanto más, mejor."
        
            slow_typing(string, update, context)

        else:
            string = "¡A mí no me vengas con amenazas, eh! Que te estoy ayudando de forma altruista..."
        
            slow_typing(string, update, context)

            string = "Venga, háblame de " + PJ.characterName + "." + " Su historia, su aspecto físico, su forma de ser... cuanto más, mejor."
        
            slow_typing(string, update, context)
    
    return HISTORY    

def history(update, context):

    context.bot.sendChatAction(chat_id=update.message.chat_id , action = ChatAction.TYPING)

    time.sleep(3)

    global PJ

    if "fuerza" in PJ.salva: 
        PJ.mod['fuerza'] = str(PJ.mod['fuerza']) + "+2"

    if "destreza" in PJ.salva: 
        PJ.mod['destreza'] = str(PJ.mod['destreza']) + "+2"

    if "constitucion" in PJ.salva: 
        PJ.mod['constitucion'] = str(PJ.mod['constitucion']) + "+2"

    if "inteligencia" in PJ.salva: 
        PJ.mod['inteligencia'] = str(PJ.mod['inteligencia']) + "+2"

    if "sabiduria" in PJ.salva: 
        PJ.mod['sabiduria'] = str(PJ.mod['sabiduria']) + "+2"

    if "carisma" in PJ.salva: 
        PJ.mod['carisma'] = str(PJ.mod['carisma']) + "+2"

    string = "De acuerdo, dame un momento . . ."
    
    slow_typing(string, update, context)

    context.bot.sendSticker(chat_id=update.effective_chat.id, sticker="CAACAgIAAxkBAAEYUt9jLCeequdD2m9Rm4cuus-Rh_8wNgACvAwAAocoMEntN5GZWCFoBCkE")

    time.sleep(2)

    string = "¡Aquí tienes tu hoja de personaje!"
    
    slow_typing(string, update, context)

    PJ.updateStats()

    response = telegraph.create_page(
        "Hoja de personaje de " + PJ.characterName,
        html_content =  "<br> <b>" + "[" + PJ.race + "] [" + PJ._class + "] </b>" +
                        "<br> <i>- Creado por: " + PJ.playerName + " -</i>" + "<br>" +
                        "<br> -------------------- <b>[ Estadísticas ]</b> --------------------" + "<br>" +
                        "<br> [] Fuerza: " + str(PJ.stats['fuerza']) + " [" + str(PJ.mod['fuerza']) + "]" + 
                        "<br> [] Destreza: " + str(PJ.stats['destreza']) + " [" + str(PJ.mod['destreza']) + "]" +
                        "<br> [] Constitución: " + str(PJ.stats['constitucion']) + " [" + str(PJ.mod['constitucion']) + "]" +
                        "<br> [] Inteligencia: " + str(PJ.stats['inteligencia']) + " [" + str(PJ.mod['inteligencia']) + "]" +
                        "<br> [] Sabiduría: " + str(PJ.stats['sabiduria']) + " [" + str(PJ.mod['sabiduria']) + "]" + 
                        "<br> [] Carisma: " + str(PJ.stats['carisma']) + " " + " [" + str(PJ.mod['carisma']) + "]" + "<br>"
                        "<br> -------------------- <b>[ Combate ]</b> --------------------" + "<br>" +
                        "<br> [] Clase de Armadura: " + str(PJ.stats['CA']) + 
                        "<br> [] Puntos de golpe: " + str(PJ.stats['PG']) + 
                        "<br> [] Dado: " + str(PJ.dice) + "<br>" +
                        "<br> -------------------- <b>[ Historia ]</b> --------------------" + "<br>" +
                        "<br>" + update.message.text 
    )

    context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=response['url'],
                                parse_mode= "Markdown")

    context.bot.sendChatAction(chat_id=update.message.chat_id , action = ChatAction.TYPING)

    time.sleep(3)

    string = "Ahora ya estás listo para empezar."
    
    slow_typing(string, update, context)

    string = "Para crear otro personaje o volver a consultar la información de razas y clases, solo tienes que escribir /start."
    
    slow_typing(string, update, context)

    return ConversationHandler.END

def cancel(update, context):
    #Cancels and ends the conversation.
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)

    context.bot.sendChatAction(chat_id=update.message.chat_id , action = ChatAction.TYPING)

    time.sleep(2)
    
    update.message.reply_text(
        "De acuerdo, nos vemos la próxima vez.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

def slow_typing(string, update, context):

    lst = []
    txt = "— "

    lst = string.split()

    print(lst)

    msg = context.bot.send_message(chat_id=update.effective_chat.id,
                                    text = txt)

    for i in lst:

        txt = txt + i + " "
        
        context.bot.sendChatAction(chat_id=update.message.chat_id , action = ChatAction.TYPING)

        time.sleep(0.2)

        context.bot.edit_message_text(chat_id=update.message.chat_id, 
                                            message_id=msg.message_id,
                                            text=txt,
                                            parse_mode= "Markdown")

        if("." in i):
            time.sleep(1.3)
            print("Hay un punto")

        elif ("," in i):
            time.sleep(0.8)
            print("Hay una coma")

def main():

    updater = Updater(token= token)
    dispatcher = updater.dispatcher

    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        fallbacks=[CommandHandler('cancel', cancel)],

        states={
            TYPE: [MessageHandler(Filters.text & (~ Filters.command), type)],
            WIKI_RACE: [MessageHandler(Filters.text & (~ Filters.command), wiki_race)],
            WIKI_CLASS: [MessageHandler(Filters.text & (~ Filters.command), wiki_class)],
            BUTTON: [MessageHandler(Filters.text & (~ Filters.command), prename)],
            NAME: [MessageHandler(Filters.text & (~ Filters.command), name)],
            RACE: [MessageHandler(Filters.text & (~ Filters.command), race)],
            CLASS: [MessageHandler(Filters.text & (~ Filters.command), _class)],
            HISTORY: [MessageHandler(Filters.text & (~ Filters.command), history)]
        },
    )

    # log all errors
    dispatcher.add_error_handler(error)

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
