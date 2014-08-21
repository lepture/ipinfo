clean:
	@rm -fr data

fetch:
	@bash fetch.sh download
	@bash fetch.sh unzip
	@bash fetch.sh encode 

read:
	@python ip17mon.py
	@python3 geolite.py
