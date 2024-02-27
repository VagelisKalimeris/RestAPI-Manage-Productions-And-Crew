import pytest
from assertpy import assert_that

from tests.testing_dependencies.util import AvailableCrew


@pytest.mark.run(order=0)
@pytest.mark.parametrize(['origin_dict', 'subtractions_dict', 'result_dict'], [
    ({'a': 5, 'b': 3, 'c': 1}, {'a': 3, 'b': 2, 'c': 1}, {'a': 2, 'b': 1}),
    ({'a': 5, 'b': 3}, {'b': 1}, {'a': 5, 'b': 2}),
    ({'a': 5, 'b': 3, 'c': 1}, {'b': 1}, {'a': 5, 'b': 2, 'c': 1}),
    ({'b': 3}, {'b': 3}, {}),
    ({}, {}, {})
])
def test_subtract_valid_dict_values(origin_dict, subtractions_dict, result_dict):
    assert_that(AvailableCrew(origin_dict)
                .subtract_crew(subtractions_dict))\
        .is_equal_to(result_dict)


@pytest.mark.run(order=0)
@pytest.mark.parametrize(['origin_dict', 'subtractions_dict', 'result_dict'], [
    ({'a': 5, 'b': 3, 'c': 1}, {'a': 3, 'b': 2, 'c': 1}, {'a': 2, 'b': 1, 'c': 0}),
])
def test_subtract_equal_dict_values(origin_dict, subtractions_dict, result_dict):
    assert_that(AvailableCrew(origin_dict)
                .subtract_crew(subtractions_dict))\
        .is_not_equal_to(result_dict)


@pytest.mark.run(order=0)
@pytest.mark.xfail(strict=True)
@pytest.mark.parametrize(['origin_dict', 'subtractions_dict'], [
    ({'a': 5, 'b': 3, 'c': 1}, {'d': 3}),
])
def test_subtract_unavailable_dict_values(origin_dict, subtractions_dict, ):
    assert_that(AvailableCrew(origin_dict)
                .subtract_crew(subtractions_dict))


@pytest.mark.run(order=0)
@pytest.mark.parametrize(['origin_dict', 'additions_dict', 'result_dict'], [
    ({'a': 5, 'b': 3, 'c': 1}, {'a': 3, 'b': 2, 'c': 1}, {'a': 8, 'b': 5, 'c': 2}),
    ({'a': 5, 'b': 3}, {'b': 1}, {'a': 5, 'b': 4}),
    ({'a': 5, 'b': 3}, {'c': 1}, {'a': 5, 'b': 3, 'c': 1}),
    ({}, {'b': 3}, {'b': 3}),
    ({}, {}, {})
])
def test_add_valid_dict_values(origin_dict, additions_dict, result_dict):
    assert_that(AvailableCrew(origin_dict)
                .add_crew(additions_dict))\
        .is_equal_to(result_dict)
