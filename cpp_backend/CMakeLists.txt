# CMakeLists.txt for the C++ backend

# Minimum CMake version
cmake_minimum_required(VERSION 3.10)

# Project name
project(HabitatOptimizer)

# Set C++ standard to C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# --- Dependencies ---
# You need to download these libraries and place them in a 'dependencies' folder
# inside 'cpp_backend'.
#
# 1. GLM (OpenGL Mathematics)
#    - Download: https://github.com/g-truc/glm/releases
#    - Place the 'glm' folder inside 'dependencies'.
#
# 2. nlohmann/json (JSON for Modern C++)
#    - Download: https://github.com/nlohmann/json/releases (the 'json.hpp' file)
#    - Place 'json.hpp' inside a 'nlohmann' folder in 'dependencies'.
#
# Your 'dependencies' folder should look like this:
# cpp_backend/
# |-- dependencies/
# |   |-- glm/
# |   |-- nlohmann/
# |   |   |-- json.hpp

include_directories(dependencies)

# --- Source Files ---
# Add all your .cpp files here. Since main.cpp is the only one, it's simple.
add_executable(habitat_optimizer src/main.cpp)

# --- Linking ---
# For this command-line tool, we don't need to link against OpenGL or GLFW
# because we are not creating a window. If you were to add visualization,
# you would need to find and link those libraries here.
#
# Example for visualizer:
# find_package(OpenGL REQUIRED)
# find_package(glfw3 REQUIRED)
# target_link_libraries(habitat_optimizer PUBLIC OpenGL::GL glfw)

# --- Installation ---
# This tells CMake where to put the final executable after building.
# It will be placed in the root of the cpp_backend folder.
install(TARGETS habitat_optimizer DESTINATION .)
