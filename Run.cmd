@echo off
echo Installing Packages...
pip install -r packages.txt
cls
python Clippy.py
echo CLIPPY ENDED
pause