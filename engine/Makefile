OS := $(shell uname -s)

ifeq ($(OS),Linux)
    CXX = g++
    CC = gcc
    LIBS = -lGLEW -lGL
    ARGS = -fPIC
    DLL_EXT = .so
    DLL_FLAGS = -shared
endif

ifeq ($(OS),Windows_NT)
    CXX = g++
    CC = gcc
    LIBS = -lglew32s -lopengl32 -lgdi32 -limm32
    ARGS = -Llibs/lib -Ilibs/include -DGLEW_STATIC
    DLL_EXT = .dll
    DLL_FLAGS = -shared -Wl,--out-implib,lib.dll.a
endif

SRC_DIR := src
OBJ_DIR := builds
BIN := bin/q3d_engine$(DLL_EXT)

C_SOURCES := $(shell find $(SRC_DIR) -type f -name "*.c")
CPP_SOURCES := $(shell find $(SRC_DIR) -type f -name "*.cpp")

C_OBJECTS := $(patsubst $(SRC_DIR)/%, $(OBJ_DIR)/%, $(C_SOURCES:.c=.o))
CPP_OBJECTS := $(patsubst $(SRC_DIR)/%, $(OBJ_DIR)/%, $(CPP_SOURCES:.cpp=.o))

OBJECTS := $(C_OBJECTS) $(CPP_OBJECTS)

$(shell mkdir -p $(OBJ_DIR))

$(BIN): $(OBJECTS)
	$(CXX) $(DLL_FLAGS) $^ -o $@ $(ARGS) $(LIBS)

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c
	@mkdir -p $(dir $@)
	$(CC) $(ARGS) -c $< -o $@

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	@mkdir -p $(dir $@)
	$(CXX) $(ARGS) -c $< -o $@
    
clean:
	rm -rf $(OBJ_DIR) $(BIN)