import sys
from league import League

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <teams.csv> <opponents_length>")
        sys.exit(1)

    # Get team data file path from command line argument
    team_data_file = sys.argv[1]

    try:
        opponents_length = int(sys.argv[2])
    except Exception:
        print("Opponents length command arg must be an integer")
        sys.exit(1)

    league = League(team_data_file, opponents_length)
    schedule = league.generate_schedule()
    league.write_schedule("schedule.txt", schedule)
    league.write_matchups("matchups.txt")

    print("Schedule generated and written to schedule.txt")
