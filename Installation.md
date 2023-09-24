# Installation

Clone the GitHub repository

```
git clone https://github.com/napon2545/ku-polls.git
```

Creating a virtual environment

```
python -m venv env
```

Activate a virtual environment

*Window
```
.\venv\Scripts\activate
```
*macOS and Linux
```
source venv/bin/activate
```

Install the required libraries from "requirements.txt"

```
pip install -r requirements.txt
```

Migrate a django application
```
python manage.py migrate
```

Run tests
```
python manage.py test
```

Load the json data

```
python manage.py loaddata data/polls.json
python manage.py loaddata data/polls-v1.json
python manage.py loaddata data/users.json
```
