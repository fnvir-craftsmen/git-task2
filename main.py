import argparse
from datetime import datetime
from datetime import date

def parse_date(date_str:str) -> date:
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
        if d > date.today():
            raise argparse.ArgumentTypeError("You aren't event born yet! Birthdate must be in the past")
        return d
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid date format. Expected: YYYY-MM-DD")

def main():
    parser = argparse.ArgumentParser(description="Simple CLI tool to show general fun facts based on birthday.")
    parser.add_argument("-b", "--birthday", required=True, type=parse_date, help="Your birthday in the format YYYY-MM-DD")
    args = parser.parse_args()
    
    birthday:date = args.birthday
    print(f"Your birthday is: {birthday}")


if __name__ == "__main__":
    main()
