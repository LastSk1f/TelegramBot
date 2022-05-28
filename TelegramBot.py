import re

import telebot
import sqlite3
from telebot import types


bot = telebot.TeleBot('5152527390:AAGXJR9ytAU2pY2mkVSkNzLG6hKZTJPYw8I')


@bot.message_handler(commands=["start"])
def start(m):
    markups = types.ReplyKeyboardMarkup(resize_keyboard=True)
    items = types.KeyboardButton("Начать")
    markups.add(items)
    bot.send_message(m.chat.id, 'Приветствую Вас!', reply_markup=markups)


dict_all = {'date_bool': False, 'time_bool': False, 'note_bool': False, 'delete_date': False, 'delete_time': False,
            'show_on_date': False, 'show_on_time': False, 'delete_on_date': '', 'delete_on_time': '',
            'input_date': '',
            'input_time': '', 'input_note': '', 'show_on_date_input': '', 'show_on_time_input': ''}


@bot.message_handler(content_types='text')
def reply(input_message):

    db = sqlite3.connect('project.sqlite')
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS notes (
                       dd TEXT,
                       mm TEXT,
                       yyyy TEXT,
                       hour TEXT,
                       minute TEXT,
                       notedoby TEXT
                   )""")

    def input_db(date, time, note_content):
        date_input = date.split('.')
        dd = date_input[0]
        mm = date_input[1]
        yyyy = date_input[2]
        time_input = time.split(':')
        hour = time_input[0]
        minute = time_input[1]
        input_note_db = (dd, mm, yyyy, hour, minute, note_content)
        return input_note_db

    def convert(out_db_tuple):
        out_db_line = ''
        for i in range(0, 2):
            out_db_line += out_db_tuple[i]
            out_db_line += '.'
        out_db_line += out_db_tuple[2]
        out_db_line += ' '
        out_db_line += out_db_tuple[3] + ':' + out_db_tuple[4]
        out_db_line += ' '
        out_db_line += out_db_tuple[5]
        return out_db_line

    def get_count_notes():
        cursor.execute("SELECT * FROM notes")
        rows = cursor.fetchall()
        return len(rows)
        db.commit()

    def split(date, time):
        date_array = date.split('.')
        time_array = time.split(':')
        count_dd = date_array[0]
        count_mm = date_array[1]
        count_yyyy = date_array[2]
        count_hh = time_array[0]
        count_minutes = time_array[1]
        date_tuple = (count_dd, count_mm, count_yyyy, count_hh, count_minutes)
        return date_tuple

    def get_count_notes_on_date(date_count, time_count):
        count_tuple = split(date_count, time_count)
        cursor.execute(f"SELECT * FROM notes WHERE dd = '{count_tuple[0]}' AND mm = '{count_tuple[1] }'"
                       f" AND yyyy = '{count_tuple[2]}' AND hour = '{count_tuple[3]}' AND minute = '{count_tuple[4]}'")
        rows = cursor.fetchall()
        return len(rows)
        db.commit()

    def delete_note(date_of_delete_note, time_of_delete_note):
        delete_tuple = split(date_of_delete_note, time_of_delete_note)
        cursor.execute(
            f"DELETE FROM notes WHERE dd = '{delete_tuple[0]}' AND mm = '{delete_tuple[1]}'"
            f" AND yyyy = '{delete_tuple[2]}' AND hour = '{delete_tuple[3]}' AND minute = '{delete_tuple[4]}'  ")
        db.commit()

    def show_on(show_date, show_time):
        show_date_array = show_date.split('.')
        show_time_array = show_time.split(':')
        show_dd = show_date_array[0]
        show_mm = show_date_array[1]
        show_yyyy = show_date_array[2]
        show_hour = show_time_array[0]
        show_minute = show_time_array[1]
        show_on_tuple = cursor.execute(f"SELECT * FROM notes WHERE dd = '{show_dd}' AND mm = '{show_mm}'"
                                       f" AND yyyy = '{show_yyyy}' AND hour = '{show_hour}' "
                                       f"AND minute = '{show_minute}'")

        db.commit()
        return show_on_tuple

    def check_date(message):
        message_array = message.split('.')
        if int(message_array[0]) > 31 or int(message_array[1]) > 12 or int(message_array[2]) < 2022:
            return False
        else:
            return True

    def check_time(message):
        message_array = message.split(':')
        if int(message_array[0]) > 24 or int(message_array[1]) > 60:
            return False
        else:
            return True

    def get_back():
        item_back = types.KeyboardButton("Вернуться в начало")
        markup_back = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup_back.add(item_back)
        bot.send_message(input_message.chat.id, 'Введите время в формате чч:мм', reply_markup=markup_back)

    if input_message.text == 'Начать' or input_message.text == 'Вернуться в начало':
        dict_all['delete_time'] = False
        dict_all['delete_date'] = False
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Заметки")
        item2 = types.KeyboardButton("Новая заметка")
        markup1.add(item1, item2)
        bot.send_message(input_message.chat.id, 'Нажмите: \nЗаметки - просмотр всех заметок '
                                                '\nНовая заметка - создание новой заметки',
                         reply_markup=markup1)
    elif input_message.text == "Заметки":
        item_all_note = types.KeyboardButton("Просмотр всех заметок")
        item_delete_note = types.KeyboardButton("Удалить заметку")
        item_return = types.KeyboardButton("Вернуться в начало")
        item_note_time = types.KeyboardButton("Заметки на дату")
        markup_notes = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup_notes.add(item_all_note, item_note_time, item_return, item_delete_note)
        bot.send_message(input_message.chat.id, 'Нажмите на кнопку нужного раздела: ', reply_markup=markup_notes)
    elif input_message.text == "Удалить заметку":
        item_delete_note = types.KeyboardButton("Вернуться в начало")
        markup_delete_note = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup_delete_note.add(item_delete_note)
        check_delete = get_count_notes()
        if check_delete == 0:
            bot.send_message(input_message.chat.id, 'Удаление недоступно - заметок нет')
        else:
            bot.send_message(input_message.chat.id, 'При нажатии кнопки, удаление будет отменено')
            dict_all['delete_date'] = True
            bot.send_message(input_message.chat.id, 'Введите дату удаляемой заметки в формате дд.мм.гггг',
                             reply_markup=markup_delete_note)

    elif dict_all['delete_date'] is True:
        if re.fullmatch(r'\d{2}.\d{2}.\d{4}', input_message.text):
            if check_date(input_message.text) is True:
                dict_all['delete_date'] = False
                dict_all['delete_on_date'] = input_message.text
                dict_all['delete_time'] = True
                bot.send_message(input_message.chat.id, 'Введите время удаляемой заметки в формате чч:мм')
            else:
                dict_all['date_bool'] = True
                bot.send_message(input_message.chat.id, 'Дата некорректна по значениям!')
        else:
            dict_all['delete_date'] = True
            bot.send_message(input_message.chat.id, 'Дата указана в неверном формате, повторите ввод!')

    elif dict_all['delete_time'] is True:
        if re.fullmatch(r'\d{2}:\d{2}', input_message.text):
            if check_time(input_message.text) is True:
                dict_all['delete_time'] = False
                dict_all['delete_on_time'] = input_message.text
                delete_note(dict_all['delete_on_date'], dict_all['delete_on_time'])
                bot.send_message(input_message.chat.id, 'Заметка на указанную дату удалена')
            else:
                dict_all['delete_time'] = True
                bot.send_message(input_message.chat.id, 'Время некорректно по значениям!')
        else:
            dict_all['delete_time'] = True
            bot.send_message(input_message.chat.id, 'Время указано в неверном формате, повторите ввод!')

    elif input_message.text == "Просмотр всех заметок":
        rows_number = get_count_notes()
        if rows_number != 0:
            for out_db_value in cursor.execute(" SELECT * FROM notes ORDER BY yyyy,mm,dd,hour,minute"):
                done_value = convert(out_db_value)
                bot.send_message(input_message.chat.id, done_value)
                db.commit()
        else:
            bot.send_message(input_message.chat.id, 'Заметок нет')
    elif input_message.text == "Новая заметка" or input_message.text == "Изменить дату":
        item_return_date = types.KeyboardButton("Вернуться в начало")
        markup_notes_date = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup_notes_date.add(item_return_date)
        bot.send_message(input_message.chat.id, 'Введите дату в формате дд.мм.гггг', reply_markup=markup_notes_date)
        dict_all['date_bool'] = True
    elif input_message.text == "Заметки на дату":
        rows_number_on_date = get_count_notes()
        if rows_number_on_date != 0:
            item_return_button = types.KeyboardButton("Вернуться в начало")
            markup_return = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup_return.add(item_return_button)
            bot.send_message(input_message.chat.id, 'Введите дату в формате дд.мм.гггг', reply_markup=markup_return)
            dict_all['show_on_date'] = True
        else:
            bot.send_message(input_message.chat.id, 'Просмотр на дату недоступен - заметок нет')
    elif dict_all['show_on_date'] is True:
        dict_all['show_on_date'] = False
        if re.fullmatch(r'\d{2}.\d{2}.\d{4}', input_message.text):
            if check_date(input_message.text) is True:
                dict_all['show_on_date_input'] = input_message.text
                dict_all['show_on_time'] = True
                get_back()
            else:
                dict_all['date_bool'] = True
                bot.send_message(input_message.chat.id, 'Дата некорректна по значениям!')

        elif input_message.text is not 'Вернуться в начало':
            dict_all['show_on_date'] = True
            bot.send_message(input_message.chat.id, 'Введенная дата не соответствует формату дд.мм.ггг! '
                                                    '\nПовторите попытку')
    elif dict_all['show_on_time'] is True:
        dict_all['show_on_time'] = False
        if re.fullmatch(r'\d\d:\d\d', input_message.text):
            if check_time(input_message.text) is True:
                dict_all['show_on_time_input'] = input_message.text
                if get_count_notes_on_date(dict_all['show_on_date_input'], dict_all['show_on_time_input']) != 0:
                    show_send = show_on(dict_all['show_on_date_input'], dict_all['show_on_time_input'])
                    for out_show_date in show_send:
                        input_done_show = convert(out_show_date)
                        bot.send_message(input_message.chat.id, input_done_show)
                else:
                    bot.send_message(input_message.chat.id, 'На выбранную дату и время нет заметки')
            else:
                bot.send_message(input_message.chat.id, 'Время некорректно по значениям!')
                dict_all['show_on_time'] = True

        elif input_message.text is not 'Вернуться в начало':
            bot.send_message(input_message.chat.id, 'Введенное время не соответствует формату чч:мм! '
                                                    '\nПовториите попытку')
            dict_all['show_on_time'] = True

    elif dict_all['date_bool'] is True:
        dict_all['date_bool'] = False
        if re.fullmatch(r'\d{2}.\d{2}.\d{4}', input_message.text):
            if check_date(input_message.text) is True:
                dict_all['input_date'] = input_message.text
                dict_all['time_bool'] = True
                get_back()
            else:
                dict_all['date_bool'] = True
                bot.send_message(input_message.chat.id, 'Дата некорректна по значениям!')

        elif input_message.text is not 'Вернуться в начало':
            bot.send_message(input_message.chat.id, 'Введенная дата не соответствует формату дд.мм.ггг! '
                                                    '\nПовторите попытку')
            dict_all['date_bool'] = True
    elif dict_all['time_bool'] is True:
        dict_all['time_bool'] = False
        if re.fullmatch(r'\d\d:\d\d', input_message.text):
            if check_time(input_message.text) is True:
                dict_all['input_time'] = input_message.text
                if get_count_notes_on_date(dict_all['input_date'], dict_all['input_time']) != 1:
                    dict_all['note_bool'] = True
                    bot.send_message(input_message.chat.id, 'Введите текст заметки:')
                else:
                    item_change_data = types.KeyboardButton("Изменить дату")
                    item_return_date_already = types.KeyboardButton("Вернуться в начало")
                    markup_change = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    markup_change.add(item_change_data, item_return_date_already)
                    bot.send_message(input_message.chat.id, 'На выбранную дату и время уже есть заметка!',
                                     reply_markup=markup_change)
            else:
                bot.send_message(input_message.chat.id, 'Время некорректно по значениям!')
                dict_all['time_bool'] = True

        elif input_message.text is not 'Вернуться в начало':
            bot.send_message(input_message.chat.id, 'Введенное время не соответствует формату чч:мм! '
                                                    '\nПовториите попытку')
            dict_all['time_bool'] = True
    elif dict_all['note_bool'] is True:
        markup15 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        dict_all['note_bool'] = False
        dict_all['input_note'] = input_message.text
        item15 = types.KeyboardButton("Вернуться в начало")
        markup15.add(item15)
        bot.send_message(input_message.chat.id, 'Заметка создана! ', reply_markup=markup15)
        done_note = input_db(dict_all['input_date'], dict_all['input_time'], dict_all['input_note'])
        cursor.execute("INSERT INTO notes VALUES (?,?,?,?,?,?)", done_note)
        db.commit()
        dict_all['input_date'] = ''
        dict_all['input_time'] = ''
        dict_all['input_note'] = ''


bot.polling(none_stop=True, interval=1)
