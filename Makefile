# This is the default action, it's always the first target
# .PHONY <target> at the end of the build step. Common phony targets
# are: clean, install, run,...
# Otherwise, if somebody creates an install directory, make will
# silently fail, because the build target already exists.

.PHONY: help print

help:
	@echo "Run make with:"
	@echo " > run-all-tests			...to run all tests using Docker Compose"
	@echo " > tests-cleanup			...to remove undesired files after a tests execution."
	@echo " > run-tests-and-clean   ...call the previous two rules."

run-all-tests:
	@echo "Tests will be run now..."
	@docker-compose -p selenium_testing up --build --abort-on-container-exit --remove-orphans
	@echo "Tests are run."

tests-cleanup:
	@echo Containers used for the project will be removed now.
	@docker-compose down && docker system prune -f --volumes
	@docker rmi -f selenium_testing_pytest-host
	@echo All unused containers are removed.

run-tests-and-clean: run-all-tests tests-cleanup

.DEFAULT_GOAL := help
