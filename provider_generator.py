import random
import os
import pandas as pd

# File name variables and constants
PERSON_LIST_FILE = "OUTPUT/person_list.csv"
PROVIDER_TYPE_FILE = "REFERENCE/provider/provider_type.csv"
PROVIDER_SPECIALTY_FILE = "REFERENCE/provider/provider_specialty.csv"
provider_list_file = "OUTPUT/provider_list.csv"

# global constants
TARGET_PROVIDER_COUNT = 1000
PROVIDER_ID_PREFIX_CODES = ["01","02","03","00","04","89","05","55","75","92","06","91","07","81","08","09","10","68","69","11","85","12","13","54","14","78","15","16","76","17","70","18","19","71","95","30","31","83","32","96","33","57","34","86","35","36","72","37","90","38","93","39","73","40","84","41","42","87","43","44","88","45","67","74","97","46","47","48","20","21","80","22","82","23","24","77","25","26","79","27","28","29","49","50","94","51","58","52","53","56","59","64","65","66","99"]
PROVIDER_ID_THIRD_DIGIT_CODES = ["0","1","2","3","4","5","6","7","8","9","M","S","T","U","W","Y","Z"]

# Global variables
provider_dict = dict()
provider_list = []
provider_id_list = [""]
provider_type_DF = pd.read_csv(PROVIDER_TYPE_FILE)
provider_specialty_DF = pd.read_csv(PROVIDER_SPECIALTY_FILE)


def Check_Input_File_Exists():

    ''' Checks to see if the input file for providers yet exists.  If not, abort. '''

    # Delete the output file if it already exists
    if not os.path.isfile(PERSON_LIST_FILE):
        quit

    return


def Check_Output_File_Exists():

    ''' Checks to see if the output file for providers yet exists.  If not, create it. '''

    # Delete the output file if it already exists
    if os.path.isfile(provider_list_file):
        os.remove(provider_list_file)

    return


def Gather_Provider_Names_List():

    ''' Collects a list of age appropriate names from the persons_list output file. '''

    # Load person list into memory
    with open(PERSON_LIST_FILE, 'r') as input_file:

        # Ignore the first line (headers)
        read_string = input_file.readline()

        for x in range(TARGET_PROVIDER_COUNT):

            # Then read the first entry
            read_string = input_file.readline().split(sep=',')

            # Make sure the person read is over the age of 25
            while int(read_string[4]) < 25:
                read_string = input_file.readline().split(sep=',')

            # Add the provider to the list of names
            provider_list.append((read_string[0] + " " + read_string[2]))

    return


def Get_Provider_Specialty():

    ''' Returns a weighted random choice for practitioner specialty. '''
 
    return random.choices(provider_specialty_DF['specialty'], weights = provider_specialty_DF['count'])[0]


def Get_Provider_Type():

    ''' Returns a weighted random choice for practitioner type. '''

    return str(random.choices(provider_type_DF['type'], weights = provider_type_DF['count'])[0])


def Update_Provider_Name(provider_type, provider_name):

    ''' Updates the provider's name to reflect the new type. '''

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


def Generate_Provider_ID():

    ''' Generates a provider ID number according to allowable values from Medicare. '''

    provider_id = ""

    # check that provider id is unique
    while provider_id in provider_id_list:

        # create a provider ID based on rules from medicare website
        provider_id = (str(random.choice(PROVIDER_ID_PREFIX_CODES)) + str(random.choice(PROVIDER_ID_THIRD_DIGIT_CODES)) + str(random.randint(0, 9999)).zfill(4))

    return provider_id


# Main loop
def main():

    Check_Input_File_Exists()
    Check_Output_File_Exists()
    Gather_Provider_Names_List()

    with open(provider_list_file, 'w') as output_file:

        output_file.write("provider_name,provider_id,provider_specialty")

        for x in provider_list:

            provider_name = str(x)
            provider_specialty = Get_Provider_Specialty()
            provider_type = Get_Provider_Type()
            provider_name = Update_Provider_Name(provider_type, provider_name)
            provider_id = Generate_Provider_ID()

            output_file.write((provider_name + ',' + provider_id + ',' + provider_specialty))

    print("Provider list generation complete.")


# Protection from accidental calling
if __name__ == "__main__":
    main()
