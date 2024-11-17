# Makefile for building the gatorTicketMaster executable without using a spec file

# Define variables
PYTHON := python3
PIP := pip3
PYINSTALLER := pyinstaller
MAIN_SCRIPT := gatorTicketMaster.py
EXECUTABLE_NAME := gatorTicketMaster
DISTPATH := .
HIDDEN_IMPORTS := rbnode,rbtree,minheapnode,minheap,seatheap

# Default target
all: install build

# Install requirements
install:
	@echo "Installing requirements..."
	$(PIP) install -r requirements.txt

# Declare build as a phony target
.PHONY: build

# Build the executable using PyInstaller command-line options
build:
	@echo "Building the executable..."
	$(PYINSTALLER) --onefile --distpath $(DISTPATH) \
		--hidden-import=$(HIDDEN_IMPORTS) \
		$(MAIN_SCRIPT)

# Clean up build artifacts
clean:
	@echo "Cleaning up build artifacts..."
	rm -rf build __pycache__ *.spec
	rm -f $(EXECUTABLE_NAME) $(EXECUTABLE_NAME).exe

# Help target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  make          - Install requirements and build the executable (default)"
	@echo "  make install  - Install requirements from requirements.txt"
	@echo "  make build    - Build the executable"
	@echo "  make clean    - Clean up build artifacts"
	@echo "  make help     - Display this help message"

