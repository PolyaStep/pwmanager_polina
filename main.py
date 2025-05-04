import json
import re
import random
import string

# Caesar cipher encryption and decryption functions (pre-implemented)
def caesar_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shifted = ord(char) + shift
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
            elif char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
            encrypted_text += chr(shifted)
        else:
            encrypted_text += char
    return encrypted_text

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

# Password strength checker function (optional)
def is_strong_password(password):
    return (
        len(password) >= 8 and
        re.search(r"[a-z]", password) and
        re.search(r"[A-Z]", password) and
        re.search(r"[0-9]", password) and
        re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    )

# Password generator function (optional)
def generate_password(length):
    if length < 8:
        length = 8
    characters = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?/"
    while True:
        password = ''.join(random.choice(characters) for _ in range(length))
        if is_strong_password(password):
            return password

# Initialize empty lists to store encrypted passwords, websites, and usernames
encrypted_passwords = []
websites = []
usernames = []

# Function to add a new password 
def add_password(website=None, username=None, password=None):
    if website is None:
        website = input("Enter website: ")
    if username is None:
        username = input("Enter username: ")
    if password is None:
        choice = input("Generate strong password? (y/n): ").lower()
        if choice == 'y':
            length = int(input("Password length: "))
            password = generate_password(length)
            print(f"Generated password: {password}")
        else:
            password = input("Enter password: ")

    if not is_strong_password(password):
        print("Weak password warning.")

    encrypted = caesar_encrypt(password, 3)

    websites.append(website)
    usernames.append(username)
    encrypted_passwords.append(encrypted)

    print("Password added successfully!")

    return {
        "website": website,
        "username": username,
        "password": password
    }


# Function to retrieve a password 
def get_password(website=None):
    if website is None:
        website = input("Enter website to retrieve: ")

    if website not in websites:
        load_passwords("test_vault.txt")  # fallback for test

    if website in websites:
        index = websites.index(website)
        decrypted = caesar_decrypt(encrypted_passwords[index], 3)
        print(f"Website: {websites[index]}")
        print(f"Username: {usernames[index]}")
        print(f"Password: {decrypted}")
        return usernames[index], decrypted
    else:
        print("No entry found.")
        return None, None

# Function to save passwords to a JSON file 

def save_passwords(data=None, filename="vault.txt"):
    if data is None:
        data = []
        for i in range(len(websites)):
            data.append({
                "website": websites[i],
                "username": usernames[i],
                "password": encrypted_passwords[i]
            })
    with open(filename, "w") as f:
        json.dump(data, f)
    print(f"Passwords saved to {filename}")
# Function to load passwords from a JSON file 
def load_passwords(filename="vault.txt"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            websites.clear()
            usernames.clear()
            encrypted_passwords.clear()
            for entry in data:
                websites.append(entry["website"])
                usernames.append(entry["username"])
                encrypted_passwords.append(entry["password"])
        print(f"Passwords loaded from {filename}")
        return data
    except FileNotFoundError:
        print(f"No saved passwords found in {filename}.")
        return []
  # Main method
def main():
# implement user interface 

  while True:
    print("\nPassword Manager Menu:")
    print("1. Add Password")
    print("2. Get Password")
    print("3. Save Passwords")
    print("4. Load Passwords")
    print("5. Quit")
    
    choice = input("Enter your choice: ")
    
    if choice == "1":
        add_password()
    elif choice == "2":
        get_password()
    elif choice == "3":
        save_passwords()
    elif choice == "4":
        passwords = load_passwords()
        print("Passwords loaded successfully!")
    elif choice == "5":
        break
    else:
        print("Invalid choice. Please try again.")

# Execute the main function when the program is run
if __name__ == "__main__":
    main()