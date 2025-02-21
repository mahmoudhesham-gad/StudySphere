import magic
from django.core.exceptions import ValidationError
from urllib.parse import urlparse
from django.utils.deconstruct import deconstructible

def validate_file_mime(file):
    # Read the beginning of the file to determine its MIME type.
    file.seek(0)
    mime = magic.from_buffer(file.read(1024), mime=True)
    file.seek(0)  # Reset file pointer after reading

    # Define allowed MIME types for the specified extensions.
    allowed_mime_types = [
        'application/pdf',  # PDF
        'application/msword',  # DOC
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # DOCX
        'application/vnd.ms-powerpoint',  # PPT
        'application/vnd.openxmlformats-officedocument.presentationml.presentation',  # PPTX
        'application/vnd.ms-excel',  # XLS
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # XLSX
        'text/plain'  # TXT
    ]

    if mime not in allowed_mime_types:
        raise ValidationError(f'Unsupported file type: {mime}')


@deconstructible
class VideoURLValidator:
    # List of allowed domains for video URLs.
    allowed_domains = [
        'youtube.com',
        'youtu.be',
        'drive.google.com',
        'vimeo.com',         
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
        raise ValidationError(f'File size must be under 100 MB. Current file size: {value.size} bytes.')