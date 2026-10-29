"""Code coverage test suite for marathon_registration module.

Designed to execute every statement in marathon_registration.py
to achieve 100% line (statement) coverage.
"""

import pytest
from marathon_registration import entry_fee, start_wave, finisher_status


# --- Tests for entry_fee statement execution ---

def test_entry_fee_standard():
    """Verify standard entry fee calculation without discounts or addons."""
    assert entry_fee("10k", 30, False, False) == 800


def test_entry_fee_unknown_race():
    """Verify ValueError is raised when an unsupported race distance is supplied."""
    with pytest.raises(ValueError, match="unknown race"):
        entry_fee("ultra", 30, False, False)


def test_entry_fee_age_under_12():
    """Verify ValueError is raised when runner age is under 12."""
    with pytest.raises(ValueError, match="too young"):
        entry_fee("5k", 10, False, False)


def test_entry_fee_distance_under_18():
    """Verify ValueError is raised when under-18 runner enters half/full marathon."""
    with pytest.raises(ValueError, match="too young for this distance"):
        entry_fee("half", 16, False, False)


def test_entry_fee_early_bird():
    """Verify 25% discount is applied for early-bird registration."""
    # 800 - (800 // 4) = 600
    assert entry_fee("10k", 30, True, False) == 600


def test_entry_fee_senior():
    """Verify 50% discount is applied for senior runners (>= 65)."""
    # 1800 // 2 = 900
    assert entry_fee("full", 68, False, False) == 900


def test_entry_fee_needs_tshirt():
    """Verify Rs. 300 addon is added when t-shirt is requested."""
    # 500 + 300 = 800
    assert entry_fee("5k", 25, False, True) == 800


# --- Tests for start_wave statement execution ---

def test_start_wave_unseeded():
    """Verify runners with no qualifying time are placed in wave D."""
    assert start_wave(None, "full") == "D"


def test_start_wave_full_wave_a():
    """Verify full marathon runners meeting <= 75% cutoff are placed in wave A."""
    # cutoff 240; 170 * 4 <= 720 -> True -> "A"
    assert start_wave(170, "full") == "A"


def test_start_wave_other_wave_b():
    """Verify non-full marathon runners within cutoff are placed in wave B."""
    # cutoff 120; 100 * 4 = 400 > 360; 100 <= 120 -> "B"
    assert start_wave(100, "10k") == "B"


def test_start_wave_other_wave_c():
    """Verify non-full marathon runners exceeding cutoff are placed in wave C."""
    # cutoff 120; 130 > 120 -> "C"
    assert start_wave(130, "5k") == "C"


# --- Tests for finisher_status statement execution ---

def test_finisher_status_disqualified():
    """Verify runner is marked DSQ when checkpoints are missed."""
    assert finisher_status(50, "10k", 1) == "DSQ"


def test_finisher_status_full_finisher():
    """Verify full marathon runner finishing within 360 minutes is marked finisher."""
    assert finisher_status(350, "full", 0) == "finisher"


def test_finisher_status_half_finisher():
    """Verify half marathon runner finishing within 180 minutes is marked finisher."""
    assert finisher_status(170, "half", 0) == "finisher"


def test_finisher_status_other_dnf():
    """Verify 5k/10k runner exceeding 90 minute limit is marked DNF."""
    assert finisher_status(105, "10k", 0) == "DNF"
