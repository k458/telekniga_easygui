# create data if not exists   afonov afonya beregobas 22 12 1998 3 008 009 0019
data = open('data.csv', 'a')
data.close()
data = open('data.csv', 'r')
data_listed = []
for line in data:
    line_parsed = ''
    for_add = []
    for s in range(0, len(line) - 1):
        line_parsed += line[s]
    line_parsed = line_parsed.split()
    inst_for_add = []
    inst_for_add += [line_parsed[x] for x in range(0, 6)]
    telefons_last_index = 7 + int(line_parsed[6])
    telefons = [line_parsed[x] for x in range(7, telefons_last_index)]
    inst_for_add.append(telefons)
    data_listed.append(inst_for_add)
data.close()


# save
def save_data_listed_as_data():
    data = open('data.csv', 'w')
    for listed in data_listed:
        listed_for_save = [listed[x] for x in range(0, 6)]
        listed_for_save += [str(len(listed[6]))]
        listed_for_save += listed[6]
        line = ' '.join(elem for elem in listed_for_save)
        data.writelines(line)
        data.writelines('\n')
    data.close()
    print('Сохранено.\n')


# get str
def get_str_by_index(index):
    # original = [str(x) for x in data_listed[index]]
    # print(f'original {str(original)}')

    inst = data_listed[index]
    denulled = [inst[x] for x in range(0, 3)]
    birthDayCorrect = True
    for x in range(3, 6):
        if inst[x] == 'None':
            birthDayCorrect = False
            birthDayCorrect = True
    if birthDayCorrect:
        denulled += ['.'.join(str(inst[x]) for x in range(3, 6))]
    denulled += ['Номера:']
    numbers_count = len(inst[6])
    denulled += [', '.join(str(x) for x in inst[6])]
    # remove None
    while denulled.count('None') > 0:
        denulled.remove('None')
    ret = [str(index) + '.'] + denulled
    return ' '.join(str(elem) for elem in ret)


# help
def help_main():
    print('Программа парсит данные из файла, затем работает с данными, а не с файлом, поэтому не забывайте сохраняться!')
    print('clear, c - очистить консоль')
    print('save, s - сохранить')
    print('quit, q - выход из программы')
    print('add, a - добавить новую запись(подробнее - help -add)')
    print('print, p - вывести данные(подробнее - help -print)')
    print('delete, d - удалить данные(подробнее - help -delete)')
    print('change, ch - изменить данные(подробнее - help -change)')
def help_add():
    print('Для добавления новой записи используйте команду вида: ')
    print('add ИМЯ ФАМИЛИЯ ОТЧЕСТВО ДД.ММ.ГГГГ -t НОМЕР1 НОМЕР2 НОМЕР3')
    print('Если вы не знаете ФИО полностью или дату, вводите None вместо неизвестных. Номер должен быть хотя бы один.')
    print('Если указать индекс и номер телефона, можно добавлять номера:')
    print('add -i ИНДЕКС -t НОМЕР')
def help_print():
    print('Для вывода данных используйте команду вида: ')
    print('print -i ИНДЕКС чтобы вывести данные по нужному индексу')
    print('либо, например print -n ИМЯ чтобы вывести данные отфильтрованные по имени. Фильтровать можно также по фамилии(-s), отчеству(-o).')
    print('Флаги можно комбинировать. После каждого флага нужно вводить и соотвутствующее значение.')
def help_delete():
    print('Для удаления записи используйте команду вида: ')
    print('delete -i ИНДЕКС чтобы удалить данные по нужному индексу')
    print('либо delete -i ИНДЕКС -t ИНДЕКС_НОМЕРА чтобы удалить номер телефона')
def help_change():
    print('Для изменения данных используйте команду вида: ')
    print('change -i ИНДЕКС -n ИМЯ чтобы изменить имя в данных по нужному индексу')
    print('Изменять можно также по фамилии(-s), отчеству(-o), дате рождения(-bd)')
    print('Флаги можно комбинировать. После каждого флага нужно вводить и соотвутствующее значение.')


# print
def print_all():
    max = len(data_listed)
    for index in range(0, max):
        print(get_str_by_index(index))
def print_by_index(index):
    print(get_str_by_index(index))
def print_by_filter(surname = None, name = None, otch = None, birth = None, number = None):
    found = []
    for index in range(0, len(data_listed)):
        inst = data_listed[index]
        if surname != None and inst[0].lower() != surname.lower():
            continue
        if name != None and inst[1].lower() != name.lower():
            continue
        if otch != None and inst[2].lower() != otch.lower():
            continue
        #if birth != None:
        #if number != None:
        found.append(index) 
    if len(found) == 0:
        print(f'Не найдено записей.')
    else:
        print(f'Найдено записей: {len(found)}')
        for elem in found:
            print_by_index(int(elem))


