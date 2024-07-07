# PasswordManager

This is a simple yet versatile password manager designed to store and retrieve passwords for different accounts. Unlike most password managers, this one does not require a master password to access stored passwords and runs entirely on your local machine. Note that you are solely responsible for the security of your passwords.

## Table of Contents

- [Warning/Disclaimer](#warningdisclaimer)
- [Technologies](#technologies)
- [How to Execute the Program](#how-to-execute-the-program)
- [Features](#features)
- [Author](#author)

## Warning/Disclaimer

The author, contributors, and the software itself are not responsible for any loss of data or security breaches resulting from the use of this software. This software is provided "as-is," and the user assumes all responsibility for the security of their passwords. For more details, refer to the [license](LICENSE.md).

Being Italian, the comments in the code are written in Italian. If you want to contribute to the project, I welcome your pull requests with comments in English.

## Technologies

This program was developed using the following technologies:

- **Python**
- **Cryptography** (for encryption/decryption, specifically using the Fernet symmetric encryption algorithm)
- **Pandas** (for data manipulation, used here for "pretty data printing")
- **Zxcvbn** (for password strength estimation)
- **Levenshtein** (for string similarity estimation)

## How to Execute the Program

To run the program, ensure Python is installed on your machine. Download Python from the official website [here](https://www.python.org/downloads/).

This program was developed using Python 3.10.11 but should work with any version of Python 3.10.x. Check your Python version by running the following command in your terminal:
```bash
python --version
```

Install the required libraries with this command:
```bash
pip install cryptography pandas zxcvbn Levenshtein
```

After installing Python and the required libraries, clone this repository and open it in your favorite IDE. Then, run the program by starting the "user_interface.py" file and follow the instructions that appear in the terminal.

# Features

This program includes the following features:

- **Initialization of the Password Manager** (creation of the password database)
- **Addition of New Entries**
- **Modification of Entries**
- **Deletion of Entries**
- **Search and Print Entries by Criteria:**
    - Entries containing a string similar to an inserted string in a selected field
    - Entries containing a string similar to an inserted string in any field
    - Entries containing a string equal to an inserted string in a selected field
    - Entries containing a string similar to another string in another entry in a selected field
    - Entries containing a string equal to another string in another entry in a selected field
    - Search by ID
- **Display of All Entries**
- **Addition of New Fields**
- **Modification of Fields**
- **Deletion of Fields**
- **Backup of the Dataset**
- **Elimination/Invalidation of the Dataset**
- **Password Strength Estimation** (using the Zxcvbn library)

## Author

- [LorenBll](https://github.com/LorenBll) .
