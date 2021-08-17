from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import os

# Constants block
base_URL = "https://geographic.org/streetview/"
records = 0

# Main Loop to hit all the stages of processing
for stage in ['states','counties','cities','streets']:

    # Adding this 'stage' or 'pass' feature to make file name changing easier
    if stage == 'states':
        input_file = '../miscellaneous/country.txt'
        output_file = '../miscellaneous/states.txt'
    if stage == 'counties':
        input_file = '../miscellaneous/states.txt'
        output_file = '../miscellaneous/counties.txt'
    if stage == 'cities':
        input_file = '../miscellaneous/counties.txt'
        output_file = '../miscellaneous/cities.txt'
    if stage == 'streets':
        input_file = '../miscellaneous/cities.txt'
        output_file = '../miscellaneous/streets.txt'

    # Load in the source file
    file = open(input_file, 'r')
    URL_list = file.readlines()
    file.close()

    # Wipe out the file if it already exists, because things are written in append mode
    if os.path.exists(output_file):
        os.remove(output_file)

    # Reset the list, but add washington DC, because it's special
    if stage == 'cities':
        records_list = ['usa/dc/washington.html\n']
    else:
        records_list = list()

    # Step through all the links from the previous stage
    for old_link in URL_list:

        # Open connection, read page, close connection
        if stage != 'streets':
            myURL = base_URL + old_link.strip() + '/'
        else:
            myURL = base_URL + old_link.strip()

        # User Feedback for monitoring process
        print(myURL.strip())

        # Request the page, store as a variable, then close the request tool
        uClient = uReq(myURL)
        page_html = uClient.read()
        uClient.close()

        # html parsing
        page_soup = soup(page_html, 'html.parser')

        # Loop through all links on page scraping
        for new_link in page_soup.find_all('a'):

            # Filter off the garbage links
            if 'http' not in str(new_link) and 'twitter' not in str(new_link):

                # Script processes better if this is a string -- converting now
                write_me = str(new_link.get('href'))

                # Use this for scraping states
                if stage == 'states':
                    if write_me[0:3] == 'dc/':
                        file = open('../miscellaneous/cities.txt', 'a', encoding='UTF-8')
                        file.write('dc/washington.html')
                        file.close()
                    else:
                        records_list.append(old_link + write_me[0:3] + '\n') 

                # Use this for scraping counties
                if stage == 'counties':
                    records_list.append(old_link.strip() + write_me[0:-10].strip() + '\n') 

                # Use this for scraping cities
                if stage == 'cities':
                    records_list.append(old_link.strip() + write_me + '\n') 

                # Use this for scraping streets
                if stage == 'streets':

                    # Washington, D.C. is a nightmare...
                    if "D.C." in str(write_me):
                        records_list.append(str(write_me)[len('../../view.php?place='):-20] + ',' + str(write_me)[-20:len(str(write_me))] + '\n')

                    # All other cities follow this structure
                    else:
                        if str(write_me) not in ['#0-9','#A','#B','#C','#D','#E','#F','#G','#H','#I','#J','#K','#L','#M','#N','#O','#P','#Q','#R','#S','#T','#U','#V','#W','#Y','#Z','None','']:
                            records_list.append(str(write_me)[len('../../../view.php?place='):len(str(write_me))] + '\n')
                
        # Write out the list to file
        file = open(output_file, 'a', encoding='UTF-8')

        for record in records_list:

            # Don't write a blank line
            if record.strip() != '': 
                file.write(record)

        file.close()

        # Reset the list
        records_list = list()

    # User Feedback
    print("Stage", stage.upper, "scraping finished.")