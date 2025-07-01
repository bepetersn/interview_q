import hashlib
import re
import time

import nh3
from django.utils.text import slugify


def sanitize_html(content):
    """
    Sanitize HTML content using nh3 library and clean up excessive newlines.

    Args:
        content (str): The HTML content to sanitize

    Returns:
        str: Sanitized and cleaned content
    """
    if not content:
        return content
    # Use nh3's default sanitization which is already quite comprehensive
    sanitized = nh3.clean(content)

    # Handle both actual newlines and literal \n strings
    # First replace literal \n strings with actual newlines
    cleaned = sanitized.replace("\\n", "\n")
    # Then compact multiple newlines into single newlines
    cleaned = re.sub(r"\n{2,}", "\n", cleaned)
    # Replace all remaining newlines with spaces
    cleaned = cleaned.replace("\n", " ")
    # Remove excessive spaces (more than 2 consecutive spaces)
    cleaned = re.sub(r" {3,}", "  ", cleaned)
    # Trim leading and trailing whitespace
    cleaned = cleaned.strip()
    return cleaned


class SlugGenerator:
    @staticmethod
    def generate_slug_candidate(base_slug):
        now = str(time.time()).encode("utf-8")
        # Use SHA256 instead of SHA1 for better security
        hash_suffix = hashlib.sha256(now).hexdigest()[:8]
        return f"{base_slug}-{hash_suffix}", hash_suffix

    @staticmethod
    def ensure_unique_slug(model_class, slug_candidate, base_slug, hash_suffix):
        counter = 1
        while model_class.objects.filter(slug=slug_candidate).exists():
            slug_candidate = f"{base_slug}-{hash_suffix}-{counter}"
            counter += 1
        return slug_candidate

    @classmethod
    def generate_unique_slug(cls, model_class, title):
        base_slug = slugify(title)
        slug_candidate, hash_suffix = cls.generate_slug_candidate(base_slug)
        return cls.ensure_unique_slug(
            model_class, slug_candidate, base_slug, hash_suffix
        )
