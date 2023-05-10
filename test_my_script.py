# Importing the relevant functions to be tested, along with pytest
# Here, we're only trying to test get_result()
from driver import beam_verification
from moment import Moment
import pytest

def input_test_cases():
    # Opening the file and reading a single line
    lines = None
    with open("test_cases.txt", "r") as file:
        lines = next(file)

    # Strip whitespaces and convert to list of strings
    lines = lines.strip().split()
    # Slice the part containing the input data as list of strings
    data_dump = lines[:-1]
    # Slice the relevant information out of the input data
    str_data = data_dump[8:-2]
    # Convert the input data to floating-point numbers
    data = list(map(float, str_data))

    # Index out the expected result
    str_expected_result = lines[-1]
    # Convert the expected result to a floating-point number
    expected_result = float(str_expected_result)
    
    # Return the data, and expected result as a tuple
    return data, expected_result

def test_code():
    # Get the test case input + expected result from a text file
    data, expected_result = input_test_cases()

    # Compute the actual result for this test case
    result = beam_verification(data)
    
    # Testing for equality of two floating-point numbers is considered a bad practice
    # Instead, we check whether their absolute difference lies within a tolerance
    tolerance = 0.001

    # Test the actual result with the expected result
    assert abs(result - expected_result) <= tolerance