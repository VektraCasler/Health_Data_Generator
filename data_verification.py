lines = []
counter = 0

with open('OUTPUT/person_list.csv', 'r', encoding='UTF-8') as file:

    line = file.readline()
    print(line)

    while line != '':

        counter += 1
        if counter % 1000 == 0:
            print(counter)

        lines.append(line.split(sep=','))
        line = file.readline()

with open('OUTPUT/data_verification.csv', 'w', encoding='UTF-8') as file:

    for x in lines:

        writeout = "{},{},{},{},{}\n".format(x[4],x[5],x[6],x[7],x[15])
        file.write(writeout)
