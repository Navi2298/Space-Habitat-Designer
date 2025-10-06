#pragma once

#include <vector>
#include <random>
#include <algorithm>
#include "Geometry.h"
#include "Evaluator.h"

namespace Optimizer {

// --- Part 4: Particle Swarm Optimization (PSO) ---

// Represents a single "particle" in the swarm. A particle is a complete layout solution.
struct Particle {
    std::vector<HabitatObject> layout; // The layout itself (position of all modules)
    std::vector<glm::vec3> velocity;   // The "velocity" of each module in the layout
    double score;                      // The evaluated score of this layout
    ViolationTracker violations;       // Track violations for this layout

    std::vector<HabitatObject> best_known_layout; // This particle's best-ever layout
    double best_known_score;
    ViolationTracker best_known_violations;
};

// The main PSO function
inline std::vector<HabitatObject> findBestLayout(const std::vector<HabitatObject>& initialLayout, int iterations = 100, int num_particles = 30) {
    std::vector<Particle> swarm(num_particles);
    std::vector<HabitatObject> global_best_layout = initialLayout;
    double global_best_score = -std::numeric_limits<double>::infinity();
    ViolationTracker global_best_violations;

    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> pos_distr(-4.0, 4.0); // Position distribution
    std::uniform_real_distribution<> vel_distr(-0.5, 0.5); // Velocity distribution

    // 1. Initialize the swarm
    for (int i = 0; i < num_particles; ++i) {
        swarm[i].layout = initialLayout;
        swarm[i].velocity.resize(initialLayout.size());

        for (size_t j = 0; j < initialLayout.size(); ++j) {
            // Assign random initial positions and velocities
            swarm[i].layout[j].position = glm::vec3(pos_distr(gen), pos_distr(gen), pos_distr(gen));
            swarm[i].velocity[j] = glm::vec3(vel_distr(gen), vel_distr(gen), vel_distr(gen));
        }

        // Evaluate with violation tracking
        swarm[i].score = Evaluator::evaluateLayout(swarm[i].layout, {1.0}, &swarm[i].violations);
        swarm[i].best_known_layout = swarm[i].layout;
        swarm[i].best_known_score = swarm[i].score;
        swarm[i].best_known_violations = swarm[i].violations;

        if (swarm[i].score > global_best_score) {
            global_best_score = swarm[i].score;
            global_best_layout = swarm[i].layout;
            global_best_violations = swarm[i].violations;
        }
    }

    // PSO parameters
    const float w = 0.5;  // Inertia weight
    const float c1 = 1.5; // Cognitive (personal best) weight
    const float c2 = 1.5; // Social (global best) weight
    
    // Adaptive parameters based on violations
    const float violation_repulsion = 0.2f; // Strength of violation avoidance

    // 2. Run the optimization loop
    for (int iter = 0; iter < iterations; ++iter) {
        for (auto& p : swarm) {
            // Update velocity and position for each module in the particle's layout
            for (size_t i = 0; i < p.layout.size(); ++i) {
                std::uniform_real_distribution<> r_distr(0.0, 1.0);
                float r1 = r_distr(gen);
                float r2 = r_distr(gen);

                glm::vec3 cognitive_component = c1 * r1 * (p.best_known_layout[i].position - p.layout[i].position);
                glm::vec3 social_component = c2 * r2 * (global_best_layout[i].position - p.layout[i].position);
                
                // Add violation avoidance component
                glm::vec3 violation_avoidance(0.0f);
                for (const auto& v : p.violations.getViolations()) {
                    if (v.object1Index == i || v.object2Index == i) {
                        // Move away from violation
                        glm::vec3 violation_pos;
                        if (v.object1Index == i) {
                            violation_pos = p.layout[v.object2Index].position;
                        } else {
                            violation_pos = p.layout[v.object1Index].position;
                        }
                        glm::vec3 away_dir = p.layout[i].position - violation_pos;
                        if (glm::length(away_dir) > 0.0001f) { // Prevent division by zero
                            away_dir = glm::normalize(away_dir);
                        }
                        violation_avoidance += violation_repulsion * v.severity * away_dir;
                    }
                }
                
                p.velocity[i] = w * p.velocity[i] + cognitive_component + social_component + violation_avoidance;

                // Clamp velocity to avoid explosion
                p.velocity[i] = glm::clamp(p.velocity[i], -1.0f, 1.0f);

                p.layout[i].position += p.velocity[i];
                p.layout[i].updateAABB();
            }

            // Evaluate with violation tracking
            p.score = Evaluator::evaluateLayout(p.layout, {1.0}, &p.violations);

            // Update personal best
            if (p.score > p.best_known_score) {
                p.best_known_score = p.score;
                p.best_known_layout = p.layout;
                p.best_known_violations = p.violations;

                // Update global best
                if (p.score > global_best_score) {
                    global_best_score = p.score;
                    global_best_layout = p.layout;
                    global_best_violations = p.violations;
                }
            }
        }
    }

    return global_best_layout;
}
}
