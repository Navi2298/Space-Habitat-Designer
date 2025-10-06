#pragma once

#include <vector>
#include <numeric>
#include "Geometry.h"
#include "Collision.h"
#include "ViolationTracker.h"

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
    inline double evaluateLayout(const std::vector<HabitatObject>& layout, const std::vector<double>& weights, ViolationTracker* tracker = nullptr) {
        double score = 0.0;

        // Clear previous violations if tracker is provided
        if (tracker) {
            tracker->clear();
        }

        // --- Penalties (negative contributions to score) ---

        // 1. Penalty for collisions between objects
        double collision_penalty = 0.0;
        for (size_t i = 0; i < layout.size(); ++i) {
            for (size_t j = i + 1; j < layout.size(); ++j) {
                if (Collision::checkAABBCollision(layout[i], layout[j])) {
                    float overlap = Collision::calculateOverlapVolume(layout[i], layout[j]);
                    float severity = std::min(1.0f, overlap / 2.0f); // Normalize severity
                    collision_penalty += 2000.0 * severity; // Increased penalty
                    
                    if (tracker) {
                        std::string desc = "Module collision detected with " + 
                                         std::to_string(overlap) + " m³ overlap";
                        tracker->addViolation(Violation::Type::COLLISION, i, j, desc, severity);
                    }
                }
            }
        }

        // 2. Penalty for objects being out of bounds
        double bounds_penalty = 0.0;
        const float HABITAT_RADIUS = 4.5f; // meters
        const float HABITAT_HEIGHT = 10.0f; // meters
        
        for (size_t i = 0; i < layout.size(); ++i) {
            const auto& obj = layout[i];
            float radialDist = sqrt(obj.position.x * obj.position.x + obj.position.y * obj.position.y);
            float radialViolation = radialDist + obj.scale.x / 2.0f - HABITAT_RADIUS;
            
            if (radialViolation > 0) {
                float severity = std::min(1.0f, radialViolation / 2.0f);
                bounds_penalty += 1000.0 * severity;
                
                if (tracker) {
                    std::string desc = "Module extends beyond habitat radius by " + 
                                     std::to_string(radialViolation) + " meters";
                    tracker->addViolation(Violation::Type::BOUNDS, i, -1, desc, severity);
                }
            }

            if (obj.position.z < 0 || obj.position.z > HABITAT_HEIGHT) {
                float heightViolation = std::max(-obj.position.z, 
                                               obj.position.z - HABITAT_HEIGHT);
                float severity = std::min(1.0f, heightViolation / 2.0f);
                bounds_penalty += 1000.0 * severity;
                
                if (tracker) {
                    std::string desc = "Module extends beyond habitat height by " + 
                                     std::to_string(heightViolation) + " meters";
                    tracker->addViolation(Violation::Type::BOUNDS, i, -1, desc, severity);
                }
            }
        }

        // 3. Penalty for violating adjacency rules
        double adjacency_penalty = 0.0;
        const float MIN_CLEAN_DIRTY_DISTANCE = 3.0f; // meters
        const float MIN_QUIET_NOISY_DISTANCE = 4.0f; // meters
        
        for (size_t i = 0; i < layout.size(); ++i) {
            for (size_t j = i + 1; j < layout.size(); ++j) {
                const auto& mod1 = layout[i];
                const auto& mod2 = layout[j];

                float distance = glm::distance(mod1.position, mod2.position);

                // Clean-Dirty violation check
                if ((mod1.category == ModuleCategory::CLEAN && mod2.category == ModuleCategory::DIRTY) ||
                    (mod1.category == ModuleCategory::DIRTY && mod2.category == ModuleCategory::CLEAN)) {
                    
                    if (distance < MIN_CLEAN_DIRTY_DISTANCE) {
                        float violation = MIN_CLEAN_DIRTY_DISTANCE - distance;
                        float severity = std::min(1.0f, violation / MIN_CLEAN_DIRTY_DISTANCE);
                        adjacency_penalty += 1500.0 * severity;
                        
                        if (tracker) {
                            std::string desc = "Clean and dirty modules too close by " + 
                                             std::to_string(violation) + " meters";
                            tracker->addViolation(Violation::Type::ADJACENCY_CLEAN_DIRTY, 
                                               i, j, desc, severity);
                        }
                    }
                }

                // Quiet-Noisy violation check
                if ((mod1.category == ModuleCategory::QUIET && mod2.category == ModuleCategory::NOISY) ||
                    (mod1.category == ModuleCategory::NOISY && mod2.category == ModuleCategory::QUIET)) {
                    
                    if (distance < MIN_QUIET_NOISY_DISTANCE) {
                        float violation = MIN_QUIET_NOISY_DISTANCE - distance;
                        float severity = std::min(1.0f, violation / MIN_QUIET_NOISY_DISTANCE);
                        adjacency_penalty += 1500.0 * severity;
                        
                        if (tracker) {
                            std::string desc = "Quiet and noisy modules too close by " + 
                                             std::to_string(violation) + " meters";
                            tracker->addViolation(Violation::Type::ADJACENCY_QUIET_NOISY, 
                                               i, j, desc, severity);
                        }
                    }
                }
            }
        }


        // --- Rewards (positive contributions to score) ---

        // 1. Reward for compact layouts (minimize average distance from center)
        double compactness_reward = 0.0;
        glm::vec3 center(0.0f);
        for (const auto& obj : layout) {
            center += obj.position;
        }
        center /= layout.size();

        double avg_dist_from_center = 0.0;
        for (const auto& obj : layout) {
            avg_dist_from_center += glm::distance(obj.position, center);
        }
        avg_dist_from_center /= layout.size();
        compactness_reward = 1.0 / (1.0 + avg_dist_from_center); // Higher reward for smaller average distance


        // Final Score Calculation
        score = (compactness_reward * weights[0]) - (collision_penalty + bounds_penalty + adjacency_penalty);

        return score;
    }
}
