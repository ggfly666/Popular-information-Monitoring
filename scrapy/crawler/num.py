def digit(chinese_number):
    '''
    将热度中带中文单位的数字转化为对应的阿拉伯数字
    '''
    units = {
    '十': 10,
    '百': 100,
    '千': 1000,
    '万': 10000,
    '亿': 100000000
    }
    if not isinstance(chinese_number, str):
        return chinese_number 
    for unit in units:
        if unit in chinese_number:
            num_part = chinese_number.split(unit)[0] 
            try:
                num = float(num_part)
                return int(num * units[unit]) if num.is_integer()  else num * units[unit]
            except ValueError:
                return chinese_number 
    try:
        return int(chinese_number) if float(chinese_number).is_integer() else float(chinese_number)
    except ValueError:
        return chinese_number 