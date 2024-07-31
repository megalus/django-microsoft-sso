import importlib
from copy import deepcopy

import pytest
from django.contrib.auth.models import User

from django_microsoft_sso import conf
from django_microsoft_sso.main import UserHelper

pytestmark = pytest.mark.django_db


def test_user_email(microsoft_response, callback_request):
    # Act
    helper = UserHelper(microsoft_response, callback_request)

    # Assert
    assert helper.user_email == "kalel@dailyplanet.com"


@pytest.mark.parametrize(
    "allowable_domains, expected_result", [(["dailyplanet.com"], True), ([], False)]
)
def test_email_is_valid(
    microsoft_response, callback_request, allowable_domains, expected_result, settings
):
    # Arrange
    settings.MICROSOFT_SSO_ALLOWABLE_DOMAINS = allowable_domains
    importlib.reload(conf)

    # Act
    helper = UserHelper(microsoft_response, callback_request)

    # Assert
    assert helper.email_is_valid == expected_result


@pytest.mark.parametrize("auto_create_super_user", [True, False])
def test_get_or_create_user(
    auto_create_super_user, microsoft_response, callback_request, settings
):
    # Arrange
    settings.MICROSOFT_SSO_AUTO_CREATE_FIRST_SUPERUSER = auto_create_super_user
    importlib.reload(conf)

    # Act
    helper = UserHelper(microsoft_response, callback_request)
    user = helper.get_or_create_user()

    # Assert
    assert user.first_name == microsoft_response["givenName"]
    assert user.last_name == microsoft_response["surname"]
    assert user.username == microsoft_response["userPrincipalName"]
    assert user.email == microsoft_response["mail"]
    assert user.is_active is True
    assert user.is_staff == auto_create_super_user
    assert user.is_superuser == auto_create_super_user


@pytest.mark.parametrize(
    "always_update_user_data, expected_is_equal", [(True, True), (False, False)]
)
def test_update_existing_user_record(
    always_update_user_data,
    callback_request,
    expected_is_equal,
    microsoft_response,
    microsoft_response_update,
    settings,
):
    # Arrange
    settings.MICROSOFT_SSO_ALWAYS_UPDATE_USER_DATA = always_update_user_data
    importlib.reload(conf)
    helper = UserHelper(microsoft_response, callback_request)
    helper.get_or_create_user()

    # Act
    helper = UserHelper(microsoft_response_update, callback_request)
    user = helper.get_or_create_user()

    # Assert
    assert (user.first_name == microsoft_response_update["givenName"]) == expected_is_equal
    assert (user.last_name == microsoft_response_update["surname"]) == expected_is_equal
    assert user.email == microsoft_response_update["mail"]


@pytest.mark.parametrize("use_email", [True, False])
def test_create_staff_from_list(
    microsoft_response, callback_request, settings, use_email, monkeypatch
):
    # Arrange
    monkeypatch.setattr(conf, "MICROSOFT_SSO_UNIQUE_EMAIL", use_email)
    settings.MICROSOFT_SSO_STAFF_LIST = [microsoft_response["mail"]]
    ms_response = deepcopy(microsoft_response)
    if not use_email:
        del ms_response["mail"]
        settings.MICROSOFT_SSO_STAFF_LIST = [microsoft_response["userPrincipalName"]]
    settings.MICROSOFT_SSO_AUTO_CREATE_FIRST_SUPERUSER = False
    importlib.reload(conf)

    # Act
    helper = UserHelper(ms_response, callback_request)
    helper.get_or_create_user()
    user = helper.find_user()

    # Assert
    assert user.is_active is True
    assert user.is_staff is True
    assert user.is_superuser is False


