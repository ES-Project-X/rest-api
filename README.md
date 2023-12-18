# BiX - REST API

## Description

This repository contains the REST API for our project.

**Course:** Software Engineering (2023/2024).

## Installation

- Run `sudo apt-get uvicorn` to install uvicorn in your computer.
- Run `pip3 install virtualenv` to install the module `virtualenv`.
- Run `virtualenv venv` in root to create a virtual environment.
- Run `source venv/bin/activate` in root to enter the virtual environment.
- Run `pip3 install -r requirements.txt` to install all project dependencies.

Running Locally

- Run `uvicorn main:app --reload` in root to run the project.
- The REST API should be running on http://localhost:80.

## Deployment

The REST API is deployed to AWS using GitHub Actions.

[Click here to access it!](https://gw.project-x.pt/api/)
