#include <iostream>
#include <vector>
#include <string>

// You will need to download this header-only library for JSON processing.
// Place it in the 'dependencies' folder.
#include <nlohmann/json.hpp>

#include "Geometry.h"
#include "Optimizer.h"

using json = nlohmann::json;

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

    // Create an initial layout based on parameters.
    // A real implementation would have a library of modules to choose from.
    int num_modules = 2 + (crew_size / 2) + (mission_days / 90);
    std::vector<HabitatObject> initial_layout;
    for (int i = 0; i < num_modules; ++i) {
        HabitatObject obj;
        obj.name = "Module_" + std::to_string(i);
        obj.scale = glm::vec3(2.0f, 2.0f, 3.0f); // Example dimensions
        initial_layout.push_back(obj);
    }

    // 4. Run the optimization process
    std::vector<HabitatObject> final_layout = Optimizer::findBestLayout(initial_layout, 500);

    // NOTE: Off-screen rendering would happen here.
    // This is a complex process involving setting up an OpenGL context without a window
    // (e.g., using OSMesa or EGL) and rendering to a framebuffer object (FBO),
    // then saving the FBO's color attachment to an image file.
    // For this implementation, we will return a placeholder image URL.
    std::string generated_image_path = "/Images/modern-space-habitat-with-cosmic-view.jpg.jpg"; // Placeholder

    // 5. Serialize the results to an output JSON
    json output_json;
    output_json["status"] = "success";
    
    // Create a description
    output_json["description"] = "A " + material + " habitat for " + std::to_string(crew_size) + 
                                 " crew on a " + std::to_string(mission_days) + "-day mission. " +
                                 "Layout optimized for volume and mass.";

    output_json["image_url"] = generated_image_path;

    // Add module details and sizes
    for (const auto& obj : final_layout) {
        json module_data;
        module_data["name"] = obj.name;
        module_data["position"] = {obj.position.x, obj.position.y, obj.position.z};
        output_json["modules"].push_back(module_data);

        // Add size information for the frontend
        output_json["module_sizes"][obj.name] = {
            {"area_m2", obj.scale.x * obj.scale.y},
            {"volume_m3", obj.scale.x * obj.scale.y * obj.scale.z},
            {"width_m", obj.scale.x},
            {"depth_m", obj.scale.y},
            {"height_m", obj.scale.z}
        };
    }

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

    // 6. Print the final JSON to stdout
    std::cout << output_json.dump(4) << std::endl;

    return 0;
}
