# flake8: noqa
import pytest
from backend.core.utils import SlugGenerator
from unittest.mock import MagicMock


class DummyModel:
    objects = MagicMock()


def test_generate_unique_slug_uniqueness():
    # Simulate no existing slugs
    DummyModel.objects.filter.return_value.exists.return_value = False
    title = "Test Title"
    slug1 = SlugGenerator.generate_unique_slug(DummyModel, title)
    slug2 = SlugGenerator.generate_unique_slug(DummyModel, title)
    assert slug1 != slug2, "Slugs should be unique for same title on repeated calls"


def test_generate_unique_slug_collision():
    # Simulate a collision on the first candidate, but not on the second
    call_count = {"count": 0}

    def filter_side_effect(**kwargs):
        # First call returns True (collision), second returns False
        call_count["count"] += 1

        class Exists:
            def exists(self):
                return call_count["count"] == 1

        return Exists()

    DummyModel.objects.filter.side_effect = filter_side_effect
    title = "Test Title"
    slug = SlugGenerator.generate_unique_slug(DummyModel, title)
    assert slug.endswith("-1"), "Slug should have a counter suffix after collision"
