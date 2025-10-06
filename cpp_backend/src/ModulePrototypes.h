#pragma once

#include <string>
#include <vector>
#include <map>
#include "Geometry.h"

namespace Optimizer {

// Enum to define module categories for adjacency rules
// This is now defined in Geometry.h, but kept here for context.
// enum class ModuleCategory { ... };

// Structure to define a module "template" from which actual modules can be instantiated
struct ModulePrototype {
    int id;
    std::string name;
    std::string function;
    double min_volume;
    // Dimensions in meters
    double length; 
    double width;
    double height;
    ModuleCategory category;
};

// Creates and returns a library of all available module prototypes
inline std::map<int, ModulePrototype> get_module_prototypes() {
    std::map<int, ModulePrototype> prototypes;

    // Data derived from user's spreadsheets (inches converted to meters where applicable)
    // Using a mix of specified minimums and logical sizes for demonstration.
    // ID, Name, Function, Min Volume (m^3), L, W, H (m), Category

    prototypes[1] = {1, "Private_Quarters", "Sleep, Relaxation", 
                     17.4, 2.0, 2.5, 3.5, ModuleCategory::QUIET};

    prototypes[2] = {2, "Washroom", "Hygiene", 
                     4.35, 1.5, 1.5, 2.2, ModuleCategory::DIRTY};

    prototypes[3] = {3, "Galley", "Food Prep", 
                     3.3, 2.0, 1.5, 2.2, ModuleCategory::CLEAN};

    prototypes[4] = {4, "Gym", "Exercise", 
                     7.64, 2.5, 2.0, 2.5, ModuleCategory::NOISY};

    prototypes[5] = {5, "Waste_Management", "Waste Collection", 
                     2.36, 1.2, 1.2, 2.0, ModuleCategory::DIRTY};

    prototypes[6] = {6, "Work_Area", "Lab/Science", 
                     4.82, 2.5, 2.0, 2.2, ModuleCategory::NEUTRAL};
                     
    prototypes[7] = {7, "Medical_Bay", "Medical Care", 
                     5.8, 2.5, 2.0, 2.2, ModuleCategory::CLEAN};

    return prototypes;
}

// Helper function to instantiate a HabitatObject from a prototype
inline HabitatObject create_module_from_prototype(const ModulePrototype& proto) {
    HabitatObject obj;
    obj.name = proto.name;
    obj.scale = glm::vec3(proto.width, proto.length, proto.height); // Using width for x, length for y
    obj.category = proto.category;
    return obj;
}

} // namespace Optimizer
