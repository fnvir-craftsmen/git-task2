import argparse
from datetime import datetime, timedelta
from datetime import date
import calendar
import math
from collections import Counter
import json
import random

def parse_date(date_str:str) -> date:
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
        if d > date.today():
            raise argparse.ArgumentTypeError("You aren't event born yet! Birthdate must be in the past")
        return d
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid date format. Expected: YYYY-MM-DD")

def get_simple_facts(birthday: date):
    weekday_of_birth = birthday.strftime("%A")
    exact_age = get_exact_age(birthday)
    leap_years_count = count_leap_years(birthday)
    days_until_next_birthday = (next_birthday(birthday) - date.today()).days
    return {
        "weekday_of_birth": weekday_of_birth,
        "exact_age": exact_age,
        "leap_years_count": leap_years_count,
        "days_until_next_birthday": days_until_next_birthday
    }

def get_math_facts(birthday: date):
    def is_prime(n: int) -> bool:
        if n <= 1:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    def find_any_prime_in_date(date: datetime.date):
        d = {'year': date.year, 'month': date.month, 'day': date.day}
        for k, v in d.items():
            if is_prime(v):
                return (k, v)
        return None
    
    def get_most_occuring_digit(date: datetime.date):
        digits = str(date).replace('-', '')
        return Counter(digits).most_common(1)[0][0]

    prime_info = find_any_prime_in_date(birthday)

    birthdate_components = birthday.timetuple()[:3] # year, month, day
    sum_of_birthdate_components = sum(birthdate_components)
    product_of_birthdate_components = math.prod(birthdate_components)

    gcd_of_birthdate_components = math.gcd(*birthdate_components)
    lcm_of_birthdate_components = math.lcm(*birthdate_components)

    most_occuring_digit = get_most_occuring_digit(birthday)

    return {
        "prime_info": prime_info,
        "sum_of_birthdate_components": sum_of_birthdate_components,
        "product_of_birthdate_components": product_of_birthdate_components,
        "gcd_of_birthdate_components": gcd_of_birthdate_components,
        "lcm_of_birthdate_components": lcm_of_birthdate_components,
        "most_occuring_digit": most_occuring_digit
    }

def get_month_facts(birthday: date):
    with open('months_fact.json', 'r') as f:
        months_facts = json.load(f)
        month = birthday.month
        return months_facts[str(month)]

def get_a_random_fact():
    with open('random_facts.json', 'r') as f:
        random_facts = json.load(f)
        return random.choice(random_facts)

def show_random_fact():
    print()
    print(f"{Colors.YELLOW}A random fact for you:{Colors.ENDC}")
    print(get_a_random_fact())

def show_month_facts(birthday: date):
    month_facts = get_month_facts(birthday)
    print() #newline to add top space
    print(f"{Colors.YELLOW}Month facts about your birth month ({month_facts['name']}):{Colors.ENDC}")
    print(f'Season: {month_facts["season"]}')
    print(f'Fun fact: {month_facts["fun_fact"]}')
    print(f'A famous event in your birth month: {month_facts["famous_event"]}')

def show_math_facts(birthday: date):
    print('\n\n')
    print(f"{Colors.YELLOW}Math facts about your birthday:{Colors.ENDC}\n")

    math_facts = get_math_facts(birthday)

    prime_info = math_facts["prime_info"]
    if prime_info is not None:
        unit, value = prime_info    
        print(f'The {unit} of your birthday is a prime number: {value}.')
    else:
        print("No primes in your birth day/month/year.")

    print(f'The sum of your birth year, month, and day is: {math_facts["sum_of_birthdate_components"]}')
    
    print(f'The product of your birth year, month, and day is: {math_facts["product_of_birthdate_components"]}')

    print(f'The GCD of your birth year, month, and day is: {math_facts["gcd_of_birthdate_components"]}')

    print(f'The LCM of your birth year, month, and day is: {math_facts["lcm_of_birthdate_components"]}')
    
    print(f'The most occuring digit in your birth year, month, and day is: {math_facts["most_occuring_digit"]}')

def show_simple_facts(birthday:date):
    print(f"{Colors.YELLOW}Some facts about your birthday:{Colors.ENDC}")

    simple_facts = get_simple_facts(birthday)

    weekday_of_birth = simple_facts["weekday_of_birth"]
    print(f'You were born on a {weekday_of_birth}.')
    
    age = simple_facts["exact_age"]
    print(f'You are {age["years"]} years, {age["months"]} months, and {age["days"]} days old.')

    leap_years_count = simple_facts["leap_years_count"]
    print(f'There were {leap_years_count} leap years since your birth.')

    days_until_next_birthday = simple_facts["days_until_next_birthday"]
    print(f'Days until your next birthday: {days_until_next_birthday} days')


def next_birthday(birthday: date) -> date:
    if birthday.day == 29 and birthday.month == 2:
        this_year = date.today().year
        next_leap_year = next(filter(calendar.isleap, (this_year + i for i in range(1,5))))
        return date(next_leap_year, birthday.month, birthday.day)
    return date(date.today().year+1, birthday.month, birthday.day)


def count_leap_years(birthday:date) -> int:
    today = date.today()
    return sum(1 for y in range(birthday.year, today.year + 1) if calendar.isleap(y) and birthday <= date(y, 2, 29) <= today)

def get_exact_age(birthday:date) -> dict[str, int]:
    today = date.today()
    years = today.year - birthday.year
    months = today.month - birthday.month
    days = today.day - birthday.day
    if days < 0:
        months -= 1
        prev_month_end = date(today.year, today.month, 1) - timedelta(days=1)
        days += prev_month_end.day
    if months < 0:
        years -= 1
        months += 12
    return {"years": years, "months": months, "days": days}

def main():
    parser = argparse.ArgumentParser(description="Simple CLI tool to show general fun facts based on birthday.")
    parser.add_argument("-b", "--birthday", required=True, type=parse_date, help="Your birthday in the format YYYY-MM-DD")
    parser.add_argument("--json", action="store_true", help="Output the facts in JSON format")
    args = parser.parse_args()

    print(f'{Colors.GREEN}Welcome to the birthday facts CLI!{Colors.ENDC}\n')
    
    birthday:date = args.birthday
    print(f"{Colors.BLUE}Your birthday is: {birthday}{Colors.ENDC}")

    if args.json:
        combined_facts = {
            "simple_facts": get_simple_facts(birthday),
            "math_facts": get_math_facts(birthday),
            "month_facts": get_month_facts(birthday),
            "random_fact": get_a_random_fact()
        }
        print(json.dumps(combined_facts, indent=4))
    else:
        show_simple_facts(birthday)
        show_math_facts(birthday)
        show_month_facts(birthday)
        show_random_fact()


class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    ENDC  = '\033[0m'

if __name__ == "__main__":
    main()
