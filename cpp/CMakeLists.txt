cmake_minimum_required(VERSION 3.15)

project(AutoTestX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(autotestx
    src/Calculator.cpp
    src/TestFramework.cpp
    tests/main.cpp
)

target_include_directories(autotestx
    PRIVATE
    include
)

add_executable(calculator_program
    ../examples/calculator_program.cpp
)