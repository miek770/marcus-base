# -*- coding: utf-8 -*-

# Librairies standards
#======================
import logging

# Librairies spéciales
#======================
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.ADC as ADC

# Dictionnaire de pins digitales
#================================

# pins[index] = in/out

pins = dict()
pins['P8_7'] = None # Bumper - Avant droit
pins['P8_8'] = None # Bumper - Avant gauche
pins['P8_9'] = None # Bumper - Arrière droit
pins['P8_10'] = None # Bumper - Arrière gauche
pins['P8_11'] = None # Reservee pour unittest
pins['P8_12'] = None
pins['P8_13'] = None # Peut être utilisée en PWM
pins['P8_14'] = None
pins['P8_15'] = None
pins['P8_16'] = None
pins['P8_17'] = None
pins['P8_18'] = None
pins['P8_19'] = None # Peut être utilisée en PWM
pins['P8_26'] = None # Non-testée
pins['P8_27'] = None # Non-testée
pins['P8_28'] = None # Non-testée
pins['P8_29'] = None # Non-testée
pins['P8_30'] = None # Non-testée
pins['P8_31'] = None # Non-testée
pins['P8_32'] = None # Non-testée
pins['P8_33'] = None # Non-testée
pins['P8_34'] = None # Non-testée
pins['P8_35'] = None # Non-testée
pins['P8_36'] = None # Non-testée
pins['P8_37'] = None # Non-testée
pins['P8_38'] = None # Non-testée
pins['P8_39'] = None # Non-testée
pins['P8_40'] = None # Non-testée
pins['P8_41'] = None # Non-testée
pins['P8_42'] = None # Non-testée
pins['P8_43'] = None # Non-testée
pins['P8_44'] = None # Non-testée
pins['P8_45'] = None # Non-testée
pins['P8_46'] = None # Non-testée
pins['P9_11'] = None
pins['P9_12'] = None # Direction moteur droit
pins['P9_13'] = None # Direction moteur droit
pins['P9_14'] = None # Enable moteur droit (PWM)
pins['P9_15'] = None # Direction moteur gauche
pins['P9_16'] = None # Enable moteur gauche (PWM)
pins['P9_21'] = None # Direction moteur gauche
pins['P9_22'] = None
pins['P9_23'] = None
#pins['P9_24'] = None # Réservée pour UART1
pins['P9_25'] = None
#pins['P9_26'] = None # Réservée pour UART1
pins['P9_27'] = None
pins['P9_28'] = None
pins['P9_29'] = None
pins['P9_30'] = None
pins['P9_31'] = None
pins['P9_42'] = None

# Pins analogiques
#==================
# P9_39 - AIN0 # GP2D12 avant milieu
# P9_40 - AIN1 # GP2D12 avant gauche
# P9_37 - AIN2 # GP2D12 avant droite
# P9_38 - AIN3
# P9_33 - AIN4
# P9_36 - AIN5
# P9_35 - AIN6
#ADC.setup()

#======================================================================
# Fonction :    set_low(pin)
# Description : Regle la pin digitale a 0V.
#======================================================================
def set_low(pin):
    # Vérifie si la pin est configurée en sortie
    if pins[pin] == 'out':
        GPIO.output(pin, GPIO.LOW)

    elif pins[pin] == 'in':
        logging.error("{} est configurée en entrée".format(pin))

    else:
        logging.error("{} n'est pas configurée correctement".format(pin))

#======================================================================
# Fonction :    set_high(pin)
# Description : Regle la pin digitale a 3.3V.
#======================================================================
def set_high(pin):
    # Vérifie si la pin est configurée en sortie
    if pins[pin] == 'out':
        GPIO.output(pin, GPIO.HIGH)

    elif pins[pin] == 'in':
        logging.error("{} est configurée en entrée".format(pin))

    else:
        logging.error("{} n'est pas configurée correctement".format(pin))

#======================================================================
# Fonction :    set_output(pin)
# Description : Configure la pin en mode sortie.
#======================================================================
def set_output(pin):
    GPIO.setup(pin, GPIO.OUT)
    pins[pin] = 'out'

    # Met la pin à 3.3V (high) par défaut
    set_high(pin)

#======================================================================
# Fonction :    set_input(pin)
# Description : Configure la pin en mode entrée.
#======================================================================
def set_input(pin):
    GPIO.setup(pin, GPIO.IN)
    pins[pin] = 'in'

#======================================================================
# Fonction :    get_input(pin)
# Description : Retourne la valeur de la pin.
#======================================================================
def get_input(pin):
    return GPIO.input(pin)

#======================================================================
# Fonction :    get_adc(pin)
# Description : Retourne une valeur entre 0 et 1 correspondant à une
#               lecture
#               entre 0 et 3,3V.
#======================================================================
def get_adc(pin):
    ADC.read(pin)
    reading = ADC.read(pin)
    return reading
