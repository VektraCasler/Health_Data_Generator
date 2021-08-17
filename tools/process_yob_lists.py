import pandas as pd

male_names_list_file = "Male_Names.txt"
female_names_list_file = "Female_Names.txt"
YOB_file_headers = ["Name", "Sex", "Count"]

file = open("C:/Users/vcasler/Documents/Python_Scripts/data/SSN_Data/YOB Files Name Counts.txt", 'w')
file.write(("Year,Female Name Count,Male Name Count, Female SSNs Issued, Male SSNs Issued\n"))

for x in range(1880, 2021):

    # open the yob data files sequentially
    file_name_to_read = "C:/Users/vcasler/Documents/Python_Scripts/data/SSN_Data/yob" + str(x) + ".txt"
    this_DF = pd.read_csv(file_name_to_read, names = YOB_file_headers)
    line = (str(x) + "," + str(this_DF[this_DF["Sex"] == "F"].count(axis = 'index')[0]) + "," + str(this_DF[this_DF["Sex"] == "M"].count(axis = 'index')[0]) + "," + str(this_DF[this_DF["Sex"] == "F"].sum(axis = 'index')[2]) + "," + str(this_DF[this_DF["Sex"] == "M"].sum(axis = 'index')[2]) + "\n")
    file.write(line)

file.close()