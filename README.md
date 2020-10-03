# College Fest Management

Manage college fest registrations with Realtime Analytics.

## Installation 
[![Pip](https://www.python.org/static/community_logos/python-powered-h-50x65.png)](https://pip.pypa.io/en/stable/)

- Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all the dependencies. 

```bash
pip install -r requirements.txt
```

- After executing pip install make sure Django is installed by the following command
```bash
python -m django --version
``` 
## Usage
### Running The Application API Server


```python
django-admin startproject TechTrixManager
```
### Running DataBase Migrations
```python
python manage.py makemigrations
```

### Create Django Admin Superuser
```python
python manage.py createsuperuser
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)