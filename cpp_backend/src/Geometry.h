#pragma once

#include <vector>
#include <string>

// For simplicity, we'll assume you have the GLM library for math.
// You will need to download it and place it in the 'dependencies' folder.
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>

struct Vertex {
    glm::vec3 Position;
    glm::vec3 Normal;
};

// Represents a single, movable object in the habitat.
struct HabitatObject {
    std::string name;
    std::string function;
    
    // Geometry Representation
    std::vector<Vertex> vertices;
    std::vector<unsigned int> indices;
    
    // Metadata
    float mass_kg = 100.0f;

    // Geometry Manipulation
    glm::vec3 position = glm::vec3(0.0f);
    glm::vec3 rotation_degrees = glm::vec3(0.0f);
    glm::vec3 scale = glm::vec3(1.0f);

    // Bounding Box for simplified collision detection
    glm::vec3 aabb_min;
    glm::vec3 aabb_max;

    glm::mat4 getModelMatrix() const {
        glm::mat4 model = glm::mat4(1.0f);
        model = glm::translate(model, position);
        model = glm::rotate(model, glm::radians(rotation_degrees.x), glm::vec3(1, 0, 0));
        model = glm::rotate(model, glm::radians(rotation_degrees.y), glm::vec3(0, 1, 0));
        model = glm::rotate(model, glm::radians(rotation_degrees.z), glm::vec3(0, 0, 1));
        model = glm::scale(model, scale);
        return model;
    }

    void updateAABB() {
        // A simple AABB calculation based on position and scale
        aabb_min = position - scale / 2.0f;
        aabb_max = position + scale / 2.0f;
    }
};
