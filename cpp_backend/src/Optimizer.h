#pragma once

#include <vector>
#include <random>
#include "Geometry.h"
#include "Evaluator.h"

// A simplified placeholder for a real optimization algorithm like PSO.
// This version uses a simple "random search" or "hill climbing" approach.
namespace Optimizer {

    /**
     * @brief Generates a number of random layouts and returns the one with the best score.
     * This is a placeholder for a more sophisticated algorithm like Particle Swarm Optimization (PSO).
     * @param initialLayout The starting layout configuration.
     * @param iterations The number of random layouts to try.
     * @return The best layout found after all iterations.
     */
    inline std::vector<HabitatObject> findBestLayout(const std::vector<HabitatObject>& initialLayout, int iterations = 100) {
        
        std::vector<HabitatObject> bestLayout = initialLayout;
        double bestScore = Evaluator::evaluateLayout(bestLayout, {0.5, 0.5});

        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_real_distribution<> distr(-5.0, 5.0); // Random positions within a 10x10x10 box

        for (int i = 0; i < iterations; ++i) {
            std::vector<HabitatObject> currentLayout = initialLayout;
            for (auto& obj : currentLayout) {
                // Mutate the position of each object randomly
                obj.position.x = distr(gen);
                obj.position.y = distr(gen);
                obj.position.z = distr(gen);
            }

            double currentScore = Evaluator::evaluateLayout(currentLayout, {0.5, 0.5});

            if (currentScore > bestScore) {
                bestScore = currentScore;
                bestLayout = currentLayout;
            }
        }

        return bestLayout;
    }
}
