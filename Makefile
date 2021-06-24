update: venv
	. venv/bin/activate; \
	python3 -m pip install -r requirements.txt

venv:
	test -d venv || virtualenv -p python3.7 venv

setup-systemd:
	sudo cp deployment/neuraltextserver.service /etc/systemd/system
	sudo systemctl daemon-reload
	sudo systemctl enable neuraltextserver.service
	sudo systemctl restart neuraltextserver.service

test:
	. venv/bin/activate; \
	python3 -W ignore::DeprecationWarning -m unittest

run:
	. venv/bin/activate; \
	flask run --eager-loading

cli:
	. venv/bin/activate; \
	python3 cli.py

clean:
	find -iname "*.pyc" -delete

.PHONY: update venv setup-systemd test run cli clean
