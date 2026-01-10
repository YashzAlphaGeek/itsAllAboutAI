@echo off
echo Training PPO Actor...
python -m train.train_ppo

echo Launching Flask server...
start python server/app.py
pause
