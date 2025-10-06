#include <iostream>
#include <vector>
#include <string>

// You will need to download this header-only library for JSON processing.
// Place it in the 'dependencies' folder.
#include <nlohmann/json.hpp>

#include "Geometry.h"
#include "Optimizer.h"
#include "ModulePrototypes.h" // Include the new module library

using json = nlohmann::json;

// Part 2: Intelligent Module Generation
std::vector<HabitatObject> select_modules_for_mission(int crew_size, const std::map<int, Optimizer::ModulePrototype>& prototypes) {
    std::vector<HabitatObject> selected_modules;

    // Core modules always included
    selected_modules.push_back(Optimizer::create_module_from_prototype(prototypes.at(3))); // Galley
    selected_modules.push_back(Optimizer::create_module_from_prototype(prototypes.at(4))); // Gym
    selected_modules.push_back(Optimizer::create_module_from_prototype(prototypes.at(5))); // Waste Management
    selected_modules.push_back(Optimizer::create_module_from_prototype(prototypes.at(6))); // Work Area
    selected_modules.push_back(Optimizer::create_module_from_prototype(prototypes.at(7))); // Medical Bay

    // Add modules based on crew size
    int num_private_quarters = std::max(1, crew_size / 2);
    for (int i = 0; i < num_private_quarters; ++i) {
        selected_modules.push_back(Optimizer::create_module_from_prototype(prototypes.at(1)));
    }

    int num_washrooms = std::max(1, crew_size / 4);
    for (int i = 0; i < num_washrooms; ++i) {
        selected_modules.push_back(Optimizer::create_module_from_prototype(prototypes.at(2)));
    }
    
    // Assign unique names
    std::map<std::string, int> name_counts;
    for (auto& mod : selected_modules) {
        name_counts[mod.name]++;
        if (name_counts[mod.name] > 1) {
            mod.name += "_" + std::to_string(name_counts[mod.name] -1);
        }
    }

    return selected_modules;
}


// Helper function to organize modules into levels
struct Level {
    float min_z;
    float max_z;
    std::vector<size_t> module_indices;
};

std::vector<Level> organize_into_levels(const std::vector<HabitatObject>& layout, float level_height = 2.5f) {
    std::vector<Level> levels;
    
    // Find the overall z-range of the habitat
    float min_z = std::numeric_limits<float>::max();
    float max_z = std::numeric_limits<float>::lowest();
    
    for (const auto& obj : layout) {
        min_z = std::min(min_z, obj.position.z - obj.scale.z / 2.0f);
        max_z = std::max(max_z, obj.position.z + obj.scale.z / 2.0f);
    }
    
    // Create levels
    int num_levels = std::ceil((max_z - min_z) / level_height);
    levels.resize(num_levels);
    
    // Initialize level boundaries
    for (int i = 0; i < num_levels; i++) {
        levels[i].min_z = min_z + i * level_height;
        levels[i].max_z = min_z + (i + 1) * level_height;
    }
    
    // Assign modules to levels
    for (size_t i = 0; i < layout.size(); i++) {
        const auto& obj = layout[i];
        float obj_center_z = obj.position.z;
        
        // Find which level(s) this module belongs to
        for (auto& level : levels) {
            if (obj_center_z >= level.min_z && obj_center_z < level.max_z) {
                level.module_indices.push_back(i);
                break;  // Assign to only one level based on center position
            }
        }
    }
    
    return levels;
}

json level_to_json(const Level& level, const std::vector<HabitatObject>& layout) {
    json level_json;
    level_json["min_z"] = level.min_z;
    level_json["max_z"] = level.max_z;
    
    json modules = json::array();
    for (size_t idx : level.module_indices) {
        const auto& obj = layout[idx];
        json module_json;
        module_json["index"] = idx;
        module_json["name"] = obj.name;
        module_json["position"] = {
            {"x", obj.position.x},
            {"y", obj.position.y},
            {"z", obj.position.z}
        };
        module_json["scale"] = {
            {"x", obj.scale.x},
            {"y", obj.scale.y},
            {"z", obj.scale.z}
        };
        module_json["category"] = [&obj]() {
            switch (obj.category) {
                case ModuleCategory::CLEAN: return "CLEAN";
                case ModuleCategory::DIRTY: return "DIRTY";
                case ModuleCategory::QUIET: return "QUIET";
                case ModuleCategory::NOISY: return "NOISY";
                default: return "NEUTRAL";
            }
        }();
        modules.push_back(module_json);
    }
    level_json["modules"] = modules;
    
    return level_json;
}

