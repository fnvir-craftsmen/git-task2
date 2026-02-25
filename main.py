import argparse
from datetime import datetime, timedelta
from datetime import date
import calendar

def parse_date(date:str) -> date:
    try:
        return datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid date format. Expected: YYYY-MM-DD")

def show_simple_facts(birthday:date):
    print("Some facts about your birthday:")

    weekday_of_birth = birthday.strftime("%A")
    print(f'You were born on a {weekday_of_birth}.')
    
    age = get_exact_age(birthday)
    print(f'You are {age["years"]} years, {age["months"]} months, and {age["days"]} days old.')

    leap_years_count = count_leap_years(birthday)
    print(f'There were {leap_years_count} leap years since your birth.')


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
