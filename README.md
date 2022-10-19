# Unified Automation Framework #

This repository contains an approach to an automation framework that allows to run web, mobile and api test cases, all in a single framework.


### Project Structure ###
WIP
```
|____test_scripts
|...

```

## Getting Started ##

### Set up Virtual Environment ###

NOTE: pipenv is recommended over other virtual environment. Strongly recommended to use this one.

Pipenv is the recommended way to install Python packages and use a virtual environment because when you use the pip package
manager that's bundled with Python anything you install gets installed globally so you don't have encapsulated environments for each project that you create with Python. Whatever it maybe you want to have each project have its own environment and pipenv allows us to do that easily now before we would use virtually env to create a virtual environment and then run pip from within there but pipenv automatically creates and manages a virtual environment and it also allows us to easily add and remove packages using a pip file which is similar to a
package.json file if you're familiar with NodeJS.

[Configure a Pipenv environment | PyCharm (jetbrains.com)](https://www.jetbrains.com/help/pycharm/pipenv.html)

### Open the project with PyCharm and pipenv ###

Follow the instructions in this link to [set the pipenv as default](https://www.jetbrains.com/help/pycharm/pipenv.html#pipenv-existing-project)

### Install all dependencies ###

Open the bash or terminal console and run the following command. **NOTE: Do not use PowerShell if you're a Windows user**
```bash
pip install -r requirements.txt

pre-commit install
```


### XRAY Implementation ###
WIP 


### Commit Follow Standard ###
Project standard is 99 char per line using PEP8
On project dir follow the next command
Run pre-commit checker to format code, imports and check code standard:
```bash
pre-commit run --all-files
```
