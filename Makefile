update:
	git pull
	python3 -m pip install -r requirements.txt

install: update
	sudo cp neuraltextserver.service /etc/systemd/system
	sudo systemctl daemon-reload
	sudo systemctl enable neuraltextserver.service
	sudo systemctl restart neuraltextserver.service

test:
	python3 -m unittest

run:
	python3 neuraltextserver

cli:
	python3 cli.py

.PHONY: init test
