import pytest
from json import dumps


def beautify_response(resp):
    """
    Makes testing produced responses humanly readable, for better error reporting.
    """
    return dumps(resp.json(), indent=4)


class AvailableCrew:
    """
    Provides operations for calculations between crew member dicts.
    Note: could be turned into assertpy extensions.
    """
    def __init__(self, members_dict):
        self.members = members_dict

    def add_crew(self, additions_dict):
        for key in additions_dict:
            self.members[key] = self.members.get(key, 0) + additions_dict[key]

        return self.members

    def subtract_crew(self, subtractions_dict):
        for key in subtractions_dict:
            if key not in self.members:
                pytest.fail('Can only subtract from existing role!')

            self.members[key] = self.members[key] - subtractions_dict[key]

            if self.members[key] == 0:
                self.members.pop(key)

        return self.members
