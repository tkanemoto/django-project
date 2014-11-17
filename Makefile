# Makefile for Django sites
#
# Aimed to simplify development and release processes.

NO_COLOR    = \033[0m
COLOR       = \033[32;01m
SUCCESS_COLOR   = \033[35;01m

TEST_VERBOSITY ?= 1

ifeq ($(VIRTUALENV_DIR),)
  VIRTUALENV_DIR := .virtualenv
endif

LOCAL_PATH := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

all: clean kwalitee test

test: install
	@echo "$(COLOR)* Launching the tests suite$(NO_COLOR)"
	@bash -c "\
      source $(VIRTUALENV_DIR)/bin/activate && \
      $(LOCAL_PATH)/manage.py test \
        -v $(TEST_VERBOSITY) --traceback \
        --liveserver=localhost:8080,8090-8100,9000-9200 \
        $(TESTED_APPS)"

kwalitee: install
	@echo "$(COLOR)* Running pyflakes$(NO_COLOR)"
	@bash -c "\
      source $(VIRTUALENV_DIR)/bin/activate && \
      find . -type f -name "*.py" | \
      grep -v '/migrations/.*\.py' | \
      grep -v '/project/.*\.py' | \
      xargs pyflakes"
	@echo "$(COLOR)* Running pep8$(NO_COLOR)"
	@bash -c "\
      source $(VIRTUALENV_DIR)/bin/activate && \
      pep8 --config $(LOCAL_PATH)/.pep8rc \
        --exclude=project,static,migrations ."
	@echo "$(SUCCESS_COLOR)* No kwalitee errors, Congratulations ! :)$(NO_COLOR)"

clean:
	@echo "$(COLOR)* Removing useless files$(NO_COLOR)"
	@find . -type f \( -name "*.pyc" -o -name "*~" \) -exec rm -f {} \;


install: $(VIRTUALENV_DIR)/.freeze.list

$(VIRTUALENV_DIR)/.freeze.list: $(VIRTUALENV_DIR) \
                                $(LOCAL_PATH)/etc/requirements.txt \
                                $(LOCAL_PATH)/etc/apt-get.list \
                                $(LOCAL_PATH)/Makefile
	@echo "$(COLOR)* Installing pre-requisites$(NO_COLOR)"
	sudo apt-get install -y $(shell cat $(LOCAL_PATH)/etc/apt-get.list)
	@bash -c "\
      export PIP_DOWNLOAD_CACHE=$$HOME/.pip-download-cache && \
      source $(VIRTUALENV_DIR)/bin/activate && \
      pip install pip --upgrade && \
      pip install setuptools --upgrade && \
      pip install pbr --upgrade && \
      pip install -r $(LOCAL_PATH)/etc/requirements.txt && \
      pip freeze > $@"

$(VIRTUALENV_DIR):
	@echo "$(COLOR)* Setting up the virtualenv$(NO_COLOR)"
	@bash -c "\
      sudo apt-get install -y python-pip && \
      sudo pip install virtualenv --upgrade && \
      virtualenv --system-site-packages $@"
