# Module Imports
print("Importing modules.")

import random
import datetime
from re import X
import pandas as pd
import math
from tqdm import tqdm
import os
import pickle
import numpy as np

# File names and global variables---------------------

# Output files
PATIENT_LIST_FILE_NAME = 'OUTPUT/patient_pool.pkl'
PROVIDER_LIST_FILE_NAME = 'OUTPUT/provider_pool.pkl'
HOSPITAL_SYSTEM_FILE_NAME = 'OUTPUT/hospitals.pkl'
LABORATORY_LIST_FILE_NAME = 'OUTPUT/labs.pkl'
RECORDS_FILE_NAME = 'OUTPUT/records.csv'

if os.path.exists(PATIENT_LIST_FILE_NAME) and os.path.exists(PROVIDER_LIST_FILE_NAME) and os.path.exists(HOSPITAL_SYSTEM_FILE_NAME) and os.path.exists(LABORATORY_LIST_FILE_NAME):
    print("Patient, provider, and hospital system files found.")
else:
    print("Patient, provider, and hospital system files not found.  These will be generated.")

    # Conditional Reference Files -- not loaded if possible, due to their size
    print("Reading reference files.")

    RACE_DISTRIBUTION_FILE = 'REFERENCE/ancestry/race_distribution.csv'
    DF_RACE_DISTRIBUTION = pd.read_csv(RACE_DISTRIBUTION_FILE)

    ETHNICITY_DISTRIBUTION_FILE = 'REFERENCE/ancestry/ethnicity_distribution.csv'
    DF_ETHNICITY_DISTRIBUTION = pd.read_csv(ETHNICITY_DISTRIBUTION_FILE)

    AGE_CATEGORY_DISTRIBUTION_FILE = 'REFERENCE/age/age_category_distribution.csv'
    DF_AGE_CATEGORY_DISTRIBUTION = pd.read_csv(AGE_CATEGORY_DISTRIBUTION_FILE)

    ZIP_CODE_DISTRIBUTION_FILE = 'REFERENCE/location/population_by_zip_code.csv'
    USA_ADDRESSES_FILE = 'REFERENCE/location/usa_addresses.csv'
    DF_ZIP_CODE_DISTRIBUTION = pd.read_csv(ZIP_CODE_DISTRIBUTION_FILE)
    DF_USA_ADDRESSES = pd.read_csv(USA_ADDRESSES_FILE)

    #PERSON_NAMES_FILE = 'REFERENCE/name/person_names.csv'
    #DF_PERSON_NAMES = pd.read_csv(PERSON_NAMES_FILE)
    MALE_NAMES_FILE = 'REFERENCE/name/male_names.csv'
    DF_MALE_NAMES = pd.read_csv(MALE_NAMES_FILE)
    FEMALE_NAMES_FILE = 'REFERENCE/name/female_names.csv'
    DF_FEMALE_NAMES = pd.read_csv(FEMALE_NAMES_FILE)

    SURNAMES_ASIAN_FILE = 'REFERENCE/surname/surnames_asian.csv'
    SURNAMES_BLACK_FILE = 'REFERENCE/surname/surnames_black.csv'
    SURNAMES_GENERIC_FILE = 'REFERENCE/surname/surnames_generic.csv'
    SURNAMES_HISPANIC_FILE = 'REFERENCE/surname/surnames_hispanic.csv'
    SURNAMES_NATIVE_FILE = 'REFERENCE/surname/surnames_native.csv'
    SURNAMES_WHITE_FILE = 'REFERENCE/surname/surnames_white.csv'
    DF_SURNAME_ASIAN = pd.read_csv(SURNAMES_ASIAN_FILE)
    DF_SURNAME_BLACK = pd.read_csv(SURNAMES_BLACK_FILE)
    DF_SURNAME_GENERIC = pd.read_csv(SURNAMES_GENERIC_FILE)
    DF_SURNAME_HISPANIC = pd.read_csv(SURNAMES_HISPANIC_FILE)
    DF_SURNAME_NATIVE = pd.read_csv(SURNAMES_NATIVE_FILE)
    DF_SURNAME_WHITE = pd.read_csv(SURNAMES_WHITE_FILE)

    EMAIL_DOMAINS_FILE = 'REFERENCE/email/email_domains.csv'
    DF_EMAIL_DOMAINS = pd.read_csv(EMAIL_DOMAINS_FILE)

    PROVIDER_TYPE_FILE = "REFERENCE/provider/provider_type.csv"
    PROVIDER_SPECIALTY_FILE = "REFERENCE/provider/provider_specialty.csv"
    DF_PROVIDER_TYPE = pd.read_csv(PROVIDER_TYPE_FILE)
    DF_PROVIDER_SPECIALTY = pd.read_csv(PROVIDER_SPECIALTY_FILE)

# Unconditional Refrence files --------------------------------------------
DX_CODES_FILE = 'REFERENCE/encounter/ICD10_dictionary.tsv'
DF_DX_CODES = pd.read_csv(DX_CODES_FILE, sep='\t')

TEST_MENU_FILE = 'REFERENCE/tests/test_menu.csv'
DF_TEST_MENU = pd.read_csv(TEST_MENU_FILE)
DF_TEST_MENU = DF_TEST_MENU.set_index('TEST_CODE')
TEST_MENU_DICTIONARY = DF_TEST_MENU.to_dict('index')

# Storing this data as both a dictionary, and pulling in empirical weights (eventually)
DX_CODES_DICT = dict()
with open(DX_CODES_FILE,'r') as file_input:
    for line in file_input.readlines():
        line = line.split(sep='\t')
        DX_CODES_DICT[line[0]] = line[2][:-1]

# Global Variables
print("Declaring variables.")

# Main Variables to Tweak
NUMBER_OF_BEDS = 1000
NUMBER_OF_TEST_RESULTS = 1000000
NUMBER_OF_PATIENTS = 10000
NUMBER_OF_PROVIDERS = 200
BED_PERCENTAGE_OCCUPANCY_TARGET = 0.85
ENCOUNTER_TYPES_ALLOWED_LIST = ['Inpatient', 'Outpatient']

# Global Variables, probably are close enough
PERCENT_CHANCE_FOR_ADDON_TEST = 0.05

CELL_PHONE_AGES = [10, 3]
CELL_PHONE_CHANCE = 0.97
EMAIL_AGES = [8, 3]  # x0, gamma values, used in 'cummulative_distribution()'
HOME_PHONE_AGES = [15, 4]
HOME_PHONE_CHANCE = 0.40
WORK_PHONE_AGES = [20, 5]
WORK_PHONE_CHANCE = 0.75

CHANCE_FOR_NAME_SUFFIX = 0.01
GENDERS_WITH_NAME_SUFFIX = ["Male"]
MD_TO_DO_RATIO = 0.9
NAME_SUFFIX_AGE_CUTOFF = 20
PERSON_SEXES = ["Male", "Female"]
SUFFIX_LIST = ['Sr.', 'Jr.', 'II', 'III', 'IV']
SUFFIX_WEIGHTS = [100,100,100,50,10]

# Miscellaneous coding lists
HOSPITAL_SIZES = {
    "Huge Hospital":(1000,10), 
    "Large Hospital":(750,7), 
    "Medium Hospital": (300,4), 
    "Small Hospital": (100,3), 
    "Tiny Hospital": (50,2)
    }
PRIMARY_CARE_PROVIDER_SPECIALTIES = [
    "Family Medicine/General Practice", 
    "Geriatric Medicine", 
    "Internal Medicine", 
    "Internal Medicine/Pediatrics", 
    "Pediatrics", 
    "Preventive Medicine"
    ]
