PY = python2.7 -m compileall -q -f
#PY = python2.6 -m compileall -q -f

CONFIG = config

SRC = src
SRC_CONF = $(SRC)/$(CONFIG)

TARGETS = trouble
TARGET_CONF = $(TARGETS)/$(CONFIG)

all: clean $(TARGETS)

$(TARGETS):
	cp -r $(SRC) $(TARGETS)
	cat $(TARGETS)/app_settings.py >> $(TARGETS)/app_helper.py
	-$(PY) $(TARGETS)
	find $(TARGETS) -name '*.py' -delete
	rm $(TARGET_CONF)/setting.pyc
	rm $(TARGETS)/app_settings.pyc
	cp $(SRC_CONF)/setting.py $(TARGET_CONF)

clean: 
	rm -rf $(TARGETS)
