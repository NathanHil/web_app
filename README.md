# Pahlisch Web App
***Data Visualization and Management Web Application***

for use by Pahlisch Homes(C) Family of Brands
## Pre-requisites
***Optimized for use on linux-based systems***
- [Python](https://www.python.org/downloads/) version 3.x+ installed
- **pip** for dependency installation
	> **Note:** pip is already installed if you are using Python 2 >=2.7.9 or Python 3 >=3.4 downloaded from [python.org](https://www.python.org/) or if you are working in a [Virtual Environment](https://packaging.python.org/tutorials/installing-packages/#creating-and-using-virtual-environments "(in Python Packaging User Guide)") created by [virtualenv](https://packaging.python.org/key_projects/#virtualenv "(in Python Packaging User Guide)") or [venv](https://packaging.python.org/key_projects/#venv "(in Python Packaging User Guide)").
- Django version 3+ installed
	- ```pip install Django==3.2.4```
## Installation
- Once downloaded, enter the project folder
- Enter  ``python -m pip install -r requirements.txt``
- Once installed you should be able to successfully run all the ``python manage.py [command]`` [list of commands](https://gist.github.com/hezhao/d48ddc37579c25f46408)
## Running Django local server 
In your project's directory, type ``python manage.py runserver``
- Once your server is successfully running (ignoring warnings) visit localhost at port 8000: ``http://localhost:8000/``
	> **Note:** If styles and JS files are not loading properly, run ``python manage.py collectstatic`` and type 'yes' when prompted to overwrite the existing files
## Credits
Created and modified by [Matt Wilson](https://github.com/mattrw2) and [Nathan Hildebrandt](https://github.com/NathanHil) for Pahlisch Homes(C) Family of Brands