PROVIDER_ID_PREFIX_CODES = [
    "01","02","03","00","04","89","05","55","75","92","06","91","07","81","08","09","10","68","69","11",
    "85","12","13","54","14","78","15","16","76","17","70","18","19","71","95","30","31","83","32","96",
    "33","57","34","86","35","36","72","37","90","38","93","39","73","40","84","41","42","87","43","44",
    "88","45","67","74","97","46","47","48","20","21","80","22","82","23","24","77","25","26","79","27",
    "28","29","49","50","94","51","58","52","53","56","59","64","65","66","99"
    ]
PROVIDER_ID_THIRD_DIGIT_CODES = ["0","1","2","3","4","5","6","7","8","9","M","S","T","U","W","Y","Z"]
USABLE_AREA_CODES = [
    201,202,203,205,206,207,208,209,210,212,213,214,215,216,217,218,219,220,221,223,224,225,227,228,229,230,
    231,232,234,235,237,238,239,240,241,242,243,245,246,247,248,251,252,253,254,256,257,258,259,260,261,262,
    264,265,267,268,269,270,271,272,273,274,275,276,278,279,280,281,282,283,284,285,286,287,289,301,302,303,
    304,305,307,308,309,310,312,313,314,315,316,317,318,319,320,321,323,324,325,326,327,328,329,330,331,332,
    334,335,336,337,338,339,340,341,342,345,346,347,348,349,350,351,352,353,356,357,358,359,360,361,362,363,
    364,369,380,381,383,384,385,386,389,401,402,403,404,405,406,407,408,409,410,412,413,414,415,416,417,418,
    419,420,421,423,424,425,426,427,428,429,430,431,432,434,435,436,437,438,439,440,441,442,443,445,446,447,
    448,449,450,451,452,453,454,456,457,458,459,460,461,462,463,464,465,467,468,469,470,471,472,473,474,475,
    476,478,479,480,481,482,483,484,485,486,487,489,501,502,503,504,505,507,508,509,510,512,513,515,516,517,
    518,520,530,531,534,536,537,539,540,541,551,557,559,560,561,562,563,564,565,567,568,570,571,572,573,574,
    575,576,580,582,583,585,586,601,602,603,605,606,607,608,609,610,612,614,615,616,617,618,619,620,621,623,
    624,625,626,627,628,629,630,631,632,634,635,636,637,638,640,641,642,643,645,646,648,649,650,651,652,653,
    654,656,657,658,659,660,661,662,663,664,665,667,668,669,670,671,673,674,675,676,678,679,680,681,682,684,
    685,686,687,689,701,702,703,704,706,707,708,712,713,714,715,716,717,718,719,720,721,723,724,725,726,727,
    728,729,730,731,732,734,735,736,737,738,739,740,741,743,745,746,747,748,749,750,751,752,754,756,757,758,
    759,760,761,762,763,764,765,767,768,769,770,771,772,773,774,775,776,779,781,783,784,785,786,787,789,801,
    802,803,804,805,806,808,809,810,812,813,814,815,816,817,818,820,821,823,824,826,827,828,829,830,831,832,
    834,835,836,837,838,839,840,841,842,843,845,846,847,848,849,850,851,852,853,854,856,857,858,859,860,861,
    862,863,864,865,868,869,870,871,872,874,875,876,878,901,903,904,906,907,908,909,910,912,913,914,915,916,
    917,918,919,920,921,923,924,925,926,927,928,929,930,931,932,934,935,936,937,938,939,940,941,943,945,946,
    947,948,949,951,952,953,954,956,957,958,959,970,971,972,973,974,975,976,978,979,980,981,982,983,984,985,
    986,987,989
    ]

# "Stamper" dictionary declaraction -----------------------

# stamper_reportable_keys contains the header information and the keys which will have their information stamped when the stamper function is called.
# stamper is a dictionary to hold the values of the various data components present in each record stamp.  

stamper_reportable_keys = [
    'patient_name',
    'patient_age',
    'patient_sex',
    'patient_race',
    'patient_ethnicity',

    'patient_ssn',
    'patient_mrn',
    'patient_dob',
    
    'patient_address',
    'patient_city',
    'patient_state',
    'patient_zip_code',
    
    'patient_cell_phone',
    'patient_home_phone',
    'patient_work_phone',
    
    'patient_email',

    # primary_care_provider_info_block_header

    'primary_care_provider_name',
    'primary_care_provider_id',

    'primary_care_provider_specialty',
    'primary_care_provider_type',

    'primary_care_provider_address',
    'primary_care_provider_city',
    'primary_care_provider_state',
    'primary_care_provider_zip_code',

    'primary_care_provider_phone',
    
    #ordering_physician_info_block_header

    'ordering_provider_name',
    'ordering_provider_id',
    
    'ordering_provider_specialty',
    'ordering_provider_type',
    
    'ordering_provider_address',
    'ordering_provider_city',
    'ordering_provider_state',
    'ordering_provider_zip_code',
    
    'ordering_provider_phone',
    
    # bed_info_header

    'hospital_name',
    'hospital_pfi_number',
    'hospital_bed_id',

    'hospital_address',
    'hospital_city',
    'hospital_state',
    'hospital_zip_code',
    
    'hospital_phone',

    # laboratory_info_block_header

    'laboratory_name',
    'laboratory_pfi_number',
    'laboratory_clia_number',

    'laboratory_address',
    'laboratory_city',
    'laboratory_state',
    'laboratory_zip_code',
    
    'laboratory_phone',

    # encounter_info_header

    'encounter_type',
    'encounter_id',
    'encounter_admission_date',
    'encounter_discharge_date',

    # order_info_header 

    'order_number',
    'order_status',

    'order_placed_timestamp',
    'result_reported_timestamp',

    # sample_info_header

    'sample_id',

    'sample_drawn_timestamp',
    'sample_delivered_timestamp',
    'sample_accessioned_timestamp',
    
    # test_info_header

    'test_code',
    'test_name',
    #'test_description',

    'test_resulted_timestamp',
    'result_verified_timestamp',

    # 'test_result_alpha',
    'test_result_numeric',
    'test_reported_units',

    'test_result_threshold_low',
    'test_result_threshold_high',
    'test_result_critical_flag'
]

