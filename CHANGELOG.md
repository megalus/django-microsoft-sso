# Changelog

<!--next-version-placeholder-->

## v3.5.1 (2024-07-31)

### Fix

* Bug when combining email and user principal names, for upper and lower cases scenarios, during user creation ([`4a4d258`](https://github.com/megalus/django-microsoft-sso/commit/4a4d2587067f89b36cb0d1849208b47513556a9d))

## v3.5.0 (2024-07-30)

### Feature

* Add option to add all created users as admin staff ([`567f5aa`](https://github.com/megalus/django-microsoft-sso/commit/567f5aa11e7e1c8b9138427a986ad9e0a0d86822))

### Documentation

* Update docs ([`1f4c224`](https://github.com/megalus/django-microsoft-sso/commit/1f4c22451b6a04af6ca3b58f51809b5c31640020))

## v3.4.1 (2024-06-07)

### Fix

* Add support to Django USERNAME_FIELD ([`16e1a2f`](https://github.com/megalus/django-microsoft-sso/commit/16e1a2f4feacc0988f56b6bf5696eab895c112e6))

## v3.4.0 (2024-04-23)

### Feature

* Add more control on messaging ([`ff037c3`](https://github.com/megalus/django-microsoft-sso/commit/ff037c3e05fa7f27cf49266c6557359112217845))

## v3.3.1 (2024-04-09)

### Fix

* Add token in request before call pre-create callback ([`e6d2bb8`](https://github.com/megalus/django-microsoft-sso/commit/e6d2bb8afcf51c0533e545fc58f21a292e30f2eb))

## v3.3.0 (2024-04-09)

### Feature

* Add support to custom attributes in User model before creation. ([`acbc5f1`](https://github.com/megalus/django-microsoft-sso/commit/acbc5f1c25ba8b6716b950758dd7995853564a67))

## v3.2.0 (2024-03-14)

### Feature

* Change User unique index from mail to userPrincipalName ([`13d39fb`](https://github.com/megalus/django-microsoft-sso/commit/13d39fb1f8d7a478c3371dbc2e5dbb9903df58ca))

## v3.1.0 (2024-03-13)

### Feature

* Add support to custom token authorities ([`99a7e71`](https://github.com/megalus/django-microsoft-sso/commit/99a7e716304df271df2d8d0c372b0df424752667))

## v3.0.1 (2024-03-12)

### Fix

* Error when create a user with empty username when a user with no username already exists on database ([`a0cc158`](https://github.com/megalus/django-microsoft-sso/commit/a0cc158160b741cc4667f17351f24a9a6eed6046))

## v3.0.0 (2024-03-12)

### Feature

* Add basic support to custom login templates. ([`96ac7cf`](https://github.com/megalus/django-microsoft-sso/commit/96ac7cf3604fb24efc019780f0a8e5610b923660))

### Breaking

* Add basic support to custom login templates. ([`96ac7cf`](https://github.com/megalus/django-microsoft-sso/commit/96ac7cf3604fb24efc019780f0a8e5610b923660))

## v2.1.1 (2024-01-24)

### Fix

* Add missing optional args for initiate ([`5fc3c49`](https://github.com/megalus/django-microsoft-sso/commit/5fc3c497e318423d6479553bc63e465dc5a28dc6))

## v2.1.0 (2024-01-24)

### Feature

* Use microsoft official library ([`a8eeb21`](https://github.com/megalus/django-microsoft-sso/commit/a8eeb21b9e071de3b744185a4ffd5103a9cb766b))

## v2.0.1 (2023-12-22)

### Fix

* Remove debug logging ([`9c9e5de`](https://github.com/megalus/django-microsoft-sso/commit/9c9e5dea5d75a018fad679390318bf6b6b46d37e))

## v2.0.0 (2023-12-20)

### Feature

* New version ([`e4ef9cb`](https://github.com/megalus/django-microsoft-sso/commit/e4ef9cb1385d3aa0f0dc97d0c6137d6167c58d3b))

### Breaking

* * Remove Django 4.1 support * Add Django 5.0 support * Fix `SSO_USE_ALTERNATE_W003` bug * Fix several CSS issues with custom logo images * Update docs ([`e4ef9cb`](https://github.com/megalus/django-microsoft-sso/commit/e4ef9cb1385d3aa0f0dc97d0c6137d6167c58d3b))

### Documentation

* Small fix ([`53992c8`](https://github.com/megalus/django-microsoft-sso/commit/53992c82181f500546e7a08a131286914d1c6c23))

## v1.0.0 (2023-11-23)

### Feature

* V1.0 ([`838b62a`](https://github.com/megalus/django-microsoft-sso/commit/838b62ae74e85309a25ef7eab44a06e928951e83))

### Breaking

* This is the first public release ([`838b62a`](https://github.com/megalus/django-microsoft-sso/commit/838b62ae74e85309a25ef7eab44a06e928951e83))

## v3.3.0 (2023-09-27)

### Feature

* Add GOOGLE_SSO_SHOW_FORM_ON_ADMIN_PAGE option. ([`efc33cd`](https://github.com/megalus/django-google-sso/commit/efc33cd418e3a89044687c40788d195abc4a38a8))

### Documentation

* Update example in docs ([`0db95f8`](https://github.com/megalus/django-google-sso/commit/0db95f8388329fc7937b1e10299c74fb7ba2960a))
* Better docs ([`2b3e3cb`](https://github.com/megalus/django-google-sso/commit/2b3e3cb3e72a9e6f4ec2b3a03660439b8a83139d))

## v3.2.0 (2023-09-19)

### Feature

* Add GOOGLE_SSO_ALWAYS_UPDATE_USER_DATA option ([`a106fcf`](https://github.com/megalus/django-google-sso/commit/a106fcf166b1463ddf159112ffa0d43ee999868f))

### Documentation

* Update example code in admin.md ([`4c38551`](https://github.com/megalus/django-google-sso/commit/4c38551647b45ff55872929230ac8c8697bab137))

## v3.1.0 (2023-08-16)

### Feature

* Add option to save access token ([`cd23c76`](https://github.com/megalus/django-google-sso/commit/cd23c76010a589e0bbe56e4bbab673668394e378))
* Add new configuration parameters and fix bugs ([`3b26037`](https://github.com/megalus/django-google-sso/commit/3b26037c1ebe549d10b4a25533d5ed72ad4e4c99))

## v3.0.0 (2023-04-19)
### Feature
* Version 3.0 ([`24bfb2e`](https://github.com/megalus/django-google-sso/commit/24bfb2e5849f3a637de68193506c3a943fcdbba7))

### Breaking
*  ([`24bfb2e`](https://github.com/megalus/django-google-sso/commit/24bfb2e5849f3a637de68193506c3a943fcdbba7))

### Documentation
* Fix typo ([`08c782d`](https://github.com/megalus/django-google-sso/commit/08c782df65519afac67d4662f568b3b3841b26c2))
* Update docs ([`a2ef5b7`](https://github.com/megalus/django-google-sso/commit/a2ef5b7026a84e971b6a1b1bf3544e53c7bf60e5))

## v2.5.0 (2023-04-05)
### Feature
* Update to Django 4.2 ([`677a5da`](https://github.com/megalus/django-google-sso/commit/677a5da8c4d0815595e4aaa72c363f8feb409a93))

### Documentation
* Update Stela example ([`6ff6676`](https://github.com/megalus/django-google-sso/commit/6ff6676b04729ef8d2687ee7f54bd31e68cba3a0))
* Improve documentation ([`131f1b1`](https://github.com/megalus/django-google-sso/commit/131f1b10a1398cc17a8eec95feb571de3cf6a0c8))

## v2.4.1 (2023-02-25)
### Fix
* UserManager error when GOOGLE_SSO_AUTO_CREATE_USERS is set to False ([`4451c6b`](https://github.com/chrismaille/django-google-sso/commit/4451c6bf228e29cba14b11fd6ee17d9f2089cefd))
* **docs/how.md:** Add missing S with GOOGLE_SSO_AUTO_CREATE_USERS ([`3e9b661`](https://github.com/chrismaille/django-google-sso/commit/3e9b661eaec4693541b92f85de65129f18bc3fe2))

## v2.4.0 (2023-01-23)
### Feature
* Add GOOGLE_SSO_PRE_LOGIN_CALLBACK feature ([`44ade37`](https://github.com/chrismaille/django-google-sso/commit/44ade37ce4f65a530562da4edbdc4c5d122d9f85))

## v2.3.1 (2023-01-18)
### Fix
* Small fixes ([`1ec44cc`](https://github.com/chrismaille/django-google-sso/commit/1ec44cc5f6080e8de67a0548b3af647ba96cc262))

## v2.3.0 (2022-10-28)
### Feature
* Release 2.3.0 ([`8ef3b04`](https://github.com/chrismaille/django-google-sso/commit/8ef3b04e2c096338c4b92126ebbf4f6cfac0d208))
* Add new settings option GOOGLE_SSO_AUTHENTICATION_BACKEND ([`4212782`](https://github.com/chrismaille/django-google-sso/commit/4212782eae4c1400e1d9634b79df83f4a5d36f3d))

## v2.2.0 (2022-09-06)
### Feature
* Make Sites Framework optional ([`e5a3839`](https://github.com/chrismaille/django-google-sso/commit/e5a38395b68ca4614b67cc5868c5adfd2a504f82))

## v2.1.0 (2022-09-02)
### Feature
* Add new settings option GOOGLE_SSO_CALLBACK_DOMAIN ([`4b49059`](https://github.com/chrismaille/django-google-sso/commit/4b490596a0e2efc47f3067628bb939d832da5ae5))

## v2.0.0 (2022-02-23)
### Feature
* Add django 4 support ([`dcb5f9f`](https://github.com/chrismaille/django-google-sso/commit/dcb5f9ff2329e54f38985cfb2eb1c0edd06ebf5a))

### Breaking
* update tests and example app  ([`dcb5f9f`](https://github.com/chrismaille/django-google-sso/commit/dcb5f9ff2329e54f38985cfb2eb1c0edd06ebf5a))

## v1.0.2 (2022-02-23)
### Fix
* Change license to MIT ([`750f979`](https://github.com/chrismaille/django-google-sso/commit/750f9791dcc7057359da08b69774515b63a3578d))

## v1.0.1 (2021-11-23)
### Fix
* Update Django Classifiers ([`17664cb`](https://github.com/chrismaille/django-google-sso/commit/17664cb89430f2be730b859a3d5926acb708300c))

### Documentation
* Add `login_required` use example and add Django Classifiers ([`fccc7b6`](https://github.com/chrismaille/django-google-sso/commit/fccc7b62174a2898e93a0ad483ffe014884b538c))
* Update README.md ([`c2e6c3b`](https://github.com/chrismaille/django-google-sso/commit/c2e6c3b17388f9ac7d5442f3d780cc2859071afd))

## v1.0.0 (2021-11-22)
### Feature
* First Release ([`54d979f`](https://github.com/chrismaille/django-google-sso/commit/54d979f06c76f6985483d642823f85c006776b19))

### Breaking
* This is version 1.0. To find additional information please check README.md file.  ([`54d979f`](https://github.com/chrismaille/django-google-sso/commit/54d979f06c76f6985483d642823f85c006776b19))

## v0.2.1 (2021-11-20)
### Fix
* Unit test ([`220920c`](https://github.com/chrismaille/django-google-sso/commit/220920cef5913bd24e78fe4da379b66b037078df))

## v0.2.0 (2021-11-20)
### Feature
* Add alpha version ([`98c78e5`](https://github.com/chrismaille/django-google-sso/commit/98c78e589016948f352c67849e36d937c455456e))
