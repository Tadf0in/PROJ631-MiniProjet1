def read_file(file_name:str) -> str:    
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            content = f.read()
            return content
    except OSError:
        print("File not found")


def dates2dic(dates:str) -> dict:
    dic = {}
    splitted_dates = dates.split("\n")
    for stop_dates in splitted_dates:
        tmp = stop_dates.split(" ")
        dic[tmp[0]] = tmp[1:]
    return dic


def get_data(data_file_name:str) -> dict:
    content = read_file(data_file_name)
    splited_content = content.split("\n\n")
    regular_path = splited_content[0].split(' N ')
    regular_date_go = dates2dic(splited_content[1])
    regular_date_back = dates2dic(splited_content[2])
    we_holidays_path = splited_content[3].split(' N ')
    we_holidays_date_go = dates2dic(splited_content[4])
    we_holidays_date_back = dates2dic(splited_content[5])
    return {
        'regular_path': regular_path,
        'regular_date_go': regular_date_go,
        'regular_date_back': regular_date_back,
        'we_holidays_path': we_holidays_path,
        'we_holidays_date_go': we_holidays_date_go,
        'we_holidays_date_back': we_holidays_date_back
    }


if __name__ == '__main__':
    # data_file_name = 'data/sibra/1_Poisy-ParcDesGlaisins.txt' 
    data_file_name = 'data/sibra/2_Piscine-Patinoire_Campus.txt'
    #data_file_name = 'data/sibra/4_Seynod_Neigeos-Campus.txt'
    
    data = get_data(data_file_name)
    
    print("regular_path", data['regular_path'])
    # print("regular_date_go", data['regular_date_go'])
    # print("regular_date_back", data['regular_date_back'])
