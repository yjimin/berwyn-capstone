# berwyn-capstone

Do this in command line in your directory before running the cleaning script:

```
python3 -m venv venv
source .venv/bin/activate  # On macOS/Linux
.\venv\Scripts\activate   # On Windows
pip install -r requirements.txt
```

# When you make changes do this workflow:

1. Activate Virtual Environment:
```
source .venv/bin/activate  # On macOS/Linux
.\venv\Scripts\activate   # On Windows
```

2. Generate requirements.txt:
```
pip freeze > requirements.txt
```

3. Check the requirements.txt File:
Open the requirements.txt file to ensure it contains the list of installed packages and their versions.

# When you are done with making changes disconnect from venv

```
deactivate
```