import unittest
import pwnedpasswords
from create_database import mydb, my_cursor
import random
from settings import lowercase, uppercase, symbol, numbers


def check_pwned_password(password):
    x = pwnedpasswords.check(password, plain_text=True)
    return x


def autogenerate():
    sql4 = "SELECT uppercase, lowercase, symbols, numbers FROM complexity WHERE complexity_id = 1"
    result4 = my_cursor.execute(sql4)
    result4 = my_cursor.fetchall()
    password_length = result4[0][0] + result4[0][1] + result4[0][2] + result4[0][3]
    password_check = 1
    password = [None] * password_length  # Password string is set to empty
    while password_check == 1:
        for i in range(result4[0][0]):
            random_placeholder = random.randrange(1, password_length, 1)
            random_character = random.randrange(1, 26, 1)
            password[random_placeholder] = uppercase[random_character]
        for i in range(result4[0][1]):
            random_placeholder = random.randrange(1, password_length, 1)
            while password[random_placeholder] is not None:
                random_placeholder = random.randrange(1, password_length, 1)
            random_character = random.randrange(1, 26, 1)
            password[random_placeholder] = lowercase[random_character]
        for i in range(result4[0][2]):
            random_placeholder = random.randrange(1, password_length, 1)
            while password[random_placeholder] is not None:
                random_placeholder = random.randrange(1, password_length, 1)
            random_character = random.randrange(1, 10, 1)
            password[random_placeholder] = symbol[random_character]
        for i in range(password_length):
            if password[i] is None:
                random_character = random.randrange(1, 10, 1)
                password[i] = numbers[random_character]
        final_password = ""
        for i in password:
            final_password += i
        password_check = pwnedpasswords.check(final_password, plain_text=True)

    assert password_check == 0
    # print("Secured Password!")
    return final_password


class Autogenerate_Test(unittest.TestCase):
    def setUp(self):
        # Create a cursor and initialize it
        my_cursor = mydb.cursor()
        print("SetUp Called:")
        sql4 = "SELECT uppercase, lowercase, symbols, numbers FROM complexity WHERE complexity_id = 1"
        result4 = my_cursor.execute(sql4)
        result4 = my_cursor.fetchall()
        self.uppercase = result4[0][0]
        self.lowercase = result4[0][1]
        self.symbol = result4[0][2]
        self.number = result4[0][3]

    def tearDown(self):
        self.uppercase = 0
        self.lowercase = 0
        self.symbol = 0
        self.number = 0
        print("Teardown Called ... ")

    def test_password_length(self):
        print("Test - Password Length Test Called ...")
        # Act
        password_length = len(autogenerate())
        # Assert
        self.assertEqual(password_length, self.uppercase + self.lowercase + self.symbol + self.number)

    def test_complexity(self):
        print("Test - Password Complexity")
        # Act
        password = autogenerate()
        lowerc = 0
        upperc = 0
        symbolc = 0
        numberc = 0
        for character in password:
            if character.islower():
                lowerc = lowerc + 1
            if character.isupper():
                upperc = upperc + 1
            if character in symbol:
                symbolc = symbolc + 1
            if character.isnumeric():
                numberc = numberc + 1
        # Assert
        self.assertEqual(lowerc, self.lowercase)
        self.assertEqual(upperc, self.uppercase)
        self.assertEqual(symbolc, self.symbol)
        self.assertEqual(numberc, self.number)


class pwndpassword_test(unittest.TestCase):
    def setUp(self):
        print("SetUp Called:")
        self.ispwned = 1
        self.notpwned = 0

    def tearDown(self):
        self.ispwned = 0
        self.notpwned = 0
        print("Teardown Called ... ")

    def test_pwnedpassword(self):
        print("Test - Pwn Password Test Called ...")
        # Act
        pwnedpassword = check_pwned_password("123456")
        # Assert
        self.assertNotEqual(pwnedpassword, self.notpwned)


if __name__ == "__main__":
    unittest.main()
