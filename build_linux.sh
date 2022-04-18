pyinstaller --onefile ./secretStore.py -F --paths=\lib\site-packages
pyinstaller --onefile ./getData_orcl.py -F --paths=\lib\site-packages
pyinstaller --onefile ./outputJSON.py -F --paths=\lib\site-packages
pyinstaller --onefile ./uploadAZURE.py -F --paths=\lib\site-packages
