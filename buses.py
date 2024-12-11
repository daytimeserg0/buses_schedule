import random
import re
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.patheffects import withStroke
from matplotlib.patches import Rectangle
import tkinter as tk
from tkinter import simpledialog

def run_simulation(visualisation, driver_list, bus_list):
    station_1_free_positions = [True] * 9  # Две станции для автобусов
    station_2_free_positions = [True] * 9

    angry_passengers = 0  # Счетчик недовольных пассажиров
    spent_money = 0  # Счетчик потраченных денег

    class Bus:
        def __init__(self, stops, station_1_positions, station_2_positions, bus_number):
            """
            Инициализация автобуса.
            """
            self.x = 0
            self.y = 0
            self.driver = False # Водитель автобуса(при инициализации отсутсвует)
            self.num = bus_number # Номер автобуса
            self.time_in_drive = 0 # Время в пути между остановками
            self.capacity = 50 # Вместимость автобуса
            self.passengers = 0 # Количество пассажиров в автобусе
            self.stops = stops  # Список координат остановок
            self.current_stop = 0  # Индекс текущей остановки
            self.station_1_positions = station_1_positions
            self.station_2_positions = station_2_positions
            self.station_1_position_index = None
            self.station_2_position_index = None
            self.stay_on_station()
            if visualisation:
                self.driver_marker = ax.text(0, 0, '',
                                           color='black', fontsize=12, ha='left', zorder=10)
                self.passengers_marker = ax.text(0, 0, '',
                                           color='black', fontsize=12, ha='left', zorder=10)



        def move_to_next_stop(self):
            """
            Перемещает автобус к следующей остановке.
            """
            if not self.driver:
                pass
            else:

                # Освобождение позиций на парковке если были заняты
                if self.station_1_position_index is not None:
                    station_1_free_positions[self.station_1_position_index] = True
                    self.station_1_position_index = None
                if self.station_2_position_index is not None:
                    station_2_free_positions[self.station_2_position_index] = True
                    self.station_2_position_index = None

                if self.current_stop == 28: # Если сделали круг обнуляем остановку
                    self.current_stop = 0

                if self.current_stop < len(self.stops):
                    self.x, self.y = self.stops[self.current_stop]
                    self.current_stop += 1
                    # Обновляем позицию автобуса
                    if visualisation:
                        self.bus_marker.set_data([self.x], [self.y])  # Передаем x и y как списки
                        self.text_marker.set_position((self.x, self.y + 0.6))
                        self.driver_marker.set_text(f'{self.driver.name}')
                        self.driver_marker.set_position((self.x, self.y + 1.6))
                        self.passengers_marker.set_text((f'Passengers: {self.passengers}'))
                        self.passengers_marker.set_position((self.x, self.y + 2.6))
                else:
                    self.current_stop = 0
                    self.move_to_next_stop()

        def move_to_station(self):
            if self.station_1_position_index is not None or self.station_2_position_index is not None:
                pass
            else:
                if self.current_stop == 28: # Если сделали круг обнуляем остановку
                    self.current_stop = 0
                if self.current_stop != 0 and self.current_stop != 14:
                    if self.current_stop < len(self.stops):
                        self.x, self.y = self.stops[self.current_stop]
                        self.current_stop += 1
                        # Обновляем позицию автобуса
                        if visualisation:
                            self.bus_marker.set_data([self.x], [self.y])  # Передаем x и y как списки
                            self.text_marker.set_position((self.x, self.y + 0.6))
                            self.driver_marker.set_text(f'{self.driver.name}')
                            self.driver_marker.set_position((self.x, self.y + 1.6))
                            self.passengers_marker.set_text((f'Passengers: {self.passengers}'))
                            self.passengers_marker.set_position((self.x, self.y + 2.6))
                    else:
                        self.current_stop = 0
                else:
                    if self.stops[self.current_stop] == (0, 0):
                        for i in range(len(self.station_1_positions)):
                            if station_1_free_positions[i] == True:
                                self.station_position_x = self.station_1_positions[i][0]
                                self.station_position_y = self.station_1_positions[i][1]
                                if visualisation:
                                    self.bus_marker.set_data([self.station_position_x], [self.station_position_y])
                                    self.text_marker.set_position((self.station_position_x, self.station_position_y + 0.6))
                                    self.driver_marker.set_text(f'')
                                    self.passengers_marker.set_text(f'')
                                self.passengers = 0
                                station_1_free_positions[i] = self
                                self.station_1_position_index = i
                                break
                            else:
                                continue
                    elif self.stops[self.current_stop] == (19, 9):
                        for i in range(len(self.station_2_positions)):
                            if station_2_free_positions[i] == True:
                                self.station_position_x = self.station_2_positions[i][0]
                                self.station_position_y = self.station_2_positions[i][1]
                                if visualisation:
                                    self.bus_marker.set_data([self.station_position_x], [self.station_position_y])
                                    self.text_marker.set_position((self.station_position_x, self.station_position_y + 0.6))
                                    self.driver_marker.set_text(f'')
                                    self.passengers_marker.set_text(f'')
                                self.passengers = 0
                                station_2_free_positions[i] = self
                                self.station_2_position_index = i
                                break
                            else:
                                continue

        def stay_on_station(self):
            # Создаём эффект для текста с чёрной окантовкой
            if visualisation:
                stroke_effect = withStroke(linewidth=2, foreground='black')

            # Cоздаем объект для отображения автобуса(изначально на станции)
            if self.stops[0] == (0, 0):
                for i in range(len(self.station_1_positions)):
                    if station_1_free_positions[i] == True:
                        self.station_position_x = self.station_1_positions[i][0]
                        self.station_position_y = self.station_1_positions[i][1]
                        if visualisation:
                            self.bus_marker, = ax.plot([self.station_position_x], [self.station_position_y], 'go',
                                                        color='orange',
                                                        markersize=15, path_effects=[stroke_effect])  # Оранжевая точка для автобуса
                        station_1_free_positions[i] = self
                        self.station_1_position_index = i
                        break
                    else:
                        continue
            else:
                for i in range(len(self.station_2_positions)):
                    if station_2_free_positions[i] == True:
                        self.station_position_x = self.station_2_positions[i][0]
                        self.station_position_y = self.station_2_positions[i][1]
                        if visualisation:
                            self.bus_marker, = ax.plot([self.station_position_x], [self.station_position_y], 'go',
                                                        color='orange',
                                                        markersize=15, path_effects=[stroke_effect])  # Оранжевая точка для автобуса
                        station_2_free_positions[i] = self
                        self.station_2_position_index = i
                        break
                    else:
                        continue
            if visualisation:
                self.text_marker = ax.text(self.station_position_x, self.station_position_y + 0.6, f'№{self.num}',
                                            color='orange', fontsize=12, ha='left', zorder=10,
                                           path_effects=[stroke_effect])

        def get_passengers_in_and_out(self, passengers_number_in):
            nonlocal angry_passengers
            angry_people = 0
            self.passengers -= random.randint(0 , self.passengers) # Люди, которые выходят из автобуса
            self.passengers += passengers_number_in
            if self.passengers > self.capacity:
                angry_people += self.passengers - self.capacity
                self.passengers = self.capacity

            angry_passengers += angry_people # Обновляем глобальный счетчик недовольных людей
            return angry_people



    class DriverType1:
        def __init__(self, name, start_time, end_time, start_break_time, end_break_time, location, weekend_days=[]):
            self.name = name
            self.type = 1
            self.start_time = start_time
            self.end_time = end_time
            self.start_break_time = start_break_time
            self.end_break_time = end_break_time
            self.location = location # На какой станции водитель будет брать автобус
            self.weekend_days = weekend_days
            self.bus_number = None
            self.is_working = False

        def chek_for_bus(self):
            self.chek_for_work()
            # Проверка на то, находится ли автобус на одной из станций, если да, то выходить из него
            for i in range(len(station_1_free_positions)):
                if station_1_free_positions[i] != True and station_1_free_positions[i].num == self.bus_number:
                    station_1_free_positions[i].driver = False
                    self.bus_number = None
                    self.location = 'station 1'
                    break
                elif station_2_free_positions[i] != True and station_2_free_positions[i].num == self.bus_number:
                    station_2_free_positions[i].driver = False
                    self.bus_number = None
                    self.location = 'station 2'
                    break

            if self.location == 'bus':
                pass
            elif self.location == 'station 1' and self.is_working == True:
                for i in range(len(station_1_free_positions)):
                    if station_1_free_positions[i] != True:
                        station_1_free_positions[i].driver = self
                        self.bus_number = station_1_free_positions[i].num
                        self.location = 'bus'
                        break
            elif self.location == 'station 2' and self.is_working == True:
                for i in range(len(station_2_free_positions)):
                    if station_2_free_positions[i] != True:
                        station_2_free_positions[i].driver = self
                        self.bus_number = station_2_free_positions[i].num
                        self.location = 'bus'
                        break


        def chek_for_work(self):
            nonlocal time
            if day_of_week in self.weekend_days:
                self.is_working = False
            else:
                if time == self.start_time:
                    self.is_working = True
                elif time == self.end_time:
                    self.is_working = False

                if time == self.start_break_time:
                    self.is_working = False
                elif time == self.end_break_time:
                    self.is_working = True

    class DriverType2:
        def __init__(self, name, start_time, end_time, location, starts_from=1):
            self.name = name
            self.type = 2
            self.start_time = start_time
            self.end_time = end_time
            self.location = location # На какой станции водитель будет брать автобус
            self.starts_from = starts_from # День с которого водитель выходит на работу
            self.start_break_time = None
            self.end_break_time = None
            self.bus_number = None
            self.is_working = False

        def chek_for_bus(self):
            self.chek_for_work()
            # Проверка на то, находится ли автобус на одной из станций, если да, то выходить из него
            for i in range(len(station_1_free_positions)):
                if station_1_free_positions[i] != True and station_1_free_positions[i].num == self.bus_number:
                    station_1_free_positions[i].driver = False
                    self.bus_number = None
                    self.location = 'station 1'
                    break
                elif station_2_free_positions[i] != True and station_2_free_positions[i].num == self.bus_number:
                    station_2_free_positions[i].driver = False
                    self.bus_number = None
                    self.location = 'station 2'
                    break

            if self.location == 'bus':
                pass
            elif self.location == 'station 1' and self.is_working == True:
                for i in range(len(station_1_free_positions)):
                    if station_1_free_positions[i] != True:
                        station_1_free_positions[i].driver = self
                        self.bus_number = station_1_free_positions[i].num
                        self.location = 'bus'
                        break
            elif self.location == 'station 2' and self.is_working == True:
                for i in range(len(station_2_free_positions)):
                    if station_2_free_positions[i] != True:
                        station_2_free_positions[i].driver = self
                        self.bus_number = station_2_free_positions[i].num
                        self.location = 'bus'
                        break

        def chek_for_work(self):
            nonlocal time
            nonlocal days
            if days >= self.starts_from:
                if days % 3 == self.starts_from % 3:
                    if time == self.start_time:
                        self.is_working = True

                if time == self.end_time:
                    self.is_working = False

                if self.start_break_time is not None and self.end_break_time is not None:
                    if time == self.start_break_time:
                        self.is_working = False
                    elif time == self.end_break_time:
                        self.is_working = True
                        self.start_break_time = None
                        self.end_break_time = None

        def set_break_time(self, start, end):
            self.start_break_time = start
            self.end_break_time = end
            #self.chek_for_work()

    class Stop:
        def __init__(self, stop_coords, stop_num):
            self.x = stop_coords[0]
            self.y = stop_coords[1]
            self.stop_num = stop_num
            self.people = 0
            self.max_people = 30
            self.information = [] # Информация о прибытии автобусов


        def get_people(self):
            nonlocal angry_passengers
            if self.people > 0:
                angry_people = random.randint(0, 1) # Недовольные люди, которые уходят
                self.people -= angry_people
                angry_passengers += angry_people # Обновляем глобальный счетчик недовольных людей

            self.people += random.randint(0, 20)  # Добавление людей на остановку
            if self.people > self.max_people:
                angry_passengers += self.people - self.max_people  # Обновляем глобальный счетчик недовольных людей
                self.people = self.max_people

        def get_data(self, bus_num, driver, angry_people):
            info = f'Stop №{self.stop_num}, Bus №{bus_num}, {driver}, day of week - {day_of_week}, time - {time}, people didnt get a place - {angry_people}'
            self.information.append(info)

        # Функция для вывода информации о прибытии автобусов на конкретную остановку
        def show_info(self):
            for info_string in self.information:
                print(info_string)

    # Координаты остановок (пример маршрута)
    stops = [
        (0, 0), (1, 1), (1, 3), (3, 2), (5, 5), (4, 7), (8, 6), (10, 6),
        (12, 6), (11, 7), (12, 8), (10, 10), (14, 13), (17, 13), (19, 9),
        (21, 7), (21, 5), (22, 3), (19, 3), (17, 1), (15, 4), (13, 3),
        (10, 3), (8, 3), (6, 2), (5, 1), (3, 1), (2, 0), (0, 0)
    ]

    stops_from_other_station = [
        (19, 9), (21, 7), (21, 5), (22, 3), (19, 3), (17, 1), (15, 4),
        (13, 3), (10, 3), (8, 3), (6, 2), (5, 1), (3, 1), (2, 0), (0, 0),
        (1, 1), (1, 3), (3, 2), (5, 5), (4, 7), (8, 6), (10, 6), (12, 6),
        (11, 7), (12, 8), (10, 10), (14, 13), (17, 13)
    ]

    end_stops = [(0, 0), (19, 9)]

    # Места для автобусов на конечных
    station_1_positions = [
        (-2, 0), (-4, 0), (-6, 0), (-2, -2), (-4, -2), (-6, -2),
        (-2, -4), (-4, -4), (-6, -4)
    ]

    station_2_positions = [
        (21, 9), (23, 9), (25, 9), (21, 11), (23, 11), (25, 11),
        (21, 13), (23, 13), (25, 13)
    ]

    stops_objects = [] # Массив остановок как объектов
    #Создание объектов всех остановок
    for i in range(len(stops_from_other_station)):
        stops_objects.append(Stop(stops[i], i + 1))


    is_paused = False # Переменная для паузы анимации
    speed = 1 # Переменная для определения скорости анимации

    # Функция для свитча переменная паузы
    def on_pause_button_click(event):
        nonlocal is_paused
        is_paused = not is_paused

    # Функция для изменения скорости анимации
    def on_speed_button_click(event):
        nonlocal speed
        root = tk.Tk()  # Создаём основное окно
        root.withdraw()  # Прячем основное окно, чтобы показывалось только диалоговое окно

        # Всплывающее окно для ввода числа
        value = simpledialog.askfloat("Введите число", "Введите число от 0.5 до 50:",
                                      minvalue=0.5, maxvalue=50)
        if value is not None:  # Проверяем, что пользователь ввёл число
            speed = 1 / value
        root.destroy()  # Закрываем tkinter окно

    # Функция для добавления автобуса
    def on_bus_button_click(event):
        root = tk.Tk()  # Создаём основное окно
        root.withdraw()  # Прячем основное окно, чтобы показывалось только диалоговое окно

        # Всплывающее окно для ввода станции
        station = simpledialog.askinteger("Введите станцию", "Введите станцию (1 или 2):",
                                      minvalue=1, maxvalue=2)

        if station in [1, 2]:
            add_bus(station)

        root.destroy()  # Закрываем tkinter окно

    # Функция для добавления водителя
    def on_driver_button_click(event):
        root = tk.Tk()  # Создаём основное окно
        root.withdraw()  # Прячем основное окно, чтобы показывалось только диалоговое окно

        # Всплывающее окно для ввода станции
        type = simpledialog.askinteger("Введите тип водителя", "Введите тип водителя (1 или 2):",
                                        minvalue=1, maxvalue=2)

        station = simpledialog.askinteger("Введите станцию", "Введите станцию (1 или 2):",
                                      minvalue=1, maxvalue=2)

        start_time = simpledialog.askstring("Введите время начала работы", "Введите время начала работы в формате(00:00):")

        if not re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", start_time): # Проверка правильности введенного формата
            print('Неправильно задан формат времени')
            return

        start_break_time = None
        end_break_time = None
        if type == 1:
            start_break_time = simpledialog.askstring("Введите время начала перерыва", "Введите время начала перерыва (с 13:00 до 15:00):")
            if not re.fullmatch(r"^(13:[0-5]\d|14:[0-5]\d|15:00)$", start_break_time):
                print('Неправильно указано время начала перерыва')
                return

            end_break_time = simpledialog.askstring("Введите время конца перерыва", "Введите время конца перерыва (с 14:00 до 16:00):")
            if not re.fullmatch(r"^(14:[0-5]\d|14:[0-5]\d|16:00)$", end_break_time):
                print('Неправильно указано время конца перерыва')
                return

        end_time = simpledialog.askstring("Введите время конца работы", "Введите время конца работы в формате(00:00):")

        if not re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", end_time):  # Проверка правильности введенного формата
            print('Неправильно задан формат времени')
            return

        add_driver(type, start_time, end_time, start_break_time, end_break_time, station)
        root.destroy()  # Закрываем tkinter окно

    # Функция для отображения списка водителей
    def on_driver_list_button_click(event):
        root = tk.Tk()  # Создаём основное окно
        root.title("Driver List")  # Устанавливаем заголовок окна

        # Текстовое поле для вывода информации
        text_widget = tk.Text(root, wrap=tk.WORD, width=80, height=20)
        text_widget.pack(padx=10, pady=10)

        # Формируем строки информации о водителях
        information_list = []
        for driver in drivers:
            if driver.type == 1:
                information = (
                    f"Name: {driver.name}, "
                    f"Type: {driver.type}, "
                    f"Start Time: {driver.start_time}, "
                    f"End Time: {driver.end_time}, "
                    f"Start Break Time: {driver.start_break_time}, "
                    f"End Break Time: {driver.end_break_time}"
                )
            else:
                information = (
                    f"Name: {driver.name}, "
                    f"Type: {driver.type}, "
                    f"Start Time: {driver.start_time}, "
                    f"End Time: {driver.end_time}"
                )
            information_list.append(information)

        # Вставляем информацию в текстовый виджет
        for info in information_list:
            text_widget.insert(tk.END, info + "\n\n")

        # Делаем текстовое поле только для чтения
        text_widget.config(state=tk.DISABLED)


    # Функция для добавления автобуса
    def add_bus(station):
        nonlocal spent_money

        if station == 1:
            buses.append(Bus(stops, station_1_positions, station_2_positions, bus_number=len(buses) + 1))
        else:
            buses.append(Bus(stops_from_other_station, station_1_positions, station_2_positions, bus_number=len(buses) + 1))

        spent_money += 5000000  # Цена одного автобуса условно 5м

    # Функция для добавления водителя
    def add_driver(type, start_time, end_time, start_break_time, end_break_time, station):
        nonlocal spent_money

        if type == 1:
            if station == 1:
                drivers.append(DriverType1(name=f'Driver {len(drivers) + 1}', start_time=start_time, end_time=end_time,
                            start_break_time=start_break_time, end_break_time=end_break_time,
                            location="station 1", weekend_days=['Saturday', 'Sunday']))
            else:
                drivers.append(DriverType1(name=f'Driver {len(drivers) + 1}', start_time=start_time, end_time=end_time,
                                           start_break_time=start_break_time, end_break_time=end_break_time,
                                           location="station 2", weekend_days=['Saturday', 'Sunday']))
            spent_money += 100000
        else:
            if station == 1:
                drivers.append(DriverType2(name=f'Driver {len(drivers) + 1}', start_time=start_time, end_time=end_time,
                                           location="station 1", starts_from=days))
            else:
                drivers.append(DriverType2(name=f'Driver {len(drivers) + 1}', start_time=start_time, end_time=end_time,
                                           location="station 2", starts_from=days))
            spent_money += 60000


    # Координаты начальной и конечной остановок
    end_stop_x, end_stop_y = zip(*end_stops)

    # Разделяем координаты для построения
    x_coords, y_coords = zip(*stops)

    stops.pop() # Удаление последней остановки, так как совпадает с первой

    # Создаём фигуру и оси
    if visualisation:
        fig, ax = plt.subplots()
        plt.subplots_adjust(bottom=0.2)  # Увеличиваем нижний отступ, чтобы разместить кнопку

        # Рисуем прямоугольники вокруг каждой позиции станции 1
        for (x, y) in station_1_positions:
            rect = Rectangle((x - 0.5, y - 0.5), 1, 1, linewidth=1, edgecolor='green', facecolor='none', linestyle='--')
            ax.add_patch(rect)

        # Рисуем прямоугольники вокруг каждой позиции станции 2
        for (x, y) in station_2_positions:
            rect = Rectangle((x - 0.5, y - 0.5), 1, 1, linewidth=1, edgecolor='green', facecolor='none', linestyle='--')
            ax.add_patch(rect)

        # Добавляем кнопку паузы
        pause_button_ax = plt.axes([0.48, 0.05, 0.2, 0.075])  # [лево, низ, ширина, высота]
        pause_button = Button(pause_button_ax, 'Pause/Continue')
        pause_button.on_clicked(on_pause_button_click)

        # Добавляем кнопку изменения скорости анимации
        speed_button_ax = plt.axes([0.7, 0.05, 0.2, 0.075])  # [лево, низ, ширина, высота]
        speed_button = Button(speed_button_ax, 'Enter speed')
        speed_button.on_clicked(on_speed_button_click)

        # Добавляем кнопку добавления автобуса
        bus_button_ax = plt.axes([0.26, 0.05, 0.2, 0.075])  # [лево, низ, ширина, высота]
        bus_button = Button(bus_button_ax, 'Add Bus')
        bus_button.on_clicked(on_bus_button_click)

        # Добавляем кнопку добавления водителя
        driver_button_ax = plt.axes([0.04, 0.05, 0.2, 0.075])  # [лево, низ, ширина, высота]
        driver_button = Button(driver_button_ax, 'Add Driver')
        driver_button.on_clicked(on_driver_button_click)

        # Добавляем кнопку вывода списка водителей
        driver_list_button_ax = plt.axes([0.04, 0.7, 0.2, 0.075])  # [лево, низ, ширина, высота]
        driver_list_button = Button(driver_list_button_ax, 'Drivers List')
        driver_list_button.on_clicked(on_driver_list_button_click)

        # Построение маршрута
        ax.plot(x_coords, y_coords, color='b', linestyle='-', linewidth=2)

        # Точки остановок
        ax.scatter(x_coords, y_coords, color='b', label='Bus stop', s=50, zorder=5)

        # Пометка начальной остановки
        ax.scatter(end_stop_x, end_stop_y, color='green', s=50, label='Bus station', zorder=5)  # Зелёная точка
        #plt.text(end_stop_x, int(end_stop_y) + 0.3, "Start", color='green', fontsize=10, ha='center')

    # Таймер на графике
    time = "00:00"
    day_of_week = 'Monday'
    if visualisation:
        time_text = ax.text(-10, 15, f"Time: {time}", color='black', fontsize=12, ha='left')
        day_of_week_text = ax.text(-10, 13, f"{day_of_week}", color='black', fontsize='12', ha='left')
        day_text = ax.text(-10, 14, "Day: 1", color='black', fontsize=12, ha='left')

    drivers = [] # Массив водителей
    for driver_info in driver_list:
        if driver_info['type'] == 1:
            drivers.append(DriverType1(name=driver_info['name'], start_time=driver_info['start_time'], end_time=driver_info['end_time'],
                                       start_break_time=driver_info['start_break_time'], end_break_time=driver_info['end_break_time'],
                                       location=driver_info['location'], weekend_days=driver_info['weekend_days']))
        elif driver_info['type'] == 2:
            drivers.append(DriverType2(name=driver_info['name'], start_time=driver_info['start_time'], end_time=driver_info['end_time'],
                                       location=driver_info['location'], starts_from=driver_info['starts_from']))

    # Создаем объекты автобусов
    buses = [] # Массив автобусов
    for bus_info in bus_list:
        if bus_info['location'] == 'station 1':
            buses.append(Bus(stops, station_1_positions, station_2_positions, bus_number=bus_info['bus_number']))
        elif bus_info['location'] == 'station 2':
            buses.append(Bus(stops_from_other_station, station_1_positions, station_2_positions, bus_number=bus_info['bus_number']))



    # Симуляция движения автобуса
    step = 0
    hours = 0
    minutes = 0
    days = 1
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    # Создаём эффект для текста с чёрной окантовкой
    if visualisation:
        stroke_effect = withStroke(linewidth=2, foreground='black')
        ax.scatter([], [], color='orange', label='Bus', s=150, path_effects=[stroke_effect]) # Фиктивный маркер только для легенды
        rect = Rectangle((station_1_positions[0][0] - 0.5, station_1_positions[0][1] - 0.5), 1, 1, label='Parking place', linewidth=1, edgecolor='green', facecolor='none', linestyle='--') # Фиктивный маркер только для легенды
        ax.add_patch(rect)

    time_of_day_flag = 'night'

    while days != 8:
        if not is_paused:
            # Обновляем таймер
            minutes += 1
            if minutes >= 60:
                minutes = 0
                hours += 1
            if hours >= 24:
                hours = 0
                days += 1
            day_of_week = days_of_week[(days - 1) % 7]
            time = f'{hours:02d}:{minutes:02d}'
            if visualisation:
                time_text.set_text(f"Time: {time}")
                day_of_week_text.set_text(f"{day_of_week}")
                day_text.set_text(f"Day: {days}")

            if hours == 20:
                time_of_day_flag = 'night'
            if hours == 8:
                time_of_day_flag = 'morning'
            if hours == 15:
                time_of_day_flag = 'day'

        if not is_paused:
            # Обновляем количество людей на остановке в зависимости от времени суток
            if ((time_of_day_flag == 'night' and minutes == 59) or
                    (time_of_day_flag == 'morning' and minutes == 30) or
                    (time_of_day_flag == 'day' and minutes == 15)):
                for stop in stops_objects:
                    stop.get_people()

            for driver in drivers:
                driver.chek_for_bus()
            for bus in buses:
                if bus.driver:
                    bus.time_in_drive += 1

                # Интервалы прохождения остановок в зависимости от времени суток
                if ((bus.time_in_drive >= 4 and random.randint(0, 10) <= 2 or bus.time_in_drive == 9 and time_of_day_flag == 'night') or
                        (bus.time_in_drive >= 6 and random.randint(0, 10) <= 2 or bus.time_in_drive == 11 and time_of_day_flag == 'morning') or
                        (bus.time_in_drive >= 9 and random.randint(0, 10) <= 2 or bus.time_in_drive == 14 and time_of_day_flag == 'day')):
                    bus.time_in_drive = 0

                    for stop in stops_objects:
                        if (bus.x, bus.y) == (stop.x, stop.y):
                            angry_people = bus.get_passengers_in_and_out(stop.people) # Сажаем в автобус людей на остановке и возвращаем тех на кого не хватило места
                            stop.people = angry_people # Те на кого не хватило места остаются на остановке
                            if bus.driver:
                                stop.get_data(bus_num=bus.num, driver=bus.driver.name, angry_people=angry_people) # Сохраняем информацию о прибытии автобуса на каждую остановку
                            break

                    if bus.driver:
                        #bus.driver.chek_for_work() # Проверяем рабочие часы водителя
                        if bus.driver.is_working:
                            bus.move_to_next_stop()

                            if bus.driver.type == 2:
                                current_stop = (bus.x, bus.y)
                                if current_stop in [(2, 0), (17, 13)]:  # Если 2 тип подъезжает на конечную
                                    current_minutes = minutes
                                    current_hours = hours
                                    current_minutes += 4
                                    if current_minutes >= 60:
                                        current_minutes = 0
                                        current_hours += 1
                                    if current_hours >= 24:
                                        current_hours = 0

                                    start_break_time = f'{current_hours:02d}:{current_minutes:02d}'
                                    current_minutes += 20  # Выделяем 20 минут на перерыв
                                    if current_minutes >= 60:
                                        current_minutes = 0
                                        current_hours += 1
                                    if current_hours >= 24:
                                        current_hours = 0
                                    end_break_time = f'{current_hours:02d}:{current_minutes:02d}'

                                    bus.driver.set_break_time(start_break_time, end_break_time)

                        else:
                            bus.move_to_station()


            if visualisation:
                # Обновляем график
                ax.axis('off')  # Убираем оси
                ax.legend(loc='best')
                fig.canvas.draw()
                plt.pause(speed)  # Пауза для анимации
                step += 1

        if visualisation:
            plt.pause(0.1) # Продолжение работы с меньшим интервалом без изменений при нажатой паузе


    def count_spent_money():
        nonlocal spent_money
        for _ in buses:
            spent_money += 5000000 # Цена одного автобуса условно 5м
        for driver in drivers:
            if driver.type == 1:
                spent_money += 100000 # Месячная зарплата водителя 1-ого типа 100к
            else:
                spent_money += 60000 # Месячная зарплата водителя 2-ого типа 60к

    count_spent_money()

    stops_objects[20].show_info() # Вывод информации об автобусах на конкретной остановке
    return angry_passengers, spent_money

