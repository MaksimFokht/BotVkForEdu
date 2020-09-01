# -*- coding: utf-8 -*-
"""
:authors: MaksimFokht
:license: Apache License, Version 2.0, see LICENSE file

:copyright: (c) 2020 MaksimFokht
"""

import datetime
import DbQuery
import bot_config
import vkbot_api


class BotModel:
    """

    :param text: Текст, который отправил пользователь боту.
    :type text: str

    :param from_id: ID пользователя, который отправил запрос боту.
    :type from_id: int

    Модель предназначена для выполнения всей логической части бота и возвращения ответа контрллеру.
    """

    def __init__(self, text, from_id):
        self.text = text
        self.from_id = from_id
        print('[DEBUG-MODEL]: The model is initialized with the following data: \n '
              '[DEBUG-MODEL]: text - ' + str(self.text) + '\n '
                                                          '[DEBUG-MODEL]: from_id - ' + str(self.from_id) + '\n ')

    def test(self):
        """ Метод проверки работоспособности бота """
        if self.access_check():
            out = '[DEBUG]: MVC pattern successfully assembled'
            return out
        else:
            return bot_config.error_access_denied

    def validation(self):
        """
        Метод выполняет валидацию текста пользователя путем разделения его на составляющие(
        команда и аргументы), проверки на существование в БД и проверки статуса в БД.
        """
        if self.text[0] == '.' and self.text != '':
            split_text = self.text.split()
            if len(split_text) == 1:
                command = str(split_text[0])
                args = ' '
            else:
                command = str(split_text[0])
                del split_text[0]
                args = ' '.join(split_text)
            query = "SELECT * FROM command WHERE command = '" + command + "'"
            dbq = DbQuery.Query(query)
            check_cmd = dbq.db_query_wrt()
            for row in check_cmd:
                if len(row) > 0:
                    query = "SELECT turn FROM public.command WHERE command='" + str(command) + "'"
                    dbq = DbQuery.Query(query)
                    check_status = dbq.db_query_wrt()
                    for row_two in check_status:
                        if len(row_two) > 0:
                            if row_two[0] is True:
                                return command, args
                            else:
                                print('[DEBUG]: Command disabled')
                else:
                    print('[DEBUG]: Command not existence')

    def access_check(self):
        """Метод, сверяющий ID пользователя с ID Администратора, который записан в конфигурации."""
        if self.from_id == bot_config.admin:
            return True
        else:
            return False

    def command_existence_check(self, command):
        """
        Метод проверки существования команды в БД.

        :param command: Строка с командой.
        :type command: str

        """
        query = "SELECT * FROM public.command WHERE command = '" + str(command) + "'"
        dbq = DbQuery.Query(query)
        check_exists = dbq.db_query_wrt()
        for row in check_exists:
            if len(row) > 0:
                return True, self
            else:
                return False, self

    def add_cmd(self, command):
        """
        Данный метод добавляет новую команду в БД.

        :param command: Строка с командой(идет в качестве аргумента к основной команде).
        :type command: str

        """
        if self.access_check():
            if str(command[0])[0] == '.':
                if self.command_existence_check(command):
                    return 'Команда уже добавлена в БД'
                else:
                    query = "INSERT INTO public.command(command) VALUES('" + command + "')"
                    dbq = DbQuery.Query(query)
                    dbq.db_query_nrt()
                    return 'Команда успешно добавлена в БД'
            else:
                return 'Ошибка выполнения команды: команда начинается с точки'
        else:
            return bot_config.error_access_denied

    def turn_on(self, command):
        """
        Метод изменения статуса команды на ВКЛ.

        :param command: Строка с командой(идет в качестве аргумента к основной команде).
        :type command: str
        """
        if self.access_check():
            query = "UPDATE public.command SET turn = true WHERE command = '" + command + "'"
            dbq = DbQuery.Query(query)
            dbq.db_query_nrt()
            return 'Команда успешно включена'
        else:
            return bot_config.error_access_denied

    def turn_off(self, command):
        """
        Метод изменения статуса команды на ВЫКЛ.

        :param command: Строка с командой(идет в качестве аргумента к основной команде).
        :type command: str
        """
        if self.access_check():
            query = "UPDATE public.command SET turn = false WHERE command = '" + command + "'"
            dbq = DbQuery.Query(query)
            dbq.db_query_nrt()
            return 'Команда успешно выключена'
        else:
            return bot_config.error_access_denied

    @staticmethod
    def report_existence_check():
        """
        Метод проверяет существование таблицы с отчетом за текущий месяц.
        """
        query = "SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME='" + bot_config.report_name + "'"
        dbq = DbQuery.Query(query)
        check_exists = dbq.db_query_wrt()
        for row in check_exists:
            if len(row) > 0:
                return True
            else:
                return False

    @staticmethod
    def surname_check(surname):
        """
        Метод проверяет наличие фамилии в таблице со студентами.

        :param surname: Поле с фамилией студента.
        :type surname: str

        """
        query = "SELECT * FROM public.student WHERE surname='" + str(surname) + "'"
        dbq = DbQuery.Query(query)
        check_srn = dbq.db_query_wrt()
        for row in check_srn:
            if len(row) > 0:
                return True
            else:
                return False

    def skipped(self, args, user_id):
        """
        Метод, выполняющий функционал системы пропусков студента(добваление пропущенных часов, их вывод и т.д.)

        :param args: Поле с аргументами к команде.
        :type args: str

        :param user_id: Поле с ID пользователя.
        :type user_id: int

        """
        query = args.split()
        print('[DEBUG]: length args = ', len(query))
        if len(query) == 0:
            return 'Ошибка выполнения команды: недостаточно аргументов. \nДля справки введите ".skip -h"'
        if self.report_existence_check():
            print('[DEBUG]: Report exists')
        else:
            query = "SELECT public.add_report('" + bot_config.report_name + "')"
            dbq = DbQuery.Query(query)
            dbq.db_query_nrt()
        if str(query[0]) == '-t' and user_id in bot_config.grant_id:
            surname = str(query[1])
            date = str(datetime.datetime.today().strftime("%d.%m.%Y"))
            hours = str(query[2])
            resp = str(query[3])
            query = "INSERT INTO public.skipped(surname, date, hours, respectfully) VALUES('" + surname + "', '" + date + "', '" + hours + "', '" + resp + "')"
            dbq = DbQuery.Query(query)
            dbq.db_query_nrt()
            query2 = "UPDATE public." + bot_config.report_name + " SET hours = hours + '" + hours + "', respectfully = respectfully + '" + resp + "' WHERE surname = '" + surname + "'"
            dbq2 = DbQuery.Query(query2)
            dbq2.db_query_nrt()
            return 'Вы успешно добавили часы пропусков в количестве \n' + \
                   hours + ' - общих часов \n' + \
                   resp + ' - уважительных часов студенту ' + surname + ' за \n' + \
                   date
        elif str(query[0]) == '-d' and user_id in bot_config.grant_id:
            surname = str(query[1])
            date = str(query[2])
            hours = str(query[3])
            resp = str(query[4])
            query = "INSERT INTO public.skipped(surname, date, hours, respectfully) VALUES('" + surname + "', '" + date + "', '" + hours + "', '" + resp + "')"
            dbq = DbQuery.Query(query)
            dbq.db_query_nrt()
            query2 = "UPDATE public." + bot_config.report_name + " SET hours = hours + '" + hours + "', respectfully = respectfully + '" + resp + "' WHERE surname = '" + surname + "'"
            dbq2 = DbQuery.Query(query2)
            dbq2.db_query_nrt()
            return 'Вы успешно добавили часы пропусков в количестве \n' + \
                   hours + ' - общих часов \n' + \
                   resp + ' - уважительных часов студенту ' + surname + ' за \n' + \
                   date
        elif str(query[0]) == '-m':
            if self.report_existence_check():
                if len(query) > 1:
                    if user_id in bot_config.grant_id:
                        if self.surname_check(str(query[1])):
                            surname = str(query[1])
                            msg = 'Количество пропусков за текущий месяц студента ' + surname + ': \n'
                            query = "SELECT date, hours, respectfully FROM public.skipped WHERE surname = '" + surname + "'"
                            dbq = DbQuery.Query(query)
                            student_report = dbq.db_query_wrt()
                            for row in student_report:
                                month = str(row[0])
                                month.split(".")
                                if str(month[1] == bot_config.report_date):
                                    hours = str(row[1])
                                    resp = str(row[2])
                                    st_msg = month[0] + '.' + month[1] + ' - ' + hours + ' часов, из них ' + resp + ' по ув. причине \n'
                                    msg = msg + st_msg
                            return msg
                        else:
                            return 'Ошибка выполнения команды: неверно введена фамилия'
                else:
                    if user_id in bot_config.grant_id:
                        query = "SELECT * FROM public." + bot_config.report_name + " ORDER BY id ASC"
                        dbq = DbQuery.Query(query)
                        report = dbq.db_query_wrt()
                        student_skip = ''
                        rep_text = 'Вывод статистики пропусков за месяц: \n'
                        for row in report:
                            surname = str(row[1])
                            hours = str(row[2])
                            resp = str(row[3])
                            student_skip = student_skip + '\n' + surname + ' - ' + hours + ' пропущенных часов, из них ' + resp + ' по ув. причине'
                        return rep_text + student_skip
                    else:
                        surname = ''
                        query = "SELECT surname FROM public.student WHERE vk_id = '" + str(user_id) + "'"
                        dbq = DbQuery.Query(query)
                        sel_srn_db = dbq.db_query_wrt()
                        for row in sel_srn_db:
                            surname = str(row[0])
                        msg = 'Количество пропусков за текущий месяц студента ' + surname + ': \n'
                        query2 = "SELECT date, hours, respectfully FROM public.skipped WHERE surname = '" + surname + "'"
                        dbq2 = DbQuery.Query(query2)
                        student_report = dbq2.db_query_wrt()
                        for row in student_report:
                            month = str(row[0])
                            month.split(".")
                            if str(month[1] == bot_config.report_date):
                                hours = str(row[1])
                                resp = str(row[2])
                                st_msg = month[0] + '.' + month[
                                    1] + ' - ' + hours + ' часов, из них ' + resp + ' по ув. причине \n'
                                msg = msg + st_msg
                        return msg
            else:
                return 'Отчета по пропускам за текущий месяц еще не существует'
        elif str(query[0]) == '-s' and len(query) > 1 and user_id in bot_config.grant_id:
            if self.surname_check(str(query[1])) is True:
                q_surname = query[1]
                query = "SELECT surname, hours, respectfully FROM public." + bot_config.report_name + " WHERE surname = '" + q_surname + "'"
                dbq = DbQuery.Query(query)
                result = dbq.db_query_wrt()
                for row in result:
                    r_surname = str(row[0])
                    r_hours = str(row[1])
                    r_resp = str(row[2])
                    r_msg = "Количество пропущенных часов студента " + r_surname + " \n" + \
                            "Всего часов: " + r_hours + "\n" + \
                            "По уважительной причине: " + r_resp
                    return r_msg
            else:
                return 'Введите правильно фамилию'
        elif str(query[0]) == '-s':
            if len(query) >= 2:
                return bot_config.error_access_denied
            elif len(query) == 1:
                sel_srn = ''
                query = "SELECT surname FROM public.student WHERE vk_id = '" + str(user_id) + "'"
                dbq = DbQuery.Query(query)
                sel_srn_db = dbq.db_query_wrt()
                for row in sel_srn_db:
                    sel_srn = str(row[0])
                query2 = "SELECT surname, hours, respectfully FROM public." + bot_config.report_name + " WHERE surname = '" + sel_srn + "'"
                dbq2 = DbQuery.Query(query2)
                result = dbq2.db_query_wrt()
                r_msg = ''
                for row in result:
                    r_surname = str(row[0])
                    r_hours = str(row[1])
                    r_resp = str(row[2])
                    r_msg = "Количество пропущенных часов студента " + r_surname + " \n" + \
                            "Всего часов: " + r_hours + "\n" + \
                            "По уважительной причине: " + r_resp
                return r_msg
        elif str(query[0]) == '-h':
            if user_id in bot_config.grant_id:
                return bot_config.skip_help
            else:
                return bot_config.skip_help_st
        elif (str(query[0]) == '-t' or str(query[0]) == '-d' or (str(query[0]) == '-s' and len(
                query) > 1) or (str(query[0]) == '-m' and len(query) > 1)) and user_id not in bot_config.grant_id:
            return bot_config.error_access_denied
        else:
            return 'Ошибка выполнения команды: неверный аргумент. \nДля справки введите ".skip -h"'

    def get_conversation_info(self):
        """
        Метод отображает в консоли информацию о беседе студентов.
        """
        if self.access_check():
            temp = vkbot_api.vk.messages.getConversationMembers(peer_id=bot_config.bich_conv)
            temp_profiles = temp['profiles']
            for row in temp_profiles:
                st_id = row['id']
                surname = row['last_name']
                push_id = row['screen_name']
                print(str(surname) + " " + str(push_id) + " " + str(st_id))
            return 'Команда выполнена успешно'
        else:
            return bot_config.error_access_denied

    @staticmethod
    def show_exam():
        """
        Метод, выводящий список аттестаций из БД.
        """
        exam_list = 'Список экзаменов/зачетов: \n'
        query = "SELECT discipline, type_of_exam, date_exam FROM public.exam"
        dbq = DbQuery.Query(query)
        show = dbq.db_query_wrt()
        for row in show:
            exam_name = str(row[0])
            exam_type = str(row[1])
            exam_date = str(row[2])
            exam_list = exam_list + exam_name + '(' + exam_type + '): ' + exam_date + '\n'
        return exam_list

    @staticmethod
    def add_exam(args, from_id):
        """
        Метод добавляет информацию о предстоящих аттестациях студента.

        :param args: Поле с аргументами к команде.
        :type args: str

        :param from_id: Поле с ID Пользователя.
        :type from_id: int

        """
        if from_id in bot_config.grant_id:
            values = args.split(", ")
            exam_name = str(values[0])
            exam_type = str(values[1])
            exam_date = str(values[2])
            query = "INSERT INTO public.exam(discipline, type_of_exam, date_exam) VALUES('" + exam_name + "', '" + exam_type + "', '" + exam_date + "')"
            dbq = DbQuery.Query(query)
            dbq.db_query_nrt()
            return 'Экзамен/зачет успешно добавлен.'
        else:
            return bot_config.error_access_denied

    @staticmethod
    def show_help(user_id):
        """
        Данный метод выводит справку по боту.
        :param user_id: Поле с ID Пользователя.
        """
        if user_id == bot_config.admin:
            return bot_config.cmd_adm_help
        else:
            return bot_config.cmd_help
