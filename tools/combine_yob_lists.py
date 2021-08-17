import pandas as pd

final_output_file_name = "../reference/name/person_names.csv"
processing_file = "../miscellaneous/yob_processing.csv"
output_file = open(processing_file, 'w', encoding='ascii')
output_file.write("name,sex,count,year\n")
YOB_file_headers = ["name", "sex", "count"]

# yob name files range from 1880 to 2020
for year in range(1880, 2021):

    # open the yob data files sequentially
    file_name_to_read = "../miscellaneous/yobs/yob" + str(year) + ".txt"
    this_DF = pd.read_csv(file_name_to_read, names = YOB_file_headers)

    # creating a list to use to make a column for year data while outputting to file
    year_series = list()

    for y in range(len(this_DF.index)):
        year_series.append(year)

    # create a column from list data
    this_DF["year"] = year_series

    # Add chunk from single yob file to master
    output_file.write(this_DF.to_csv(index=False,line_terminator="",header=False))
    print("Writing data for year", year, "to", processing_file)

# user feedback and close file
print("File successfully written.")
output_file.close()

# Second part of processing: help with funky windows text formatting making double lines, and reorder columns
print("Removing additional carriage returns...")

# open processing file and final output file
output_file = open(final_output_file_name, 'w')
input_file = open(processing_file, 'r')
count = 1

# pull first line
line = input_file.readline()

# If not EOF, process...
while line:
 
    # skip blank lines, reorder column outputs
    if line.strip() != "":
        line_items = line.strip().split(sep=',')
        output_file.write('{},{},{},{}\n'.format(line_items[3],line_items[1],line_items[0],line_items[2]))
    
    # pull another line
    line = input_file.readline()

    # user feedback
    if count % 100000 == 0:
        print("Writing line", count)
    count += 1

# close all and user feedback
output_file.close()
input_file.close()
print("Processing complete:", final_output_file_name, "successfully written.")