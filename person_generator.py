import random
import datetime
import pandas as pd
from tqdm import tqdm
import math

# File names and global variables
output_file_name = 'OUTPUT/person_list.csv'
race_distribution_file = 'REFERENCE/ancestry/race_distribution.csv'
ethnicity_distribution_file = 'REFERENCE/ancestry/ethnicity_distribution.csv'
age_category_distribution_file = 'REFERENCE/age/age_category_distribution.csv'
zip_code_distribution_file = 'REFERENCE/location/population_by_zip_code.csv'
usa_addresses_file = 'REFERENCE/location/usa_addresses.csv'
person_names_file = 'REFERENCE/name/person_names.csv'
surnames_asian_file = 'REFERENCE/surname/surnames_asian.csv'
surnames_black_file = 'REFERENCE/surname/surnames_black.csv'
surnames_generic_file = 'REFERENCE/surname/surnames_generic.csv'
surnames_hispanic_file = 'REFERENCE/surname/surnames_hispanic.csv'
surnames_native_file = 'REFERENCE/surname/surnames_native.csv'
surnames_white_file = 'REFERENCE/surname/surnames_white.csv'
email_domains_file = 'REFERENCE/email/email_domains.csv'

# read source files into memory
DF_race_distribution = pd.read_csv(race_distribution_file)
DF_ethnicity_distribution = pd.read_csv(ethnicity_distribution_file)
DF_age_category_distribution = pd.read_csv(age_category_distribution_file)
DF_zip_code_distribution = pd.read_csv(zip_code_distribution_file)
DF_usa_addresses = pd.read_csv(usa_addresses_file)
DF_person_names = pd.read_csv(person_names_file)
DF_surname_asian = pd.read_csv(surnames_asian_file)
DF_surname_black = pd.read_csv(surnames_black_file)
DF_surname_generic = pd.read_csv(surnames_generic_file)
DF_surname_hispanic = pd.read_csv(surnames_hispanic_file)
DF_surname_native = pd.read_csv(surnames_native_file)
DF_surname_white = pd.read_csv(surnames_white_file)
DF_email_domains = pd.read_csv(email_domains_file)

# Global Variables
number_of_records = 100000 # Number of records to generate
person_sexes = ["Male", "Female"]
SSN_list = ['000-00-0000']  # Track SSN values to ensure no duplicates for person, with 000-00-0000 as a guaranteed 'not used'
MRN_list = ['M00000000']

# permitted phone area codes
usable_area_codes = [201,202,203,205,206,207,208,209,210,212,213,214,215,216,217,218,219,220,221,223,224,225,227,228,229,230,231,232,234,235,237,238,239,240,241,242,243,245,246,247,248,251,252,253,254,256,257,258,259,260,261,262,264,265,267,268,269,270,271,272,273,274,275,276,278,279,280,281,282,283,284,285,286,287,289,301,302,303,304,305,307,308,309,310,312,313,314,315,316,317,318,319,320,321,323,324,325,326,327,328,329,330,331,332,334,335,336,337,338,339,340,341,342,345,346,347,348,349,350,351,352,353,356,357,358,359,360,361,362,363,364,369,380,381,383,384,385,386,389,401,402,403,404,405,406,407,408,409,410,412,413,414,415,416,417,418,419,420,421,423,424,425,426,427,428,429,430,431,432,434,435,436,437,438,439,440,441,442,443,445,446,447,448,449,450,451,452,453,454,456,457,458,459,460,461,462,463,464,465,467,468,469,470,471,472,473,474,475,476,478,479,480,481,482,483,484,485,486,487,489,501,502,503,504,505,507,508,509,510,512,513,515,516,517,518,520,530,531,534,536,537,539,540,541,551,557,559,560,561,562,563,564,565,567,568,570,571,572,573,574,575,576,580,582,583,585,586,601,602,603,605,606,607,608,609,610,612,614,615,616,617,618,619,620,621,623,624,625,626,627,628,629,630,631,632,634,635,636,637,638,640,641,642,643,645,646,648,649,650,651,652,653,654,656,657,658,659,660,661,662,663,664,665,667,668,669,670,671,673,674,675,676,678,679,680,681,682,684,685,686,687,689,701,702,703,704,706,707,708,712,713,714,715,716,717,718,719,720,721,723,724,725,726,727,728,729,730,731,732,734,735,736,737,738,739,740,741,743,745,746,747,748,749,750,751,752,754,756,757,758,759,760,761,762,763,764,765,767,768,769,770,771,772,773,774,775,776,779,781,783,784,785,786,787,789,801,802,803,804,805,806,808,809,810,812,813,814,815,816,817,818,820,821,823,824,826,827,828,829,830,831,832,834,835,836,837,838,839,840,841,842,843,845,846,847,848,849,850,851,852,853,854,856,857,858,859,860,861,862,863,864,865,868,869,870,871,872,874,875,876,878,901,903,904,906,907,908,909,910,912,913,914,915,916,917,918,919,920,921,923,924,925,926,927,928,929,930,931,932,934,935,936,937,938,939,940,941,943,945,946,947,948,949,951,952,953,954,956,957,958,959,970,971,972,973,974,975,976,978,979,980,981,982,983,984,985,986,987,989]


