cmake_minimum_required(VERSION 3.10)

project(_flecs VERSION 0.0.1 LANGUAGES C CXX)
include(CTest)

# Set a few variables
set(CPP_DIR ${CMAKE_CURRENT_SOURCE_DIR}/cpp)
set(PYTHON_DIR ${CMAKE_CURRENT_SOURCE_DIR}/python)

# ECS
add_subdirectory(${CPP_DIR}/third_party/flecs EXCLUDE_FROM_ALL)

# Add pybind11
find_package(pybind11 REQUIRED)

pybind11_add_module(${PROJECT_NAME} ${CPP_DIR}/src/bindings.cpp
    ${CPP_DIR}/src/world.cpp
    ${CPP_DIR}/src/entity.cpp
    ${CPP_DIR}/src/iter.cpp
    ${CPP_DIR}/src/filter.cpp
    ${CPP_DIR}/src/query.cpp
)

target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_17)
target_link_libraries(${PROJECT_NAME}
    PUBLIC flecs::flecs_static
)
target_include_directories(${PROJECT_NAME} 
    PRIVATE ${CPP_DIR}/third_party/flecs/src
)

install(TARGETS ${PROJECT_NAME} DESTINATION ${PYTHON_DIR}/src/flecs)