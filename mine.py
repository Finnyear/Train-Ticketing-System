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
    return final_id