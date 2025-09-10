```
python -m venv venv
```

```
venv/Scripts/activate
```

```
pip install -r requirements.txt
```

```
python manage.py runserver 0.0.0.0:8001
```

```
python .\manage.py makemigrations
```

```
python .\manage.py migrate
```

```
django-admin makemessages -a
```

```
django-admin compilemessages
```

```
python manage.py runserver_plus 0.0.0.0:8000 --cert-file cert.pem --key-file key.pem
```
http://127.0.0.1:8001/auth-test/
http://127.0.0.1:8001/cookie-demo/
http://127.0.0.1:8001/cart/
http://127.0.0.1:8001/products-ajax/
