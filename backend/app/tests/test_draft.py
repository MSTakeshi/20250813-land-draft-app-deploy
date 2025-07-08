from app.services.draft import run_draft


def test_run_draft_deterministic_assignment():
    """
    Tests the run_draft function for deterministic assignment with a fixed seed,
    correct round progression, and skip behavior.
    """
    voters = [
        {"email": "voter1@example.com", "choice1": 1, "choice2": 2, "choice3": 3},
        {"email": "voter2@example.com", "choice1": 1, "choice2": 4, "choice3": 5},
        {"email": "voter3@example.com", "choice1": 2, "choice2": 1, "choice3": 6},
        {"email": "voter4@example.com", "choice1": 3, "choice2": 7, "choice3": 8},
        {"email": "voter5@example.com", "choice1": 4, "choice2": 9, "choice3": 10},
    ]

    # Run draft with a fixed seed
    results = run_draft(voters, seed=42)

    # Assertions for Round 1
    # With seed=42, voter1 should win land 1 in round 1
    # voter2 should go to round 2
    round1_results = {v["email"]: v["assigned_land"] for v in results["round1"]}
    assert round1_results["voter1@example.com"] == 1
    assert round1_results["voter2@example.com"] is None
    assert round1_results["voter3@example.com"] == 2
    assert round1_results["voter4@example.com"] == 3
    assert round1_results["voter5@example.com"] == 4

    # Assertions for Round 2
    # voter2's choice2 (land 4) was taken by voter5 in round 1, so voter2 should skip to round 3
    round2_results = {v["email"]: v["assigned_land"] for v in results["round2"]}
    assert round2_results["voter1@example.com"] == 1
    assert (
        round2_results["voter2@example.com"] is None
    )  # Still None, skipped to round 3
    assert round2_results["voter3@example.com"] == 2
    assert round2_results["voter4@example.com"] == 3
    assert round2_results["voter5@example.com"] == 4

    # Assertions for Round 3
    # voter2 should get land 5 (choice3)
    round3_results = {v["email"]: v["assigned_land"] for v in results["round3"]}
    assert round3_results["voter1@example.com"] == 1
    assert round3_results["voter2@example.com"] == 5
    assert round3_results["voter3@example.com"] == 2
    assert round3_results["voter4@example.com"] == 3
    assert round3_results["voter5@example.com"] == 4

    # Assertions for Round 4 (should be no participants if all assigned in previous rounds)
    round4_results = {v["email"]: v["assigned_land"] for v in results["round4"]}
    assert round4_results["voter1@example.com"] == 1
    assert round4_results["voter2@example.com"] == 5
    assert round4_results["voter3@example.com"] == 2
    assert round4_results["voter4@example.com"] == 3
    assert round4_results["voter5@example.com"] == 4


def test_all_lands_unique_and_assigned():
    """
    Tests that all assigned lands are unique and within the valid range (1-32).
    """
    # Create 32 voters, each with unique choices to ensure all lands are assigned
    voters = []
    for i in range(1, 33):
        voters.append(
            {
                "email": f"voter{i}@example.com",
                "choice1": i,
                "choice2": (i % 32) + 1,
                "choice3": ((i + 1) % 32) + 1,
            }
        )

    results = run_draft(voters, seed=123)  # Use a different seed for this test

    final_assignments = [
        v["assigned_land"] for v in results["round4"] if v["assigned_land"] is not None
    ]

    # All 32 voters should have been assigned a land
    assert len(final_assignments) == 32

    # All assigned lands should be unique
    assert len(set(final_assignments)) == 32

    # All assigned lands should be within the range 1-32
    for land in final_assignments:
        assert 1 <= land <= 32
