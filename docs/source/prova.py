def _contains_only_integers(array):
    """
    Checks if an array contains only integer values.

    :param array-like array: The array to be checked.

    :return: True if the array contains only integer values, False otherwise.
    :rtype: bool
    """
    integers_array = np.asarray(array).astype(int)
    check_array = np.unique(integers_array == array)
    if len(check_array) == 1 and check_array[0]:
        return True
    else:
        return False
