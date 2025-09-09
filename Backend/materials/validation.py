from django.core.exceptions import ValidationError
from urllib.parse import urlparse
from django.utils.deconstruct import deconstructible


@deconstructible
class VideoURLValidator:
    # List of allowed domains for video URLs.
    allowed_domains = [
        "youtube.com",
        "youtu.be",
        "drive.google.com",
        "vimeo.com",
    ]

    def __call__(self, value):
        parsed_url = urlparse(value)
        domain = parsed_url.netloc.lower()
        # Remove 'www.' prefix if present
        if domain.startswith("www."):
            domain = domain[4:]
        # Check if the domain matches any allowed provider
        if any(allowed in domain for allowed in self.allowed_domains):
            return
        allowed = ", ".join(self.allowed_domains)
        raise ValidationError(
            f"URL must be a video URL from one of the following providers: {allowed}."
        )


def validate_file_size(value):
    max_size = 100 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError(
            f"File size must be under 100 MB. Current file size: {value.size} bytes."
        )

