from django.test import SimpleTestCase

from ..base import Constants, C


class TestConstants(SimpleTestCase):

    def test_invalid_codename(self):
        """Each codename must be a valid Python identifier."""
        with self.assertRaises(AttributeError):
            Constants(C(codename='9invalid', value=1, description='Invalid'))

    def test_conflicting_codename(self):
        """Codename cannot conflict with an existing attribute."""
        with self.assertRaises(AttributeError):
            Constants(C(codename='get_choices', value=1, description='Conflicting'))

    def test_duplicate_codename(self):
        """Codenames cannot be duplicated."""
        with self.assertRaises(AttributeError):
            Constants(
                C(codename='duplicate', value=1, description='Duplicated 1'),
                C(codename='duplicate', value=2, description='Duplicated 2'),
            )

    def test_get_choices(self):
        """
        get_choices() should return a choices list in Django's format, in the
        order in which the choices were originally passed in.
        """
        constants = Constants(
            C(codename='hello', value=1, description='First'),
            C(codename='world', value=2, description='Second'),
        )
        self.assertEquals(constants.get_choices(), [
            (1, 'First'),
            (2, 'Second'),
        ])

    def test_repr(self):
        """Smoke test for string representation."""
        str(Constants(C(codename='hello', value=1, description='Hello')))

    def test_get_values(self):
        constants = Constants(
            C(codename='hello', value=1, description='First'),
            C(codename='world', value=2, description='Second'),
        )
        self.assertEquals(constants.get_values('hello', 'world'), [1, 2])

    def test_get_invalid_value(self):
        constants = Constants(
            C(codename='hello', value=1, description='First'),
            C(codename='world', value=2, description='Second'),
        )
        with self.assertRaises(AttributeError):
            self.assertEquals(constants.get_values('invalid'))
