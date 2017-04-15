# Botnet experiment

## Contents
- [Setup](#setup)
- [Running](#running)
- [Troubleshooting](#troubleshooting)

## Setup
Requires `python3.6` and `irc3`.

#### Virtualenv (optional)
Setup a Python virtual environment:
```bash
mkvirtualenv -p python3 botnet
workon botnet
```

#### Install Python packages
```bash
pip install irc3
```

#### Clone project
```bash
git clone https://github.com/cnsatuva/botnet.git
```

## Running
Set the environment variable `IP` to the IP of your IRC server, then run `client.py`.
```bash
export IP='xxx.xxx.xxx.xxx'
python3 client.py
```

## Troubleshooting
- Ensure your python version is 3.6+ (`python -v` >= 3.6)
- Ensure you are in your virtualenv, if you set one up
- Ensure you have set the environment variable `IP`
