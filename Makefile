update: venv
	git pull
	. venv/bin/activate; \
	python3 -m pip install -r requirements.txt

venv:
	test -d venv || virtualenv -p python3.7 venv

deploy-web:
	sudo cp deployment/neuraltextserver.service /etc/systemd/system
	sudo systemctl daemon-reload
	sudo systemctl enable neuraltextserver.service
	sudo systemctl restart neuraltextserver.service

	sudo cp deployment/odin.deadtired.me /etc/nginx/sites-available/odin.deadtired.me
	sudo ln -sf /etc/nginx/sites-available/odin.deadtired.me /etc/nginx/sites-enabled/odin.deadtired.me
	sudo service nginx restart

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

.PHONY: update venv deploy-web test run cli clean
