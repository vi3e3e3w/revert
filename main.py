import random
import time
import os
import json
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPEEDRUN_FILE = os.path.join(BASE_DIR, "speedrun_records.json")

VERSION = "alpha 0.1.3"
ROUNDS = 10

MODE = {
    "Easy": 5,
    "Med": 6,
    "Less hard": 7,
    "Hard": 8,
    "Extremely difficult": 9
}

# =====================================
# SPEEDRUN SYSTEM
# =====================================

def load_speedrun_records():

    try:
        with open(SPEEDRUN_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return {}

    if not isinstance(data, dict):
        return {}

    return data


def save_speedrun_records(records):

    with open(SPEEDRUN_FILE, "w", encoding="utf-8") as file:
        json.dump(records, file, indent=2)


def format_time(seconds):

    minutes = int(seconds // 60)
    remaining = seconds - (minutes * 60)

    return f"{minutes:02d}:{remaining:05.2f}"


def update_speedrun_record(diff_name, elapsed, percent, full_combo):

    records = load_speedrun_records()
    entries = records.get(diff_name, [])

    if isinstance(entries, dict):
        entries = [entries]

    entries.sort(key=lambda record: record.get("time", float("inf")))
    previous_best = entries[0] if entries else None

    entry = {
        "time": elapsed,
        "percent": percent,
        "full_combo": full_combo
    }

    entries.append(entry)
    entries.sort(key=lambda record: record.get("time", float("inf")))
    records[diff_name] = entries[:5]
    save_speedrun_records(records)

    new_record = previous_best is None or elapsed < previous_best.get("time", float("inf"))

    return new_record, records[diff_name][0], records[diff_name]

# =====================================
# CLEAR SCREEN
# =====================================

def clear():
    command = "cls" if os.name == "nt" else "clear"
    subprocess.run([command], check=False)


def wait_return():

    input("Press Enter to return...")


def goodbye():

    clear()

    print("shutting down RE√(E)Rt...")
    time.sleep(1)

    print("saving memory...")
    time.sleep(1)

    print("return to terminal")
    time.sleep(1)

# =====================================
# INTRO
# =====================================

def intro():

    frames = [
        "00010011",
        "11101100",
        "v1001011",
        "v0110100",
        "vi001101",
        "vi110010",
        "vi301001",
        "vi3e1011",
        "vi3e1001",
        "vi3e3001",
        "vi3e3110",
        "vi3e3e31",
        "vi3e3e30",
        "vi3e3e3w",
        "vi3e3e3w",
        "vi3e3e3w G",
        "vi3e3e3w GA",
        "vi3e3e3w GAM",
        "vi3e3e3w GAME",
        "vi3e3e3w GAME",
        "Made By (odex",
        "Made by codex",
        "Made By (odex",
        "Made By codex",
        "Made By (odex",
        "Made by codex",
        "Made By (odex",
        "Made By codex",
        "Made By Codex (AI)"
    ]

    try:
        width = os.get_terminal_size().columns
    except OSError:
        width = 80

    width = max(width, len(frames[-1]) + 4)
    padding = max(0, (width - len(frames[-1])) // 2)

    for frame in frames:

        clear()
        print()
        print(" " * padding + frame)
        time.sleep(0.12)

    time.sleep(3.35)
    clear()

# =====================================
# INVERT BINARY
# =====================================

def invert_bits(binary):

    result = ""

    for bit in binary:

        if bit == "1":
            result += "0"

        else:
            result += "1"

    return result

# =====================================
# GRADE SYSTEM
# =====================================

def grade(percent, full_combo):

    if full_combo:
        return "A+ (Full Combo!)"

    elif percent >= 75:
        return "A"

    elif percent >= 65:
        return "B"

    elif percent >= 50:
        return "C"

    elif percent > 0:
        return "D"

    else:
        return "F"

# =====================================
# GAME
# =====================================

def ask_number(prompt, minimum, maximum):

    while True:

        try:
            value = int(input(prompt))
        except ValueError:
            print(f"Enter a number from {minimum} to {maximum}.")
            continue

        if minimum <= value <= maximum:
            return value

        print(f"Enter a number from {minimum} to {maximum}.")


def play_session(session_name, bit_length, rounds, save_records):

    max_score = bit_length * rounds

    progress = "0" * rounds
    round_scores = []
    mistake_review = []
    current_streak = 0
    max_streak = 0
    started_at = time.perf_counter()

    for round_num in range(1, rounds + 1):

        clear()

        binary = ""

        for _ in range(bit_length):
            binary += random.choice("01")

        answer = invert_bits(binary)

        # current x position
        display_progress = (
            progress[:round_num - 1]
            + "x"
            + progress[round_num:]
        )

        # dashboard
        print("------------------------------------------------")
        print(f"ROUND({round_num}/{rounds})   |  {display_progress}")
        print(f"MODE: {session_name}")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print()

        print("----     " + binary + "     ---")
        print()

        while True:

            user = input("+++      ").strip()

            if len(user) == bit_length and all(bit in "01" for bit in user):
                break

            print()
            print(f"INVALID INPUT: enter exactly {bit_length} bits using only 0 and 1.")
            print()

        print()

        check_line = ""
        correct_count = 0

        for i in range(bit_length):

            if i < len(user) and user[i] == answer[i]:

                check_line += "✓"
                correct_count += 1

            else:

                check_line += "×"

        print("#########" + check_line + "##########")

        round_scores.append(correct_count)

        # update progress
        if correct_count == bit_length:
            current_streak += 1
            max_streak = max(max_streak, current_streak)

            progress = (
                progress[:round_num - 1]
                + "C"
                + progress[round_num:]
            )

        else:
            current_streak = 0
            mistake_review.append({
                "round": round_num,
                "binary": binary,
                "input": user,
                "answer": answer,
                "score": correct_count
            })

            progress = (
                progress[:round_num - 1]
                + str(correct_count)
                + progress[round_num:]
            )

        print()
        print("CORRECT:", answer)
        print("BIT SCORE:", correct_count)
        print("STREAK:", current_streak)

        time.sleep(2)

    # =====================================

    # FINAL RESULT
    # =====================================

    clear()

    score = sum(round_scores)

    if len(round_scores) > 0:

        formula_score = (
            rounds
            * ((round_scores[0] + round_scores[-1]) / 2)
        )

    else:

        formula_score = 0

    percent = (score / max_score) * 100

    full_combo = score == max_score

    rank = grade(percent, full_combo)
    elapsed = time.perf_counter() - started_at

    if save_records:
        new_record, best_record, top_records = update_speedrun_record(session_name, elapsed, percent, full_combo)
    else:
        new_record, best_record, top_records = False, None, []

    print("======================================")
    print("       RE√(E)Rt COMPLETE")
    print("======================================")
    print()

    print("PROGRESS :", progress + "x")
    print()

    print("TOTAL SCORE :", score, "/", max_score)
    print(f"PERCENT     : {percent:.1f}%")
    print(f"FORMULA     : {formula_score:.1f}")
    print(f"TIME        : {format_time(elapsed)}")
    print(f"MAX STREAK  : {max_streak}")

    if best_record:
        print(f"BEST TIME   : {format_time(best_record['time'])}")

    print()
    print("RANK:", rank)
    print()

    if save_records and new_record:

        print("SPEEDRUN: NEW PERSONAL BEST")

    elif save_records:

        print("SPEEDRUN: PB UNCHANGED")

    else:

        print("PRACTICE: RECORD NOT SAVED")

    print()

    if mistake_review:

        print("MISTAKE REVIEW:")

        for mistake in mistake_review:

            print(
                f"R{mistake['round']:02d}: "
                f"{mistake['binary']} -> {mistake['answer']} | "
                f"YOU: {mistake['input']} | "
                f"{mistake['score']}/{bit_length}"
            )

        print()

    if save_records:

        print("TOP 5:")

        for index, record in enumerate(top_records, start=1):

            label = "FC" if record.get("full_combo") else f"{record.get('percent', 0):.1f}%"
            print(f"{index}. {format_time(record['time'])}  {label}")

        print()


    if full_combo:

        print("STATUS: FULL CLEAR ")

    elif percent >= 75:

        print("STATUS: CASIO GOD ")

    elif percent >= 50:

        print("STATUS: TERMINAL USER ")

    else:

        print("STATUS: HUMAN ERROR ")

    print()

    input("Press Enter to return...")


def play_game(diff_name):

    play_session(diff_name, MODE[diff_name], ROUNDS, True)


def practice_mode():

    clear()

    print("======================================")
    print("            PRACTICE MODE")
    print("======================================")
    print()

    bit_length = ask_number("BIT LENGTH (3-16) > ", 3, 16)
    rounds = ask_number("ROUNDS (1-20) > ", 1, 20)

    play_session("Practice", bit_length, rounds, False)


def about_screen():

    clear()

    print("======================================")
    print("                ABOUT")
    print("======================================")
    print()

    print("RE√(E)Rt")
    print(f"Version: {VERSION}")
    print()

    print("A terminal game about flipping binary bits.")
    print("The goal is simple: convert every 0 to 1 and every 1 to 0.")
    print()

    print("Made as a learning project.")
    print("Still alpha, so expect rough edges.")
    print()

    wait_return()

# =====================================
# MAIN MENU
# =====================================

try:

    clear()

    print("""=========================================================
                        WARNING!
        This game is still an alpha version.
        Expect some bugs and crashes.
        Please report any issues to the developer.
=========================================================""")
    print()

    input("Press Enter to continue ...")

    intro()

    while True:

        clear()

        print(f"""=========================================================
                        RE√(E)Rt
             Convert the binary is never boring                          
 {VERSION} =============================================""")
        print()

        print("[1] PLAY GAME")
        print("[2] HTP")
        print("[3] SPEEDRUN RECORDS")
        print("[4] PRACTICE MODE")
        print("[5] ABOUT")
        print("[6] EXIT")

        print()

        choice = input("SELECT > ")

        # =====================================
        # PLAY
        # =====================================

        if choice == "1":

            while True:

                clear()

                print("======================================")
                print("          SELECT DIFFICULTY")
                print("======================================")
                print()

                print("[1] EASY")
                print("[2] MED")
                print("[3] LESS HARD")
                print("[4] HARD")
                print("[5] EXTREMELY DIFFICULT")
                print("[6] BACK")

                print()

                diff = input("SELECT > ")

                if diff == "1":

                    play_game("Easy")
                    break

                elif diff == "2":

                    play_game("Med")
                    break

                elif diff == "3":

                    play_game("Less hard")
                    break

                elif diff == "4":

                    play_game("Hard")
                    break

                elif diff == "5":

                    play_game("Extremely difficult")
                    break

                elif diff == "6":

                    break

                else:

                    print()
                    print("Unknown error:404")
                    time.sleep(1)

        # =====================================
        # HOW TO PLAY
        # =====================================

        elif choice == "2":

            clear()

            print("======================================")
            print("             HOW TO PLAY")
            print("======================================")
            print()

            print("Convert all bits to opposite form.")
            print()

            print("0 -> 1")
            print("1 -> 0")

            print()

            print("EXAMPLE:")
            print()

            print("101001")
            print("010110")

            print()

            print("C = FULL CLEAR")
            print("x = CURRENT ROUND")

            print()

            print("Invalid input is not counted.")
            print("Practice mode lets you choose bit length and rounds.")
            print("Speedrun records keep local top 5 per difficulty.")
            print()

            print("RANK SYSTEM:")
            print("A+ = FULL COMBO")
            print("A  = 75%+")
            print("B  = 65%+")
            print("C  = 50%+")
            print("D  = 1% - 49.9%")
            print("F  = 0%")

            print()

            wait_return()

        # =====================================
        # SPEEDRUN RECORDS
        # =====================================

        elif choice == "3":

            clear()

            print("======================================")
            print("          SPEEDRUN RECORDS")
            print("======================================")
            print()

            records = load_speedrun_records()

            if not records:

                print("No records yet.")

            else:

                for diff_name in MODE:

                    entries = records.get(diff_name, [])

                    if isinstance(entries, dict):
                        entries = [entries]

                    print(diff_name)

                    if entries:

                        for index, record in enumerate(entries[:5], start=1):

                            label = "FC" if record.get("full_combo") else f"{record.get('percent', 0):.1f}%"
                            print(f"  {index}. {format_time(record['time'])}  {label}")

                    else:

                        print("  --:--.--")

                    print()

            print()
            wait_return()

        # =====================================
        # PRACTICE MODE
        # =====================================

        elif choice == "4":

            practice_mode()

        # =====================================
        # ABOUT
        # =====================================

        elif choice == "5":

            about_screen()

        # =====================================
        # EXIT
        # =====================================

        elif choice == "6":

            goodbye()
            break

        # =====================================
        # INVALID
        # =====================================

        else:

            print()
            print("404")
            time.sleep(2.3)

except KeyboardInterrupt:

    print()
    goodbye()