# Информация о водителях
driver_list = [
    {'name':'Driver 1', 'type':1, 'start_time':'06:00', 'end_time':'15:00', 'start_break_time':'13:00', 'end_break_time':'14:00', 'location':"station 1", 'weekend_days':['Saturday', 'Sunday']},
    {'name':'Driver 2', 'type':1, 'start_time':'06:30', 'end_time':'15:30', 'start_break_time':'13:30', 'end_break_time':'14:30', 'location':"station 1", 'weekend_days':['Saturday', 'Sunday']},
    {'name':'Driver 3', 'type':1, 'start_time':'06:00', 'end_time':'15:00', 'start_break_time':'13:00', 'end_break_time':'14:00', 'location':"station 2", 'weekend_days':['Saturday', 'Sunday']},
    {'name':'Driver 4', 'type':1, 'start_time':'06:30', 'end_time':'15:30', 'start_break_time':'13:30', 'end_break_time':'14:30', 'location':"station 2", 'weekend_days':['Saturday', 'Sunday']},
    {'name':'Driver 5', 'type':2, 'start_time':'17:00', 'end_time':'5:00', 'location':"station 1", 'starts_from':1},
    {'name':'Driver 6', 'type':2, 'start_time':'18:00', 'end_time':'6:00', 'location':"station 1", 'starts_from':1},
    {'name':'Driver 7', 'type':2, 'start_time':'16:00', 'end_time':'4:00', 'location':"station 2", 'starts_from':3},
    {'name':'Driver 8', 'type':2, 'start_time':'16:00', 'end_time':'4:00', 'location':"station 1", 'starts_from':3},
    {'name':'Driver 9', 'type':1, 'start_time':'07:30', 'end_time':'16:30', 'start_break_time':'14:30', 'end_break_time':'15:30', 'location':"station 2", 'weekend_days':['Saturday', 'Sunday']},
    {'name':'Driver 10', 'type':2, 'start_time':'22:00', 'end_time':'10:00', 'location':"station 1", 'starts_from':2}
]

