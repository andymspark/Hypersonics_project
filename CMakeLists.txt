cmake_minimum_required(VERSION 3.20)

project(HypersonicsProject LANGUAGES CXX)

# C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# MSVC: warnings + UTF-8 (helps with non-ASCII paths like 바탕 화면)
if (MSVC)
  add_compile_options(/W4 /utf-8)
else()
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# -------- yaml-cpp via FetchContent (no need for find_package) --------
include(FetchContent)
FetchContent_Declare(
  yaml-cpp
  GIT_REPOSITORY https://github.com/jbeder/yaml-cpp.git
  GIT_TAG yaml-cpp-0.7.0
)
FetchContent_MakeAvailable(yaml-cpp)

# -------- Your executable --------
add_executable(hypersonics
  src/main.cpp
  # add other source files here if you have them, e.g.:
  # src/solver.cpp
  # src/utils.cpp
)

target_link_libraries(hypersonics PRIVATE yaml-cpp)
# If you have headers in include/, uncomment:
# target_include_directories(hypersonics PRIVATE ${CMAKE_SOURCE_DIR}/include)
