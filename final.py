#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from gs_flight import FlightController, CallbackEvent
from gs_board import BoardManager
from time import sleep

rospy.init_node("flight_test_node")  # инициализируем ноду

coordinates = [ # массив координат точе
    [2.7,4.6,1.7], #1
    [0.15,4.4,1.7], #2
    [0.4,2.3,1.7], #3
    [0.6,0.1,1.7], #4
    [2.6,2.3,1.7], #5
    [2.6,2.3,1.7], #6
    [2.3,3.4,1.7], #7
    [1.4,4.4,1.7], #8
    [0.5,3.55,1.7], #9
    [0.5,1.2,1.7], #10
    [1.3,0.4,1.7], #11
    [0.6,5.2,1.7], #12
    [0.15,3.6,1.7], #13
    [0.1,1.3,1.7], #14
    [1.2,0.5,1.7], #15
    [1.33,1.3,0.93], # пасадка 
]
run = True # переменная отвечающая за работу программы
position_number = 0 # счетчик пройденных точек

def callback(event): # функция обработки событй Автопилота
    global ap
    global run
    global coordinates
    global position_number

    event = event.data
    if event == CallbackEvent.ENGINES_STARTED: # блок обработки события запуска двигателя
        print("engine started")
        ap.takeoff() # отдаем команду взлета
    elif event == CallbackEvent.TAKEOFF_COMPLETE: # блок обработки с обытия завершения взлета
        moduleLed.changeAllColor(0.0,255.0,0.0)
        rospy.sleep(1)
        moduleLed.changeAllColor(0.0,0.0,0.0)
        print("takeoff complite")
        position_number = 0
        ap.goToLocalPoint(coordinates[position_number][0], coordinates[position_number][1], coordinates[position_number][2])

    elif event == CallbackEvent.POINT_REACHED: # блок обработки события достижения точки
        rospy.sleep(0.6)
        print(f"point {position_number} reached")
        position_number += 1 # наращиваем счетчик точек
        if position_number < len(coordinates): # проверяем количество текущее количество точек с количеством точек в полетном задании
            ap.goToLocalPoint(coordinates[position_number][0], coordinates[position_number][1], coordinates[position_number][2])   

        else:
            ap.deserve() # отдаем команду посадки
    elif event == CallbackEvent.COPTER_LANDED: # блок обработки события приземления
        print("finish programm")
        run = False # прекращем программу

board = BoardManager() # создаем объект бортового менеджера
ap = FlightController(callback) # создаем объект управления полета

once = False # переменная отвечающая за первое вхождение в начало программы

while not rospy.is_shutdown() and run:
    if board.runStatus() and not once: # проверка подлкючения RPi к Пионеру
        print("start programm")
        ap.preflight() # отдаем команду выполенения предстартовой подготовки
        once = True
    pass
