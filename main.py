#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from subprocess import Popen

TIME=15
GIORNO_SUCCESSIVO=5

def Execute(target):#avvia un client
    Popen(["python3",target + ".py"])
    
def Main():#avvia tutti i client all' infinito
    counter=0
    print("Stazioni IOT operative...\n")
    while True:
        
        counter+=1
        print("Giorno %d  \n"%(counter))
        time.sleep(2)
        Execute("stazione1")
        time.sleep(TIME)
        print()
        time.sleep(2)
        Execute("stazione2")
        time.sleep(TIME)
        print()
        time.sleep(2)
        Execute("stazione3")
        time.sleep(TIME)
        print()
        time.sleep(2)
        Execute("stazione4")
        time.sleep(GIORNO_SUCCESSIVO)
        print("\n\n\n")
    
#AVVIO CLIENT
Main()