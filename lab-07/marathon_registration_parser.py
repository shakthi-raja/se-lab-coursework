def format_bib_name(name):
    """Upper-cases a runner's name and cuts it to 12 characters for the bib.

    Handles non-string, None, and empty inputs gracefully without crashing.
    """
    if not isinstance(name, str):
        return ""
    return name.strip().upper()[:12]


def parse_finish_time(text):
    """Converts a finish time written as H:MM:SS into seconds.

    Handles non-string, malformed, negative, or invalid format inputs
    gracefully without crashing, returning None when parsing cannot be completed.
    """
    if not isinstance(text, str):
        return None
    try:
        parts = text.split(":")
        if len(parts) != 3:
            return None
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])
        if hours < 0 or minutes < 0 or seconds < 0:
            return None
        return hours * 3600 + minutes * 60 + seconds
    except (ValueError, TypeError):
        return None


def average_split(text):
    """Averages split times given in minutes, separated by spaces.

    Handles non-string, empty, non-numeric, or malformed inputs
    gracefully without crashing, returning None when splits cannot be calculated.
    """
    if not isinstance(text, str):
        return None
    try:
        tokens = text.split()
        if not tokens:
            return None
        splits = [int(s) for s in tokens]
        if not splits:
            return None
        return sum(splits) / len(splits)
    except (ValueError, TypeError, ZeroDivisionError):
        return None


def main():
    print("==== Running format_bib_name ====")
    value = input("Enter the name to print on the bib: ")
    print("Bib name:", format_bib_name(value))

    print("\n==== Running parse_finish_time ====")
    value = input("Enter a finish time as H:MM:SS (e.g. 3:45:10): ")
    print("Finish time in seconds:", parse_finish_time(value))

    print("\n==== Running average_split ====")
    value = input(
        "Enter your 5 km split times in minutes separated by spaces (e.g. 25 26 24): "
    )
    print("Average split (minutes):", average_split(value))


if __name__ == "__main__":
    main()