stamper = {
    # patient_info_block_header
    'patient_name':'',
    'patient_age':'',
    'patient_sex':'',
    'patient_race':'',
    'patient_ethnicity':'',

    'patient_ssn':'',
    'patient_mrn':'',
    'patient_dob':'',
    
    'patient_address':'',
    'patient_city':'',
    'patient_state':'',
    'patient_zip_code':'',
    
    'patient_cell_phone':'',
    'patient_home_phone':'',
    'patient_work_phone':'',
    
    'patient_email':'',

    # primary_care_provider_info_block_header
    'primary_care_provider_name':'',
    'primary_care_provider_id':'',

    'primary_care_provider_specialty':'',
    'primary_care_provider_type':'',

    'primary_care_provider_address':'',
    'primary_care_provider_city':'',
    'primary_care_provider_state':'',
    'primary_care_provider_zip_code':'',

    'primary_care_provider_phone':'',
    
    #ordering_physician_info_block_header
    'ordering_provider_name':'',
    'ordering_provider_id':'',
    
    'ordering_provider_specialty':'',
    'ordering_provider_type':'',
    
    'ordering_provider_address':'',
    'ordering_provider_city':'',
    'ordering_provider_state':'',
    'ordering_provider_zip_code':'',
    
    'ordering_provider_phone':'',
    
    # bed_info_header
    'hospital_name':'',
    'hospital_pfi_number':'',
    'hospital_bed_id':'',

    'hospital_address':'',
    'hospital_city':'',
    'hospital_state':'',
    'hospital_zip_code':'',
    
    'hospital_phone':'',

    # laboratory_info_block_header
    'laboratory_name':'',
    'laboratory_pfi_number':'',
    'laboratory_clia_number':'',

    'laboratory_address':'',
    'laboratory_city':'',
    'laboratory_state':'',
    'laboratory_zip_code':'',
    
    'laboratory_phone':'',

    # encounter_info_header
    'encounter_type':'',
    'encounter_id':'',
    'encounter_admission_date':'',
    'encounter_discharge_date':'',

    # order_info_header 
    'order_number':'',
    'order_status':'',

    'order_placed_timestamp':'',
    'result_reported_timestamp':'',

    # sample_info_header
    'sample_id':'',

    'sample_drawn_timestamp':'',
    'sample_delivered_timestamp':'',
    'sample_accessioned_timestamp':'',
    
    # test_info_header
    'test_code':'',
    'test_name':'',
    'test_description':[False,"TEST_DESCRIPTION",""],

    'test_resulted_timestamp':'',
    'result_verified_timestamp':'',

    'test_result_alpha':'',
    'test_result_numeric':'',
    'test_reported_units':'',

    'test_result_threshold_critical_low':'',
    'test_result_threshold_low':'',
    'test_result_threshold_high':'',
    'test_result_threshold_critical_high':'',
    'test_result_critical_flag':'',
}

# Lists of Unique Numbers ---------------------------------
print("Resetting tracking lists of unique-values.")

MRN_list = ['M00000000','E00000000','D00000000','I00000000','C00000000','A00000000','L00000000']
phone_number_list = ['000-000-0000']
email_list = [""]
provider_id_list = [""]
hospital_name_list = [""]
SSN_list = ['000-00-0000'] 

# Incrementables ------------------------------------------
simulation_day_number = 0
sample_id = "S" + str(datetime.date.today())[2:4] + "P" + str(random.randint(1000,1000000)).zfill(7)
order_id = "R" + str(datetime.date.today())[2:4] + "D" + str(random.randint(1000,1000000)).zfill(7)
encounter_id = "N" + str(datetime.date.today())[2:4] + "C" + str(random.randint(1000,1000000)).zfill(7)

# Lists of class items -------------------------------------
print("Initializing data pools.")

provider_pool = []
patient_pool = []
hospital_list = []
laboratory_list = []

available_bed_pool = []
occupied_bed_count = 0  # beds are stored in encounters.  When occupied, just use a counter for math.  When the encounter ends, copy the bed back to the available list

encounter_list = []

write_buffer = []

# CLASS DEFINITIONS ------------------------------------------
print("Defining classes.")

class Provider:

    name = ""
    id_number = ""
    type = ""
    primary_care = False
    ordering = True
    specialty = ""

    age = 0
    sex = ""
    YOB = ""

    address = ""
    city = ""
    county = ""
    state = ""
    country = ""
    zip_code = ""

    phone = ""

    def __init__(self) -> None:

        self.age = random.randint(30, 75)
        self.sex = random.choice(PERSON_SEXES).strip().capitalize()
        self.YOB = str(datetime.date.today() - datetime.timedelta(days = 365 * float(self.age)) - datetime.timedelta(days=random.random() * 365))[0:4]
        
        self.specialty = str(random.choices(DF_PROVIDER_SPECIALTY['specialty'], weights = DF_PROVIDER_SPECIALTY['count'])[0])
        if self.specialty in PRIMARY_CARE_PROVIDER_SPECIALTIES:
            self.primary_care = True
        self.type = str(random.choices(DF_PROVIDER_TYPE['type'], weights = DF_PROVIDER_TYPE['count'])[0])
        if str(DF_PROVIDER_SPECIALTY[(DF_PROVIDER_SPECIALTY['specialty'] == str(self.specialty))]['ordering']) == 'y':
            self.ordering = True
        self.generate_provider_id()

        self.name = generate_name(self.sex, self.YOB)
        self.name += " " + generate_surname("Unreported", "Unreported", "Male")
        self.update_provider_name()
        
        self.zip_code = generate_zip_code()
        self.address, self.city, self.county, self.state, self.country = generate_address(str(self.zip_code), False)

        self.phone = generate_phone_number()

    def generate_provider_id(self):

        ''' Generates a provider ID number according to allowable values from Medicare. '''

        # check that provider id is unique
        while self.id_number in provider_id_list:

            # create a provider ID based on rules from medicare website
            self.id_number = (str(random.choice(PROVIDER_ID_PREFIX_CODES)) + str(random.choice(PROVIDER_ID_THIRD_DIGIT_CODES)) + str(random.randint(0, 9999)).zfill(4))

    def update_provider_name(self):

        ''' Updates the provider's name to reflect the new type. '''

        # nurse practitioners degree
        if self.type == 'Nurse Practitioner':
            self.name += ' RN'

        # physicians assistant degree
        elif self.type == 'Physician Assistant':
            self.name += ' PA-C'

        else: # self.type == "Physcian"

            # approximately 9:1 DO:MD ratio
            if random.random() > MD_TO_DO_RATIO:
                self.name += ' DO'
            else:
                self.name += ' MD'

    def fill_stamper_ordering(self):

        global stamper

        stamper['ordering_provider_name'] = str(self.name)
        stamper['ordering_provider_id'] = str(self.id_number)

        stamper['ordering_provider_specialty'] = str(self.specialty)
        stamper['ordering_provider_type'] = str(self.type)

        stamper['ordering_provider_address'] = str(self.address)
        stamper['ordering_provider_city'] = str(self.city)
        stamper['ordering_provider_state'] = str(self.state)
        stamper['ordering_provider_zip_code'] = str(self.zip_code)

        stamper['ordering_provider_phone'] = str(self.phone)

    def fill_stamper_primary_care(self):

        global stamper

        stamper['primary_care_provider_name'] = str(self.name)
        stamper['primary_care_provider_id'] = str(self.id_number)

        stamper['primary_care_provider_specialty'] = str(self.specialty)
        stamper['primary_care_provider_type'] = str(self.type)

        stamper['primary_care_provider_address'] = str(self.address)
        stamper['primary_care_provider_city'] = str(self.city)
        stamper['primary_care_provider_state'] = str(self.state)
        stamper['primary_care_provider_zip_code'] = str(self.zip_code)

        stamper['primary_care_provider_phone'] = str(self.phone)
       
