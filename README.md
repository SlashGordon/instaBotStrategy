## install on windows

 1. `git clone https://github.com/InstaPy/instapy-quickstart`
 2. `cd instapy-quickstart\installation\Windows`
 3. run install.bat with admin privileges
 4. run recently update.bat
 5. `git clone https://github.com/SlashGordon/instaBotStrategy`
 6. `cd instaBotStrategy`
 7. configure the config.json
 8. create venv `python -m venv .venv`
 9. load virtual environment `.venv/Scripts/activate.ps1`
 10. install requirements `pip install -r requirements.txt`
 11. run `python src/simple_strategy.py --path config.json`