import argparse
from datetime import datetime, timedelta
from datetime import date
import calendar

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

def show_simple_facts(birthday:date):
    print("Some facts about your birthday:")

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
    args = parser.parse_args()
    
    birthday:date = args.birthday
    print(f"Your birthday is: {birthday}")

    show_simple_facts(birthday)


if __name__ == "__main__":
    main()
