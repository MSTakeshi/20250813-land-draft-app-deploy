import random
from typing import Dict, List, Optional


class Voter:
    """
    Represents a voter in the land draft.

    Attributes:
        email (str): The voter's email address (used for identification).
        choice1 (int): The voter's first land choice (1-32).
        choice2 (int): The voter's second land choice (1-32).
        choice3 (int): The voter's third land choice (1-32).
        assigned_land (Optional[int]): The land assigned to the voter, if any.
        skipped_round (Optional[int]): The round the voter was skipped to, if any.
    """

    def __init__(
        self,
        name: str,
        choice1: int,
        choice2: int,
        choice3: int,
        assigned_land: Optional[int] = None,
    ):
        self.name = name
        self.choice1 = choice1
        self.choice2 = choice2
        self.choice3 = choice3
        self.assigned_land = assigned_land
        self.skipped_round = None

    def to_dict(self) -> Dict:
        """
        Converts the Voter object to a dictionary.
        """
        data = {
            "name": self.name,
            "choice1": self.choice1,
            "choice2": self.choice2,
            "choice3": self.choice3,
        }
        if self.assigned_land is not None:
            data["assigned_land"] = self.assigned_land
        return data


def run_draft(voters: List[Dict], seed: Optional[int] = None) -> Dict[str, List[Dict]]:
    """
    Runs the land draft algorithm through four rounds.

    Args:
        voters (List[Dict]): A list of dictionaries, each representing a voter
                             with 'email', 'choice1', 'choice2', and 'choice3'.
        seed (Optional[int]): An optional seed for the random number generator
                              to ensure reproducibility.

    Returns:
        Dict[str, List[Dict]]: A dictionary with keys 'round1', 'round2', 'round3', 'round4',
                               each containing a list of voter dictionaries with their assigned lands
                               at the end of that round.
    """
    if seed is not None:
        random.seed(seed)

    # Initialize voters as Voter objects
    voter_objects = [Voter(**voter_data) for voter_data in voters]

    # All possible lands (1 to 32)
    available_lands = set(range(1, 33))

    results = {
        "round1": [],
        "round2": [],
        "round3": [],
        "round4": [],
    }

    assigned_lands_this_round = set()

    # Round 1: choice1
    round1_participants = [v for v in voter_objects]

    # Group voters by their choice1
    choice1_groups = {}
    for voter in round1_participants:
        choice1_groups.setdefault(voter.choice1, []).append(voter)

    for choice, group in choice1_groups.items():
        if choice in available_lands:
            if len(group) == 1:
                # Unique choice, assign immediately
                voter = group[0]
                voter.assigned_land = choice
                assigned_lands_this_round.add(choice)
                available_lands.remove(choice)
            else:
                # Duplicated choice, random.choice winner
                winner = random.choice(group)
                winner.assigned_land = choice
                assigned_lands_this_round.add(choice)
                available_lands.remove(choice)
                # Losers go to next round (implicitly, by not being assigned)

    results["round1"] = [v.to_dict() for v in voter_objects]

    # Round 2: choice2
    round2_participants = [v for v in voter_objects if v.assigned_land is None]
    assigned_lands_this_round = set()  # Reset for this round's assignments

    choice2_groups = {}
    for voter in round2_participants:
        # Skip voters whose choice2 land was already awarded in Round 1
        if voter.choice2 in results["round1"] and any(
            v["assigned_land"] == voter.choice2 for v in results["round1"]
        ):
            voter.skipped_round = 3  # Send to Round 3
            continue
        choice2_groups.setdefault(voter.choice2, []).append(voter)

    for choice, group in choice2_groups.items():
        if choice in available_lands:
            if len(group) == 1:
                voter = group[0]
                voter.assigned_land = choice
                assigned_lands_this_round.add(choice)
                available_lands.remove(choice)
            else:
                winner = random.choice(group)
                winner.assigned_land = choice
                assigned_lands_this_round.add(choice)
                available_lands.remove(choice)

    results["round2"] = [v.to_dict() for v in voter_objects]

    # Round 3: choice3
    round3_participants = [v for v in voter_objects if v.assigned_land is None]
    assigned_lands_this_round = set()  # Reset for this round's assignments

    choice3_groups = {}
    for voter in round3_participants:
        # Skip voters whose choice3 land was awarded in Round 1 or 2
        if (
            voter.choice3 in results["round1"]
            and any(v["assigned_land"] == voter.choice3 for v in results["round1"])
            or voter.choice3 in results["round2"]
            and any(v["assigned_land"] == voter.choice3 for v in results["round2"])
        ):
            voter.skipped_round = 4  # Send to Round 4
            continue
        choice3_groups.setdefault(voter.choice3, []).append(voter)

    for choice, group in choice3_groups.items():
        if choice in available_lands:
            if len(group) == 1:
                voter = group[0]
                voter.assigned_land = choice
                assigned_lands_this_round.add(choice)
                available_lands.remove(choice)
            else:
                winner = random.choice(group)
                winner.assigned_land = choice
                assigned_lands_this_round.add(choice)
                available_lands.remove(choice)

    results["round3"] = [v.to_dict() for v in voter_objects]

    # Round 4: left-over random
    round4_participants = [v for v in voter_objects if v.assigned_land is None]

    random.shuffle(round4_participants)  # Randomize order of remaining voters
    remaining_lands_list = list(available_lands)
    random.shuffle(remaining_lands_list)  # Randomize order of remaining lands

    for i, voter in enumerate(round4_participants):
        if i < len(remaining_lands_list):
            voter.assigned_land = remaining_lands_list[i]
            available_lands.remove(remaining_lands_list[i])  # Remove assigned land

    results["round4"] = [v.to_dict() for v in voter_objects]

    return results
