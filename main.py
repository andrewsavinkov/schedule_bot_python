from datetime import datetime, date, time
import time as timers

weekdays = {1: 'Mon', 2: 'Tue', 3: 'Wed',
            4: 'Thu', 5: 'Fri', 6: 'Sat', 7: 'Sun'}


def create_times():
    time_dictionary = {}
    for i in range(7, 24):
        mins = time(hour=i, minute=0).isoformat(timespec='minutes')
        time_dictionary[mins] = 'No entry'
        mins = time(hour=i, minute=30).isoformat(timespec='minutes')
        time_dictionary[mins] = 'No entry'
    return time_dictionary


empty_schedule = create_times()


def create_empty_schedule(date_input):
    with open('schedule.txt', 'a', encoding="utf-8") as f:
        global weekdays
        f.write(
            f'Расписание на {weekdays[datetime.isoweekday(date_input)]} {date_input}')
        f.write('\n')
        for k in empty_schedule.keys():
            f.write(f'{k} --- No Entry')
            f.write('\n')


def create_entry(date_input):
    time_reserved = False
    index = 0
    idx = 0
    lines = []
    time_entry = input('Введите время в формате: ЧЧ:ММ\t')
    with open('schedule.txt', 'r', encoding="utf-8") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if lines[i].__contains__(str(date_input)) and lines[i].__contains__('Расписание на'):
                index = i
                break

        for i in range(index, index+35):
            if lines[i].__contains__(time_entry) and lines[i].__contains__('No Entry'):
                time_reserved = False
                idx = i
            elif lines[i].__contains__(time_entry) and not lines[i].__contains__('No Entry'):
                time_reserved = True
                idx = i

    if time_reserved:
        print('Время занято!')
        timers.sleep(2)
        user_input = input(
            'Выберите, что сделать: 1-внести новую запись 2-выбрать другое время\t')
        if user_input == '1':
            entry = input('Введите, что хотите добавить: ')
            with open('schedule.txt', 'w', encoding="utf-8") as f:
                lines[idx] = time_entry+' --- '+entry+'\n'
                f.writelines(lines)
        elif user_input == '2':
            create_entry(date_input)
        else:
            print('Некорректная запись!')
    else:
        print('Время не занято!')
        entry = input('Введите, что хотите добавить: ')
        with open('schedule.txt', 'w', encoding="utf-8") as f:
            lines[idx] = time_entry+' --- '+entry+'\n'
            f.writelines(lines)


def show_tasks(date_input):
    task_list = []
    idx = 0
    schedule_created = False
    with open('schedule.txt', 'r', encoding="utf-8") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if lines[i].__contains__(str(date_input)) and lines[i].__contains__('Расписание на'):
                schedule_created = True
                idx = i
        if not schedule_created:
            print('Расписание на введенную дату не создано')
            timers.sleep(2)
            user_input = input(
                'Выберите, что сделать: 1-создать событие на выбранную дату? 2-выйти из программы?\t')
            if user_input == '1':
                create_empty_schedule(date_input)
                create_entry()
            elif user_input == '2':
                quit()
            else:
                print('Некорректный ввод!')
        for i in range(idx+1, idx+35):
            if not lines[i].__contains__('No Entry'):
                task_list.append(lines[i])
        print(
            f'Список дел на {weekdays[datetime.isoweekday(date_input)]} {date_input}')
        for i in range(len(task_list)):
            print(task_list[i])
        print()
    with open('schedule.txt', 'a', encoding="utf-8") as f:
        f.write(
            f'Список дел на {weekdays[datetime.isoweekday(date_input)]} {date_input} \n')
        f.writelines(task_list)


def schedule_exists(date_input):
    schedule_created = False
    with open('schedule.txt', 'r', encoding="utf-8") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if lines[i].__contains__(str(date_input)) and lines[i].__contains__('Расписание на'):
                schedule_created = True
                return True
        if not schedule_created:
            return False


def date_input():
    user_input = input('Введите дату в формате: ДД.ММ.ГГГГ:\t')
    date_components = str.split(user_input, '.')
    return date(int(date_components[2]), int(date_components[1]), int(date_components[0]))


def delete_entry(date_input):
    index = 0
    is_empty = True
    time_entry = input('Введите время в формате: ЧЧ:ММ\t')
    with open('schedule.txt', 'r', encoding="utf-8") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if lines[i].__contains__(str(date_input)) and lines[i].__contains__('Расписание на'):
                index = i
                break

        for i in range(index, index+35):
            if lines[i].__contains__(time_entry) and lines[i].__contains__('No Entry'):
                print('Выбранное вами время свободно!')
            elif lines[i].__contains__(time_entry) and not lines[i].__contains__('No Entry'):
                with open('schedule.txt', 'w', encoding="utf-8") as f:
                    lines[i] = time_entry+' --- No Entry\n'
                    f.writelines(lines)


def print_schedule(date_input):
    idx = 0
    schedule_exists = False
    with open('schedule.txt', 'r', encoding="utf-8") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if lines[i].__contains__(str(date_input)) and lines[i].__contains__('Расписание на'):
                idx = i
                schedule_exists = True
        if not schedule_exists:
            print('Расписание на указанную вами дату не создано')

        for i in range(idx, idx+35):
            print(f'{lines[i]}')


while True:
    print('Добрый день! Я - ваш консольный бот, который поможет вам составить расписание на день!')
    timers.sleep(2)
    user_input = input('Выберите, что хотите сделать: \n 1-Создать расписание на день \n 2-Добавить событие \n 3-Показать расписание на день в консоли \
        \n 4-Удалить запись из расписания \n 5-Сгенерировать список дел на день \n')

    if user_input == '1':
        user_date = date_input()
        if not schedule_exists(user_date):
            create_empty_schedule(user_date)
            print('Вы можете посмотреть созданное расписание, выбрав соответствующий пункт меню, или открыв файл ''schedule.txt''')
            timers.sleep(2)
        else:
            print('Расписание на этот день уже создано')
            print('Перезапустите программу и попробуйте снова. Все изменения сохранены в файле ''schedule.txt''')
            break
    elif user_input == '2':
        user_date = date_input()
        if not schedule_exists(user_date):
            print('На эту дату расписания не создано! Попробуйте ввести новую дату или создайте расписание на этот день!')
            print('Перезапустите программу и попробуйте снова. Все изменения сохранены в файле ''schedule.txt''')
            break
        create_entry(user_date)
        print('Вы можете посмотреть созданное расписание, выбрав соответствующий пункт меню, или открыв файл ''schedule.txt''')
        timers.sleep(2)
    elif user_input == '3':
        user_date = date_input()
        if not schedule_exists(user_date):
            print('На эту дату расписания не создано! Попробуйте ввести новую дату или создайте расписание на этот день!')
            print('Перезапустите программу и попробуйте снова. Все изменения сохранены в файле ''schedule.txt''')
            break
        print_schedule(user_date)
    elif user_input == '4':
        user_date = date_input()
        if not schedule_exists(user_date):
            print('На эту дату расписания не создано! Попробуйте ввести новую дату или создайте расписание на этот день!')
            print('Перезапустите программу и попробуйте снова. Все изменения сохранены в файле ''schedule.txt''')
            break
        delete_entry(user_date)
        print('Запись удалена! Сгенерируйте актуальный список дел, если необходимо!')
        timers.sleep(2)
    elif user_input == '5':
        user_date = date_input()
        show_tasks(user_date)
        print('Ваш список дел также сохранен в файле ''schedule.txt''')
        timers.sleep(2)
    else:
        print('Некорректный ввод!')