# Информация об автобусах
bus_list = [
    {'bus_number':1, 'location':'station 1'},
    {'bus_number':2, 'location':'station 1'},
    {'bus_number':3, 'location':'station 1'},
    {'bus_number':4, 'location':'station 1'},
    {'bus_number':5, 'location':'station 2'},
    {'bus_number':6, 'location':'station 2'},
    {'bus_number':7, 'location':'station 2'},
    {'bus_number':8, 'location':'station 2'}
]

angry_passengers, spent_money = run_simulation(visualisation=True, driver_list=driver_list, bus_list=bus_list) # Запуск симуляции
print(f'Angry People: {angry_passengers}')


def initialize_population(driver_list, population_size=100):
    population = []
    for _ in range(population_size):
        individual = []
        for driver in driver_list:
            type = random.randint(1, 2)
            if type == 1:
                # Задаем время начала работы
                int_hours_start_time = random.randint(6, 9)
                int_minutes_start_time = random.choice([0, 15, 30, 45])

                # Задаем время начала перерыва
                int_hours_start_break_time = random.randint(13, 15)
                int_minutes_start_break_time = random.choice([0, 15, 30, 45])

                # Задаем время конца перерыва
                int_hours_end_break_time = int_hours_start_break_time + 1
                int_minutes_end_break_time = int_minutes_start_break_time

                # Задаем время конца работы
                hours_worked = int_hours_start_break_time - int_hours_start_time
                minutes_worked = int_minutes_start_break_time - int_minutes_start_time
                if minutes_worked < 0:
                    minutes_worked += 60
                    hours_worked -= 1

                hours_left = 8 - hours_worked
                minutes_left = 0
                if minutes_worked != 0:
                    minutes_left = 60 - minutes_worked
                    hours_left -= 1

                int_hours_end_time = int_hours_end_break_time + hours_left
                int_minutes_end_time = int_minutes_end_break_time + minutes_left
                if int_minutes_end_time >= 60:
                    int_minutes_end_time -= 60
                    int_hours_end_time += 1

                # Водитель получает свое расписание
                schedule = {
                    'name': driver['name'],
                    'type': type,
                    'start_time': f'{int_hours_start_time:02d}:{int_minutes_start_time:02d}',
                    'end_time': f'{int_hours_end_time:02d}:{int_minutes_end_time:02d}',
                    'start_break_time': f'{int_hours_start_break_time:02d}:{int_minutes_start_break_time:02d}',
                    'end_break_time': f'{int_hours_end_break_time:02d}:{int_minutes_end_break_time:02d}',
                    'location': random.choice(['station 1', 'station 2']),
                    'weekend_days': ['Saturday', 'Sunday']
                }
            else:
                # Задаем время начала работы
                int_hours_start_time = random.randint(0, 23)
                int_minutes_start_time = random.choice([0, 15, 30, 45])

                # Задаем время конца работы
                int_hours_end_time = int_hours_start_time + 12
                if int_hours_end_time >= 24:
                    int_hours_end_time -= 24
                int_minutes_end_time = int_minutes_start_time

                # Водитель получает свое расписание
                schedule = {
                    'name': driver['name'],
                    'type': type,
                    'start_time': f'{int_hours_start_time:02d}:{int_minutes_start_time:02d}',
                    'end_time': f'{int_hours_end_time:02d}:{int_minutes_end_time:02d}',
                    'location': random.choice(['station 1', 'station 2']),
                    'starts_from': random.randint(1, 5)
                }
            individual.append(schedule)
        population.append(individual)
    return population

