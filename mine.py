class Order_:
    status = ''
    id_ = ''
    from_ = ''
    from_date = ''
    from_time = ''
    to = ''
    to_date = ''
    to_time = ''
    price = ''
    num = ''
    
class Ticket_:
    id_ = ''
    from_ = ''
    from_date = ''
    from_time = ''
    to = ''
    to_date = ''
    to_time = ''
    price = ''
    seats = ''

class Train_:
    station = ''
    to_date = ''
    to_time = ''
    from_date = ''
    from_time = ''
    price = ''
    remain = ''

class User_:
    u_name = ''
    name = ''
    mail = ''
    p_ = ''

def id_check_valid(input_id):
    final_id = ''
    cnt_space = 0
    for i in input_id:
        if i == ' ' and (cnt_space == 0 or cnt_space == 2):
            continue
        if i != ' ' and cnt_space == 0:
            cnt_space = 1
            if (i <= 'Z' and i >= 'A') or (i <= 'z' and i >= 'a'):
                final_id += i
                continue
            else:
                return '!'
        if i != ' ' and cnt_space == 2:
            return '!'
        if i == ' ' and cnt_space == 1:
            cnt_space = 2
            continue

        if (i <= '9' and i >= '0') or (i <= 'Z' and i >= 'A') or (i <= 'z' and i >= 'a') or i == '_':
            final_id += i
        else:
            return '!'
    if len(final_id) > 20:
        return '!'
    return final_id

def password_check_valid(input_password):
    if len(input_password) > 30 or len(input_password) < 6:
        return '!'
    for i in input_password:
        if not((i <= '9' and i >= '0') or (i <= 'Z' and i >= 'A') or (i <= 'z' and i >= 'a') or i == '_'):
            return '!'
    return input_password

def name_check_valid(input_name):
    if len(input_name) > 5 or len(input_name) < 2:
        return '!'
    return input_name

def check_num(input, x, y):
    if x == 0:
        return 1
    inputs = input.split('|')
    if len(inputs) != x:
        return 0
    for i in inputs:
        if int(i) > y:
            return 0
    return 1

def check_station_name(input, x):
    inputs = input.split('|')
    if len(inputs) != x:
        return 0
    for i in inputs:
        if len(i) > 10:
            return 0
    return 1

def check_date(x, y):
    if int(x) == 6 and 0<int(y)<31:
        return 1
    if (int(x) == 7 or int(x) == 8) and 0 < int(y) <= 31:
        return 1
    return 0 