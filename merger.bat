SET mypath=%~dp0
cd %mypath:~0,-1%
set PYTHONPATH=%cd%\src
python .\src\merger.py