class Patient:

    SSN = ""
    MRN = ""
    DOB = ""

    age = 0
    sex = ""
    race = ""
    ethnicity = ""

    name = ""
    middle_name = ""
    surname = ""
    suffix = ""
    full_name = ""

    address = ""
    city = ""
    county = ""
    state = ""
    country = ""
    zip_code = ""

    cell_phone = ""
    home_phone = ""
    work_phone = ""

    email = ""

    primary_care_provider = ""

    def __init__(self) -> None:
        self.generate_MRN()
        self.generate_SSN()

        self.generate_race()
        self.sex = random.choice(PERSON_SEXES).strip().capitalize()
        self.generate_age()
        self.DOB = str(datetime.date.today() - datetime.timedelta(days = 365 * float(self.age)) - datetime.timedelta(days=random.random() * 365))

        self.surname = generate_surname(self.race, self.ethnicity, self.sex)
        self.name = generate_name(self.sex, (str(self.DOB)[0:4]))
        self.middle_name = self.name
        while self.middle_name == self.name:
            self.middle_name = generate_name(self.sex, (str(self.DOB)[0:4]))
        if self.sex in GENDERS_WITH_NAME_SUFFIX and self.age > NAME_SUFFIX_AGE_CUTOFF and random.random() < CHANCE_FOR_NAME_SUFFIX:
            self.suffix = str(random.choices(SUFFIX_LIST, weights = SUFFIX_WEIGHTS)[0])

        self.zip_code = generate_zip_code()
        self.address, self.city, self.county, self.state, self.country = generate_address(self.zip_code, True)

        if random.random() < cumulative_distribution(self.age, EMAIL_AGES[0], EMAIL_AGES[1]):
            self.generate_email()
        if random.random() < (CELL_PHONE_CHANCE * cumulative_distribution(self.age, CELL_PHONE_AGES[0], CELL_PHONE_AGES[1])):
            self.cell_phone = generate_phone_number()
        if random.random() < (HOME_PHONE_CHANCE * cumulative_distribution(self.age, HOME_PHONE_AGES[0], HOME_PHONE_AGES[1])):
            self.home_phone = generate_phone_number()
        if random.random() < (WORK_PHONE_CHANCE * cumulative_distribution(self.age, WORK_PHONE_AGES[0], WORK_PHONE_AGES[1])):
            self.work_phone = generate_phone_number()

        self.assign_primary_care()

        self.full_name = self.name + " " + (self.middle_name + " " + self.surname + " " + self.suffix).strip()

    def generate_MRN(self):

        ''' Randomly generates a unique MRN. Uses MRN_list to ensure MRNs are tracked for duplicates. '''

        while self.MRN in MRN_list:
            self.MRN = random.choice(['M','E','D','I','C','A','L'])
            for x in range(8):
                self.MRN += str(random.randint(0,9))

        MRN_list.append(self.MRN)

    def generate_SSN(self):

        ''' Generates a random SSN, ensures that it is not all 0's, records the new SSN into a list (to ensure a unique identifier for the person), and returns the value. '''

        while self.SSN in SSN_list:
            AAA = str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9))
            GG = str(random.randint(0,9)) + str(random.randint(0,9))
            SSSS = str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9))
            self.SSN = AAA + "-" + GG + "-" + SSSS

        SSN_list.append(self.SSN)

    def generate_age(self):

        ''' Generates a random person age, according to population distributions from 2010 US census data. '''

        if self.sex == "Male":
            category_weights = DF_AGE_CATEGORY_DISTRIBUTION["male_count"]
        else:
            category_weights = DF_AGE_CATEGORY_DISTRIBUTION["female_count"]

        person_age_category = int(random.choices(DF_AGE_CATEGORY_DISTRIBUTION["age_floor"], weights = category_weights)[0])

        self.age = person_age_category + random.choice(range(5))

    def generate_race(self):

        ''' Randomly choses a person's race/heritage, based on US population 2010 census data. '''
        
        self.race = random.choices(DF_RACE_DISTRIBUTION["identification"], weights = DF_RACE_DISTRIBUTION["weight"])[0]

        if self.race in ['White','Mixed','Unreported']:
            self.ethnicity = random.choices(DF_ETHNICITY_DISTRIBUTION['identification'], weights = DF_ETHNICITY_DISTRIBUTION['weight'])[0]
        else:
            self.ethnicity = "Unreported"

    def generate_email(self):

        ''' Randomly generates an email address. '''

        while self.email in email_list:

            temp_name = self.name
            temp_surname = self.surname

            # random flip-flop
            if random.random() < 0.5:
                store_me = temp_name
                temp_name = temp_surname
                temp_surname = store_me

            email = random.choice([temp_name, (temp_name + "_"), (temp_name + '.'), ""])
            email += temp_surname + str(random.randint(1,999)) + '@'
            email += random.choices(DF_EMAIL_DOMAINS['domain'], weights = DF_EMAIL_DOMAINS['count'])[0].strip()

            self.email = email

    def assign_primary_care(self):

        ''' Picks a random primary care provider and examines the characteristics for a proper fit before assigning. '''

        while self.primary_care_provider == "":
            provider = random.choice(provider_pool)

            if provider.primary_care:

                if provider.specialty == "Geriatrics":
                    if self.age > 60:
                        self.primary_care_provider = provider

                elif provider.specialty == "Pediatrics":
                    if self.age < 18:
                        self.primary_care_provider = provider

                else:
                    self.primary_care_provider = provider

    def fill_stamper(self):

        global stamper

        stamper['patient_name'] = str(self.full_name)
        stamper['patient_age'] = str(self.age)
        stamper['patient_sex'] = str(self.sex)
        stamper['patient_race'] = str(self.race)
        stamper['patient_ethnicity'] = str(self.ethnicity)

        stamper['patient_ssn'] = str(self.SSN)
        stamper['patient_mrn'] = str(self.MRN)
        stamper['patient_dob'] = str(self.DOB)
        
        stamper['patient_address'] = str(self.address)
        stamper['patient_city'] = str(self.city)
        stamper['patient_state'] = str(self.state)
        stamper['patient_zip_code'] = str(self.zip_code)
        
        stamper['patient_cell_phone'] = str(self.cell_phone)
        stamper['patient_home_phone'] = str(self.home_phone)
        stamper['patient_work_phone'] = str(self.work_phone)
        
        stamper['patient_email'] = str(self.email)

