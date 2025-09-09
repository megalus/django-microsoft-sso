# CHANGELOG


## v6.0.0 (2025-09-09)

### Breaking

* feat!: Version 6.0 - BREAKING CHANGE

* Add support to Django 5.2
* SSO configuration can be defined per request now
* SSO Tags can be customized in views now.
* Fix PEP 562 for django_microsoft_sso.conf
* Use Django's EMAIL_FIELD to determine email field in User ([`5e1502c`](https://github.com/megalus/django-microsoft-sso/commit/5e1502c82f73692c1addb343d2fd46efca81a218))

### Chores

* chore: additional fixes after PR ([`cdd4f53`](https://github.com/megalus/django-microsoft-sso/commit/cdd4f534e0fd6ecc535a322861aa0a20bd68ec08))

* chore: fixes from PR ([`484b675`](https://github.com/megalus/django-microsoft-sso/commit/484b6757b205385e0af37cb8b4c36ecc04f2e963))

* chore: update Makefile, pre-commit config, and docs for project setup and guidelines ([`f6f56a7`](https://github.com/megalus/django-microsoft-sso/commit/f6f56a7fecb6425461fb50bac65ef987f04c5e60))

### Continuous Integration

* ci: fix lint ([`25b51e1`](https://github.com/megalus/django-microsoft-sso/commit/25b51e1a184995ed6370293e55c9d88d798034ef))

### Documentation

* docs: add coding guidelines and project instructions ([`b689bd0`](https://github.com/megalus/django-microsoft-sso/commit/b689bd0f720f65bbb72499b77cc84852824c9d74))

* docs: expand and clarify coding guidelines across multiple sections ([`795ce78`](https://github.com/megalus/django-microsoft-sso/commit/795ce7865bd5f1919f087e8ce0ed799bd3f13808))

* docs: Add section on blocking admin password authentication. ([`ce49593`](https://github.com/megalus/django-microsoft-sso/commit/ce495933331ef09dfa2d59e592fa49abbfc76d92))

### Unknown

* Merge pull request #20 from megalus/v6

Version 6.0 ([`f3e5619`](https://github.com/megalus/django-microsoft-sso/commit/f3e561918e269c2f95a67256c7dda3eaea6200c0))

* Merge pull request #19 from megalus/develop

Develop ([`7344401`](https://github.com/megalus/django-microsoft-sso/commit/7344401f4ab8387ffb4d2a1166ebc61e57f717b8))

* Merge pull request #18 from rajee-a/patch-1

Update button name to Microsoft ([`67337d9`](https://github.com/megalus/django-microsoft-sso/commit/67337d9348f48323cf35dba66e92098d767d0cd7))

* Update button name to Microsoft

typo fixed ([`4751b8a`](https://github.com/megalus/django-microsoft-sso/commit/4751b8ad11839ba0e704af361207c381b2847c40))

* Merge pull request #16 from noamkush/docs-admin-password

docs: Add section on blocking admin password authentication. ([`dbb84ef`](https://github.com/megalus/django-microsoft-sso/commit/dbb84ef3fd2e32e9d2e836f94fbd1079cfe008fc))


## v5.1.0 (2025-01-14)

### Features

* feat: add wildcard support to MICROSOFT_SSO_ALLOWABLE_DOMAINS

Fixes #15 ([`7ecdac1`](https://github.com/megalus/django-microsoft-sso/commit/7ecdac1968cd165f7e5f332369e12792b68ae76e))


## v5.0.0 (2024-10-09)

### Breaking

* feat!: Add support to Python 3.13

This is a BREAKING CHANGE commit. Changes:

* Add support to 3.13
* Remove support to 3.10
* Add new option `MICROSOFT_SSO_GRAPH_TIMEOUT`
 * Update GitHub Actions ([`6718685`](https://github.com/megalus/django-microsoft-sso/commit/671868572245211192e92c58e6cad346a0cd0902))

### Continuous Integration

* ci: fix github actions ([`26dffbf`](https://github.com/megalus/django-microsoft-sso/commit/26dffbf3a0f0761b60f054c37aa35728ab4d043d))

### Documentation

* docs: update docs ([`e5a46f5`](https://github.com/megalus/django-microsoft-sso/commit/e5a46f5100722fcb6184b2ebb98b2d2449c81d1b))

* docs: update docs ([`7cd19ce`](https://github.com/megalus/django-microsoft-sso/commit/7cd19cebd43267a4efbec81d9c7c01fb1dc62c13))

* docs: update docs ([`65168bb`](https://github.com/megalus/django-microsoft-sso/commit/65168bbf80693d7714c53a51de95eb8fae6b1e30))

### Unknown

* Merge pull request #14 from megalus/develop

feat!: Add support to Python 3.13 ([`17c5ed3`](https://github.com/megalus/django-microsoft-sso/commit/17c5ed3df5d6a68768dc45ad743520daab073b1f))


## v4.1.0 (2024-09-17)

### Features

* feat: Add new option MICROSOFT_SSO_SHOW_FAILED_LOGIN_MESSAGE

Also failed attempts to create user in database will be logged on terminal ([`abbc1b4`](https://github.com/megalus/django-microsoft-sso/commit/abbc1b4f02a2ebf2c8b1da6b4e0ec81e88ca17b2))


## v4.0.0 (2024-08-29)

### Breaking

* feat!: Add new options and update versions

Changes:
* Remove support for Django 4.1
* Add support for Django 5.1
* Add option `MICROSOFT_SSO_PRE_VALIDATE_CALLBACK`
* Add option `MICROSOFT_SSO_SAVE_BASIC_MICROSOFT_INFO`
* Update docs

This is a BREAKING CHANGE commit. ([`9250b51`](https://github.com/megalus/django-microsoft-sso/commit/9250b516094594d2730257ef5fa46ee65d349876))


## v3.5.1 (2024-07-31)

### Fixes

* fix: bug when combining email and user principal names, for upper and lower cases scenarios, during user creation ([`4a4d258`](https://github.com/megalus/django-microsoft-sso/commit/4a4d2587067f89b36cb0d1849208b47513556a9d))


## v3.5.0 (2024-07-30)

### Documentation

* docs: update docs ([`1f4c224`](https://github.com/megalus/django-microsoft-sso/commit/1f4c22451b6a04af6ca3b58f51809b5c31640020))

### Features

* feat: add option to add all created users as admin staff

Also fix avoid duplicate users when email is not lowercase ([`567f5aa`](https://github.com/megalus/django-microsoft-sso/commit/567f5aa11e7e1c8b9138427a986ad9e0a0d86822))

### Unknown

* Merge pull request #12 from megalus/develop

Feat: Add option in include all users as staff ([`cb8f55b`](https://github.com/megalus/django-microsoft-sso/commit/cb8f55b593b925d027f6859ba8e5c9afed0ad9bc))

* Merge pull request #11 from darkjonas88/Wildcard_Staff_user_creation

Creation of a wildcard for is staff flag for admin. ([`3500e27`](https://github.com/megalus/django-microsoft-sso/commit/3500e27f66e620e1920fc35907c10707a46503b9))

* Insensitive case for the filter ([`088edbc`](https://github.com/megalus/django-microsoft-sso/commit/088edbc110f8d82c93581e09e26ac1a4bacd2327))

* Forcing email to lower case  so that there aren't duplicate accounts ([`1e1b6c6`](https://github.com/megalus/django-microsoft-sso/commit/1e1b6c6332057a5ffda27ed67335eac58500b092))

* Creation of a wildcard for is staff flag for admin. ([`904bc34`](https://github.com/megalus/django-microsoft-sso/commit/904bc347442ad972dee5784c0577ac494bd9ace5))

* Merge pull request #10 from megalus/develop

Docs: Update Docs for initial setup ([`6a289aa`](https://github.com/megalus/django-microsoft-sso/commit/6a289aa355f1c9f444f32125497b7da801dbe959))

* Merge pull request #9 from illgitthat/main

(minor) Docs update for some initial setup errors ([`84b0f1a`](https://github.com/megalus/django-microsoft-sso/commit/84b0f1a41a59e6ff83882f8e76b8cae41647911c))

* (minor) Docs update for some initial setup errors ([`8c6c9d6`](https://github.com/megalus/django-microsoft-sso/commit/8c6c9d66c27835f9080bd5c744801952763cb16b))


## v3.4.1 (2024-06-07)

### Fixes

* fix: Add support to Django USERNAME_FIELD ([`16e1a2f`](https://github.com/megalus/django-microsoft-sso/commit/16e1a2f4feacc0988f56b6bf5696eab895c112e6))


## v3.4.0 (2024-04-23)

### Features

* feat: add more control on messaging

Use the `MICROSOFT_SSO_ENABLE_LOGS` to enable/disable logs. Logs now will show all info send to django messages.

Use the `MICROSOFT_SSO_ENABLE_MESSAGES` to enable/disable django messages. ([`ff037c3`](https://github.com/megalus/django-microsoft-sso/commit/ff037c3e05fa7f27cf49266c6557359112217845))


## v3.3.1 (2024-04-09)

### Fixes

* fix: add token in request before call pre-create callback ([`e6d2bb8`](https://github.com/megalus/django-microsoft-sso/commit/e6d2bb8afcf51c0533e545fc58f21a292e30f2eb))


## v3.3.0 (2024-04-09)

### Features

* feat: Add support to custom attributes in User model before creation.

    Use the `MICROSOFT_SSO_PRE_CREATE_CALLBACK` setting to define a custom function which can return a dictionary which will be used during user creation for the `defaults` value. ([`acbc5f1`](https://github.com/megalus/django-microsoft-sso/commit/acbc5f1c25ba8b6716b950758dd7995853564a67))


## v3.2.0 (2024-03-14)

### Chores

* chore: check for different null values in Azure response ([`6e4fa9b`](https://github.com/megalus/django-microsoft-sso/commit/6e4fa9b245e413c34e952943ab75453226d979b8))

* chore: return empty string instead of None for optional azure fields ([`5a3c412`](https://github.com/megalus/django-microsoft-sso/commit/5a3c4124718877595c75ffa984013035dd585e4c))

### Features

* feat: change User unique index from mail to userPrincipalName

This means the lib will check for the `user.username` field to decide when to get or create a user. This is needed to work with tenant users with no email address saved.

If you want to enforce unique email addresses in your database (checking against `user.email`) please set the option `MICROSOFT_SSO_UNIQUE_EMAIL=True` ([`13d39fb`](https://github.com/megalus/django-microsoft-sso/commit/13d39fb1f8d7a478c3371dbc2e5dbb9903df58ca))

### Unknown

* Merge pull request #7 from megalus/develop

Change unique index to username ([`936ddac`](https://github.com/megalus/django-microsoft-sso/commit/936ddacb01564c0ebdf7d399b3225c675b37930c))

* Merge pull request #5 from darqs1/patch-1

Update main.py ([`83aef24`](https://github.com/megalus/django-microsoft-sso/commit/83aef242b42d63b4ff39dae3c102d54a2a129828))

* Update main.py

line 153: added if user_mail is None use upn instead of mail. ([`57560a8`](https://github.com/megalus/django-microsoft-sso/commit/57560a80e11947240878c3ce2b8854c90ec201c7))


## v3.1.0 (2024-03-13)

### Features

* feat: Add support to custom token authorities

Use the MICROSOFT_SSO_AUTHORITY passing the full authority URL (like: `https://login.microsoftonline.com/your_tenant`) or a `AuthorityBuilder` instance. ([`99a7e71`](https://github.com/megalus/django-microsoft-sso/commit/99a7e716304df271df2d8d0c372b0df424752667))

### Unknown

* Merge pull request #3 from megalus/develop

New Release ([`31b46a4`](https://github.com/megalus/django-microsoft-sso/commit/31b46a40eb766c3e3c148c1fe3b206f5e667f765))

* Merge pull request #2 from darqs1/main

Added MICROSOFT_SSO_AUTHORITY ([`4dbb5c2`](https://github.com/megalus/django-microsoft-sso/commit/4dbb5c2ea712d9dc98203e252fb54e8337b14bbe))

* docs added ([`230b95f`](https://github.com/megalus/django-microsoft-sso/commit/230b95f55d80d7c07432ba562f3bd572e8bc997e))

* Added MICROSOFT_SSO_AUTHORITY ([`4c95903`](https://github.com/megalus/django-microsoft-sso/commit/4c959036e86868df7563d9b8b20048ee0011da36))


## v3.0.1 (2024-03-12)

### Fixes

* fix: error when create a user with empty username when a user with no username already exists on database ([`a0cc158`](https://github.com/megalus/django-microsoft-sso/commit/a0cc158160b741cc4667f17351f24a9a6eed6046))


## v3.0.0 (2024-03-12)

### Breaking

* feat!: Add basic support to custom login templates.

Rework the login.html and login_sso.html to simplify login template customization. The use case is the [Django Unfold](https://github.com/unfoldadmin/django-unfold) package. This is a BREAKING CHANGE for the static and html files.

Also:
* Remove pytest-lazy-fixture to upgrade pytest to latest version ([`96ac7cf`](https://github.com/megalus/django-microsoft-sso/commit/96ac7cf3604fb24efc019780f0a8e5610b923660))


## v2.1.1 (2024-01-24)

### Fixes

* fix: Add missing optional args for initiate

Call initiate passing custom scopes or redirect. Pending documentation. ([`5fc3c49`](https://github.com/megalus/django-microsoft-sso/commit/5fc3c497e318423d6479553bc63e465dc5a28dc6))


## v2.1.0 (2024-01-24)

### Chores

* chore: Better Stela use

Also add missing tests in GitHub Actions ([`09c58ca`](https://github.com/megalus/django-microsoft-sso/commit/09c58ca9e4efaf3ac116de037929309be43db0da))

### Features

* feat: use microsoft official library

Replacing `identity` for `msal`. The previous library is good, but out intent here is to reduce the number of dependencies involved in case Microsoft rewrites its sign-in process. ([`a8eeb21`](https://github.com/megalus/django-microsoft-sso/commit/a8eeb21b9e071de3b744185a4ffd5103a9cb766b))


## v2.0.1 (2023-12-22)

### Fixes

* fix: remove debug logging ([`9c9e5de`](https://github.com/megalus/django-microsoft-sso/commit/9c9e5dea5d75a018fad679390318bf6b6b46d37e))


## v2.0.0 (2023-12-20)

### Breaking

* feat!: New version

BREAKING CHANGE:
* Remove Django 4.1 support
* Add Django 5.0 support
* Fix `SSO_USE_ALTERNATE_W003` bug
* Fix several CSS issues with custom logo images
* Update docs ([`e4ef9cb`](https://github.com/megalus/django-microsoft-sso/commit/e4ef9cb1385d3aa0f0dc97d0c6137d6167c58d3b))

### Documentation

* docs: small fix ([`53992c8`](https://github.com/megalus/django-microsoft-sso/commit/53992c82181f500546e7a08a131286914d1c6c23))


## v1.0.0 (2023-11-23)

### Breaking

* feat!: v1.0

BREAKING CHANGE: This is the first public release ([`838b62a`](https://github.com/megalus/django-microsoft-sso/commit/838b62ae74e85309a25ef7eab44a06e928951e83))

### Chores

* chore: normalize temp version ([`fc43178`](https://github.com/megalus/django-microsoft-sso/commit/fc431781bf6c126a4098ec7ae697abec25d34a91))

* chore: update docs ([`b9c633b`](https://github.com/megalus/django-microsoft-sso/commit/b9c633b830f22307ea54d5b789da38e0c19ed267))

* chore: fix failed merge ([`34b533e`](https://github.com/megalus/django-microsoft-sso/commit/34b533ee59723205e4bd22c0d7380a5f36468bfa))

### Unknown

* fix merge ([`07f41b8`](https://github.com/megalus/django-microsoft-sso/commit/07f41b82769525d060f2a29caf2cf18feaf192df))

* Initial commit ([`23fb8e9`](https://github.com/megalus/django-microsoft-sso/commit/23fb8e97c22b8285ee89c504d9df1b4f4139e924))
