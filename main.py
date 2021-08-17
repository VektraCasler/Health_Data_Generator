import random
import datetime
import pandas as pd
from tqdm import tqdm
import math
import os

# File names global constants
PERSON_LIST_FILE_NAME = 'OUTPUT/person_list.csv'
PROVIDER_LIST_FILE_NAME = 'OUTPUT/provider_list.csv'
RACE_DISTRIBUTION_FILE_NAME = 'REFERENCE/ancestry/race_distribution.csv'
ETHNICITY_DISTRIBUTION_FILE_NAME = 'REFERENCE/ancestry/ethnicity_distribution.csv'
AGE_CATEGORY_DISTRIBUTION_FILE_NAME = 'REFERENCE/age/age_category_distribution.csv'
ZIP_CODE_DISTRIBUTION_FILE_NAME = 'REFERENCE/location/population_by_zip_code.csv'
USA_ADDRESSES_FILE_NAME = 'REFERENCE/location/usa_addresses.csv'  # Warning, very large file
PERSON_NAMES_FILE_NAME = 'REFERENCE/name/person_names.csv'  # Warning, large file
SURNAMES_ASIAN_FILE_NAME = 'REFERENCE/surname/surnames_asian.csv'
SURNAMES_BLACK_FILE_NAME = 'REFERENCE/surname/surnames_black.csv'
SURNAMES_GENERIC_FILE_NAME = 'REFERENCE/surname/surnames_generic.csv'
SURNAMES_HISPANIC_FILE_NAME = 'REFERENCE/surname/surnames_hispanic.csv'
SURNAMES_NATIVE_FILE_NAME = 'REFERENCE/surname/surnames_native.csv'
SURNAMES_WHITE_FILE_NAME = 'REFERENCE/surname/surnames_white.csv'
EMAIL_DOMAINS_FILE_NAME = 'REFERENCE/email/email_domains.csv'
PROVIDER_TYPE_FILE = "REFERENCE/provider/provider_type.csv"
PROVIDER_SPECIALTY_FILE = "REFERENCE/provider/provider_specialty.csv"

# read source files into dataframes in memory
DF_race_distribution = pd.read_csv(RACE_DISTRIBUTION_FILE_NAME)
DF_ethnicity_distribution = pd.read_csv(ETHNICITY_DISTRIBUTION_FILE_NAME)
DF_age_category_distribution = pd.read_csv(AGE_CATEGORY_DISTRIBUTION_FILE_NAME)
DF_zip_code_distribution = pd.read_csv(ZIP_CODE_DISTRIBUTION_FILE_NAME)
DF_usa_addresses = pd.read_csv(USA_ADDRESSES_FILE_NAME)
DF_person_names = pd.read_csv(PERSON_NAMES_FILE_NAME)
DF_surname_asian = pd.read_csv(SURNAMES_ASIAN_FILE_NAME)
DF_surname_black = pd.read_csv(SURNAMES_BLACK_FILE_NAME)
DF_surname_generic = pd.read_csv(SURNAMES_GENERIC_FILE_NAME)
DF_surname_hispanic = pd.read_csv(SURNAMES_HISPANIC_FILE_NAME)
DF_surname_native = pd.read_csv(SURNAMES_NATIVE_FILE_NAME)
DF_surname_white = pd.read_csv(SURNAMES_WHITE_FILE_NAME)
DF_email_domains = pd.read_csv(EMAIL_DOMAINS_FILE_NAME)
DF_provider_specialty = pd.read_csv(PROVIDER_SPECIALTY_FILE)
DF_provider_type = pd.read_csv(PROVIDER_TYPE_FILE)

