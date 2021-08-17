import os

print(os.getcwd())

input_file = '../miscellaneous/streets.txt'
output_file = '../miscellaneous/streets_flipped.txt'
write_me = str()
count_me = 0

# open the output file as necessary
with open(output_file, 'w') as outfile:

    # write the string to file
    outfile.write('zip_code,state,county,city,street\n')

# Open input file, line by line.  Avoids loading whole thing in memory?
with open(input_file,'r') as infile:

    for line in infile:

        # Make a list of all address items(new order = general -> specific)
        address_item_list = line.split(sep=',')
        address_item_list = address_item_list[::-1]
        write_me = ''

        # Safeguard against wrong length read lines
        if len(address_item_list) >= 6:

            # Once again, making exceptions for D.C.
            if address_item_list[3].strip() == 'D.C.':

                # steps through comma-separated items in read-in line
                for x in [1,3,2,4]:
                    write_me += str(address_item_list[x]).strip() + ','

            # All other states
            else:

                # steps through comma-separated items in read-in line
                for x in [1,2,3,4]:
                    write_me += str(address_item_list[x]).strip() + ','

            # combine annoying 5th portion of address (usually cardinal direction) with street name
            if len(address_item_list) == 7:
                write_me += address_item_list[5].strip() + ' ' + address_item_list[6].strip()
            else:
                write_me += address_item_list[5]
    
            # User feedback
            count_me += 1
            if count_me > 10000:
                print(write_me)
                count_me = 0

            # append a new-line character to the end of the line to write
            write_me += '\n'

            # open the output file as necessary
            with open(output_file, 'a') as outfile:

                # write the string to file
                outfile.write(write_me)
