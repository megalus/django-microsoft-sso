# How Django Microsoft SSO works?

## Current Flow

1. First, the user is redirected to the Django login page. If settings `MICROSOFT_SSO_ENABLED` is True, the
"Login with Microsoft" button will be added to a default form.

2. On click, **Django-Microsoft-SSO** will add, in a anonymous request session, the `sso_next_url` and Microsoft Auth info.
This data will expire in 10 minutes. Then user will be redirected to Microsoft login page.

    !!! info "Using Request Anonymous session"
        If you make any actions which change or destroy this session, like restart django, clear cookies or change
        browsers, the login will fail, and you can see the message "State Mismatched. Time expired?" in the next time
        you log in again.

3. On callback, **Django-Microsoft-SSO** will check `code` and `state` received. If they are valid,
Microsoft's UserInfo will be retrieved. If the user is already registered in Django, the user
will be logged in. The Graph request has a timeout of 10 seconds, defined in `MICROSOFT_SSO_GRAPH_TIMEOUT`.

4. Otherwise, the user will be created and logged in, if his email domain,
matches one of the `MICROSOFT_SSO_ALLOWABLE_DOMAINS`. You can disable the auto-creation setting `MICROSOFT_SSO_AUTO_CREATE_USERS`
to False.

5. On creation only, this user can be set to the`staff` or `superuser` status, if his email are in `MICROSOFT_SSO_STAFF_LIST` or
`MICROSOFT_SSO_SUPERUSER_LIST` respectively. Please note if you add an email to one of these lists, the email domain
must be added to `MICROSOFT_SSO_ALLOWABLE_DOMAINS`too.

6. This authenticated session will expire in 1 hour, or the time defined, in seconds, in `MICROSOFT_SSO_SESSION_COOKIE_AGE`.

7.  If login fails, you will be redirected to route defined in `MICROSOFT_SSO_LOGIN_FAILED_URL` (default: `admin:index`)
which will use Django Messaging system to show the error message.

8. If login succeeds, the user will be redirected to the `next_path` saved in the anonymous session, or to the route
defined in `MICROSOFT_SSO_NEXT_URL` (default: `admin:index`) as a fallback.
