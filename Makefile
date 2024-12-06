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
	@ touch testgmailrulesengine.sqlite
	@ pdm install -v --no-self;
	@ pdm run env DATABASE_NAME=testgmailrulesengine.sqlite piccolo migrations forwards gmail_rules_engine;
	@ pdm run env DATABASE_NAME=gmailrulesengine.sqlite piccolo migrations forwards gmail_rules_engine;

test:
	@ pdm run env DATABASE_NAME=testgmailrulesengine.sqlite pytest;

create-migrations:
	@ pdm run piccolo migrations new gmail_rules_engine --auto;

format:
	@ pdm run black core/ tests/;

migration:
	@ pdm run piccolo migrations forwards gmail_rules_engine;
