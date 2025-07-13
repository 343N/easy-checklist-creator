set APPNAME=EasyChecklistCreator

pyinstaller --noconfirm --onefile --windowed --name %APPNAME%  "app.py"
xcopy "config.yaml" "dist\"