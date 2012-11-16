all: test docs

test:
	python tests/runtests.py

# docs:
# 	groc --out docs src/*.py