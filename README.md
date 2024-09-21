# Program Manager

This script manages the launching and stopping of programs. It can either start programs listed in a file or stop them based on their names. It uses the `psutil` library to handle processes.

## Features

- **Stop Programs**: Forcefully terminates programs if they don't stop normally.
- **Run Programs**: Launches programs based on provided paths.
- **Data Management**: Reads and writes program data to and from files.

## Requirements

- Python 3.x
- `psutil` library (`pip install psutil`)

## Usage

1. **Prepare Data**: 
   - The first time you run the script, it will prompt you to enter program paths.
   - The data is saved in `run_programs/data.txt`.

2. **Run the Script**:
   - Executes the programs listed in `data.txt` if the state file `runs.txt` indicates it.

3. **Stop Programs**:
   - If the state file indicates "wait stop", it will stop the running programs.

## File Structure

- `data.txt`: Stores the program names and paths.
- `runs.txt`: Keeps track of the current state (`wait run` or `wait stop`).

## Example

To start the program manager:

```bash
python run_programms.py
```