# Global Constants
NUMBER_OF_PERSONS_TO_GENERATE = 100000 # Number of records to generate
NUMBER_OF_PROVIDERS_TO_GENERATE = 500
MIN_PROVIDER_AGE = 25
PROVIDER_ID_PREFIX_CODES = ["01","02","03","00","04","89","05","55","75","92","06","91","07","81","08","09","10","68","69","11","85","12","13","54","14","78","15","16","76","17","70","18","19","71","95","30","31","83","32","96","33","57","34","86","35","36","72","37","90","38","93","39","73","40","84","41","42","87","43","44","88","45","67","74","97","46","47","48","20","21","80","22","82","23","24","77","25","26","79","27","28","29","49","50","94","51","58","52","53","56","59","64","65","66","99"]
PROVIDER_ID_THIRD_DIGIT_CODES = ["0","1","2","3","4","5","6","7","8","9","M","S","T","U","W","Y","Z"]
LIST_OF_SUFFIXES = ['Sr.', 'Jr.', 'II', 'III', 'IV']
PERSON_SEXES = ["Male", "Female"]
USABLE_AREA_CODES = [201,202,203,205,206,207,208,209,210,212,213,214,215,216,217,218,219,220,221,223,224,225,227,228,229,230,231,232,234,235,237,238,239,240,241,242,243,245,246,247,248,251,252,253,254,256,257,258,259,260,261,262,264,265,267,268,269,270,271,272,273,274,275,276,278,279,280,281,282,283,284,285,286,287,289,301,302,303,304,305,307,308,309,310,312,313,314,315,316,317,318,319,320,321,323,324,325,326,327,328,329,330,331,332,334,335,336,337,338,339,340,341,342,345,346,347,348,349,350,351,352,353,356,357,358,359,360,361,362,363,364,369,380,381,383,384,385,386,389,401,402,403,404,405,406,407,408,409,410,412,413,414,415,416,417,418,419,420,421,423,424,425,426,427,428,429,430,431,432,434,435,436,437,438,439,440,441,442,443,445,446,447,448,449,450,451,452,453,454,456,457,458,459,460,461,462,463,464,465,467,468,469,470,471,472,473,474,475,476,478,479,480,481,482,483,484,485,486,487,489,501,502,503,504,505,507,508,509,510,512,513,515,516,517,518,520,530,531,534,536,537,539,540,541,551,557,559,560,561,562,563,564,565,567,568,570,571,572,573,574,575,576,580,582,583,585,586,601,602,603,605,606,607,608,609,610,612,614,615,616,617,618,619,620,621,623,624,625,626,627,628,629,630,631,632,634,635,636,637,638,640,641,642,643,645,646,648,649,650,651,652,653,654,656,657,658,659,660,661,662,663,664,665,667,668,669,670,671,673,674,675,676,678,679,680,681,682,684,685,686,687,689,701,702,703,704,706,707,708,712,713,714,715,716,717,718,719,720,721,723,724,725,726,727,728,729,730,731,732,734,735,736,737,738,739,740,741,743,745,746,747,748,749,750,751,752,754,756,757,758,759,760,761,762,763,764,765,767,768,769,770,771,772,773,774,775,776,779,781,783,784,785,786,787,789,801,802,803,804,805,806,808,809,810,812,813,814,815,816,817,818,820,821,823,824,826,827,828,829,830,831,832,834,835,836,837,838,839,840,841,842,843,845,846,847,848,849,850,851,852,853,854,856,857,858,859,860,861,862,863,864,865,868,869,870,871,872,874,875,876,878,901,903,904,906,907,908,909,910,912,913,914,915,916,917,918,919,920,921,923,924,925,926,927,928,929,930,931,932,934,935,936,937,938,939,940,941,943,945,946,947,948,949,951,952,953,954,956,957,958,959,970,971,972,973,974,975,976,978,979,980,981,982,983,984,985,986,987,989]

# Global Variables, lists to track unique identifiers
SSN_list = ['000-00-0000']  # Track SSN values to ensure no duplicates for person, with 000-00-0000 as a guaranteed 'not used'
MRN_list = ['M00000000']
provider_list = []
provider_id_list = [""]
provider_dict = dict()

