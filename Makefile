help:
	@echo "##################################### Targets ####################################"
	@echo "install: Install all dependencies in the virtualenv"
	@echo "setup-db: Setup the database"
	@echo "test: Run tests"
	@echo "format: Format the code"
	@echo "migration: Run migration"
	@echo "##################################################################################"

install:
	@ pdm install -v --no-self; 

setup-db:
	@ rm -rf gmailrulesengine.sqlite
	@ touch gmailrulesengine.sqlite
	@ pdm run env DATABASE_NAME=gmailrulesengine.sqlite piccolo migrations forwards gmail_rules_engine;

test:
	@ rm -rf testgmailrulesengine.sqlite
	@ touch testgmailrulesengine.sqlite
	@ pdm run env DATABASE_NAME=testgmailrulesengine.sqlite piccolo migrations forwards gmail_rules_engine;
	@ pdm run env DATABASE_NAME=testgmailrulesengine.sqlite pytest;
	@ rm -rf testgmailrulesengine.sqlite

create-migrations:
	@ pdm run piccolo migrations new gmail_rules_engine --auto;

format:
	@ pdm run black core/ tests/;

migration:
	@ pdm run piccolo migrations forwards gmail_rules_engine;

teardown:
	@ rm -rf gmailrulesengine.sqlite
	@ rm -rf testgmailrulesengine.sqlite
	@ unset PATH_TO_CREDENTIALS_JSON
	@ unset DATABASE_NAME
