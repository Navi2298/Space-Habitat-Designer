#pragma once

#include <vector>
#include <string>
#include "Geometry.h"

struct Violation {
    enum class Type {
        COLLISION,
        BOUNDS,
        ADJACENCY_CLEAN_DIRTY,
        ADJACENCY_QUIET_NOISY
    };

    Type type;
    size_t object1Index;
    size_t object2Index;  // -1 if not applicable (e.g., bounds violation)
    std::string description;
    float severity;  // 0.0 to 1.0

    Violation(Type t, size_t obj1, size_t obj2, const std::string& desc, float sev)
        : type(t), object1Index(obj1), object2Index(obj2), description(desc), severity(sev) {}
};

class ViolationTracker {
private:
    std::vector<Violation> violations;

public:
    void clear() {
        violations.clear();
    }

    void addViolation(Violation::Type type, size_t obj1, size_t obj2, const std::string& description, float severity) {
        violations.emplace_back(type, obj1, obj2, description, severity);
    }

    const std::vector<Violation>& getViolations() const {
        return violations;
    }

    size_t getViolationCount() const {
        return violations.size();
    }

    float getTotalSeverity() const {
        float total = 0.0f;
        for (const auto& v : violations) {
            total += v.severity;
        }
        return total;
    }
};