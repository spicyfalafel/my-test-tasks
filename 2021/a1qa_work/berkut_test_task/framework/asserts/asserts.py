from hamcrest import assert_that, has_entries


class Asserts:
    @staticmethod
    def assert_has_entries(obj, **expected_values):
        assert_that(actual=obj.__dict__,
                    matcher=has_entries(**expected_values))
