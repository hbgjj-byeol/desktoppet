@echo off
chcp 65001 >nul
cd /d "%~dp0"
py -m pip install -r requirements.txt
py -m PyInstaller --noconfirm --clean --onefile --windowed --name HamsterPet --add-data "assets;assets" hamster_pet.py
echo.
echo 완료! dist\HamsterPet.exe 파일을 확인하세요.
pause