def fitness_function(individual, driver_list, bus_list):
    # Обновляем информацию о водителях в individual
    updated_driver_list = []
    for i, driver in enumerate(driver_list):
        #updated_driver = driver.copy()
        #updated_driver.update(individual[i])
        updated_driver = individual[i]
        updated_driver_list.append(updated_driver)
    #print(updated_driver_list)

    # Запускаем симуляцию и оцениваем результат
    angry_passengers, _ = run_simulation(visualisation=False, driver_list=updated_driver_list, bus_list=bus_list)
    return -angry_passengers  # Чем меньше недовольных, тем лучше

def select_top_parents(population, fitness_scores, top_n=50):
    # Создаем пары (индивидуум, фитнес), сортируем по фитнесу
    paired = list(zip(fitness_scores, population))
    sorted_population = sorted(paired, key=lambda x: x[0], reverse=True)  # Сортируем по фитнесу
    top_individuals = [x[1] for x in sorted_population[:top_n]]  # Извлекаем только топовые расписания
    return top_individuals

def crossover(parent1, parent2):
    # Одноточечный кроссовер
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(individual, mutation_rate=0.1):
    for gene in individual:
        if random.random() < mutation_rate:
            if gene['type'] == 1:
                # Задаем время начала работы
                int_hours_start_time = random.randint(6, 9)
                int_minutes_start_time = random.choice([0, 15, 30, 45])

                # Задаем время начала перерыва
                int_hours_start_break_time = random.randint(13, 15)
                int_minutes_start_break_time = random.choice([0, 15, 30, 45])

                # Задаем время конца перерыва
                int_hours_end_break_time = int_hours_start_break_time + 1
                int_minutes_end_break_time = int_minutes_start_break_time

                # Задаем время конца работы
                hours_worked = int_hours_start_break_time - int_hours_start_time
                minutes_worked = int_minutes_start_break_time - int_minutes_start_time
                if minutes_worked < 0:
                    minutes_worked += 60
                    hours_worked -= 1

                hours_left = 8 - hours_worked
                minutes_left = 0
                if minutes_worked != 0:
                    minutes_left = 60 - minutes_worked
                    hours_left -= 1

                int_hours_end_time = int_hours_end_break_time + hours_left
                int_minutes_end_time = int_minutes_end_break_time + minutes_left
                if int_minutes_end_time >= 60:
                    int_minutes_end_time -= 60
                    int_hours_end_time += 1

                # Водитель получает свое расписание в случае мутации
                gene['start_time'] = f'{int_hours_start_time:02d}:{int_minutes_start_time:02d}'
                gene['end_time'] = f'{int_hours_end_time:02d}:{int_minutes_end_time:02d}'
                gene['start_break_time'] = f'{int_hours_start_break_time:02d}:{int_minutes_start_break_time:02d}'
                gene['end_break_time'] = f'{int_hours_end_break_time:02d}:{int_minutes_end_break_time:02d}'
                gene['location'] = random.choice(['station 1', 'station 2'])
            else:
                # Задаем время начала работы
                int_hours_start_time = random.randint(0, 23)
                int_minutes_start_time = random.choice([0, 15, 30, 45])

                # Задаем время конца работы
                int_hours_end_time = int_hours_start_time + 12
                if int_hours_end_time >= 24:
                    int_hours_end_time -= 24
                int_minutes_end_time = int_minutes_start_time

                # Водитель получает свое расписание в случае мутации
                gene['start_time'] = f'{int_hours_start_time:02d}:{int_minutes_start_time:02d}'
                gene['end_time'] = f'{int_hours_end_time:02d}:{int_minutes_end_time:02d}'
                gene['location'] = random.choice(['station 1', 'station 2'])
                gene['starts_from'] = random.randint(1, 5)
    return individual

