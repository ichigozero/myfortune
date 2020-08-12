# About
Daily horoscope scraper modules for various Japanese television websites.\
Japanese television websites supported by this program is as follow:
- Fuji TV (mezamashi)
- Nippon TV (sukkirisu)
- TV Asahi (go-go-hoshi)
- TBS (gudetama)

All output will be written in Japanese language.

# Installation
```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install .
```

# Usage
There are two ways on how to use this program.

## Printing fetched horoscope to command line
```bash
$ myfortune uranatte COMMAND BIRTHDATE
```

Where:
- COMMAND is one of the following:
  * go-go-hoshi
  * gudetama
  * mezamashi
  * sukkirisu

- BIRTHDATE is your birthday with month/day format.
  e.g. 1st April would be 4/1.

## Send fetched horoscope to an e-mail address
1. First define SMTP server details for the e-mail used to send
   the program output by typing the following command:
   ```bash
   $ myfortune init-config
   ```
2. Enter SMTP server details as required.
3. Run the following command.
   ```bash
   $ myfortune uranatte -e <e-mail address> COMMAND BIRTHDATE
   ```
