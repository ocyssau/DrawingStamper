SET mypath=%~dp0
cd %mypath:~0,-1%
cd src
pyinstaller --distpath ../dist --workpath ../build --icon=logo.ico gui/stamperFS.py