class Hospital:

    name = ""
    type = ""
    bed_count = 0

    laboratory_name = ""
    laboratory = ""

    address = ""
    laboratory_address = ""
    city = ""
    county = ""
    state = ""
    country = ""
    zip_code = ""

    phone = ""

    pfi_number = ""

    beds_per_floor = 0
    number_of_floors = 0
    bed_id_list = []

    def __init__(self) -> None:
        
        global laboratory_list

        # Number_of_beds here is determinitive (prescriptive)
        self.hospital_type = str(random.choice(list(HOSPITAL_SIZES.keys())))
        self.bed_count = int(random.normalvariate(1,0.1) * HOSPITAL_SIZES[self.hospital_type][0])
        self.number_of_floors = HOSPITAL_SIZES[self.hospital_type][1] - 1 + random.randint(0,2)
        self.beds_per_floor = int(self.bed_count / self.number_of_floors)

        # generates building location and name information
        self.zip_code = generate_zip_code()
        self.address,self.city,self.county,self.state,self.country = generate_address(self.zip_code, False)
        self.laboratory_address,self.city,self.county,self.state,self.country = generate_address(self.zip_code, False)
        self.generate_hospital_name()
        self.laboratory_name = self.name + " Laboratory"
        self.phone = generate_phone_number()

        # laboratory unique identifiers
        self.pfi_number = str(random.randint(1,999999)).zfill(6)

        # Add the hospital laboratory to the list of available laboratorys
        self.laboratory = Laboratory(str(self.laboratory_name),str(self.pfi_number),str(self.laboratory_address),str(self.city),str(self.state),str(self.zip_code))
        laboratory_list.append(self.laboratory)

    def generate_hospital_name(self):

        while self.name in hospital_name_list:
            type_of_name = random.choice(['Religious','Clinic','Memorial','University'])

            if type_of_name == 'Religious':
                saint = random.choice(["Adalbert","Adamnan","Adelaide","Adrian","Aelfheah","Aelred","Agapetus","Agatha","Agatho","Agnes","Agobard","Agobard","Aidan","Aidan","Alban","Albertus","Alexander","Alexander","Alexis","Alfonso","Aloysius","Ambrose","Anacletus","Anastasius","Anastasius","Andrew","Andrew","Angela","Anne","Anno","Anselm","Ansgar","Ansgar","Anterus","Anthony","Anthony","Anthony","Antoninus","Antonio","Arsenius","Athanasius","Athanasius","Athanasius","Augustine","Augustine","Barbara","Barnabas","Bartholomew","Basil","Bede","Benedict","Benedict","Benedict","Benezet","Benno","Bernadette","Bernard","Bernard","Bernardine","Blaise","Bonaventure","Boniface","Boniface","Boniface","Boris","Brendan","Bridget","Brigit","Bruno","Bruno","Bruno","Cabrini","Caesarius","Cajetan","Calixtus","Camillus","Canute","Catherine","Catherine","Catherine","Catherine","Catherine","Catherine","Cecilia","Celestine","Celestine","Chad","Charles","Christopher","Ciaran","Clare","Claude","Clement","Clement","Clement","Clement","Clotilda","Colette","Colman","Columba","Columban","Constantine","Cornelius","Cosmas","Crispin","Crispinian","Cunibert","Cuthbert","Cuthbert","Cyprian","Cyprian","Cyril","Cyril","Dagobert","Damasus","Damian","Damien","Damien","David","Denis","Deusdedit","Diadochus","Dionysius","Dioscorus","Dioynsius","Dominic","Drexel","Duchesne","Dunstan","Edith","Edmund","Edmund","Edward","Eleutherius","Elizabeth","Elizabeth","Elizabeth","Ephraem","Epiphanius","Erasmus","Eugenius","Eusebius","Eusebius","Eusebius","Eustace","Eustathius","Eustathius","Eustathius","Euthymius","Euthymius","Eutychian","Evaristus","Fabian","Faustus","Felix","Felix","Felix","Felix","Flavian","Frances","Frances","Frances","Francis","Francis","Francis","Francis","Francis","Fridolin","Fulbert","Fulgentius","Fursey","Gaius","Gall","Gelasius","Gennadius","George","Gerard","Gerard","Germanus","Germanus","Germanus","Germanus","Gilbert","Giuseppe","Gotthard","Gregory","Gregory","Gregory","Gregory","Gregory","Gregory","Gregory","Gregory","Gregory","Gregory","Gregory","Gregory","Hegesippus","Heinrich","Helena","Henry","Hermenegild","Hesychius","Hilarion","Hilary","Hilary","Hilary","Hilda","Hildegard","Hippolytus","Hormisdas","Hugh","Hugh","Hugh","Hyginus","Ignatius","Innocent","Innocent","Irenaeus","Isaac","Isaac","Isidore","Ivo","Jacobus","Jadwiga","James","James","James","Jane","Januarius","Jean","Jean-Baptiste","Jean-Baptiste-Marie","Jerome","Joachim","Joan","John","John","John","John","John","John","John","John","John","John","John","John","John","John","John","John","John","John","John","John","John","John","Josemaria","Joseph","Joseph","Joseph","Juan","Judas","Julius","Junipero","Justin","Justus","Justus","Juvenal","Kateri","Katharine","Kenneth","Kentigern","Kevin","Kilian","Kim","Ladislas","Laurentius","Lawrence","Lawrence","Leo","Leo","Leo","Leo","Liberius","Linus","Louis","Louise","Louis-Marie","Lucian","Lucius","Lucy","Ludmila","Luke","Macarius","Madeleine-Sophie","Maksymilian","Malachy","Marcellinus","Marcellus","Margaret","Margaret","Margaret","Mark","Mark","Markos","Martin","Martin","Martín","Mary","Mary","Mary","Mary","Matthew","Matthias","Maurice","Maximus","Maximus","Meletius","Mellitus","Mesrop","Methodius","Methodius","Miltiades","Molokai","Mother","Narekatzi","Nerses","Neumann","Nicephorus","Nicholas","Nicholas","Nicholas","Nicodemus","Nikolay","Nil","Nilus","Nilus","Ninian","Norbert","Nuno","Odo","Oengus","Olaf","Olga","Oliver","Oscar","Osmund","Oswald","Oswald","Pachomius","Padre","Paschal","Paschasius","Patrick","Patrick","Paul","Paul","Paul","Paul","Paulinus","Paulinus","Pelagia","Perpetua","Peter","Peter","Peter","Peter","Peter","Peter","Peter","Peter","Peter","Peter","Philip","Philip","Philip","Philippine","Philotheus","Photius","Pius","Pius","Polycarp","Pontian","Pontian","Quadratus","Radegunda","Raymond","Remigius","Richard","Robert","Romuald","Rose","Rose","Rose","Sabas","Sarapion","Sava","Sebastian","Seraphim","Sergius","Sergius","Severus","Shenute","Silas","Silverius","Simeon","Simon","Simplicius","Siricius","Siricius","Sixtus","Sixtus","Sixtus","Sixtus","Soter","Stanislaus","Stephen","Stephen","Stephen","Stephen","Stephen","Swithin","Sylvester","Symeon","Symmachus","Telesphorus","Teresa","Teresa","Theodore","Theodore","Theodosius","Theophanes","Theophilus","Theophilus","Theophylactus","Thomas","Thomas","Thomas","Thomas","Thomas","Tikhon","Timothy","Titus","Ulrich","Urban","Ursula","Valentine","Vardan","Veronica","Victor","Vincent","Vincent","Vitalian","Vladimir","Wenceslas","Wilfrid","Willibrord","Wulfstan","Xavier","Zacharias","Zephyrinus","Zosimus"])
                self.name = "St. " + saint
                if random.random() > 0.5:
                    self.name += " Mercy"
                self.name += " Hospital"
            elif type_of_name == 'Clinic':
                self.name = self.city + " Clinic"
            elif type_of_name == 'Memorial':
                self.name = generate_surname('Unreported','Unreported','Male') + " Memorial Hospital"
            elif type_of_name == 'University':
                self.name = self.city + " University"
                if random.random() > 0.5:
                    self.name += " Medical Center"
                else:
                    self.name += " Hospital"
            else:
                self.name = self.city + " General Hospital"
        
        hospital_name_list.append(self.name)

    def fill_stamper(self):

        global stamper

        stamper['hospital_name'] = str(self.name)
        stamper['hospital_pfi_number'] = str(self.pfi_number)

        stamper['hospital_address'] = str(self.address)
        stamper['hospital_city'] = str(self.city)
        stamper['hospital_state'] = str(self.state)
        stamper['hospital_zip_code'] = str(self.zip_code)
        
        stamper['hospital_phone'] = str(self.phone)

    def generate_beds(self):

        # bed_count resets and becomes a counter (descriptive)
        self.bed_count = 0
        wings = ["N","E","S","W"]
        wings.pop(random.randint(0,len(wings) - 1)) # Randomly gets rid of one of the wings.  Simulates a hospital 'front'.

        for x in range(self.number_of_floors):
            for y in wings:
                for z in range(int(self.beds_per_floor / 3)):
                    bed_name = str(x + 1) + y.upper() + "-" + str(z + 1)
                    self.bed_id_list.append(bed_name) # maybe add bed specialties to create specialty wards (OB, NICU, etc)
                    self.bed_count += 1

        for bed_id in self.bed_id_list:
            available_bed_pool.append(Bed(hospital=self,laboratory=self.laboratory,bed_id=bed_id))

