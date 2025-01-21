import data2dict
from Line import Line


# FILE_NAME1 = 'data/sibra/1_Poisy-ParcDesGlaisins.txt' 
# FILE_NAME2 = 'data/sibra/2_Piscine-Patinoire_Campus.txt'
# FILE_NAME3 = 'data/sibra/4_Seynod_Neigeos-Campus.txt'


FILE_NAME1 = 'data/exemple/rouge.txt' 
FILE_NAME2 = 'data/exemple/vert.txt'
FILE_NAME3 = 'data/exemple/bleu.txt'


def data_to_obj(file_name:str) -> Line:
    data = data2dict.get_data(file_name)
    line_name = file_name.split('/')[-1].removesuffix('.txt')
    line = Line(line_name, data)
    return line


line1 = data_to_obj(FILE_NAME1)
line2 = data_to_obj(FILE_NAME2)
line3 = data_to_obj(FILE_NAME3)


print(line1.name, line2.name, line3.name)