# Evolvement
*A program to find connections between a primary target and the people they follow on Instagram
This program takes an initial goal and recursively extracts the people who are followed by this goal until it reaches the depth of the program's input.
At the end of the extraction process, a chart of connections between people is displayed*

# Installation

1.After entering the Evolvement folder, run the following command:
```bash
pip install -r requirements.txt
```

2.If you do not have the firefox browser, download it.

3.Log in to your account using the firefox browser.

4.Stay logged in and run the file 615_import_firefox_session.py (at this stage you can log out of your account)

```bash
python 615_import_firefox_session.py
```

5.Enter the **`conf.ini`** file and just put your user account name in front of **`USER_NAME`** and save the changes.

# Usage

Run the evolvement.py file:
```bash 
python evolvement.py
```

# Sample

input:

    {
    'a': ['b', 'c', 'd'],
    'b': ['c', 'a', 'e'],
    'c': ['b', 'd', 'f'],
    'd': ['a', 'c', 'e'],
    'e': ['d', 'f', 'b'],
    'f': ['e', 'a', 'c']
    }

output:

![sample](https://github.com/ogel4s/Evolvement/assets/141678130/39b56831-c860-4bc3-9689-51ba56dc7199)

