#! /usr/bin/env python

import time, signal, sys
import RPi.GPIO as GPIO
from Adafruit_ADS1x15 import ADS1x15
import pygame.mixer

alarm_on_volt = 2.0
switch_pin=9
alarm_music = "music.mp3"
play_time = 120
play_volume = 100

ADS1015 = 0x00
ADS1115 = 0x01
gain = 4096
sps = 250
adc = ADS1x15(ic=ADS1015)

reset_flag = 1

GPIO.cleanup()
GPIO.setmode( GPIO.BCM )
GPIO.setup( switch_pin, GPIO.IN )

pygame.mixer.init()
pygame.mixer.music.load( alarm_music )
pygame.mixer.music.set_volume( play_volume/100 )

while True:
    if GPIO.input( switch_pin ) == GPIO.HIGH :
        volts = adc.readADCSingleEnded( 0, gain, sps ) / 1000
        if ( volts > alarm_on_volt ) and ( reset_flag == 1 ):
            reset_flag = 0
            pygame.mixer.music.play( -1 )
            st = time.time()
            while st + play_time > time.time():
                time.sleep( 1 )
        else:
            pygame.mixer.music.stop()
    else: 
        reset_flag = 1
    
    time.sleep( 0.1 )
