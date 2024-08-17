class Team:
    def __init__(self, name: str, rank: int, opponents_length: int):
        self.name = name
        self.rank = rank
        self.opponents_length = opponents_length
        self.played_opponents = set()

    def __str__(self):
        return f"{self.name} (Rank: {self.rank})"

    def can_play(self, other_team):
        return (
            other_team not in self.played_opponents
            and self != other_team
            and len(self.played_opponents) < self.opponents_length
            and len(other_team.played_opponents) < self.opponents_length
        )