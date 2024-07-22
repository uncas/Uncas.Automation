venv: .venv/touchfile

.venv/touchfile: requirements.txt
	test -d .venv || virtualenv .venv
	. .venv/bin/activate
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	touch .venv/touchfile

run: venv
	. .venv/bin/activate
	python run.py

scheduled: venv
	. .venv/bin/activate
	python scheduled.py

test: venv
	. .venv/bin/activate
	python -m unittest discover -s tests -p test*_unit.py

test-integration: venv
	. .venv/bin/activate
	python -m unittest discover -s tests -p test*_integration.py

test-new: venv
	. .venv/bin/activate
	python -m unittest discover -s tests -p test_new_integration.py

test-all: test test-integration test-new