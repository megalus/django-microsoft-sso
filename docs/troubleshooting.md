# Troubleshooting Guide

### Common errors:

??? question "Admin Message: _**State Mismatched. Time expired?**_"
    This error occurs when the user is redirected to the Google login page and then returns to the Django login page but
    original state are not found. Please check if the browser has the anonymous session created by Django.

??? question "My callback URL is http://example.com/microsoft_sso/callback/ but my project is running at http://localhost:8000"
    This error occurs because your Project is using the Django Sites Framework and the current site is not configured correctly.
    Please make sure that the current site is configured for your needs or, alternatively, use the `MICROSOFT_SSO_CALLBACK_DOMAIN` setting.

??? question "There's too much information on logs and messages from this app."
    You can disable the logs using the `MICROSOFT_SSO_ENABLE_LOGS` setting and the messages using the `MICROSOFT_SSO_ENABLE_MESSAGES` setting.

### Example App

To test this library please check the `Example App` provided [here](https://github.com/megalus/django-microsoft-sso/tree/main/example_microsoft_app).

### Not working?

Don't panic. Get a towel and, please, open an [issue](https://github.com/megalus/django-microsoft-sso/issues).
