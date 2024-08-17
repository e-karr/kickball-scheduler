import pandas as pd
import random
from team import Team

class League:
    def __init__(self, team_data_file, opponents_length):
        self.opponents_length = opponents_length
        self.teams = self.load_teams(team_data_file)

    def load_teams(self, file_path) -> list[Team]:
        print("Loading teams and rankings")

        df = pd.read_csv(file_path)
        teams = [Team(row["Team"], row["Rank"], self.opponents_length) for _, row in df.iterrows()]

        print("Successfully loaded teams and ranks")
        return teams

    def schedule_group_games(self):
        print("Selecting immediate rank matchups")
        # Group teams into sets of 6 based on rank
        groups = [self.teams[i : i + 6] for i in range(0, len(self.teams), 6)]

        # Schedule games within each group (round-robin)
        for group in groups:
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    group[i].played_opponents.add(group[j])
                    group[j].played_opponents.add(group[i])
                    yield (group[i], group[j])

    def weighted_random_matchup(self, team: Team):
        # Define weights based on rank difference and played opponents
        weights = [0 if opponent in team.played_opponents else (37 - abs(team.rank - i)) / 36 for i, opponent in enumerate(self.teams, 1)]

        while True:
            try:
                # Choose a random opponent with weighted probability
                opponent_rank: int = random.choices(range(1, 37), weights=weights)[0]
                opponent: Team = next(t for t in self.teams if t.rank == opponent_rank and team.can_play(t))

                team.played_opponents.add(opponent)
                opponent.played_opponents.add(team)
                return team, opponent
            except StopIteration:
                # Shuffle teams for potential different results
                random.shuffle(self.teams)

    def schedule_remaining_games(self):
        print("Selecting weighted random matchups")
        while any(len(team.played_opponents) < self.opponents_length for team in self.teams):
            for team in sorted(self.teams, key=lambda t: len(t.played_opponents)):
                if len(team.played_opponents) < self.opponents_length:
                    team1, team2 = self.weighted_random_matchup(team)
                    yield (team1, team2)

    def generate_schedule(self):
        while True:
            all_matchups = list(self.schedule_group_games()) + list(self.schedule_remaining_games())
            random.shuffle(all_matchups)

            print("Generating weekly schedule")

            weekly_schedule = []
            for _ in range(self.opponents_length):
                week_matchups = []
                used_teams = set()
                for matchup in all_matchups:
                    team1, team2 = matchup
                    if team1 not in used_teams and team2 not in used_teams:
                        week_matchups.append(matchup)
                        used_teams.add(team1)
                        used_teams.add(team2)
                weekly_schedule.append(week_matchups)
                all_matchups = [matchup for matchup in all_matchups if matchup not in week_matchups]

            # Check if the schedule is valid
            if all(len(set(team for matchup in week for team in matchup)) == 18 for week in weekly_schedule):
                print("Successfully generated weekly schedule")
                return weekly_schedule

    def write_schedule(self, filename, schedule):
        print("Writing schedule")
        with open(filename, "w") as f:
            for week, games in enumerate(schedule):
                f.write(f"Week {week + 1}:\n")
                for matchup in games:
                    f.write(f"\t{matchup[0]} vs {matchup[1]}\n")
                f.write("\n")

    def write_matchups(self, filename):
        print("Writing matchups")
        with open(filename, "w") as f:
            for team in self.teams:
                f.write(f"{team.name}:\n")
                for opponent in team.played_opponents:
                    f.write(f"\t{opponent.name} (Rank: {opponent.rank})\n")
                f.write("\n")