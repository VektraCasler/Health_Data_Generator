import random

permitted_numbers = "1 2 3 4 5 6 7 8 9 0 "
permitted_letters = "a b c d e f g h j k m n p q r s t u v w x y z "

permitted_pool = (permitted_numbers + permitted_letters.upper() + permitted_letters.lower()).split()
#permitted_pool = permitted_string.split()

password_length = 16
password_count = 10
password = ""

for x in range(password_count):

    password = ""

    for y in range(password_length):
        
        random.shuffle(permitted_pool)
        password += permitted_pool[0]

    print(password)