import os
import psutil


def stop(programs: list[str]) -> None:
    """Stops the programs in the list. Forcefully terminates the process if it cannot be terminated normally."""
    for proc in psutil.process_iter():
        try:
            if proc.name().lower() in programs:
                proc.terminate()  # Attempt to terminate the process
                proc.wait(3)  # Wait for 3 seconds
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
        except psutil.TimeoutExpired:  # If the process did not terminate within 3 seconds
            try:
                proc.kill()  # Forcefully terminate the process
                print(f"Process {proc.name()} was forcefully terminated.")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue


def run(programs_path: list[str]) -> None:
    """Launches programs from the list of paths."""
    for path in programs_path:
        if os.path.isfile(path):
            os.startfile(path)
        else:
            print(f"File not found: {path}")


def parse_program_data(file_path: str) -> tuple[list[str], list[str]]:
    """Parses program data from a file."""
    programs = []
    programs_path = []
    with open(file_path, "r") as data:
        lines = data.readlines()
        for i in range(0, len(lines), 2):
            programs.append(lines[i].strip())
            programs_path.append(lines[i + 1].strip())
    return programs, programs_path


def collect_programs_from_user(data_file: str) -> tuple[list[str], list[str]]:
    """Prompts the user for program paths and saves them to a file."""
    programs = []
    programs_path = []
    n = int(input("Enter the number of programs: "))
    with open(data_file, "w") as data:
        for _ in range(n):
            path = input("Enter the absolute (full) path to the program: ").strip()
            programs_path.append(path)
            prg = os.path.basename(path)  # Get the filename from the path
            programs.append(prg)
            data.write(f"{prg}\n{path}\n")
    return programs, programs_path


def main() -> None:
    """Main function of the program."""
    # Get the path to the folder where the script is located
    base_dir = ''
    run_programs_dir = os.path.join(base_dir, "run_programs")

    # File paths
    program_data_path = os.path.join(run_programs_dir, "data.txt")
    run_state_file = os.path.join(run_programs_dir, "runs.txt")

    # Create the folder if it doesn't exist
    if not os.path.isdir(run_programs_dir):
        os.mkdir(run_programs_dir)

    programs_path = []
    programs = []

    # Read or prompt for program data
    if os.path.isfile(program_data_path):
        programs, programs_path = parse_program_data(program_data_path)
    else:
        programs, programs_path = collect_programs_from_user(program_data_path)

    # Manage program launching and stopping
    if os.path.isfile(run_state_file):
        with open(run_state_file, "r+") as file:
            state = file.read().strip()
            if state == "wait run":
                run(programs_path)
                file.seek(0)
                file.write("wait stop")
            elif state == "wait stop":
                stop(programs)
                file.seek(0)
                file.write("wait run")
            file.truncate()
    else:
        with open(run_state_file, "w") as file:
            file.write("wait stop")
        run(programs_path)


if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        print("Import error:", e)
    except Exception as e:
        print("An error occurred:", e)
