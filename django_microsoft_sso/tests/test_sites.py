import pytest

pytestmark = pytest.mark.django_db

TEST_SITE_SETTINGS = {
    "site.com": {
        "text": "SignWithLogin1",
    },
    "other-site.com": {"text": "SignWithLogin2"},
}


@pytest.mark.parametrize("path", ["site.com", "other-site.com"])
def test_per_site_configuration(
    client_with_session, settings, path, default_site, other_site
):
    # Arrange
    settings.MICROSOFT_SSO_TEXT = lambda request: TEST_SITE_SETTINGS[request.site.domain][
        "text"
    ]

    # Act
    response = client_with_session.get("/", HTTP_HOST=path)
    response_text = (
        response.text if hasattr(response, "text") else response.content.decode()
    )

    # Assert
    assert TEST_SITE_SETTINGS[path]["text"] in response_text