def genetic_algorithm(driver_list, bus_list, generations=100, population_size=100, mutation_rate=0.1):
    population = initialize_population(driver_list, population_size)

    best_schedule = None  # Переменная для хранения лучшего расписания
    best_fitness = float('-inf')  # Начальное значение для наилучшего фитнеса

    for generation in range(generations):
        # Оценка фитнеса
        fitness_scores = [fitness_function(individual, driver_list, bus_list) for individual in population]

        # Выбираем 50 лучших родителей
        top_parents = select_top_parents(population, fitness_scores, top_n=50)

        new_population = top_parents.copy()  # Сохраняем лучших родителей в новое поколение

        # Генерируем потомков
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(top_parents, 2)  # Случайно выбираем двух родителей из топа
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            new_population.extend([child1, child2])

        population = new_population[:population_size]  # Обновляем популяцию, ограничивая размер

        # Лог: наилучший фитнес в текущем поколении
        current_best_fitness = max(fitness_scores)
        if current_best_fitness > best_fitness:
            best_fitness = current_best_fitness
            best_schedule = population[fitness_scores.index(current_best_fitness)]

        print(f"Generation {generation + 1}: Angry people = {-current_best_fitness}")

    # Вывод финального расписания
    print("\nFinal best schedule:")
    for schedule in best_schedule:
        print(schedule)

    return best_schedule

driver_schedule = genetic_algorithm(driver_list, bus_list)

