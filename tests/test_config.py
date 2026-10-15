from app.config import settings


def test_config_values():
    """Test that the configuration values are loaded correctly."""
    assert settings.app_name == "Smart Business Agent"
    assert settings.app_version == "0.1.0"
    assert settings.debug is False
    assert settings.log_level == "INFO"
