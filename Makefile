help:
	@echo "##################################### Targets ####################################"
	@echo "install: Install all dependencies in the virtualenv"
	@echo "test: Run all tests"
	@echo "format: Format the code"
	@echo "migration: Run migration"
	@echo "##################################################################################"

install:
	@ pdm install -v --no-self; 

setup:
	@ rm -rf gmailrulesengine.sqlite
	@ touch gmailrulesengine.sqlite
	@ pdm install -v --no-self;
	@ pdm run piccolo migrations forwards gmail_rules_engine;

test:
	@ pdm run pytest;

create-migrations:
	@ pdm run piccolo migrations new gmail_rules_engine --auto;

format:
	@ pdm run black core/ tests/;

migration:
	@ pdm run piccolo migrations forwards gmail_rules_engine;
