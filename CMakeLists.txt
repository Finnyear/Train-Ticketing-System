cmake_minimum_required(VERSION 3.15)
project(TrainTicket)
set(CMAKE_CXX_STANDARD 14)
link_libraries(ws2_32 wsock32)

add_executable(TrainTicket backend/Users.cpp backend/Trains.cpp backend/Orders.cpp backend/Connector.cpp backend/Main.cpp)