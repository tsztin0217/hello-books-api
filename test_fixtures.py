import pytest

@pytest.fixture
def empty_list():
    return []

def test_len_of_empty_list(empty_list):
    assert isinstance(empty_list, list)
    assert len(empty_list) == 0

@pytest.fixture
def one_item(empty_list):
    empty_list.append("item")
    return empty_list

def test_len_of_unary_list(one_item):
    assert isinstance(one_item, list)
    assert len(one_item) == 1
    assert one_item[0] == "item"

# Define a FancyObject class to demonstrate yield with setup and cleanup
class FancyObject:
    def __init__(self):
        # Setup: Initialize with fancy = True
        self.fancy = True
        # Print shows this runs during SETUP (before test)
        print(f"\nFancyObject: {self.fancy}")

    def or_is_it(self):
        # Toggle the fancy value (True ↔ False)
        self.fancy = not self.fancy

    def cleanup(self):
        # Cleanup method - called AFTER test finishes
        # Print shows the final state after test ran
        print(f"\ncleanup: {self.fancy}")

# Fixture using yield - demonstrates setup and cleanup pattern
@pytest.fixture
def so_fancy():
    # SETUP PHASE (runs BEFORE test)
    # Create a FancyObject - prints "FancyObject: True"
    fancy_object = FancyObject()

    # YIELD: Pause here and give fancy_object to the test
    # Test runs with fancy_object while fixture is paused
    yield fancy_object

    # CLEANUP PHASE (runs AFTER test finishes)
    # Call cleanup method - prints "cleanup: False" (because test toggled it)
    fancy_object.cleanup()

# Test that uses the so_fancy fixture
def test_so_fancy(so_fancy):
    # Test receives the fancy_object from the fixture
    # At this point, fancy = True (from __init__)
    assert so_fancy.fancy
    
    # Toggle fancy from True to False
    so_fancy.or_is_it()
    
    # Now fancy = False
    assert not so_fancy.fancy
    # After this test finishes, cleanup() runs automatically!