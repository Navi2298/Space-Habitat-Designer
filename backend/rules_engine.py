from typing import TYPE_CHECKING

# To avoid circular imports, use TYPE_CHECKING for type hints
if TYPE_CHECKING:
    from backend.habitat_model import Habitat

# Requirement based on the challenge: minimum volume needed per person
# This is a constant we can change later!
MIN_VOLUME_PER_CREW = 5.0  # m³ per crew member

def check_volume_constraint(habitat: 'Habitat') -> str:
    """
    Validates if the habitat volume is sufficient for the crew size and mission.
    Returns a status message (PASS or WARNING).
    """
    required_volume = habitat.get_crew_size() * MIN_VOLUME_PER_CREW
    current_volume = habitat.get_total_volume()

    if current_volume < required_volume:
        # If the volume is too small, issue a warning
        return f"WARNING: Volume ({current_volume:.1f} m³) is too small! Requires {required_volume:.1f} m³ for {habitat.get_crew_size()} crew."
    else:
        # If the volume is sufficient
        return "PASS: Volume is sufficient for current crew requirements."
