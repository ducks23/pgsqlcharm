# VARIABLES
export PATH := /snap/bin:$(PATH)
export CHARM_NAME := flaskapp
export CHARM_STORE_GROUP := omnivector
export CHARM_BUILD_DIR := ./build/builds
export CHARM_DEPS_DIR := ./build/deps
export CHARM_PUSH_RESULT := charm-store-push-result.txt

# TARGETS
lint: ## Run linter
	tox -e lint

build: clean ## Build charm
	tox -e build

clean: ## Remove .tox and build dirs
	rm -rf .tox/
	rm -rf build/
	rm -rf $(CHARM_PUSH_RESULT)

# Display target comments in 'make help'
help: 
	grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# SETTINGS
# Use one shell for all commands in a target recipe
.ONESHELL:
# Set default goal
.DEFAULT_GOAL := help
# Use bash shell in Make instead of sh 
SHELL := /bin/bash
