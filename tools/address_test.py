import random
import pandas as pd

zip_code_distribution_file = '../reference/location/population_by_zip_code.csv'
usa_address_file = '../reference/location/usa_addresses.csv'
address_count_to_generate = 5

zip_code_distribution = pd.read_csv(zip_code_distribution_file)


def generate_zip_code():

    ''' Return a random zip code, based on 2010 Census population data. '''

    zip_code = random.choices(zip_code_distribution['zip_code'], weights = zip_code_distribution['population'])

    return(str(zip_code[0]))


def generate_address(zip_code, residence):

    ''' Return a randomly chosen street address, using zip_code and web-scraped data. Residence is a boolean value to denote a person's home, and enable apartment numbers or more complex street numbers.  (Non-commercial)'''

    possible_addresses = list()

    # Try to search the file, after loading into memory
    with open(usa_address_file, 'r', encoding='utf-8') as too_big_file:
        for line in too_big_file:
            if str(zip_code) in str(line):
                possible_addresses.append(line)

    # In case the search comes up with nothing
    if possible_addresses == []:
        possible_addresses.append('00000,STATE,COUNTY,CITY,STREET')

    # chop up the line into separate variables
    address = str(random.choice(possible_addresses)).split(sep = ',')
    address_country = 'United States'
    address_state = address[1]
    address_county = address[2]
    address_city = address[3]
    address_street = address[4]
    apartment = ''

    # Generate a bunch of random numbers, letters and apartment combinations for residences
    if residence:
        street_number = random.randint(1, 10000)
        if random.choices([True,False], weights = [1, 7])[0]:
            apartment = int(random.choices(range(1,25), weights = range(25,1,-1))[0])
            apartment += int(random.choices([0,100,200,300,400,500,600,700,800,900], weights = [50,9,8,7,6,5,4,3,2,1])[0])
            apartment = str('Apt ' + str(random.choices(['','A-','B-','C-','D-','E-','F-','G-','H-','I-'], weights = [50,9,8,7,6,5,4,3,2,1])[0]) + str(apartment))
    # Commercial address numbers are much more streamlined and likely to be a multiple of 100
    else:
        street_number = random.randrange(100, 10000, 100)

    # concatenate all the strings
    address_street = (str(street_number) + ' ' + str(address_street).strip() + ' ' + apartment).strip()

    # return the address values as discrete fields
    return(address_street, address_city, address_county, address_state, address_country)


# This is just to test the functions.  Prints out some generated addresses.
def main():

    print("COMMERCIAL ADDRESSES")

    for x in range(address_count_to_generate):
        zip_code = generate_zip_code()
        street, city, county, state, country = generate_address(zip_code, False)
        print('{}.   {}, {}, {} County, {}, {}, {}'.format(x + 1, street, city, county, state, country, str(zip_code).zfill(5)))

    print()
    print("RESIDENTIAL ADDRESSES")
    
    for x in range(address_count_to_generate):
        zip_code = generate_zip_code()
        street, city, county, state, country = generate_address(zip_code, True)
        print('{}.   {}, {}, {} County, {}, {}, {}'.format(x + 1, street, city, county, state, country, str(zip_code).zfill(5)))
    
    print()

if __name__ == '__main__':
    main()