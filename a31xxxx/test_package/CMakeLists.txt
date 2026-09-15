cmake_minimum_required(VERSION 3.15)

set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)
project(test_package C)

find_package(audk32_hal REQUIRED CONFIG)

add_executable(test_package src/test_package.c)
set_target_properties(test_package PROPERTIES SUFFIX ".elf")
target_link_libraries(test_package PRIVATE audk32_hal::audk32_hal)

target_link_options(test_package PRIVATE --specs=nosys.specs)
