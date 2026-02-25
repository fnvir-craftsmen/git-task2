import argparse

def main():
    parser = argparse.ArgumentParser(description="Simple CLI tool to show general fun facts based on birthday.")
    parser.add_argument("-b", "--birthday", required=True, type=str, help="Your birthday in the format YYYY-MM-DD")
    args = parser.parse_args()
    if args.birthday:
        print(f"Your birthday is: {args.birthday}")

if __name__ == "__main__":
    main()
