import time, json


def transfer_date(old_value, new_month, new_day):
    iso_formate = "%Y-%m-%dT%H:%M:%S.%fZ"
    normal_format = "%Y-%m-%d"
    print(normal_format)
    print(old_value)
    time_array = time.strptime(old_value, iso_formate)
    print(old_value)
    print('测试成功2')
    print(time_array)
    # right_time = time.strptime(normal_format, time_array)
    #
    # temp_month = right_time.replace('-12', new_month)
    # temp_day = temp_month.replace('-31', new_day)
    print('测试成功3')
    return time_array


def format_json(json_file, t_month, t_day):
    j = json.load(open(json_file))

    d = {}
    for key in j:
        print(key, j[key])
        print('测试成功')
        d[transfer_date(key, '-' + t_month, '-' + t_day)] = j[key]
    return d