# change
def change_by_index(index = None, surname = None, name = None, otch = None, birthDay = None):
    to_change = data_listed[index]
    str_old = get_str_by_index(index)
    if surname != None:
        to_change[0] = surname
    if name != None:
        to_change[1] = name
    if otch != None:
        to_change[2] = otch
    if birthDay != None:
        to_change[3] = birthDay[0]
        to_change[4] = birthDay[1]
        to_change[5] = birthDay[2]
    print('Изменена запись:')
    print(str_old)
    print('на:')
    print(get_str_by_index(index))


# add
def add_listed(person, telefons):
    person.append(telefons)
    data_listed.append(person)
    print(f'Добавлена запись: {get_str_by_index(len(data_listed) - 1)}\n')
def add_by_index(index = None, telefons = None, telefons_comments = None, emails = None, emails_comments = None):
    if index == None:
        return
    inst = data_listed[index]
    telefons_combined = []
    telefons_combined += inst[6]
    telefons_combined += telefons
    telefons_combined = set(telefons_combined)
    inst[6] = list(telefons_combined)
    print(f'Добавлены данные в запись: {get_str_by_index(index)}\n')
        


# del
def del_by_index(index):
    if index < 0 or index > len(data_listed) - 1:
        print('Такой записи не существует.')
        return
    print(f'Удалена запись: {get_str_by_index(index)}')
    data_listed.pop(index)
def del_t_by_index(index, t_index):
    if index < 0 or index > len(data_listed) - 1:
        print('Такой записи не существует.')
        return
    inst = data_listed[index]
    tels = inst[6]
    if t_index >= len(tels) or t_index < 0:
        print('Такого номера не существует.')
        return
    tels.remove(tels[t_index])
    print('Номер удален.')



