help:
	@echo "##################################### Targets ####################################"
	@echo "install: Install all dependencies in the virtualenv"
	@echo "##################################################################################"

install:
	@ pdm install -v --no-self; 

test:
	@ pdm run pytest;
