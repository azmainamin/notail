
set original_dir=%CD%
set venv_root_dir="C:\Workspace\refurb-notes"
cd %venv_root_dir%
call %venv_root_dir%\env\Scripts\activate.bat
"C:\Program Files\Python37\python.exe" -m pip install -r "C:\Workspace\refurb-notes\requirements.txt"

"C:\Program Files\Python37\python.exe" "C:\Workspace\refurb-notes\src\main.py"

call %venv_root_dir%\Scripts\deactivate.bat
cd %original_dir%
exit /B 1
