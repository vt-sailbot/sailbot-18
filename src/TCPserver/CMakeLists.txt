cmake_minimum_required(VERSION 2.3.2)
project(sailbot_tcp_comms)


set(TARGET server)

file(GLOB_RECURSE src src/*.cpp)
file(GLOB_RECURSE headers src/*.h)

set(CFLAGS  "-Wall -pthread")

set (CMAKE_CXX_FLAGS ${CFLAGS})

add_executable(${TARGET} ${src} ${headers})
