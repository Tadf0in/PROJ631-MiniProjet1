import data2dict
from Line import Line


FILE_NAME = 'data/1_Poisy-ParcDesGlaisins.txt' 

data = data2dict.get_data(FILE_NAME)

line1 = Line('1_Poisy-ParcDesGlaisins', data)