def generate_race():

    ''' Randomly choses a person's race/heritage, based on US population 2010 census data. '''
    
    person_race = random.choices(DF_race_distribution["identification"], weights = DF_race_distribution["weight"])[0]

    # Add ethnicity if race is in this group
    if person_race in ['White','Mixed','Unreported']:

        person_ethnicity = random.choices(DF_ethnicity_distribution['identification'], weights = DF_ethnicity_distribution['weight'])[0]

    else:

        person_ethnicity = "Unreported"

    return (str(person_race), str(person_ethnicity))

def generate_sex():

    ''' Randomly generates a person sex, with only male/female options. '''

    return random.choice(PERSON_SEXES).strip().capitalize()

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

    # SSN used to have rules for assignment based on geographic codes, but now they're just randomly assigned
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

    # Pick a random letter, then add numbers to it
    my_MRN = random.choice(['M','E','D','I','C','A','L'])
    for x in range(8):
        my_MRN += str(random.randint(0,9))

    return my_MRN

def generate_phone_number():

    ''' Randomly generates a phone number. '''

    # generate area code using restrictions above
    area_code = random.choice(USABLE_AREA_CODES)

    # generate middle 3 digits
    prefix_code = 0
    while prefix_code in [0,211,311,411,511,611,711,811,911]:
        prefix_code = random.randint(200,999)

    # assemble and last 4 digits
    phone_number = str(area_code) + '-' + str(prefix_code) + '-' + str(random.randint(0,9999)).zfill(4)

    return phone_number

def generate_name_suffix():

    ''' Randomly generates a name suffix. Generational titles only.  Non-professional. '''

    return str(random.choices(LIST_OF_SUFFIXES, weights = [100,100,100,50,10])[0])

def generate_email(person_name, person_surname):

    ''' Randomly generates an email address. '''

    # random flip-flop of names in email for variety
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

def check_provider_list_exists():

    ''' Simple check to see if the provider list already exists.  If so, skip the person list generation. '''

    if not os.path.isfile(PROVIDER_LIST_FILE_NAME):
        print("Provider list not found -- Will be generated.")
        return False
    else:
        print("Provider list found.")

        # open the target file and count the number of lines
        with open(PROVIDER_LIST_FILE_NAME, "r", encoding = 'UTF-8') as file:
            line_count = 0
            for line in file:
                if line != "\n":
                    line_count += 1
 
        # Check if threshold is met
        if line_count < NUMBER_OF_PROVIDERS_TO_GENERATE:
            print("WARNING: Less than {} providers found in list.  ({} entries found.)  Re-creating list.").format(NUMBER_OF_PROVIDERS_TO_GENERATE, line_count)
            return False

        return True

def check_person_list_exists():

    ''' Simple check to see if the person list already exists.  If so, skip the person list generation. '''

    if not os.path.isfile(PERSON_LIST_FILE_NAME):
        print("Person list not found -- Will be generated.")
        return False
    else:
        print("Person list found.")

        # open the target file and count the number of lines
        with open(PERSON_LIST_FILE_NAME, "r", encoding = 'UTF-8') as file:
            line_count = 0
            for line in file:
                if line != "\n":
                    line_count += 1
 
        # Check if threshold is met
        if line_count < NUMBER_OF_PERSONS_TO_GENERATE:
            print("WARNING: Less than {} providers found in list.  ({} entries found.)  Re-creating list.").format(NUMBER_OF_PERSONS_TO_GENERATE, line_count)
            return False

        return True
   
def generate_provider_specialty():

    ''' Returns a weighted random choice for practitioner specialty. '''
 
    return random.choices(DF_provider_specialty['specialty'], weights = DF_provider_specialty['count'])[0]

def generate_provider_type():

    ''' Returns a weighted random choice for practitioner type. '''

    return str(random.choices(DF_provider_type['type'], weights = DF_provider_type['count'])[0])