class Laboratory:

    name = ""
    pfi_number = ""
    address = ""
    city = ""
    state = ""
    zip_code = ""
    phone = ""
    clia_number = ""

    def __init__(self,laboratory_name,pfi_number,address,city,state,zip_code) -> None:

        self.name = laboratory_name
        self.pfi_number = pfi_number
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.phone = generate_phone_number()
        self.clia_number = "X4" + str(random.randint(1,99)).zfill(2) + "D" + str(random.randint(1,9999999)).zfill(7)
    
    def fill_stamper(self):

        global stamper

        stamper['laboratory_name'] = str(self.name)
        stamper['laboratory_pfi_number'] = str(self.pfi_number)
        stamper['laboratory_clia_number'] = str(self.clia_number)

        stamper['laboratory_address'] = str(self.address)
        stamper['laboratory_city'] = str(self.city)
        stamper['laboratory_state'] = str(self.state)
        stamper['laboratory_zip_code'] = str(self.zip_code)
        
        stamper['laboratory_phone'] = str(self.phone)

class Bed:

    hospital = ""
    laboratory = ""
    bed_id = ""

    def __init__(self,hospital,laboratory,bed_id) -> None:

        global laboratory_list

        self.bed_id = bed_id
        self.hospital = hospital
        self.laboratory = laboratory

    def fill_stamper(self):

        global stamper

        stamper['hospital_bed_id'] = str(self.bed_id)

class Encounter:

    encounter_id = ""
    encounter_type = ""

    admission_timestamp = ""
    discharge_timestamp = ""

    patient = ""
    primary_care_provider = ""
    ordering_provider_list = []
    hospital = ""
    bed = ""
    laboratory = ""

    def __init__(self) -> None:

        global encounter_id
        global patient_pool
        global ENCOUNTER_TYPES_ALLOWED_LIST
        global occupied_bed_count
        global hospital_list
        global laboratory_list

        self.encounter_id = encounter_id
        self.encounter_type = random.choice(ENCOUNTER_TYPES_ALLOWED_LIST)

        # pop off a patient
        patient = patient_pool.pop(random.randint(0,len(patient_pool)-1))
        self.patient = patient
        self.primary_care_provider = patient.primary_care_provider


        # Choose dates for the hospitalization and discharge
        if self.encounter_type == "Outpatient":

            # no admission/discharge times on outpatient encounters
            self.admission_timestamp = ""
            self.discharge_timestamp = ""

            # no bed information on outpatient encounters
            self.bed = ""
            self.ordering_provider = [patient.primary_care_provider]

            self.laboratory = random.choice(laboratory_list)

        elif self.encounter_type == 'Inpatient':

            # if is the first day, backdate the admissions a bit
            if simulation_day_number == 0:
                self.admission_timestamp = datetime.date.today() + datetime.timedelta(days = int(random.expovariate(-0.4)))  # on day 0, the patients in the hospital already have been there for some amount of time
            else:
                self.admission_timestamp = datetime.date.today() + datetime.timedelta(days = simulation_day_number)
            self.discharge_timestamp = datetime.date.today() + datetime.timedelta(days = simulation_day_number + (int(random.expovariate(lambd = 0.4))))

            # randomly select an available bed from the pool
            bed = available_bed_pool.pop(random.randint(0,len(available_bed_pool)-1))
            self.bed = bed
            occupied_bed_count += 1
            self.ordering_provider = []

            # Add ordering providers
            self.add_ordering_provider()
            for x in range(int(random.expovariate(1))):
                self.add_ordering_provider()

            # Get the proper hospital and laboratory
            hospital = bed.hospital
            laboratory = bed.laboratory
            self.hospital = hospital
            self.laboratory = laboratory

    def fill_stamper(self):

        global stamper

        stamper['encounter_type'] = str(self.encounter_type)
        stamper['encounter_id'] = str(self.encounter_id)
        stamper['encounter_admission_date'] = str(self.admission_timestamp)
        stamper['encounter_discharge_date'] = str(self.discharge_timestamp)

        patient = self.patient
        patient.fill_stamper()

        primary_care_provider = self.primary_care_provider
        primary_care_provider.fill_stamper_primary_care()

        ordering_provider = random.choice(self.ordering_provider_list)
        ordering_provider.fill_stamper_ordering()

        if self.encounter_type == "Inpatient":

            hospital = self.hospital
            hospital.fill_stamper()

            laboratory = self.laboratory
            laboratory.fill_stamper()

            bed = self.bed
            bed.fill_stamper()

    def add_ordering_provider(self):

        self.ordering_provider_list.append(provider_pool[random.randint(0,len(provider_pool)-1)])

    def deconstruct(self):

        global patient_pool
        global available_bed_pool
        global occupied_bed_count

        patient_pool.append(self.patient)
        if self.encounter_type != "Outpatient":
            available_bed_pool.append(self.bed)
            occupied_bed_count -= 1

class Order:

    order_id = ""
    status = ""

    placed_timestamp = ""
    reported_timestamp = ""

    def __init__(self,order_placed_timestamp,result_reported_timestamp) -> None:
        
        global order_id

        self.order_id = order_id
        self.status = "Completed"
        self.placed_timestamp = order_placed_timestamp
        self.reported_timestamp = order_placed_timestamp

    def fill_stamper(self):

        global stamper

        stamper['order_number'] = str(self.order_id)
        stamper['order_status'] = str(self.status)

        stamper['order_placed_timestamp'] = str(self.placed_timestamp)
        stamper['result_reported_timestamp'] = str(self.reported_timestamp)

class Sample:

    sample_id = ""

    drawn_timestamp = ""
    delivered_timestamp = ""
    accessioned_timestamp = ""

    def __init__(self,sample_drawn_timestamp,sample_delivered_timestamp,sample_accessioned_timestamp) -> None:

        global sample_id

        self.sample_id = sample_id
        self.drawn_timestamp = sample_drawn_timestamp
        self.delivered_timestamp = sample_delivered_timestamp
        self.accessioned_timestamp = sample_accessioned_timestamp

    def fill_stamper(self):

        global stamper

        stamper['sample_id'] = str(self.sample_id)

        stamper['sample_drawn_timestamp'] = str(self.drawn_timestamp)
        stamper['sample_delivered_timestamp'] = str(self.delivered_timestamp)
        stamper['sample_accessioned_timestamp'] = str(self.accessioned_timestamp)

class Test:

    code = ""
    name = ""
    description = ""

    type = ""
    reported_units = ""
    results_distribution = ""

    result_threshold_critical_low = ""
    result_threshold_low = ""
    result_threshold_high = ""
    result_threshold_critical_high = ""
    result_critical_flag = ""

    result_alpha = ""
    result_numeric = ""

    def __init__(self,time_dictionary) -> None:

        self.code = str(random.choice(list(TEST_MENU_DICTIONARY.keys())))
        self.name = str(TEST_MENU_DICTIONARY[self.code]['TEST_NAME'])
        self.description = ""

        self.test_resulted_timestamp = time_dictionary['test_resulted_timestamp']
        self.result_verified_timestamp = time_dictionary['result_verified_timestamp']

        self.type = str(TEST_MENU_DICTIONARY[self.code]['TEST_TYPE'])
        self.reported_units = str(TEST_MENU_DICTIONARY[self.code]['TEST_REPORTED_UNITS'])
        self.results_distribution = str(TEST_MENU_DICTIONARY[self.code]['RESULTS_DISTRIBUTION'])

        self.result_threshold_critical_low = ""
        self.result_threshold_low = float(TEST_MENU_DICTIONARY[self.code]['RESULT_THRESHOLD_LOW'])
        self.result_threshold_high = float(TEST_MENU_DICTIONARY[self.code]['RESULT_THRESHOLD_HIGH'])
        self.result_threshold_critical_high = ""

        if self.results_distribution == 'Normalvariate':
            mu = np.mean([self.result_threshold_high,self.result_threshold_low])
            sigma = (self.result_threshold_high-self.result_threshold_low) / 4
            self.result_numeric = round(random.normalvariate(mu,sigma),1)
        elif self.results_distribution == 'Expovariate':
            lambd = 1
            self.result_numeric = round(random.expovariate(lambd),1)
        else:
            self.result_numeric = ""

        if self.result_numeric <= self.result_threshold_low:
            self.result_critical_flag = "LOW"
        elif self.result_numeric >= self.result_threshold_high:
            self.result_critical_flag = "HIGH"
        else:
            self.result_critical_flag = ""

    def fill_stamper(self):

        global stamper

        stamper['test_code'] = str(self.code)
        stamper['test_name'] = str(self.name)

        stamper['test_resulted_timestamp'] = self.test_resulted_timestamp
        stamper['result_verified_timestamp'] = self.result_verified_timestamp

        stamper['test_result_numeric'] = self.result_numeric
        stamper['test_result_alpha'] = str(self.result_alpha)
        stamper['test_reported_units'] = str(self.reported_units)

        stamper['test_result_threshold_critical_low'] = str(self.result_threshold_critical_low)
        stamper['test_result_threshold_low'] = str(self.result_threshold_low)
        stamper['test_result_threshold_high'] = str(self.result_threshold_high)
        stamper['test_result_threshold_critical_high'] = str(self.result_threshold_critical_high)
        stamper['test_result_critical_flag'] = str(self.result_critical_flag)

