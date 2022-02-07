from user import *
import re 
from cowin_api import *
from datetime import *

def valid_input(max_val, input_val):
    return (input_val <= max_val)

def get_email():
    email = input('Please type in your email.\n')
    print()
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not(re.fullmatch(email_regex, email)):
        print('Email is invalid.\n')
        email = get_email()

    return email

def get_username():
    username = input('Please type in your full name.\n')
    print()
    return username.title()

def get_phone():
    number = int(input('Please type in your phone number.\n'))
    print()
    mod_val = number % 1000000000 
    
    if not(mod_val < 1000000000 and mod_val != number):
        print('Phone number is invalid.\n')
        number = get_phone()
    
    return number

def get_pin_code():
    pin_code_regex = "^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$"
    pin_code = input('Please type your pincode.\n')
    print()
    
    if not(re.fullmatch(pin_code_regex, pin_code)):
        print('Invalid pincode.\n')
        pin_code = get_pin_code()

    return pin_code

def get_date(dates):
    print('Please select a date for your vaccination.\n')
    i = 0 

    while i < len(dates):
        print(i+1 ,'. ', dates[i], sep="")
        i += 1
    
    chosen_option = int(input())

    if not(valid_input(len(dates), chosen_option)): 
        print('Please select a valid date.\n')
        chosen_option = get_date(dates)

    return dates[chosen_option]

def get_session(sessions):
    for session in sessions:
        print(session)


def get_centers_data(pin):
    api = CowinApi()
    today = datetime.now()
    dt = timedelta(days = 1)
    tomorrow = (today + dt).strftime('%d-%m-%Y')
    api.get_data(pin, tomorrow)
    dates = api.get_dates()
    date = get_date(dates)
    sessions = api.get_sessions_for_date(date)
    session = get_session(sessions)

def new_user():
    email = get_email()
    username = get_username()
    phone  = get_phone()
    age = int(input('Please type in your age\n'))
    print()
    pin_code = int(get_pin_code())
    print()
    get_centers_data(pin_code)

def run():
    print('Please type the number in front of the option to select the option.\n')
    print('1. New user\n2. Registered User\n')
    chosen_option = int(input())
    print()
    if not(valid_input(2, chosen_option)):
        print('Please input a valid option.\n')
        run()
    elif chosen_option == 1:
        new_user()

run()