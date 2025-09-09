## Django Example App

## Start the Project

Please create a `.env.local` file with the following information:

```dotenv
MICROSOFT_SSO_ALLOWABLE_DOMAINS=["<your email domain>"]
MICROSOFT_SSO_APPLICATION_ID=<your registered app id>
MICROSOFT_SSO_CLIENT_SECRET=<your client secret>
```

Then run the following commands:

```shell
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver
```

Open browser in `http://localhost:8000/admin`

## Django Admin skins

Please uncomment on `settings.py` the correct app for the skin you want to test, in `INSTALLED_APPS`.

For `django-unfold` please rename the following css files:

* `example_microsoft_app/static/django_microsoft_sso/microsoft_button_unfold.css` to `static/django_microsoft_sso/microsoft_button.css`
* `example_microsoft_app/static/django_google_sso/google_button_unfold.css` to `static/django_google_sso/google_button.css`