# FUNCTION DEFINITIONS ------------------------------------------
print("Defining functions.")

# Information Generation Functions 

def generate_surname(person_race, person_ethnicity, person_sex):

    ''' Randomly generates a person's surname from 2010 census data, and randomly hyphenates last names for data variety.  '''

    # Select proper surname list, based on ancestry
    if person_race == 'White':
        DF_surname = DF_SURNAME_WHITE
    elif person_race == 'Black':
        DF_surname = DF_SURNAME_BLACK
    elif person_race == 'Native American':
        DF_surname = DF_SURNAME_NATIVE
    elif person_race in ['Asian','Pacific Islander']:
        DF_surname = DF_SURNAME_ASIAN
    else:
        DF_surname = DF_SURNAME_GENERIC
    if person_ethnicity == 'Hispanic':
        DF_surname = DF_SURNAME_HISPANIC

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
    if person_sex == "Male":
        names_list = DF_MALE_NAMES['name'].to_list()
        names_weights = DF_MALE_NAMES[str(year_of_birth)].to_list()
    elif person_sex == "Female":
        names_list = DF_FEMALE_NAMES['name'].to_list()
        names_weights = DF_FEMALE_NAMES[str(year_of_birth)].to_list()

    # Use weighted choice method in random module
    return str(random.choices(names_list, weights = names_weights)[0]).strip().capitalize()

def generate_zip_code():

    ''' Return a random zip code, based on 2010 Census population data. '''

    zip_code = random.choices(DF_ZIP_CODE_DISTRIBUTION['zip_code'], weights = DF_ZIP_CODE_DISTRIBUTION['population'])

    return(str(zip_code[0]).zfill(5))

def generate_address(zip_code, residence):

    ''' Return a randomly chosen street address, using zip_code and web-scraped data. Residence is a boolean value to denote a person's home, and enable apartment numbers or more complex street numbers.  (Non-commercial)'''

    # slice the full address DF into matches based on zip_code
    DF_possible_addresses = DF_USA_ADDRESSES[DF_USA_ADDRESSES['zip_code'] == int(zip_code)]

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
    address_city = address[2]
    address_street = address[3]
    apartment = ''
    address_county = ''

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

def generate_phone_number():

    ''' Randomly generates a phone number. '''

    phone_number = "000-000-0000"

    while phone_number in phone_number_list:
            
        # generate area code using restrictions above
        area_code = random.choice(USABLE_AREA_CODES)

        # generate middle 3 digits
        prefix_code = 0
        while prefix_code in [0,211,311,411,511,611,711,811,911]:
            prefix_code = random.randint(200,999)

        # assemble and last 4 digits
        phone_number = str(area_code) + '-' + str(prefix_code) + '-' + str(random.randint(0,9999)).zfill(4)

    phone_number_list.append(phone_number)

    return phone_number

# Math Functions

def cumulative_distribution(x, x0, gamma):

    ''' Calculates a percentage distribution based on x0 and gamma values. x is a the independent variable.  '''

    return(1.0 / math.pi * math.atan(( x - x0) / gamma) + 0.5)

# Object Instantiation Functions

def generate_times_list(count):

    ''' This function takes an integer argument and returns a number of timestamps per day, roughly evenly distributed around the clock. '''

    global simulation_day_number

    times_list = []
    for x in range(count):
        times_list.append(datetime.date.today() + datetime.timedelta(days = simulation_day_number) + datetime.timedelta(hours = 24 / count * x, minutes = random.normalvariate(mu=0,sigma=30)))

    return times_list

def generate_times_dictionary(order_placed_timestamp):

    sample_drawn_timestamp = order_placed_timestamp
    sample_delivered_timestamp = sample_drawn_timestamp + datetime.timedelta(minutes = (random.random() * 20 + 10))
    sample_accessioned_timestamp = sample_delivered_timestamp + datetime.timedelta(minutes = (random.random() * 10 + 1))
    test_resulted_timestamp = sample_accessioned_timestamp + datetime.timedelta(minutes = (random.random() * 20 + 10))
    result_verified_timestamp = test_resulted_timestamp + datetime.timedelta(minutes = (random.random() * 5))
    result_reported_timestamp = result_verified_timestamp + datetime.timedelta(minutes = (random.random() * 30 + 1))

    time_dictionary = {
        'order_placed_timestamp':order_placed_timestamp,
        'sample_drawn_timestamp':sample_drawn_timestamp,
        'sample_delivered_timestamp':sample_delivered_timestamp,
        'sample_accessioned_timestamp':sample_accessioned_timestamp,
        'test_resulted_timestamp':test_resulted_timestamp,
        'result_verified_timestamp':result_verified_timestamp,
        'result_reported_timestamp':result_reported_timestamp
    }

    return time_dictionary

# Counter Incrementing Functions

def increment_day():

    global simulation_day_number
    global encounter_list

    simulation_day_number += 1

    for x in encounter_list:
        if x.discharge_timestamp != "":
            if (x.discharge_timestamp < datetime.date.today() + datetime.timedelta(days = simulation_day_number)):
                x.deconstruct()
                encounter_list.pop(encounter_list.index(x))
        elif x.encounter_type == "Outpatient":
            x.deconstruct()
            encounter_list.pop(encounter_list.index(x))
    return

def increment_encounter_id():
    ''' Generate a believable encounter ID number, and increment that number when called.  Returns a string. '''
    global order_id
    order_id = str(order_id)[0:4] + str( int(order_id[5:]) + 1).zfill(7) #Increment by at least 1
    return

def increment_sample_id():
    ''' Generate a believable sample ID number, and increment that number when called.  Returns a string. '''
    global sample_id
    sample_id = str(sample_id)[0:4] + str(int(sample_id[5:]) + 1).zfill(7) #Increment by at least 1
    return

def increment_order_id():
    ''' Generate a believable order ID number, and increment that number when called.  Returns a string. '''
    global order_id
    order_id = str(order_id)[0:4] + str( int(order_id[5:]) + 1 + int(random.expovariate(1))).zfill(7) #Increment by at least 1, but randomly more (not all orders are for laboratorys)
    return

# Stamper Functions 

def stamp_record():

    global stamper
    global stamper_reportable_keys
    write_me = ""

    for x in stamper_reportable_keys:
        write_me += str(stamper[x]) + ","

    return(write_me[:-1] + '\n')

