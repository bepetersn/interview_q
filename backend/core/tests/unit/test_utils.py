# flake8: noqa
import json

import pytest

from backend.core.utils import sanitize_html


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload, expected_status, slug_check",
    [
        # User supplies a slug, should fail
        ({"title": "Unique Slug Test", "slug": "user-supplied-slug"}, 400, None),
        # User omits slug, API should generate one
        ({"title": "Another Slug Test"}, 201, "another-slug-test"),
        # User supplies only slug, should fail (title required)
        ({"slug": "should-not-work"}, 400, None),
    ],
    ids=[
        "fail with user-supplied slug",
        "create and generate slug",
        "fail with only slug",
    ],
)
def test_question_api_slug_handling(client, payload, expected_status, slug_check):
    response = client.post(
        "/api/questions/",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert response.status_code == expected_status
    if expected_status == 201 and slug_check:
        data = response.json()
        assert data["slug"] is not None and data["slug"] != ""
        assert slug_check in data["slug"]


class TestSanitizeHtml:
    """Test cases for the sanitize_html utility function"""

    def test_sanitize_html_basic_text(self):
        """Test that basic text passes through unchanged"""
        content = "This is plain text"
        result = sanitize_html(content)
        assert result == "This is plain text"

    def test_sanitize_html_safe_tags(self):
        """Test that safe HTML tags are preserved"""
        content = "<p>This is a <strong>paragraph</strong> with <em>emphasis</em></p>"
        result = sanitize_html(content)
        assert "<p>" in result
        assert "<strong>" in result
        assert "<em>" in result

    def test_sanitize_html_unsafe_tags_removed(self):
        """Test that unsafe HTML tags are removed"""
        content = '<p>Safe content</p><script>alert("dangerous")</script><p>More safe content</p>'
        result = sanitize_html(content)
        assert "<p>" in result
        assert "Safe content" in result
        assert "More safe content" in result
        assert "<script>" not in result
        assert 'alert("dangerous")' not in result

    def test_sanitize_html_unsafe_attributes_removed(self):
        """Test that unsafe attributes are removed"""
        content = '<p onclick="alert(\'xss\')">Click me</p><a href="https://example.com" onclick="alert(\'xss\')">Link</a>'
        result = sanitize_html(content)
        assert "<p>" in result
        assert "Click me" in result
        assert "onclick" not in result
        assert "href=" in result  # href should be preserved for links

    def test_sanitize_html_newlines(self):
        """Test that excessive newlines are reduced"""
        content = "Line 1\n\n\n\nLine 2\n\n\n\n\nLine 3"
        result = sanitize_html(content)
        assert result == "Line 1 Line 2 Line 3"

    def test_sanitize_html_excessive_spaces(self):
        """Test that excessive spaces are reduced"""
        content = "Word1     Word2      Word3"
        result = sanitize_html(content)
        assert result == "Word1  Word2  Word3"

    def test_sanitize_html_whitespace_trimming(self):
        """Test that leading and trailing whitespace is trimmed"""
        content = "   \n  Content with spaces  \n   "
        result = sanitize_html(content)
        assert result == "Content with spaces"

    def test_sanitize_html_empty_content(self):
        """Test that empty content is handled correctly"""
        assert sanitize_html("") == ""
        assert sanitize_html(None) is None
        assert sanitize_html("   ") == ""

    def test_sanitize_html_mixed_content(self):
        """Test complex content with mixed safe/unsafe elements"""
        content = """
        <h1>Title</h1>
        <p>This is a <strong>test</strong> paragraph.</p>



        <script>alert('xss')</script>
        <div onclick="malicious()">
            <ul>
                <li>Item 1</li>
                <li>Item 2</li>
            </ul>
        </div>


        """
        result = sanitize_html(content)

        # Safe content should be preserved
        assert "<h1>" in result
        assert "Title" in result
        assert "<p>" in result
        assert "<strong>" in result
        assert "<ul>" in result
        assert "<li>" in result

        # Unsafe content should be removed
        assert "<script>" not in result
        assert "alert('xss')" not in result
        assert "onclick" not in result
        assert "malicious()" not in result

        # Excessive newlines should be reduced
        assert "\n\n\n" not in result

    def test_sanitize_html_links_with_safe_attributes(self):
        """Test that links with safe attributes are preserved"""
        content = '<a href="https://example.com" title="Example">Link</a>'
        result = sanitize_html(content)
        assert '<a href="https://example.com"' in result
        assert 'title="Example"' in result
        assert "Link" in result
