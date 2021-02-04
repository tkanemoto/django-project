# Makefile for Django sites
#
# Aimed to simplify development and release processes.

NO_COLOR    = \033[0m
COLOR       = \033[32;01m
SUCCESS_COLOR   = \033[35;01m

TEST_VERBOSITY ?= 1

ifeq ($(VIRTUALENV_DIR),)
  VIRTUALENV_DIR := ../.virtualenv
endif
ifeq ($(DJANGO_SETTINGS_MODULE),)
	DJANGO_SETTINGS_MODULE := project.settings_local
endif

LOCAL_PATH := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

MANAGE := pipenv run $(LOCAL_PATH)/manage.py

all: clean kwalitee test

test: install
	@echo "$(COLOR)* Launching the tests suite$(NO_COLOR)"
	$(MANAGE) test \
        -v $(TEST_VERBOSITY) --traceback \
        --liveserver=localhost:8080,8090-8100,9000-9200 \
        $(TESTED_APPS)

kwalitee: install
	@echo "$(COLOR)* Running pyflakes$(NO_COLOR)"
	@bash -c "\
      source $(shell pipenv --venv)/bin/activate && \
      find . -type f -name "*.py" | \
      grep -v '/migrations/.*\.py' | \
      grep -v '/project/.*\.py' | \
      grep -v '/manage\.py' | \
      xargs pyflakes"
	@echo "$(COLOR)* Running pep8$(NO_COLOR)"
	pipenv run pep8 --config $(LOCAL_PATH)/.pep8rc \
        --exclude=project,static,migrations .
	@echo "$(SUCCESS_COLOR)* No kwalitee errors, Congratulations ! :)$(NO_COLOR)"

prepare-db: install
	@echo "$(COLOR)* Prepare the database$(NO_COLOR)"
	$(MANAGE) migrate --fake-initial treemenus --noinput --traceback --settings $(DJANGO_SETTINGS_MODULE)
	$(MANAGE) migrate --fake-initial base inlines music people --noinput --traceback --settings $(DJANGO_SETTINGS_MODULE)
	$(MANAGE) migrate --noinput --traceback --settings $(DJANGO_SETTINGS_MODULE)
	$(MANAGE) collectstatic --noinput --traceback --settings $(DJANGO_SETTINGS_MODULE)

migrations:
	$(MANAGE) makemigrations --traceback --settings $(DJANGO_SETTINGS_MODULE)

clean:
	@echo "$(COLOR)* Removing useless files$(NO_COLOR)"
	@find . -type f \( -name "*.pyc" -o -name "*~" \) -exec rm -f {} \;

install: $(VIRTUALENV_DIR)/.freeze

$(VIRTUALENV_DIR)/.freeze: \
  $(LOCAL_PATH)/Pipfile.lock \
    $(LOCAL_PATH)/Pipfile \
    $(LOCAL_PATH)/Makefile
	@echo "$(COLOR)* Installing pipenv environment$(NO_COLOR)"
	pipenv --site-packages install
	rm -f $(VIRTUALENV_DIR)
	ln -s `pipenv --venv` $(VIRTUALENV_DIR)
	pipenv run pip freeze > $@
