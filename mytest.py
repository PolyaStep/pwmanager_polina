import unittest
import json
import os
from main import (
    is_strong_password, generate_password, add_password, get_password, save_passwords, load_passwords, caesar_encrypt 
)

class TestPasswordManager(unittest.TestCase):

    def setUp(self):
        # Create a temporary vault file for testing
        self.test_passwords_file = "test_vault.txt"
        self.test_passwords = [
            {"website": "example.com", "username": "user123", "password": "P@ssw0rd"},
            {"website": "test.com", "username": "testuser", "password": "TestP@ss123"}
        ]

        encrypted_data = []
        for entry in self.test_passwords:
            encrypted_data.append({
                "website": entry["website"],
                "username": entry["username"],
                "password": caesar_encrypt(entry["password"], 3)
            })

        with open(self.test_passwords_file, "w") as f:
            json.dump(encrypted_data, f)

    def tearDown(self):
        if os.path.exists(self.test_passwords_file):
            os.remove(self.test_passwords_file)

    def test_is_strong_password(self):
        self.assertTrue(is_strong_password("Str0ngP@ssw0rd"))
        self.assertFalse(is_strong_password("Weak123"))
        self.assertFalse(is_strong_password("weakpassword123!"))
        self.assertFalse(is_strong_password("Weakpassword123"))

    def test_generate_password(self):
        length = 12
        password = generate_password(length)
        self.assertEqual(len(password), length)
        self.assertTrue(is_strong_password(password))

        length = 16
        password = generate_password(length)
        self.assertEqual(len(password), length)
        self.assertTrue(is_strong_password(password))

    def test_add_password(self):
        website = "example.net"
        username = "user456"
        password = "StrongP@ssw0rd"
        result = add_password(website, username, password)
        self.assertEqual(result["website"], website)
        self.assertEqual(result["username"], username)
        self.assertEqual(result["password"], password)

    def test_get_password(self):
        load_passwords(self.test_passwords_file)

        username, password = get_password("example.com")
        self.assertEqual(username, "user123")
        self.assertEqual(password, "P@ssw0rd")

        username, password = get_password("nonexistent.com")
        self.assertIsNone(username)
        self.assertIsNone(password)

    def test_save_passwords(self):
        
        encrypted_data = []
        for entry in self.test_passwords:
            encrypted_data.append({
                "website": entry["website"],
                "username": entry["username"],
                "password": caesar_encrypt(entry["password"], 3)
            })

        save_passwords(encrypted_data, self.test_passwords_file)

        with open(self.test_passwords_file, "r") as f:
            saved = json.load(f)
        self.assertEqual(saved, encrypted_data)

    def test_load_passwords(self):
        loaded = load_passwords(self.test_passwords_file)
       
        decrypted = []
        for i in range(len(loaded)):
            decrypted.append({
                "website": loaded[i]["website"],
                "username": loaded[i]["username"],
                "password": caesar_encrypt(loaded[i]["password"], -3)
            })
        self.assertEqual(decrypted, self.test_passwords)

      
        self.assertEqual(load_passwords("nonexistent.txt"), [])

if __name__ == '__main__':
    unittest.main()