def test_add_all_users_to_staff_list(faker, microsoft_response, callback_request, settings):
    # Arrange
    settings.MICROSOFT_SSO_STAFF_LIST = ["*"]
    settings.MICROSOFT_SSO_AUTO_CREATE_FIRST_SUPERUSER = False
    importlib.reload(conf)

    emails = [
        faker.email(),
        faker.email(),
        faker.email(),
    ]

    # Act
    for email in emails:
        response = deepcopy(microsoft_response)
        response["mail"] = email
        response["userPrincipalName"] = email
        helper = UserHelper(response, callback_request)
        helper.get_or_create_user()
        helper.find_user()

    # Assert
    assert User.objects.filter(is_staff=True).count() == 3


def test_create_super_user_from_list(microsoft_response, callback_request, settings):
    # Arrange
    settings.MICROSOFT_SSO_AUTO_CREATE_FIRST_SUPERUSER = False
    settings.MICROSOFT_SSO_SUPERUSER_LIST = [microsoft_response["mail"]]
    importlib.reload(conf)

    # Act
    helper = UserHelper(microsoft_response, callback_request)
    user = helper.get_or_create_user()

    # Assert
    assert user.is_active is True
    assert user.is_staff is True
    assert user.is_superuser is True


@pytest.mark.parametrize(
    "unique_email",
    [True, False],
)
def test_create_user_without_email_address(
    microsoft_response, callback_request, unique_email, monkeypatch
):
    # Arrange
    microsoft_response_no_email = deepcopy(microsoft_response)
    del microsoft_response_no_email["mail"]
    helper = UserHelper(microsoft_response_no_email, callback_request)
    monkeypatch.setattr(conf, "MICROSOFT_SSO_UNIQUE_EMAIL", unique_email)

    if unique_email:
        # Act/Assert
        with pytest.raises(ValueError):
            helper.get_or_create_user()
    else:
        # Act
        helper.get_or_create_user()
        user = helper.find_user()

        # Assert
        assert user.email == ""
        assert user.username == microsoft_response_no_email["userPrincipalName"]


def test_different_null_values(microsoft_response, callback_request, monkeypatch):
    # Arrange
    microsoft_response_no_key = deepcopy(microsoft_response)
    del microsoft_response_no_key["mail"]
    microsoft_response_key_none = deepcopy(microsoft_response)
    microsoft_response_key_none["mail"] = None

    # Act
    no_key_helper = UserHelper(microsoft_response_no_key, callback_request)
    no_key_helper.get_or_create_user()
    user_one = no_key_helper.find_user()

    none_key_helper = UserHelper(microsoft_response_key_none, callback_request)
    none_key_helper.get_or_create_user()
    user_two = none_key_helper.find_user()

    # Assert
    assert user_one.email == ""
    assert user_one.username == microsoft_response_no_key["userPrincipalName"]
    assert user_two.email == ""
    assert user_two.username == microsoft_response_key_none["userPrincipalName"]


def test_duplicated_emails(microsoft_response, callback_request, settings):
    # Arrange
    User.objects.create(
        email=microsoft_response["mail"].upper(),
        username=microsoft_response["userPrincipalName"].upper(),
        first_name=microsoft_response["givenName"],
        last_name=microsoft_response["surname"],
    )

    lowercase_email_response = deepcopy(microsoft_response)
    lowercase_email_response["mail"] = lowercase_email_response["mail"].lower()
    lowercase_email_response["userPrincipalName"] = lowercase_email_response[
        "userPrincipalName"
    ].lower()
    uppercase_email_response = deepcopy(microsoft_response)
    uppercase_email_response["mail"] = uppercase_email_response["mail"].upper()
    uppercase_email_response["userPrincipalName"] = uppercase_email_response[
        "userPrincipalName"
    ].upper()

    # Act
    user_one_helper = UserHelper(uppercase_email_response, callback_request)
    user_one_helper.get_or_create_user()
    user_one = user_one_helper.find_user()

    user_two_helper = UserHelper(lowercase_email_response, callback_request)
    user_two_helper.get_or_create_user()
    user_two = user_two_helper.find_user()

    # Assert
    assert user_one.id == user_two.id
    assert user_one.email == user_two.email
    assert User.objects.count() == 1
