.PHONY: all clean

PY_FILES = bookxnote bookxnote_local_file potplayer potplayer_http zotero zotero_local_file PPT app_hub
DIST_DIR = dist

SEVEN_ZIP = 7z

all: build copy_config compress

build:
	@for file in $(PY_FILES); do \
		pipenv run pyinstaller -y "src/$$file.py" --noconsole --hidden-import=plyer.platforms.win.notification; \
	done

copy_config:
	@for file in $(PY_FILES); do \
		cp -f config.conf $(DIST_DIR)/$$file/config.conf; \
	done

compress:
	@for file in $(PY_FILES); do \
		$(SEVEN_ZIP) a -tzip $(DIST_DIR)/$$file.zip ./$(DIST_DIR)/$$file/*; \
	done

clean:
	@for file in $(PY_FILES); do \
		rm -rf $(DIST_DIR)\$$file; \
		rm -f $(DIST_DIR)\$$file.zip; \
	done
	rm -rf build
	rm -rf __pycache__
	rm -rf *.spec