// Helper function to convert violations to JSON
json violations_to_json(const std::vector<Violation>& violations) {
    json violations_json = json::array();
    
    for (const auto& v : violations) {
        json violation;
        violation["type"] = [&]() {
            switch (v.type) {
                case Violation::Type::COLLISION: return "COLLISION";
                case Violation::Type::BOUNDS: return "BOUNDS";
                case Violation::Type::ADJACENCY_CLEAN_DIRTY: return "ADJACENCY_CLEAN_DIRTY";
                case Violation::Type::ADJACENCY_QUIET_NOISY: return "ADJACENCY_QUIET_NOISY";
                default: return "UNKNOWN";
            }
        }();
        violation["object1"] = v.object1Index;
        violation["object2"] = v.object2Index;
        violation["description"] = v.description;
        violation["severity"] = v.severity;
        violations_json.push_back(violation);
    }
    
    return violations_json;
}

int main() {
    // 1. Read all input from stdin
    std::string input_str;
    std::string line;
    while (std::getline(std::cin, line)) {
        input_str += line;
    }

    // 2. Parse the input JSON
    json input_json;
    try {
        input_json = json::parse(input_str);
    } catch (json::parse_error& e) {
        // If parsing fails, output an error JSON and exit
        json error_output;
        error_output["status"] = "error";
        error_output["message"] = "Failed to parse input JSON: " + std::string(e.what());
        std::cout << error_output.dump(4) << std::endl;
        return 1;
    }

    // 3. Configure the simulation from the input JSON
    int crew_size = input_json["habitat"]["crew_size"];
    int mission_days = input_json["habitat"]["mission_days"];
    std::string material = input_json["habitat"]["habitat_material"];

    // Get the module library
    auto module_prototypes = Optimizer::get_module_prototypes();

    // Create an initial layout based on parameters
    std::vector<HabitatObject> initial_layout = select_modules_for_mission(crew_size, module_prototypes);


    // 4. Run the optimization process with violation tracking
    ViolationTracker violation_tracker;
    std::vector<HabitatObject> final_layout = Optimizer::findBestLayout(initial_layout, 500);
    
    // Evaluate the final layout to get violations
    std::vector<double> weights = {1.0}; // Default weights
    Evaluator::evaluateLayout(final_layout, weights, &violation_tracker);

    // NOTE: Off-screen rendering would happen here.
    // This was a placeholder and is no longer needed, as the frontend will draw the SVG.
    // std::string generated_image_path = "/Images/modern-space-habitat-with-cosmic-view.jpg.jpg"; 

    // 5. Serialize the results to an output JSON
    json output_json;
    output_json["status"] = "success";
    
    // Create a description
    output_json["description"] = "A " + material + " habitat for " + std::to_string(crew_size) + 
                                 " crew on a " + std::to_string(mission_days) + "-day mission. " +
                                 "Layout optimized using Particle Swarm Optimization.";

    // Organize modules into levels
    auto levels = organize_into_levels(final_layout);
    
    // Add level data to output
    json levels_json = json::array();
    for (const auto& level : levels) {
        levels_json.push_back(level_to_json(level, final_layout));
    }
    output_json["levels"] = levels_json;

    // Add violation information with enhanced details
    json violations = violations_to_json(violation_tracker.getViolations());
    output_json["violations"] = violations;
    
    // Add violation summary by type
    json violation_summary;
    std::map<std::string, int> violation_counts;
    std::map<std::string, float> max_severities;
    
    for (const auto& v : violation_tracker.getViolations()) {
        std::string type;
        switch (v.type) {
            case Violation::Type::COLLISION: type = "COLLISION"; break;
            case Violation::Type::BOUNDS: type = "BOUNDS"; break;
            case Violation::Type::ADJACENCY_CLEAN_DIRTY: type = "ADJACENCY_CLEAN_DIRTY"; break;
            case Violation::Type::ADJACENCY_QUIET_NOISY: type = "ADJACENCY_QUIET_NOISY"; break;
            default: type = "UNKNOWN"; break;
        }
        violation_counts[type]++;
        max_severities[type] = std::max(max_severities[type], v.severity);
    }
    
    for (const auto& [type, count] : violation_counts) {
        violation_summary[type] = {
            {"count", count},
            {"max_severity", max_severities[type]}
        };
    }
    output_json["violation_summary"] = violation_summary;
    output_json["violation_summary"] = {
        {"total_violations", violation_tracker.getViolationCount()},
        {"total_severity", violation_tracker.getTotalSeverity()}
    };

    // Add module details and sizes
    json modules_array = json::array();
    for (size_t i = 0; i < final_layout.size(); i++) {
        const auto& obj = final_layout[i];
        json module_data;
        
        // Basic module information
        module_data["index"] = i;
        module_data["name"] = obj.name;
        module_data["position"] = {
            {"x", obj.position.x},
            {"y", obj.position.y},
            {"z", obj.position.z}
        };
        module_data["scale"] = {
            {"x", obj.scale.x},
            {"y", obj.scale.y},
            {"z", obj.scale.z}
        };
        module_data["category"] = [&]() {
            switch (obj.category) {
                case ModuleCategory::CLEAN: return "CLEAN";
                case ModuleCategory::DIRTY: return "DIRTY";
                case ModuleCategory::QUIET: return "QUIET";
                case ModuleCategory::NOISY: return "NOISY";
                default: return "NEUTRAL";
            }
        }();

        // Add level information
        for (size_t level_idx = 0; level_idx < levels.size(); level_idx++) {
            if (std::find(levels[level_idx].module_indices.begin(),
                         levels[level_idx].module_indices.end(), i) != levels[level_idx].module_indices.end()) {
                module_data["level"] = level_idx;
                module_data["level_height"] = {
                    {"min", levels[level_idx].min_z},
                    {"max", levels[level_idx].max_z}
                };
                break;
            }
        }

        // Add violation information specific to this module
        json module_violations = json::array();
        for (const auto& v : violation_tracker.getViolations()) {
            if (v.object1Index == i || v.object2Index == i) {
                json violation_data = {
                    {"type", [&v]() {
                        switch (v.type) {
                            case Violation::Type::COLLISION: return "COLLISION";
                            case Violation::Type::BOUNDS: return "BOUNDS";
                            case Violation::Type::ADJACENCY_CLEAN_DIRTY: return "ADJACENCY_CLEAN_DIRTY";
                            case Violation::Type::ADJACENCY_QUIET_NOISY: return "ADJACENCY_QUIET_NOISY";
                            default: return "UNKNOWN";
                        }
                    }()},
                    {"severity", v.severity},
                    {"description", v.description}
                };
                
                if (v.object1Index == i) {
                    violation_data["other_module"] = v.object2Index;
                } else {
                    violation_data["other_module"] = v.object1Index;
                }
                
                module_violations.push_back(violation_data);
            }
        }
        module_data["violations"] = module_violations;
        
        modules_array.push_back(module_data);

        // Add size information for the frontend
        output_json["module_sizes"][obj.name] = {
            {"area_m2", obj.scale.x * obj.scale.y},
            {"volume_m3", obj.scale.x * obj.scale.y * obj.scale.z},
            {"width_m", obj.scale.x},
            {"depth_m", obj.scale.y},
            {"height_m", obj.scale.z}
        };
    }

    // Add habitat dimensions based on the final layout
    float min_z = std::numeric_limits<float>::max();
    float max_z = std::numeric_limits<float>::lowest();
    float max_radius = 0.0f;
    for(const auto& obj : final_layout) {
        if (obj.position.z - obj.scale.z / 2.0f < min_z) min_z = obj.position.z - obj.scale.z / 2.0f;
        if (obj.position.z + obj.scale.z / 2.0f > max_z) max_z = obj.position.z + obj.scale.z / 2.0f;
        float r = sqrt(obj.position.x * obj.position.x + obj.position.y * obj.position.y) + obj.scale.x / 2.0f;
        if (r > max_radius) max_radius = r;
    }

    output_json["habitat_dimensions"] = {
        {"total_height_m", max_z - min_z},
        // For now, we'll use simplified logic for the base and inflatable parts
        {"cylindrical_base_height_m", (max_z - min_z) * 0.3},
        {"cylindrical_base_diameter_m", max_radius * 2.0},
        {"inflatable_section_height_m", (max_z - min_z) * 0.7},
        {"inflatable_section_diameter_m", max_radius * 2.1} // Slightly larger
    };


    // Add a placeholder for the floor plan
    output_json["floor_plan"] = json::array();
    json layer1;
    layer1["layer"] = 1;
    layer1["radius_m"] = 5.0;
    for(const auto& obj : final_layout) {
        json mod_in_layer;
        mod_in_layer["module"] = obj.name;
        mod_in_layer["angle_deg"] = atan2(obj.position.y, obj.position.x) * 180.0 / 3.14159;
        mod_in_layer["distance_from_center_m"] = sqrt(obj.position.x * obj.position.x + obj.position.y * obj.position.y);
        layer1["modules"].push_back(mod_in_layer);
    }
    output_json["floor_plan"].push_back(layer1);

    // Add overall habitat dimensions for drawing
    output_json["habitat_dimensions"] = {
        {"total_height_m", 7.80},
        {"cylindrical_base_height_m", 2.60},
        {"cylindrical_base_diameter_m", 4.40},
        {"inflatable_section_height_m", 5.20},
        {"inflatable_section_diameter_m", 6.50}
    };

    // 6. Print the final JSON to stdout
    std::cout << output_json.dump(4) << std::endl;

    return 0;
}
