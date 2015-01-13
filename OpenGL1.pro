QT -= core
TARGET=OpenGL1
SOURCES += main.cpp
QMAKE_CXXFLAGS += $$system(sdl2-config --cflags)
LIBS+= $$system(sdl2-config --libs)
