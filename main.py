import easygui as eg

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
    # print('Сохранено.\n')


# get str
def get_str_by_index(index):
    # original = [str(x) for x in data_listed[index]]
    # print(f'original {str(original)}')
    index = int(index)
    inst = data_listed[index]
    denulled = [inst[x] for x in range(0, 3)]
    bd = []
    for x in range(3, 6):
        if inst[x] == 'None':
            bd.append('?')
        else:
            bd.append(inst[x])
    denulled += ['.'.join(str(x) for x in bd)]
    denulled += ['Номера:']
    numbers_count = len(inst[6])
    denulled += [', '.join(str(x) for x in inst[6])]
    # remove None
    while denulled.count('None') > 0:
        denulled.remove('None')
    ret = [str(index) + '.'] + denulled
    return ' '.join(str(elem) for elem in ret)


def to_add_format(to_add, add_missing = True):
    for i in range(0, len(to_add)):
        if to_add[i].count(' ') > 0:
            to_add[i] = to_add[i].replace(' ', '')
        if len(to_add[i]) == 0:
            to_add[i] = None
    if len(to_add) > 3:
        if to_add[3] != None:
            to_add[3] = to_add[3].split('.')
            while len(to_add[3]) < 3:
                to_add[3].append('?')
        elif add_missing:
            to_add[3] = ['?', '?', '?']
    if len(to_add) > 4:        
        if to_add[4] != None and type(to_add[4]) is list:
            to_add[4] = to_add[4].split(',')
    return to_add


# find
def print_all():
    max = len(data_listed)
    for index in range(0, max):
        print(get_str_by_index(index))
def print_by_index(index):
    print(get_str_by_index(index))
def list_by_filter(forma):
    surname = forma[0]
    name = forma[1]
    otch = forma[2]
    birth = forma[3]
    number = forma[4]
    found = []
    for index in range(0, len(data_listed)):
        inst = data_listed[index]
        if surname != None and inst[0].lower() != surname.lower():
            continue
        if name != None and inst[1].lower() != name.lower():
            continue
        if otch != None and inst[2].lower() != otch.lower():
            continue
        if birth != None:
            if birth[0] != 'None' and birth[0] != '?':
                if birth[0] != inst[3]:
                    continue
            if birth[1] != 'None' and birth[1] != '?':
                if birth[1] != inst[4]:
                    continue
            if birth[2] != 'None' and birth[2] != '?':
                if birth[2] != inst[5]:
                    continue
        if number != None:
            found_number = False
            for x in inst[6]:
                if number == x:
                    found_number = True
                    break
            if not found_number:
                continue
        found.append(index) 
    return found


# change
def change_by_index_msg(index):
    index = int(index)
    msg = get_str_by_index(index)
    title = "title"
    choices = ['Изменить основные данные','Изменить номера телефонов', 'Удалить запись']
    change_or_delete = eg.choicebox(msg, title, choices)
    if change_or_delete == 'Изменить основные данные':
        msg =f"Заполните поля. Дату рождения нужно указывать в формате ДД.ММ.ГГГГ. Вместо неизвестных вводите ?.\n{get_str_by_index(index)}"
        title = "title"
        fields = ['Фамилия:', 'Имя:', 'Отчество:','Дата рождения:']
        values = []
        forma = eg.multenterbox(msg, title, fields, values)
        forma = to_add_format(forma, False)
        invalid_person = True
        for i in range(0,len(forma)):
            if forma[i] != None:
                invalid_person = False
        if not invalid_person:
            change_by_index_data(index, forma)
        else:
            eg.msgbox("Неизвестная ошибка!")
    elif change_or_delete == 'Изменить номера телефонов':
        nums = [x for x in data_listed[index][6]]
        for i in range(0, len(nums)):
            nums[i] = f'{i}. {nums[i]}'
        msg ="Выберите номер."
        title = "title"
        choices = ['Добавить'] + nums
        chosen = eg.choicebox(msg, title, choices)
        if chosen == 'Добавить':
            msg =f"Добавляем номер..."
            title = "title"
            num_new = eg.enterbox(msg, title)
            data_listed[index][6].append(num_new)
        else:
            num_index = int(chosen.split('.')[0])
            msg ="Что с ним делать?."
            title = "title"
            choices = ['Изменить', 'Удалить']
            choice = eg.choicebox(msg, title, choices)
            if choice == 'Изменить':
                msg =f"Заменяем номер {data_listed[index][6][num_index]} на..."
                title = "title"
                num_new = eg.enterbox(msg, title)
                data_listed[index][6][num_index] = num_new
            elif choice == 'Удалить':
                data_listed[index][6].pop(num_index)   
    elif change_or_delete == 'Удалить запись':
        data_listed.remove(data_listed[index])