while True:
    s = str(input())
    # s = s.lower()
    s = s.strip('  ')
    # one word commands
    if s == 'clear' or s == 'c':
        print("\033[H\033[J", end="")
        continue
    if s == 'help' or s == 'h':
        help_main()
        continue
    if s == 'quit' or s == 'q':
        data.close()
        break
    if s == 'save' or s == 's':
        save_data_listed_as_data()
        continue
    if s == 'print' or s == 'p':
        print_all()
        continue
    # combined commands
    s_list = s.split()
    header = s_list.pop(0)
    if header == 'help' or header == 'h':
        header = s_list.pop(0)
        if header == "-add" or header == "-a":
            help_add()
        if header == "-print" or header == "-p":
            help_print()
        continue
    if header == "add" or header == "a":
        cancel = False
        index = None
        person = []
        birthDay = []
        telefons = []
        stacking = 'person'
        while len(s_list) > 0:
            header = s_list[0]
            if header == "-index" or header == "-i":
                stacking = None
                s_list.pop(0)
                if len(s_list) > 0:
                    index = int(s_list.pop(0))
                else:
                    print('Ошибка - после флага -i нужно указать индекс!')
                    cancel = True
                continue
            if header == "-telefons" or header == "-t":
                s_list.pop(0)
                if len(s_list) > 0:
                    stacking = 'telefons'
                else:
                    print('Ошибка - после флага -t нужно указать номер телефона!')
                    cancel = True
                continue
            if stacking == 'telefons':
                telefons.append(header)
                s_list.pop(0)
                continue
            if stacking == 'person':
                if len(person) < 3:
                    person.append(header)
                    s_list.pop(0)
                else:
                    birthDay = s_list.pop(0)
                    birthDay = birthDay.split('.')
                    if len(birthDay) < 3 and len(birthDay) > 0:
                        print('Ошибка - неверный формат даты рождения!')
                        cancel = True
        if len(s_list) > 0 and index != None:
            print('Ошибка - лишние данные в запросе.')
            cancel = True
        if not cancel:
            if index != None:
                if index < 0 or index > len(data_listed) - 1:
                    print('Ошибка - неверный индекс.')
                else:
                    add_by_index(index, telefons)
            else:
                if len(birthDay) == 0:
                    birthDay = ['None', 'None', 'None']
                person += birthDay
                if len(telefons) < 1:
                    print('Нужен хотя-бы один номер!')
                elif len(person) < 6:
                    print('Недостаточно вводных данных!')
                else:
                    add_listed(person, telefons)
        continue
    if header == 'delete' or header == 'd':
        cancel = False
        index = None
        t_index = None
        while len(s_list) > 0:
            header = s_list[0]
            if header == "-index" or header == "-i":
                s_list.pop(0)
                if len(s_list) > 0:
                    index = int(s_list.pop(0))
                else:
                    print('Ошибка - после флага -i нужно указать индекс!')
                    cancel = True
                continue
            if header == "-tel" or header == "-t":
                s_list.pop(0)
                if len(s_list) > 0:
                    t_index = int(s_list.pop(0))
                else:
                    print('Ошибка - после флага -t нужно указать индекс номера телефона!')
                    cancel = True
                continue
            break
        if len(s_list) > 0:
            print('Ошибка - лишние данные в запросе.')
            cancel = True
        if not cancel:
            if index == None or index < 0 or index > len(data_listed) - 1:
                print('Ошибка - неверный индекс.')
            else:
                if t_index != None:
                    del_t_by_index(index, t_index)
                else:
                    del_by_index(index)
        continue
    if header == "print" or header == "p":
        cancel_print = False
        index = None
        surname = None
        name = None
        otch = None
        while len(s_list) > 0:
            header = s_list[0]
            if header == "-index" or header == "-i":
                s_list.pop(0)
                if len(s_list) > 0:
                    index = int(s_list.pop(0))
                else:
                    print('Ошибка - после флага -i нужно указать индекс!')
                    cancel_print = True
                continue
            if header == "-surname" or header == "-s":
                s_list.pop(0)
                if len(s_list) > 0:
                    surname = s_list.pop(0)
                else:
                    print('Ошибка - после флага -s нужно указать фамилию!')
                    cancel_print = True
                continue
            if header == "-name" or header == "-n":
                s_list.pop(0)
                if len(s_list) > 0:
                    name = s_list.pop(0)
                else:
                    print('Ошибка - после флага -n нужно указать имя!')
                    cancel_print = True
                continue
            if header == "-otch" or header == "-o":
                s_list.pop(0)
                if len(s_list) > 0:
                    otch = s_list.pop(0)
                else:
                    print('Ошибка - после флага -o нужно указать отчество!')
                    cancel_print = True
                continue
            break
        if len(s_list) > 0:
            print('Ошибка - лишние данные в запросе.')
            cancel_print = True
        if index != None:
            if index < 0 or index > len(data_listed) - 1:
                print('Ошибка - неверный индекс.')     
            else:
                print_by_index(index)
        elif not cancel_print:
            print_by_filter(surname, name, otch)
        continue
    if header == "change" or header == "ch":
        cancel = False
        index = None
        surname = None
        name = None
        otch = None
        birthDay = None
        while len(s_list) > 0:
            header = s_list[0]
            if header == "-index" or header == "-i":
                s_list.pop(0)
                if len(s_list) > 0:
                    index = int(s_list.pop(0))
                else:
                    print('Ошибка - после флага -i нужно указать индекс!')
                    cancel = True
                continue
            if header == "-surname" or header == "-s":
                s_list.pop(0)
                if len(s_list) > 0:
                    surname = s_list.pop(0)
                else:
                    print('Ошибка - после флага -s нужно указать фамилию!')
                    cancel = True
                continue
            if header == "-name" or header == "-n":
                s_list.pop(0)
                if len(s_list) > 0:
                    name = s_list.pop(0)
                else:
                    print('Ошибка - после флага -n нужно указать имя!')
                    cancel = True
                continue
            if header == "-otch" or header == "-o":
                s_list.pop(0)
                if len(s_list) > 0:
                    otch = s_list.pop(0)
                else:
                    print('Ошибка - после флага -o нужно указать отчество!')
                    cancel = True
                continue
            if header == "-birthday" or header == "-bd":
                s_list.pop(0)
                if len(s_list) > 0:
                    birthDay = s_list.pop(0)
                    birthDay = birthDay.split('.')
                    if len(birthDay) < 3:
                        print('Ошибка - неверный формат даты рождения!')
                        cancel = True
                else:
                    print('Ошибка - после флага -d нужно указать дату!')
                    cancel = True
                continue
            break
        if len(s_list) > 0:
            print('Ошибка - лишние данные в запросе.')
            cancel = True
        if index == None or index < 0 or index > len(data_listed) - 1:
            print('Ошибка - неверный индекс.')
            cancel = True
        if not cancel:
            change_by_index(index, surname, name, otch, birthDay)
        continue
