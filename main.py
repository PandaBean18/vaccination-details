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
    print()
    chosen_option = int(input())
    print()
    if not(valid_input(len(dates), chosen_option)): 
        print('Please select a valid date.\n')
        chosen_option = get_date(dates)

    return dates[chosen_option-1]

def get_session(sessions):
    i = 0
    print('Please select the center where you would like to get vaccinated\n')
    while i < len(sessions):
        current_session = sessions[i]
        print(i+1, ".  ", current_session['name'], sep='')
        print('    Fee type:', current_session['fee_type'])

        if current_session['allow_all_age']:
            print('    Age limit: All ages above 15 allowed')
        else:
            print('    Age limit:', current_session['min_age_limit'], '-', current_session['max_age_limit'])

        print('    Capacity of dose 1:', current_session['available_capacity_dose1'])
        print('    Capicity of dose 2:', current_session['available_capacity_dose2'])
        print('    Vaccine:', current_session['vaccine'], end='\n\n')
        i += 1
    
    chosen_option = int(input())
    print()

    if not(valid_input(len(sessions), chosen_option)):
        print('Invalid option selected.\n')
        chosen_option = get_session(sessions) 

    return sessions[chosen_option-1]

def get_slot(session):
    i = 0
    slots = session['slots']
    print('Please select the vaccination slot.\n')

    while i < len(slots):
        print(i+1, '. ', slots[i], sep='')
        i += 1
    
    chosen_option = int(input())
    print()
    if not(valid_input(len(slots), chosen_option)):
        print('Invalid option selected.\n')
        get_slot(session)

    return slots[chosen_option-1]



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
    slot = get_slot(session)

    return [date, session['name'], slot]

def render_user_profile(user):
    print('Your profile:-\n')
    print('Name:', user.username)
    print('Email:', user.email)
    print('Phone number:', user.phone)
    print('Age:', user.age)
    print('Pin code:', user.pin_code)
    print('Date of vaccination:', user.vaccination_date)
    print('Center:', user.vaccination_centre)
    print('Time slot:', user.slot)
    print()

def new_user():
    email = get_email()

    if User().already_exists({'email': email}):
        print('Email is already in use.\n')
        run()

    username = get_username()
    phone  = get_phone()
    age = int(input('Please type in your age\n'))
    print()
    pin_code = int(get_pin_code())
    print()
    center_data = get_centers_data(pin_code)
    date = center_data[0]
    session = center_data[1]
    slot = center_data[2] 
    User().create({'email': email, 'username': username, 'phone': phone, 'age': age, 'pin_code': pin_code, 'vaccination_date': date, 'vaccination_centre': session, 'slot': slot})
    user = User().find({'email': email})[0]
    render_user_profile(user)

def update_profile(id):
    email = get_email()
    username = get_username()
    phone = get_phone()
    age = int(input('Please type in your age\n'))
    print()

    params = {'email': email, 'username': username, 'phone': phone, 'age': age}

    User().update(id, params)
    render_user_profile()
    run()


def existing_user():
    email = input('Please type the registered email.\n')
    user = User().find({'email': email})
    user_id = user[0].id
    if  len(user) == 0:
        print('User with email {} doesnt exist.\n'.format(email))

    render_user_profile(user[0])

    print('What would you like to do?\n')
    print('1. Update profile')
    print('2. Change vaccination center')
    print('3. Change vaccination date')

    chosen_option = int(input())
    print()

    while not(valid_input(3, chosen_option)):
        print('Please input a valid option.\n')
        chosen_option = int(input())
        print()

    if chosen_option == 1:
        update_profile(user_id)
    elif chosen_option == 2:
        date = user[0].vaccination_date
        

def run():
    print('Please type the number in front of the option to select the option.\n')
    print('1. New user\n2. Registered User\n\nEnter 0 to exit\n')
    chosen_option = int(input())
    print()
    if not(valid_input(2, chosen_option)):
        print('Please input a valid option.\n')
        run()
    elif chosen_option == 1:
        new_user()
    elif chosen_option == 2:
        existing_user()

run()