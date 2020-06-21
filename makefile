main :  Connector.cpp \
		Main.cpp \
		Orders.cpp \
		Trains.cpp \
		Users.cpp
	g++ Connector.cpp \
		Main.cpp \
		Orders.cpp \
		Trains.cpp \
		Users.cpp \
		-o code -Wall -Wextra -Wconversion -Wshadow \
		-std=c++11 -O2