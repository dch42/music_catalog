#---------------------------------------------------------------------
# Install deps & add exec permissions
#---------------------------------------------------------------------

init:
	pip3 install -r requirements.txt
	chmod +x ./music_catalog.py
