import logfire
from domain.settings.settings import get_settings

_logger_configured = False


def get_logger():
    """
    Return a configured Logfire logger.
    Configuration is applied only once per process.
    """
    global _logger_configured

    if not _logger_configured:
        settings = get_settings()

        logfire.configure(
            token=settings.logfire_token,
            service_name="graph-service-query",
            environment=settings.environment,
        )

        _logger_configured = True

    return logfire

