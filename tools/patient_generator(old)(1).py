import random
import datetime

# Global Variables
number_of_records = 1000
patient_sexes = ["Male", "Female"]
rel_path = "C:/Users/vcasler/Documents/Scripts/"
file_name = "Patient_List.txt"

# Reading in data lists 
with open(rel_path + "male_names.txt") as file: 
    male_names_list = file.readlines()

with open(rel_path + "female_names.txt") as file:
    female_names_list = file.readlines()

with open(rel_path + "last_names.txt") as file:
    last_names_list = file.readlines()


def get_patient_sex():

    return random.choice(patient_sexes).strip()


def get_patient_name(patient_sex):

    if patient_sex == "Male":
        first_name = random.choice(male_names_list).strip()
    else:
        first_name = random.choice(female_names_list).strip()

    last_name = random.choice(last_names_list).title().strip()

    return (first_name + " " + last_name)


def get_patient_age():

    age_rand = random.random()

    # Using case select to choose age bracket for patient from 2010 census data distributions for US
    if age_rand >= 0.999827159:
        age_category = 95
    elif age_rand >= 0.998624732:
        age_category = 90
    elif age_rand >= 0.9939336:
        age_category = 85
    elif age_rand >= 0.982207247:
        age_category = 80
    elif age_rand >= 0.96360511:
        age_category = 75
    elif age_rand >= 0.939903407:
        age_category = 70
    elif age_rand >= 0.909852232:
        age_category = 65
    elif age_rand >= 0.869575495:
        age_category = 60
    elif age_rand >= 0.815103699:
        age_category = 55
    elif age_rand >= 0.751411102:
        age_category = 50
    elif age_rand >= 0.679189411:
        age_category = 45
    elif age_rand >= 0.605638255:
        age_category = 40
    elif age_rand >= 0.537974236:
        age_category = 35
    elif age_rand >= 0.472614127:
        age_category = 30
    elif age_rand >= 0.407958621:
        age_category = 25
    elif age_rand >= 0.339611564:
        age_category = 20
    elif age_rand >= 0.269696387:
        age_category = 15
    elif age_rand >= 0.198309629:
        age_category = 10
    elif age_rand >= 0.131337992:
        age_category = 5
    elif age_rand >= 0.065430458:
        age_category = 5
    else:
        age_category = 0

    return (age_category + random.choice(range(5)))


def get_patient_SSN():

    AAA = "000"

    while AAA == "000":
        AAA = str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9))

    GG = "00"

    while GG == "00":
        GG = str(random.randint(0,9)) + str(random.randint(0,9))

    SSSS = "0000"

    while SSSS == "0000":
        SSSS = str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9))

    SSN = AAA + "-" + GG + "-" + SSSS

    return SSN


def get_patient_DOB(patient_age):

    return (datetime.date.today() - datetime.timedelta(days = 365 * float(patient_age)) - datetime.timedelta(days=random.random() * 365))

def main():

    header = "Last_name, First_name, Age, DOB, Sex, SSN".upper() + "\n"

    with open((rel_path + file_name), 'w') as file:
        
        file.write(header)

    for x in range(number_of_records):

        patient_age = get_patient_age()
        patient_DOB = get_patient_DOB(patient_age)
        patient_sex = get_patient_sex()
        patient_name = get_patient_name(patient_sex)
        patient_first_name = patient_name.split()[0]
        patient_last_name = patient_name.split()[1]
        patient_SSN = get_patient_SSN()

        new_record = patient_last_name + ", " + patient_first_name + ", " + str(patient_age) + ", " + str(patient_DOB) + ", " + patient_sex + ", " + patient_SSN + "\n"
    
        with open((rel_path + file_name), 'a') as file:
        
            file.write(new_record)

print(str(number_of_records) + " records generated and writtent to " + file_name )

if __name__ == "__main__":
    main()