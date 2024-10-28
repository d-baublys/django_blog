from django.test import SimpleTestCase
from ..forms import SearchForm


class SearchFormTests(SimpleTestCase):
    def test_valid_query(self):
        """
        Verify the form accepts a valid non-empty query.
        """
        form = SearchForm({"q": "test"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get("q"), "test")

    def test_empty_query(self):
        """
        Verify the form accepts empty queries.
        """
        form = SearchForm({"q": ""})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get("q"), "")

    def test_max_length_validation(self):
        """
        Verify form validation limits queries to max_length.
        """
        max_length = SearchForm().fields["q"].max_length
        form = SearchForm({"q": "a" * (max_length + 100)})
        self.assertFalse(form.is_valid())
        self.assertIn("q", form.errors)
