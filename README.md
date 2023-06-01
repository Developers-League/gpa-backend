<h3 align="center">GPA Selfcare Backend</h3>

<div align="center">

  ![Status](https://img.shields.io/badge/status-active-success.svg)
  ![GitHub issues](https://img.shields.io/github/issues/Developers-League/gpa-backend?color=yellow)
  ![GitHub pull requests](https://img.shields.io/github/issues-pr/Developers-League/gpa-backend?color=success)
  [![License](https://img.shields.io/badge/license-Proprietary-blue.svg)](/LICENSE)


</div>

---

<p align="center"> Backend API for the GPA Selfcare
    <br> 
</p>

## 📝 Table of Contents
- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Built Using](#built_using)
- [Team](#team)


## About <a name = "about"></a>
This project is a GPA Selfcare API for Developers League. It is built using [these](#built_using) technologies.

## 🏁 Getting Started <a name = "getting_started"></a>
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
- Poetry
- Python 3.10^
- Flake8


### Setting up a development environment
#### Step 1: Clone the repository

```bash
https://github.com/Developers-League/gpa-backend.git
```

or with GithubCLI
  
```bash
gh repo clone Developers-League/gpa-backend
```

#### step 2: Install poetry if you don't have it already

```bash
# Linux, macOS, Windows (WSL)
curl -sSL https://install.python-poetry.org | python3 -
```

```bash
# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

> _Note: If you have installed Python through the Microsoft Store, replace py with python in the command above._

> _Reference: [Poetry Installation](https://python-poetry.org/docs/#installation)_

#### step 3: Create a virtual environment

```bash
poetry shell
```

#### Step 4: Install dependencies

```
poetry install
```

> Note to add a package to the project, run

```bash
poetry add <package-name>
```

#### Step 7: Start the uvicorn server

```bash
uvicorn main:app --reload
```


## 🔧 Running the tests <a name = "tests"></a>
Explain how to run the automated tests for this system.

## 🎈 Usage <a name="usage"></a>
visit the API Documentation at [docs](http://127.0.0.1:8000/docs)


## ⛏️ Built Using <a name = "built_using"></a>
- [FastAPI](https://fastapi.tiangolo.com/) - Python Framework
- [Poetry](https://python-poetry.org/) - Python Package Manager
- [Pytest](https://docs.pytest.org/en/6.2.x/) - Testing Framework

## ✍️ Team <a name = "team"></a>
- [@GreatnessMensah](https://github.com/greatnessmensah)
- [@Adehwam21](https://github.com/Adehwam21)
- [@Daquiver1](https://github.com/Daquiver1)
