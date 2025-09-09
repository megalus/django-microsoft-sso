import pytest

from django_microsoft_sso.main import UserHelper

pytestmark = pytest.mark.django_db(transaction=True)


def test_microsoft_sso_model(microsoft_response, callback_request):
    # Act
    helper = UserHelper(microsoft_response, callback_request)
    user = helper.get_or_create_user()

    # Assert
    assert user.microsoftssouser.microsoft_id == microsoft_response["id"]
    assert user.microsoftssouser.picture_raw == microsoft_response["picture_raw_data"]
    assert user.microsoftssouser.locale == microsoft_response["preferredLanguage"]


def test_user_with_custom_field_names(
    custom_user_model, microsoft_response, callback_request
):
    # Arrange
    from django_microsoft_sso.main import UserHelper

    # Act
    helper = UserHelper(microsoft_response, callback_request)
    user = helper.get_or_create_user()

    # Assert
    assert user.user_name == "kalel@dailyplanet.com"
    assert user.mail == "kalel@dailyplanet.com"
