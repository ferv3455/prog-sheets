default:
	python ./src/main.py
.PHONY: default

test:
	python -m unittest discover -s ./test -p "*_test.py"
.PHONY: test