def generate_race():

    ''' Randomly choses a person's race/heritage, based on US population 2010 census data. '''
    
    person_race = random.choices(DF_race_distribution["identification"], weights = DF_race_distribution["weight"])[0]

    if person_race in ['White','Mixed','Unreported']:

        person_ethnicity = random.choices(DF_ethnicity_distribution['identification'], weights = DF_ethnicity_distribution['weight'])[0]

    else:

        person_ethnicity = "Unreported"

    return (str(person_race), str(person_ethnicity))


def generate_sex():

    ''' Randomly generates a person sex, with only male/female options. '''

    return random.choice(person_sexes).strip().capitalize()


def generate_age(person_sex):

    ''' Generates a random person age, according to population distributions from 2010 US census data. '''

    if person_sex == "Male":
        category_weights = DF_age_category_distribution["male_count"]
    else:
        category_weights = DF_age_category_distribution["female_count"]

    person_age_category = int(random.choices(DF_age_category_distribution["age_floor"], weights = category_weights)[0])

    return (person_age_category + random.choice(range(5)))


def generate_SSN():

    ''' Generates a random SSN, ensures that it is not all 0's, records the new SSN into a list (to ensure a unique identifier for the person), and returns the value. '''

    AAA = str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9))
    GG = str(random.randint(0,9)) + str(random.randint(0,9))
    SSSS = str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9))
    SSN = AAA + "-" + GG + "-" + SSSS

    return SSN


def generate_surname(person_race, person_ethnicity, person_sex):

    ''' Randomly generates a person's surname from 2010 census data, and randomly hyphenates last names for data variety.  '''

    # Select proper surname list, based on ancestry
    if person_race == 'White':
        DF_surname = DF_surname_white
    elif person_race == 'Black':
        DF_surname = DF_surname_black
    elif person_race == 'Native American':
        DF_surname = DF_surname_native
    elif person_race in ['Asian','Pacific Islander']:
        DF_surname = DF_surname_asian
    else:
        DF_surname = DF_surname_generic
    if person_ethnicity == 'Hispanic':
        DF_surname = DF_surname_hispanic

    # typical name
    hyphenate = False   
    person_surname = str(random.choices(DF_surname["Name"], weights = DF_surname["Count"])[0]).strip().capitalize()

    # These values approximate the chance of a hyphenated name (Yet to find reliable data.  Fabricating values.)
    if person_sex == "Female":
        if random.random() < 0.03: # 3% chance
            hyphenate = True
    else:
        if random.random() < 0.001: # 0.1% chance
            hyphenate = True

    # Loop to choose another name, but not the same name (Eg. No 'Lopez-Lopez' permitted.)
    while hyphenate:

        person_surname_2 = str(random.choices(DF_surname["Name"], weights = DF_surname["Count"])[0]).strip().capitalize()

        if person_surname_2 != person_surname:
            person_surname += "-" + person_surname_2
            hyphenate = False

    return person_surname


def generate_name(person_sex, year_of_birth):

    # No SSN data yet for 2021, using 2020 data
    if int(year_of_birth) >= 2021:
        year_of_birth = 2020

    # Slice the master names dataframe for the birth year
    names_list = DF_person_names[DF_person_names["year"] == int(year_of_birth)]

    # Eliminate portion of list for other gender
    names_list = names_list[names_list["sex"] == str(person_sex)[0]]

    # Use weighted choice method in random module
    return str(random.choices(list(names_list["name"]), weights = list(names_list["count"]))[0]).strip().capitalize()


def generate_DOB(person_age):
    
    """ Subtracts person's age in days, as well as a random number of days between 0 and 364, from today's date, to generate a date of birth for the person. """
    
    return str(datetime.date.today() - datetime.timedelta(days = 365 * float(person_age)) - datetime.timedelta(days=random.random() * 365))


def generate_zip_code():

    ''' Return a random zip code, based on 2010 Census population data. '''

    zip_code = random.choices(DF_zip_code_distribution['zip_code'], weights = DF_zip_code_distribution['population'])

    return(str(zip_code[0]).zfill(5))


def generate_address(zip_code, residence):

    ''' Return a randomly chosen street address, using zip_code and web-scraped data. Residence is a boolean value to denote a person's home, and enable apartment numbers or more complex street numbers.  (Non-commercial)'''

    # slice the full address DF into matches based on zip_code
    DF_possible_addresses = DF_usa_addresses[DF_usa_addresses['zip_code'] == int(zip_code)]

    # In case the search comes up with nothing
    if int(DF_possible_addresses.shape[0]) == 0:
        DF_add_me = pd.DataFrame([['00000','STATE','COUNTY','CITY','STREET']], columns = ['zip_code','state','county','city','street'])
        DF_possible_addresses = DF_possible_addresses.append(DF_add_me, ignore_index=True)
        
    # get a random index value of the possible choices
    choose_me = random.randint(0, DF_possible_addresses.shape[0]-1)

    # Then extract that row from the dataframe, based on the index value
    address = DF_possible_addresses.iloc[choose_me]

    # chop up the line into separate variables

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


