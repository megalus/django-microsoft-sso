import importlib

import pytest

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


def test_create_staff_from_list(microsoft_response, callback_request, settings):
    # Arrange
    settings.MICROSOFT_SSO_AUTO_CREATE_FIRST_SUPERUSER = False
    settings.MICROSOFT_SSO_STAFF_LIST = [microsoft_response["mail"]]
    importlib.reload(conf)

    # Act
    helper = UserHelper(microsoft_response, callback_request)
    user = helper.get_or_create_user()

    # Assert
    assert user.is_active is True
    assert user.is_staff is True
    assert user.is_superuser is False


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
