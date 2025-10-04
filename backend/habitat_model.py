# backend/habitat_model.py

class Habitat:
    """
    Represents the core data model for the lunar habitat,
    storing crew size, mission duration, and a list of modules.
    """
    def __init__(self, crew_size: int, mission_days: int):
        self._crew_size = crew_size
        self._mission_days = mission_days
        self.modules = []
        print(f"Habitat initialized: Crew={crew_size}, Days={mission_days}")

    def get_crew_size(self) -> int:
        """Returns the current crew size."""
        return self._crew_size
    
    def add_module(self, module_name: str):
        """Adds a module to the habitat structure."""
        self.modules.append(module_name)
        print(f"Module '{module_name}' added. Total modules: {len(self.modules)}")

    def __repr__(self):
        return f"Habitat(Crew={self._crew_size}, Modules={len(self.modules)})"