def change_by_index_data(index, forma):
    index = int(index)
    inst = data_listed[index]
    surname = forma[0]
    name = forma[1]
    otch = forma[2]
    birth = forma[3]
    if surname != None:
        inst[0] = surname
    if name != None:
        inst[1] = name
    if otch != None:
        inst[2] = otch
    if birth != None:
        inst[3] = birth[0]
        inst[4] = birth[1]
        inst[5] = birth[2]


# add
def add_listed(to_add):
    date = to_add[3]
    to_add[3] = date[0]
    to_add.insert(4, date[2])
    to_add.insert(4, date[1])
    data_listed.append(to_add)
    # print(f'Добавлена запись: {get_str_by_index(len(data_listed) - 1)}\n')

while True:
    find_or_add = None
    if True:
        msg ="Чтобы изменить существующую запись, ее сперва нужно найти."
        title = "title"
        choices = ["Найти", "Добавить"]
        find_or_add = eg.choicebox(msg, title, choices)
    if find_or_add == None:
        break
    elif find_or_add == 'Добавить':
        forma = []
        if True:
            msg ="Заполните поля. Дату рождения нужно указывать в формате ДД.ММ.ГГГГ. Вместо неизвестных вводите ?. Если номеров несколько, укажите их через запятую."
            title = "title"
            fields = ['Фамилия:', 'Имя:', 'Отчество:','Дата рождения:','Номера телефонов:']
            values = []
            forma = eg.multenterbox(msg, title, fields, values)
            forma = to_add_format(forma)
            invalid_person = True
            for i in range(0,len(forma)):
                if forma[i] != None:
                    invalid_person = False
            if not invalid_person:
                add_listed(forma)
            else:
                eg.msgbox("Нельзя добавить пустую запись!")
    elif find_or_add == 'Найти':
        msg ="Можно найти запись по индексу, либо по другим данным."
        title = "title"
        choices = ["По индексу", "По другим данным"]
        index_or_data = eg.choicebox(msg, title, choices)
        if index_or_data == 'По индексу':
            msg = "Введите индекс."
            title = "title"
            index = eg.integerbox(msg, title)
            if index < 0:
                eg.msgbox("Индекс должен быть больше нуля!")
            elif index > len(data_listed) - 1:
                eg.msgbox("Нет такой записи!")
            else:
                change_by_index_msg(index)
        elif index_or_data == 'По другим данным':
            forma = []
            msg ="Заполните поля, по которым будет вестись поиск, ненужные поля оставьте пустыми. Дату рождения нужно указывать в формате ДД.ММ.ГГГГ. Вместо неизвестных вводите ?."
            title = "title"
            fields = ['Фамилия:', 'Имя:', 'Отчество:','Дата рождения:', 'Номер телефона:']
            values = []
            forma = eg.multenterbox(msg, title, fields, values)
            forma = to_add_format(forma, False)
            invalid_person = True
            for i in range(0,len(forma)):
                if forma[i] != None:
                    invalid_person = False
            if not invalid_person:
                found_list = list_by_filter(forma)
                if len(found_list) == 0:
                    eg.msgbox("Не найдено записей...")
                elif len(found_list) == 1:
                    change_by_index_msg(found_list[0])
                else:
                    msg ="Выберите запись."
                    title = "title"
                    choices = [get_str_by_index(x) for x in found_list]
                    chosen = eg.choicebox(msg, title, choices)
                    index = chosen.split('.')[0]
                    change_by_index_msg(index)
            else:
                eg.msgbox("Нельзя искать пустую запись!")
    save_data_listed_as_data()

