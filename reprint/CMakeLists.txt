cmake_minimum_required(VERSION 2.8)
project(reprint)

##############################################################################
# Version info
##############################################################################
set(REPRINT_VERSION "0.1.0")

message("Configuring rePrint v${VCP_VERSION}.")

##############################################################################
# Options
##############################################################################
#option(VCP_BUILD_PYTHON "Build Python bindings." ON)
# Everybody was unit-testing:
#option(VCP_BUILD_TESTS "Build tests, requires GTest." OFF)


# Logging related
#set(REPRINT_LOG_LEVEL "debug" CACHE STRING "Select logging level")
#set_property(CACHE REPRINT_LOG_LEVEL PROPERTY STRINGS debug info warning failure)
#option(REPRINT_LOG_FILE_LOCATION "Logged messages include source file location." OFF)
#option(REPRINT_LOG_STACK_TRACE_ON_ERROR "Log stack trace on exception/exit/abort." ON)


##############################################################################
# Set up CMake internals

# RPATH for linking
#set(CMAKE_INSTALL_RPATH "$ORIGIN")

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake")

##############################################################################
# Check build type
##############################################################################
#if(NOT CMAKE_BUILD_TYPE)
#    message("  * No build type configured, default to Release")
#    set(CMAKE_BUILD_TYPE Release)
#endif()
#TODO check if needed anymore
# Set flag (in case sub-modules need to know the build type)
#string(TOLOWER "${CMAKE_BUILD_TYPE}" LBUILD_TYPE)
#if(LBUILD_TYPE MATCHES debug)
#  add_definitions(-DDEBUG_BUILD)
#  set(VCP_IS_DEBUG_BUILD TRUE)
#else()
#  set(VCP_IS_DEBUG_BUILD FALSE)
#endif()


##############################################################################
# Write current version to disk
#string(REGEX MATCHALL "[0-9]" VCP_VERSION_PARTS "${VCP_VERSION}")
#list(GET VCP_VERSION_PARTS 0 VCP_VERSION_MAJOR)
#list(GET VCP_VERSION_PARTS 1 VCP_VERSION_MINOR)
#list(GET VCP_VERSION_PARTS 1 VCP_VERSION_PATCH)

# Keep C++ version header up-to-date
#file(WRITE src/cpp/vcp_utils/version.h 
#    "#ifndef __VCP_VERSION_H__
##define __VCP_VERSION_H__
##define VCP_VERSION \"${VCP_VERSION}\"
##define VCP_VERSION_MAJOR ${VCP_VERSION_MAJOR}
##define VCP_VERSION_MINOR ${VCP_VERSION_MINOR}
##define VCP_VERSION_PATCH ${VCP_VERSION_PATCH}
##endif // __VCP_VERSION_H__\n")
#
# Keep version in python 3 bindings up-to-date
#file(WRITE src/python3/vcp/version.py
#    "__version__ = \"${VCP_VERSION}\"\n")


##############################################################################
# Compiler flags


if(WIN32)
    message(FATAL_ERROR "[${PROJECT_NAME}] TODO Need to specify MSVC-compatible flags, at least for c++11")
else()
    set(CMAKE_CXX_FLAGS ${CMAKE_CXX_FLAGS} "-Wall -std=c++11 -Wpedantic -Wextra -g -rdynamic")
endif()

unset(LIBHTTPSERVER_INCLUDE_DIRS CACHE)
unset(LIBHTTPSERVER_LIBRARIES CACHE)
find_package(LibHttpServer REQUIRED)
message(STATUS "Found libhttpserver library: ${LIBHTTPSERVER_LIBRARIES}")
# Add OpenMP if available
#find_package(OpenMP)
#if (OPENMP_FOUND)
#    set (CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
#    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
#    set (CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
#endif()

#TODO system package version of microhttpd depends on gnutls, etc.
#find_library(LIBMICROHTTPD_LIBRARIES NAMES libmicrohttpd.a)
#message(STATUS "Found libmicrohttpd library: ${LIBMICROHTTPD_LIBRARIES}")


include_directories(${LIBHTTPSERVER_INCLUDE_DIRS})

add_executable(ippdemo
    src/ippdemo.cpp
)
target_link_libraries(ippdemo
    ${LIBHTTPSERVER_LIBRARIES}
    ${LIBMICROHTTPD_LIBRARIES}
)


#TODO make separate flag - VCP_WITH_TIMING (TIC_TOC should be available to external projects, too)
#if(VCP_VERBOSE_TIMING)
#  add_definitions(-DPVT_VERBOSE_TIMING)
#endif()


# Logging-related flags
#
# ... pick configured logging level
#if(${VCP_LOG_LEVEL} STREQUAL "debug")
#    add_definitions(-DVCP_LOG_LEVEL_DEBUG)
#    message("  * vcp will log DEBUG, INFO, WARNING and FAILURE messages.")
#elseif(${VCP_LOG_LEVEL} STREQUAL "info")
#    add_definitions(-DVCP_LOG_LEVEL_INFO)
#    message("  * vcp will log INFO, WARNING and FAILURE messages.")
#elseif(${VCP_LOG_LEVEL} STREQUAL "warning")
#    add_definitions(-DVCP_LOG_LEVEL_WARNING)
#    message("  * vcp will only log WARNING and FAILURE messages.")
#elseif(${VCP_LOG_LEVEL} STREQUAL "failure")
#    add_definitions(-DVCP_LOG_LEVEL_FAILURE)
#    message("  * vcp will only log FAILURE messages.")
#else()
#    message(FATAL_ERROR "[${PROJECT_NAME}] Invalid VCP_LOG_LEVEL value")
#endif()
#
## ... should we include the source file location in our logs?
#if(VCP_LOG_LOCATION)
#  add_definitions(-DVCP_LOG_LOCATION)
#endif()
#
# ... should we log the stack trace on unrecoverable errors?
#if(VCP_LOG_STACK_TRACE_ON_ERROR)
#    add_definitions(-DVCP_LOG_STACK_TRACE_ON_ERROR)
#endif()



