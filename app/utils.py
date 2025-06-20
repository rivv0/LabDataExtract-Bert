# app/utils.py
def filter_known_tests(lab_results, known_tests):
    """
    Filters the extracted lab results to include only known tests.
    """
    return [
        result for result in lab_results
        if result.get("test_name") in known_tests
    ]