def stamp_header():

    global stamper_reportable_keys
    global write_buffer
    write_me = ""

    for x in stamper_reportable_keys:
        write_me += str(x).upper() + ","

    return(write_me[:-1] + '\n')

def clear_stamper():
    
    global stamper

    for key in stamper.keys():
        stamper[key] = ""

    return

# MAIN LOOP --------------------------------------------------------
print("Initiating main loop.")

def main():
    
    global encounter_id
    global sample_id
    global order_id
    global occupied_bed_count
    global provider_pool
    global patient_pool
    global hospital_list
    global laboratory_list
    global NUMBER_OF_TEST_RESULTS
    global simulation_day_number

    # # Loop to create specificed number of physicians
    if os.path.exists(PROVIDER_LIST_FILE_NAME):
        print("Provider pool file found at:", PROVIDER_LIST_FILE_NAME, "Loading file.")
        with open(PROVIDER_LIST_FILE_NAME, "rb") as file_input:
            provider_pool = pickle.load(file_input)
        print(len(provider_pool),'health care providers loaded. (Target:',NUMBER_OF_PROVIDERS,')')

    else:
        print("Creating list of primary care providers.")
        for x in tqdm(range(NUMBER_OF_PROVIDERS)):
            provider_pool.append(Provider())
        print(len(provider_pool),'health care providers added. (Target:',NUMBER_OF_PROVIDERS,')')

        print("Writing provider pool to file.")
        with open(PROVIDER_LIST_FILE_NAME, 'wb') as file_output:
            pickle.dump(provider_pool, file_output)
        
    # loop to create specified number of patients
    if os.path.exists(PATIENT_LIST_FILE_NAME):
        print("Patient pool file found at:", PATIENT_LIST_FILE_NAME, "Loading file.")
        with open(PATIENT_LIST_FILE_NAME, 'rb') as file_input:
            patient_pool = pickle.load(file_input)
        print(len(patient_pool),'patients loaded. (Target:',NUMBER_OF_PATIENTS,')')

    else:
        print("Creating list of patients.")
        for x in tqdm(range(NUMBER_OF_PATIENTS)):
            patient_pool.append(Patient())
        print(len(patient_pool),'patients added. (Target:',NUMBER_OF_PATIENTS,')')

        print("Writing patient pool to file.")
        with open(PATIENT_LIST_FILE_NAME, 'wb') as file_output:
            pickle.dump(patient_pool, file_output)

    # Generate hospitals until the bed target has been reached
    if os.path.exists(HOSPITAL_SYSTEM_FILE_NAME) and os.path.exists(LABORATORY_LIST_FILE_NAME):

        print("  ","Hospital list file found at:", HOSPITAL_SYSTEM_FILE_NAME, "Loading file.")
        print("  ","Laboratory list file found at:", LABORATORY_LIST_FILE_NAME, "Loading file.")

        with open(HOSPITAL_SYSTEM_FILE_NAME, 'rb') as file_input:
            hospital_list = pickle.load(file_input)
        with open(LABORATORY_LIST_FILE_NAME, 'rb') as file_input:
            laboratory_list = pickle.load(file_input)
        
    else:
        print("Creating the hospital system.")
        beds_left = NUMBER_OF_BEDS
        while beds_left > 0:
            new_hospital = Hospital()
            hospital_list.append(new_hospital)
            beds_left -= new_hospital.bed_count
        print("Writing hospital system to file.")
        with open(HOSPITAL_SYSTEM_FILE_NAME, 'wb') as file_output:
            pickle.dump(hospital_list, file_output)
        with open(LABORATORY_LIST_FILE_NAME, 'wb') as file_output:
            pickle.dump(laboratory_list, file_output)

    # Reporting out the hospital and laboratory names
    print("Hospitals:")
    for x in hospital_list:
        print("  ",x.name)
    print("Laboratories:")
    for x in laboratory_list:
        print("  ",x.name)

    # Generate the bed pool.
    print("Adding all beds to the bed pool.")
    for x in hospital_list:
        x.generate_beds()
    print(len(available_bed_pool),'beds added. (Target:',NUMBER_OF_BEDS,')')

    # The main loop for generating test records -------------------------
    print("Preparing output file.")
    file_output = open(RECORDS_FILE_NAME,'w',encoding='UTF-8')

    print("Writing CSV file headers.")
    write_me = stamp_header()
    file_output.write(write_me)

    test_results_count = 0


    # Generate and write records until the target is reached.
    while test_results_count < NUMBER_OF_TEST_RESULTS:
        
        # User feedback
        print("Beginning day", (simulation_day_number + 1), "of the simulation.")

        # Generate encounters up to the target bed occupancy
        print("Filling bed pool to occupancy target percentage.")
        variable_bed_percentage_occupancy_target = random.normalvariate(BED_PERCENTAGE_OCCUPANCY_TARGET,0.05)
        while (occupied_bed_count/(occupied_bed_count + len(available_bed_pool))) < min(variable_bed_percentage_occupancy_target,1):
            encounter_list.append(Encounter())

        # Step through each encounter and generate a number of samples and tests for each sample
        print('Resolving encounters.')
        for encounter in encounter_list:

            # clear and fill stamper with known info
            clear_stamper()
            encounter.fill_stamper()

            # Determine how many times, and when, today the patient will get poked.
            if encounter.encounter_type == "Outpatient":
                number_of_samples = 1
            else:
                number_of_samples = 1 + int(random.expovariate(1))

            order_times_list = generate_times_list(number_of_samples)

            for order_time in order_times_list:

                # generate all timestamps
                time_dictionary = generate_times_dictionary(order_time)
                
                # generate order information 
                increment_order_id()
                order = Order(
                    order_placed_timestamp=time_dictionary['order_placed_timestamp'],
                    result_reported_timestamp=time_dictionary['result_reported_timestamp']
                )
                order.fill_stamper()

                # generate sample information
                increment_sample_id()
                sample = Sample(
                    sample_drawn_timestamp = time_dictionary['sample_drawn_timestamp'],
                    sample_delivered_timestamp = time_dictionary['sample_delivered_timestamp'],
                    sample_accessioned_timestamp = time_dictionary['sample_accessioned_timestamp']
                    )
                sample.fill_stamper()

                # loop to add perform a number of tests on any given sample
                for test in range(random.randint(1,4)):

                    test = Test(time_dictionary)
                    test.fill_stamper()

                    write_me = stamp_record()
                    file_output.write(write_me)
                    test_results_count += 1


                # in the event of an add-on, redraw the text block for the encounter to randomize the ordering physician
                if random.random() < PERCENT_CHANCE_FOR_ADDON_TEST:

                    # generate all timestamps for addon
                    time_dictionary = generate_times_dictionary(time_dictionary['result_reported_timestamp'])
                    
                    # generate order information 
                    increment_order_id()
                    order = Order(
                        order_placed_timestamp=time_dictionary['order_placed_timestamp'],
                        result_reported_timestamp=time_dictionary['result_reported_timestamp']
                    )
                    order.fill_stamper()

                    test = Test(time_dictionary)
                    test.fill_stamper()

                    write_me = stamp_record()
                    file_output.write(write_me)
                    test_results_count += 1

        # Advance the day...    
        print("Finishing the day and discharging patients.")
        print(test_results_count, "results written so far. (Goal:",NUMBER_OF_TEST_RESULTS,")")
        increment_day()

    file_output.close()

    print("Script complete.")
    print("Results written to file. (", RECORDS_FILE_NAME,")")

if __name__ == "__main__":
    main()