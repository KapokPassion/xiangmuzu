import csv    #加载csv包便于读取csv文件
csv_file=open("D://average_result.csv")    #打开csv文件
csv_reader_lines = csv.reader(csv_file)   #逐行读取csv文件
date=[]    #创建列表准备接收csv各行数据

row = 0
for one_line in csv_reader_lines:

    date.append(one_line)    #将读取的csv分行数据按行存入列表‘date’中
    print(date[row][0])
    print(date[row][1])
    print(date[row][2])

    row = row + 1    #统计行数（这里是学生人数）

i=0

