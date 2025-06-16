import hashlib
import time

from django.utils.text import slugify


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
