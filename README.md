![alt text](https://user.oc-static.com/upload/2023/06/29/168805567091_LITrevu%20banner.png)

# LITRevu

Project 9: Develop a Web Application using Django

![[Pasted image 20240524175651.png]]

## Objective:

You now master Python programming best practices as well as user interface development.

It’s time to combine these two skills!

In this project, you will dive into the world of **Django**, a powerful framework for building web applications in Python. You will use **server-side rendering** to create dynamic and accessible user interfaces.

Your mission will be to create all the pages of the application by integrating essential features for users: registration, login, activity feed, comments, and subscriptions.

You will ensure that the application is developed following Django’s best practices for server-side rendering, database interaction, and user authentication.

## Requirements

### Venv
-for Windows:
```powershell
c:\>python -m venv .venv
```
-for linux:
```bash
python -m venv .venv
```
### Source activate
-for windows:
```powershell
c:\>.venv\Scripts\activate.bat
```
-for linux:
```python
source .venv/bin/activate
```

### install requirements
```python
pip install -r requirements.txt
```

If you encounter this error (using Manjaro):
```python
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try "pacman -S
    python-xyz", where xyz is the package you are trying to
    install.

```

try with this command:
```python
pip install -r requirements.txt --break-system-packages
```
## Flake8
```bash
#générer rapport flake8
flake8 --format=html --htmldir=flake8-rapport
```

### Start Django server:

If you use VSCodium and run on Linux:

- To activate the venv, start VSCodium in the LITRevu/ directory and start the Django server:
```bash
source start_working.sh
```
- Or if you just want to start the Django server:
```bash
sh src/lancement_server_django.sh
```

Otherwise, for others:

Linux/Mac:
```bash
python src/manage.py runserver
```

Windows:
```powershell
python src\manage.py runserver
```

You will see this message in your terminal:

![[Pasted image 20240524175309.png]]

Open your web browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

![[Pasted image 20240524175802.png]]

You can create your account or use this example user: username: "titi"
password: "azerty12345*"

You have multiple example users available in src/users.txt.

If you modify the models, don't forget to use these commands:

### Generate migrations

To create new migrations based on the changes made to the models, run:
```bash
python manage.py makemigrations
```

### Apply migrations

To apply the migrations and synchronize the database schema with the defined models, run:
```bash
python manage.py migrate
```


By combining these sections, you will have a clear and concise explanation of how to use `makemigrations` and `migrate` to manage migrations in Django.
