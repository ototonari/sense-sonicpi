#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import RPi.GPIO as GPIO
import time
from psonic import *


# HIGH or LOWの時計測
def pulseIn(PIN, start=1, end=0):
    if start==0: end = 1
    t_start = 0
    t_end = 0
    # ECHO_PINがHIGHである時間を計測
    while GPIO.input(PIN) == end:
        t_start = time.time()
        
    while GPIO.input(PIN) == start:
        t_end = time.time()
    return t_end - t_start

# 距離計測
def calc_distance(TRIG_PIN, ECHO_PIN, num, v=34000): 
    avg = 10
    fout = open('inputValues.txt','wt')
    for i in range(num):
        # time.sleep()の値で音がなる間隔が変わる（超音波センサーで距離を測る間隔が変わる）
        GPIO.output(TRIG_PIN, GPIO.LOW)
        time.sleep(0.5)
        # TRIGピンを0.00001[s]だけ出力(超音波発射)        
        GPIO.output(TRIG_PIN, True)
        time.sleep(0.00001)
        GPIO.output(TRIG_PIN, False)
        # HIGHの時間計測
        t = pulseIn(ECHO_PIN)
        # ここから超音波センサーの値を扱う
        # 距離[cm] = 音速[cm/s] * 時間[s]/2
        distance = int(int(v * t/2) / 5)
        # 値の整形 一つ前の値と比較してプラスマイナス４０％以内
        if ((avg + 10) > distance) and ((avg - 10) < distance):
                
            print(distance*5, "cm")
        # play()この関数に渡す引数の値によって鳴る音が変わる
            play(distance + 59)
            avg = distance 
        else:
            print(avg*5, "cm*")
            play(avg + 59)
        
        
    fout.close()	
    # ピン設定解除
    GPIO.cleanup()

# TRIGとECHOのGPIO番号   
TRIG_PIN = 14
ECHO_PIN = 15
# ピン番号をGPIOで指定
GPIO.setmode(GPIO.BCM)
# TRIG_PINを出力, ECHO_PINを入力
GPIO.setup(TRIG_PIN,GPIO.OUT)
GPIO.setup(ECHO_PIN,GPIO.IN)
GPIO.setwarnings(False)

use_synth(PROPHET)
# 距離計測(TRIGピン番号, ECHO_PIN番号, 計測回数, 音速[cm/s])
calc_distance(TRIG_PIN, ECHO_PIN, 10, 34000)
