# Darshil Shah ~ robo-advisor-project

This document walks you (the user) through this robo-advisor project. It will help you setup your environment to run the code successfully. If you have any questions, you can reach out to project lead dks53@georgetown.edu

## What does this code do?


## Setup
Use GitHub Desktop software or the command-line to download or "clone" the repository onto your computer. Choose a familiar download location like the Desktop.

After cloning the repo, navigate there from the command-line: 

```sh
cd ~/Desktop/robo-advisor/app
```
## Environment setup

Create and activate a new Anaconda virtual environment:

```sh
conda create -n stocks-env python=3.7 # (first time only)
conda activate stocks-env
```

From within the virtual environment, install the required packages specified in the "requirements.txt"

```sh
pip install -r requirements.txt
```

From within the virtual environment, demonstrate your ability to run the Python script from the command-line:

```sh
python app/robo-advisor.py
```