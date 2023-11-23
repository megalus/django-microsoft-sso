import pytest

from django_microsoft_sso.main import UserHelper

pytestmark = pytest.mark.django_db


def test_microsoft_sso_model(microsoft_response, callback_request, settings):
    # Act
    helper = UserHelper(microsoft_response, callback_request)
    user = helper.get_or_create_user()

    # Assert
    assert user.microsoftssouser.microsoft_id == microsoft_response["id"]
    assert user.microsoftssouser.picture_raw == microsoft_response["picture_raw_data"]
    assert user.microsoftssouser.locale == microsoft_response["preferredLanguage"]
