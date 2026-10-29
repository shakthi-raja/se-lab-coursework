"""Branch coverage test suite for marathon_registration module.

Specifically designed to evaluate and verify both True and False outcomes
for every decision branch, control structure, and compound conditional
in marathon_registration.py, achieving 100% branch coverage.
"""

import pytest
from marathon_registration import entry_fee, start_wave, finisher_status


# ============================================================================
# 1. Branch Coverage Tests: entry_fee
# ============================================================================

def test_entry_fee_branch_unknown_race():
    """Branch: race not in ENTRY_FEE -> True."""
    with pytest.raises(ValueError, match="unknown race"):
        entry_fee("ultra", 25, False, False)


def test_entry_fee_branch_age_under_12():
    """Branch: age < 12 -> True."""
    with pytest.raises(ValueError, match="too young"):
        entry_fee("5k", 10, False, False)


def test_entry_fee_branch_half_under_18():
    """Branch: race in ('half', 'full') [True] and age < 18 [True] -> True."""
    with pytest.raises(ValueError, match="too young for this distance"):
        entry_fee("half", 16, False, False)


def test_entry_fee_branch_full_under_18():
    """Branch: race == 'full' [True] and age < 18 [True] -> True."""
    with pytest.raises(ValueError, match="too young for this distance"):
        entry_fee("full", 17, False, False)


def test_entry_fee_branch_junior_5k_allowed():
    """Branch: race in ('half', 'full') [False] and age < 18 [True] -> False (permitted)."""
    # 5k is valid for age 12-17
    assert entry_fee("5k", 15, False, False) == 500


def test_entry_fee_branch_adult_half_allowed():
    """Branch: race in ('half', 'full') [True] and age < 18 [False] -> False (permitted)."""
    assert entry_fee("half", 25, False, False) == 1200


def test_entry_fee_branch_standard_no_discounts():
    """Branch: is_early_bird [False], age >= 65 [False], needs_tshirt [False]."""
    assert entry_fee("10k", 30, False, False) == 800


def test_entry_fee_branch_early_bird_only():
    """Branch: is_early_bird [True], age >= 65 [False], needs_tshirt [False]."""
    # 800 - 200 = 600
    assert entry_fee("10k", 30, True, False) == 600


def test_entry_fee_branch_senior_only():
    """Branch: is_early_bird [False], age >= 65 [True], needs_tshirt [False]."""
    # 1800 // 2 = 900
    assert entry_fee("full", 65, False, False) == 900


def test_entry_fee_branch_tshirt_only():
    """Branch: is_early_bird [False], age >= 65 [False], needs_tshirt [True]."""
    # 500 + 300 = 800
    assert entry_fee("5k", 30, False, True) == 800


def test_entry_fee_branch_all_modifiers_combined():
    """Branch: is_early_bird [True], age >= 65 [True], needs_tshirt [True]."""
    # Base 500 -> early-bird: 500 - 125 = 375 -> senior: 375 // 2 = 187 -> tshirt: 187 + 300 = 487
    assert entry_fee("5k", 70, True, True) == 487


# ============================================================================
# 2. Branch Coverage Tests: start_wave
# ============================================================================

def test_start_wave_branch_none_time():
    """Branch: best_time_minutes is None -> True -> Wave D."""
    assert start_wave(None, "full") == "D"


def test_start_wave_branch_full_wave_a():
    """Branch: race == 'full' [True], best_time_minutes * 4 <= cutoff * 3 [True] -> Wave A."""
    # cutoff 240; 180 * 4 = 720 <= 720 -> "A"
    assert start_wave(180, "full") == "A"


def test_start_wave_branch_full_wave_b():
    """Branch: race == 'full' [True], wave A [False], best_time_minutes <= cutoff [True] -> Wave B."""
    # cutoff 240; 200 * 4 = 800 > 720; 200 <= 240 -> "B"
    assert start_wave(200, "full") == "B"


def test_start_wave_branch_full_wave_c():
    """Branch: race == 'full' [True], wave A [False], wave B [False] -> Wave C."""
    # cutoff 240; 250 > 240 -> "C"
    assert start_wave(250, "full") == "C"


def test_start_wave_branch_other_wave_a():
    """Branch: race == 'full' [False] (cutoff 120), best_time * 4 <= 360 [True] -> Wave A."""
    # cutoff 120; 90 * 4 = 360 <= 360 -> "A"
    assert start_wave(90, "10k") == "A"


def test_start_wave_branch_other_wave_b():
    """Branch: race == 'full' [False] (cutoff 120), wave A [False], best_time <= 120 [True] -> Wave B."""
    # cutoff 120; 100 * 4 = 400 > 360; 100 <= 120 -> "B"
    assert start_wave(100, "half") == "B"


def test_start_wave_branch_other_wave_c():
    """Branch: race == 'full' [False] (cutoff 120), wave A [False], wave B [False] -> Wave C."""
    # cutoff 120; 130 > 120 -> "C"
    assert start_wave(130, "5k") == "C"


# ============================================================================
# 3. Branch Coverage Tests: finisher_status
# ============================================================================

def test_finisher_status_branch_checkpoint_missed():
    """Branch: checkpoints_missed > 0 -> True -> DSQ."""
    assert finisher_status(100, "10k", 2) == "DSQ"


def test_finisher_status_branch_full_finisher():
    """Branch: race == 'full' [True] (limit 360), elapsed <= limit [True] -> finisher."""
    assert finisher_status(360, "full", 0) == "finisher"


def test_finisher_status_branch_full_dnf():
    """Branch: race == 'full' [True] (limit 360), elapsed <= limit [False] -> DNF."""
    assert finisher_status(361, "full", 0) == "DNF"


def test_finisher_status_branch_half_finisher():
    """Branch: race == 'half' [True] (limit 180), elapsed <= limit [True] -> finisher."""
    assert finisher_status(180, "half", 0) == "finisher"


def test_finisher_status_branch_half_dnf():
    """Branch: race == 'half' [True] (limit 180), elapsed <= limit [False] -> DNF."""
    assert finisher_status(181, "half", 0) == "DNF"


def test_finisher_status_branch_other_finisher():
    """Branch: race == 'full' [False], race == 'half' [False] (limit 90), elapsed <= limit [True] -> finisher."""
    assert finisher_status(90, "5k", 0) == "finisher"


def test_finisher_status_branch_other_dnf():
    """Branch: race == 'full' [False], race == 'half' [False] (limit 90), elapsed <= limit [False] -> DNF."""
    assert finisher_status(91, "10k", 0) == "DNF"