def generate_MRN():

    ''' Randomly generates an MRN. '''

    my_MRN = random.choice(['M','E','D','I','C','A','L'])
    for x in range(8):
        my_MRN += str(random.randint(0,9))

    return my_MRN


def generate_phone_number():

    ''' Randomly generates a phone number. '''

    # generate area code using restrictions above
    area_code = random.choice(usable_area_codes)

    # generate middle 3 digits
    prefix_code = 0
    while prefix_code in [0,211,311,411,511,611,711,811,911]:
        prefix_code = random.randint(200,999)

    # assemble and last 4 digits
    phone_number = str(area_code) + '-' + str(prefix_code) + '-' + str(random.randint(0,9999)).zfill(4)

    return phone_number


def generate_name_suffix():

    ''' Randomly generates a name suffix. Generational titles only.  Non-professional. '''

    list_of_suffixes = ['Sr.', 'Jr.', 'II', 'III', 'IV']

    suffix = str(random.choices(list_of_suffixes, weights = [100,100,100,50,10])[0])

    return suffix


def generate_email(person_name, person_surname):

    ''' Randomly generates an email address. '''

    # random flip-flop
    if random.random() < 0.5:
        store_me = person_name
        person_name = person_surname
        person_surname = store_me

    person_email = random.choice([person_name, (person_name + "_"), (person_name + '.'), ""])
    person_email += person_surname + str(random.randint(1,999)) + '@'
    person_email += random.choices(DF_email_domains['domain'], weights = DF_email_domains['count'])[0].strip()

    return person_email


def cumulative_distribution(x, x0, gamma):

    ''' Calculates a percentage distribution based on x0 and gamma values. x is a the independent variable.  '''

    return(1.0 / math.pi * math.atan(( x - x0) / gamma) + 0.5)


def main():

    # Prep the main output file
    header = 'name,middle_name,surname,name_suffix,age,race,ethnicity,sex,DOB,SSN,MRN,street,city,county,state,zip,country,cell_phone,home_phone,work_phone,email'.upper() + "\n"

    with open(output_file_name, 'w', encoding='UTF-8') as file:
        
        file.write(header)

    # Loop to create specificed number of records
    for x in tqdm(range(number_of_records)):

        # Generate basic demographics
        person_race, person_ethnicity = generate_race()
        person_sex = generate_sex()
        person_age = generate_age(person_sex)
        person_DOB = generate_DOB(person_age)

        # generate names, middles names, surnames, and generational suffixes
        person_surname = generate_surname(person_race, person_ethnicity, person_sex)
        person_name = generate_name(person_sex, (str(person_DOB)[0:4]))
        person_middle_name = person_name
        while person_middle_name == person_name:
            person_middle_name = generate_name(person_sex, (str(person_DOB)[0:4]))

        if person_sex == 'Male' and person_age > 20 and random.random() < 0.01:
            person_name_suffix = generate_name_suffix()
        else:
            person_name_suffix = ""

        # Generate unique identification numbers
        person_SSN = '000-00-0000'
        while person_SSN in SSN_list:
            person_SSN = generate_SSN()
        SSN_list.append(person_SSN)

        person_MRN = 'M00000000'
        while person_MRN in MRN_list:
            person_MRN = generate_MRN()
        MRN_list.append(person_MRN)

        # reset values
        person_cell_phone = ""
        person_home_phone = ""
        person_work_phone = ""
        person_email = ""

        # Chance for person to have email based on age
        if random.random() < cumulative_distribution(person_age, 8, 3):
            person_email = generate_email(person_name, person_surname)

        # Chance for person to have phone numbers based on age
        if random.random() < (0.97 * cumulative_distribution(person_age, 10, 3)):
            person_cell_phone = generate_phone_number()
        if random.random() < (0.40 * cumulative_distribution(person_age, 15, 4)):
            person_home_phone = generate_phone_number()
        if random.random() < (0.75 * cumulative_distribution(person_age, 20, 5)):
            person_work_phone = generate_phone_number()

        # Create an address
        person_zip = generate_zip_code()
        person_street, person_city, person_county, person_state, person_country = generate_address(person_zip, True)
        
        # Create the record for writing
        new_record = '{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(
            person_name, 
            person_middle_name, 
            person_surname, 
            person_name_suffix, 
            person_age, 
            person_race, 
            person_ethnicity, 
            person_sex, 
            person_DOB, 
            person_SSN, 
            person_MRN, 
            person_street, 
            person_city, 
            person_county, 
            person_state, 
            person_zip, 
            person_country, 
            person_cell_phone, 
            person_home_phone, 
            person_work_phone, 
            person_email
            )
            
        with open((output_file_name), 'a', encoding='UTF-8') as file:
            file.write(new_record)

    print('{} records generated and written to {}'.format(number_of_records, output_file_name))


if __name__ == "__main__":
    main()