import re
import secrets
from typing import Optional, Type

import nh3
from django.db import models
from django.utils.text import slugify


def sanitize_html(content: Optional[str]) -> Optional[str]:
    """
    Sanitize HTML content using nh3 library and clean up excessive newlines.

    Args:
        content: The HTML content to sanitize

    Returns:
        Sanitized and cleaned content
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
    """
    Utility class for generating unique slugs for Django models.

    This class provides methods to generate URL-friendly slugs from titles
    and ensure uniqueness within a given model class.
    """

    # Use a more secure random source instead of time-based hashing
    _HASH_LENGTH = 8
    _MAX_RETRIES = 100  # Prevent infinite loops

    @staticmethod
    def generate_slug_candidate(base_slug: str) -> tuple[str, str]:
        """
        Generate a slug candidate with a random suffix.

        Args:
            base_slug: The base slug from the title

        Returns:
            Tuple of (slug_candidate, hash_suffix)
        """
        # Use cryptographically secure random token instead of time-based hash
        hash_suffix = secrets.token_hex(SlugGenerator._HASH_LENGTH // 2)
        return f"{base_slug}-{hash_suffix}", hash_suffix

    @staticmethod
    def ensure_unique_slug(
        model_class: Type[models.Model],
        slug_candidate: str,
        base_slug: str,
        hash_suffix: str,
    ) -> str:
        """
        Ensure the slug is unique by appending a counter if necessary.

        Args:
            model_class: The Django model class to check against
            slug_candidate: The initial slug candidate
            base_slug: The base slug from the title
            hash_suffix: The random hash suffix

        Returns:
            A unique slug

        Raises:
            RuntimeError: If unable to generate unique slug after max retries
        """
        current_slug = slug_candidate
        counter = 1

        while counter <= SlugGenerator._MAX_RETRIES:
            if not model_class.objects.filter(slug=current_slug).exists():
                return current_slug

            current_slug = f"{base_slug}-{hash_suffix}-{counter}"
            counter += 1

        raise RuntimeError(
            "Unable to generate unique slug after "
            f"{SlugGenerator._MAX_RETRIES} attempts"
        )

    @classmethod
    def generate_unique_slug(cls, model_class: Type[models.Model], title: str) -> str:
        """
        Generate a unique slug for a given model and title.

        Args:
            model_class: The Django model class
            title: The title to convert to a slug

        Returns:
            A unique slug
        """
        if not title:
            title = "untitled"

        base_slug = slugify(title)
        if not base_slug:
            base_slug = "untitled"

        slug_candidate, hash_suffix = cls.generate_slug_candidate(base_slug)
        return cls.ensure_unique_slug(
            model_class, slug_candidate, base_slug, hash_suffix
        )
