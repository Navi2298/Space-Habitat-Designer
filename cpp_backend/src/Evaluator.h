#pragma once

#include <vector>
#include <numeric>
#include "Geometry.h"
#include "Collision.h"

namespace Evaluator {

    /**
     * @brief Calculates the total habitable volume by subtracting object volumes from a total bounding volume.
     * This uses a grid-based numerical method.
     * @param layout A vector of all objects in the habitat.
     * @param habitatBoundsMin The minimum corner of the habitat's total volume.
     * @param habitatBoundsMax The maximum corner of the habitat's total volume.
     * @param gridSize The resolution of the test grid. Smaller values are more accurate but much slower.
     * @return The calculated habitable volume in cubic meters.
     */
    inline float calculateHabitableVolume(const std::vector<HabitatObject>& layout, const glm::vec3& habitatBoundsMin, const glm::vec3& habitatBoundsMax, float gridSize = 0.25f) {
        float totalVolume = 0.0f;
        float pointVolume = gridSize * gridSize * gridSize;

        for (float x = habitatBoundsMin.x; x < habitatBoundsMax.x; x += gridSize) {
            for (float y = habitatBoundsMin.y; y < habitatBoundsMax.y; y += gridSize) {
                for (float z = habitatBoundsMin.z; z < habitatBoundsMax.z; z += gridSize) {
                    glm::vec3 point(x, y, z);
                    bool isInsideObject = false;
                    for (const auto& obj : layout) {
                        if (Collision::isPointInside(point, obj)) {
                            isInsideObject = true;
                            break;
                        }
                    }
                    if (!isInsideObject) {
                        totalVolume += pointVolume;
                    }
                }
            }
        }
        return totalVolume;
    }

    /**
     * @brief The main objective function. It calculates a score for a given layout.
     * Higher scores are better.
     * @param layout The layout to evaluate.
     * @param weights A vector of weights for different criteria (e.g., mass, volume).
     * @return The final score for the layout, including penalties.
     */
    inline double evaluateLayout(const std::vector<HabitatObject>& layout, const std::vector<double>& weights) {
        // --- Calculate Criteria ---
        double totalMass = 0;
        for (const auto& obj : layout) {
            totalMass += obj.mass_kg;
        }

        double habitableVolume = calculateHabitableVolume(layout, glm::vec3(-10), glm::vec3(10));

        // --- Map to Utility Values (simple linear example) ---
        // Utility functions should be non-linear in a real scenario (e.g., diminishing returns).
        double utilityMass = 10000.0 / (1.0 + totalMass); // Lower mass is better.
        double utilityVolume = habitableVolume;           // Higher volume is better.

        // --- Calculate Unconstrained Performance ---
        double performance = weights[0] * utilityMass + weights[1] * utilityVolume;

        // --- Apply Penalty Functions for Constraints ---
        double penalty = 0.0;
        for (size_t i = 0; i < layout.size(); ++i) {
            for (size_t j = i + 1; j < layout.size(); ++j) {
                if (Collision::checkAABBCollision(layout[i], layout[j])) {
                    // Apply a large, fixed penalty for any hardware overlap.
                    penalty += 10000.0; 
                }
            }
        }
        
        return performance - penalty;
    }
}
