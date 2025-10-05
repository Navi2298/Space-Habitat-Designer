#pragma once

#include "Geometry.h"

namespace Collision {

    /**
     * @brief Checks for collision between two objects using their Axis-Aligned Bounding Boxes (AABB).
     * This is a fast but less accurate method, suitable for a first-pass or broad-phase check.
     * For more accuracy with rotated objects, a Separating Axis Theorem (SAT) or GJK algorithm would be needed.
     * @param a The first habitat object.
     * @param b The second habitat object.
     * @return True if the bounding boxes overlap, false otherwise.
     */
    inline bool checkAABBCollision(const HabitatObject& a, const HabitatObject& b) {
        // Ensure AABBs are up-to-date before checking
        // In a real engine, this would be handled more efficiently.
        const_cast<HabitatObject&>(a).updateAABB();
        const_cast<HabitatObject&>(b).updateAABB();

        bool overlapX = a.aabb_min.x <= b.aabb_max.x && a.aabb_max.x >= b.aabb_min.x;
        bool overlapY = a.aabb_min.y <= b.aabb_max.y && a.aabb_max.y >= b.aabb_min.y;
        bool overlapZ = a.aabb_min.z <= b.aabb_max.z && a.aabb_max.z >= b.aabb_min.z;
        
        return overlapX && overlapY && overlapZ;
    }

    /**
     * @brief Checks if a point is inside the AABB of a habitat object.
     * @param point The 3D point to test.
     * @param obj The habitat object.
     * @return True if the point is inside the object's AABB, false otherwise.
     */
    inline bool isPointInside(const glm::vec3& point, const HabitatObject& obj) {
        return (point.x >= obj.aabb_min.x && point.x <= obj.aabb_max.x) &&
               (point.y >= obj.aabb_min.y && point.y <= obj.aabb_max.y) &&
               (point.z >= obj.aabb_min.z && point.z <= obj.aabb_max.z);
    }
}
