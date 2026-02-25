## Fun facts based on birthday CLI

A simple python based CLI that gives fun facts after prompting the user for their birthday.

### How to run

1. Clone the repository
2. Install python 3.13+
3. Run: 
    ```sh
    python main.py --birthday YYYY-MM-DD
    ```

### CLI Arguments
Run the program with `--help` to see all available CLI options. But, just for convenience:
- `--birthday` (required): birthday in ISO format.
- `-b`: short form for `--birthday`.
- `--help`: show help message and exit.
- `--json`: show the output as json
- `--export`: export the output json into a file called output.txt in the same dir
