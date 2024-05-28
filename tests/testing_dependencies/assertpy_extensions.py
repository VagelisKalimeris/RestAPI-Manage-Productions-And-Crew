from assertpy import assert_that, add_extension


def safe_extract_response_key(self, key, status_code=200):
    """
    Abstracts 3 very common processes:
     - Verifies api response status code
     - Verifies given json key exists - no run-time error in case it is absent
     - Retrieves json key
    """
    assert_that(self.val)\
        .has_status_code(status_code)

    if key is None:
        self.val = self.val.json()
    else:
        assert_that(self.val.json())\
            .contains_key(key)

        self.val = self.val.json()[key]

    return self


add_extension(safe_extract_response_key)