def generate_provider_ID():

    ''' Generates a provider ID number according to allowable values from Medicare. '''

    provider_id = ""

    # check that provider id is unique
    while provider_id in provider_id_list:

        # create a provider ID based on rules from medicare website
        provider_id = (str(random.choice(PROVIDER_ID_PREFIX_CODES)) + str(random.choice(PROVIDER_ID_THIRD_DIGIT_CODES)) + str(random.randint(0, 9999)).zfill(4))

    return provider_id

def gather_provider_names_list():

    ''' Collects a list of age appropriate names from the persons_list output file. '''

    # Load person list into memory
    with open(PERSON_LIST_FILE_NAME, 'r') as input_file:

        # Ignore the first line (headers)
        read_string = input_file.readline()

        for x in range(NUMBER_OF_PROVIDERS_TO_GENERATE):

            # Then read the first entry
            read_string = input_file.readline().split(sep=',')

            # Make sure the person read is over the age of 25
            while int(read_string[4]) < MIN_PROVIDER_AGE:
                read_string = input_file.readline().split(sep=',')

            # Add the provider to the list of names
            provider_list.append((read_string[0] + " " + read_string[2]))

    return

def update_provider_name(provider_type, provider_name):

    ''' Updates the provider's name to reflect the new type of provider (adds degree). '''

    # nurse practitioners degree
    if provider_type == 'Nurse practitioners':
        provider_name += ' RN'

    # physicians assistant degree
    elif provider_type == 'Physician assistants':
        provider_name += ' PA-C'

    else: # Provider_type == "Physcians"

        # approximately 9:1 DO:MD ratio
        if random.random() > 0.9:
            provider_name += ' DO'
        else:
            provider_name += ' MD'

    return provider_name

def create_the_person_list():

    ''' Major function to ultimately create the persons list. '''

    if not check_person_list_exists():
        
        # Prep the main output file
        header = 'name,middle_name,surname,name_suffix,age,race,ethnicity,sex,DOB,SSN,MRN,street,city,county,state,zip,country,cell_phone,home_phone,work_phone,email'.upper() + "\n"
        with open(PERSON_LIST_FILE_NAME, 'w', encoding='UTF-8') as file:
            file.write(header)

        # Loop to create specificed number of records
        for x in tqdm(range(NUMBER_OF_PERSONS_TO_GENERATE)):

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
                
            with open((PERSON_LIST_FILE_NAME), 'a', encoding='UTF-8') as file:
                file.write(new_record)

        print('{} person records generated and written to {}'.format(NUMBER_OF_PERSONS_TO_GENERATE, PERSON_LIST_FILE_NAME))

    return

def create_the_provider_list():

    ''' Major function to ultimatley create the providers list. '''

    if not check_provider_list_exists():
        
        # Read in a sample of the persons list to providers
        gather_provider_names_list()

        with open(PROVIDER_LIST_FILE_NAME, 'w', encoding='UTF-8') as output_file:

            # Prep the provider list output file
            header = 'provider_name,provider_specialty,provider_address,provider_phone'.upper() + "\n"
            output_file.write(header)

            # Loop to create specificed number of records
            for x in provider_list:

                provider_name = str(x)
                provider_specialty = generate_provider_specialty()
                provider_type = generate_provider_type()
                provider_name = update_provider_name(provider_type, provider_name)
                provider_id = generate_provider_ID()
                provider_zip_code = generate_zip_code()
                provider_street, provider_city, provider_county, provider_state, provider_country = generate_address(provider_zip_code, False)
                provider_address = '\"{}, {}, {}  {}\"'.format(provider_street, provider_city, provider_state, provider_zip_code)
                provider_phone = generate_phone_number()

                output_file.write((provider_name + ',' + provider_id + ',' + provider_specialty + ',' + provider_address + ',' + provider_phone + '\n'))
                
        print('{} provider records generated and written to {}'.format(NUMBER_OF_PROVIDERS_TO_GENERATE, PROVIDER_LIST_FILE_NAME))

    return

def main():

    create_the_person_list()
    create_the_provider_list()

if __name__ == "__main__":
    main()