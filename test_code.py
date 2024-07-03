import pytest
import storage_json
import storage_csv
from unittest.mock import patch

# Test that a json file is created
def test_json_file_creation():
    storage = storage_json.StorageJson("movie1.json")
    data = storage.read_data()
    assert data == []


# Test that a csv file is created
def test_csv_file_creation():
    storage = storage_csv.StorageCsv("movie1.csv")
    data = storage.read_data()
    assert data == []


# Test that is creating new movie entry
def test_create_new_movie():
    test_file = "movies.csv"
    with open(test_file, 'w') as file:
        file.write("title,rating,year_of_release\n")  # Header line

    with patch('builtins.input', return_value='The Room'):   # Mock the input function to provide "The Room" as input
        storage = storage_csv.StorageCsv(test_file)
        previous_data = len(storage.read_data())
        storage.add_movie()
        data = storage.read_data()

        assert len(data) == previous_data + 1

        assert data[-1]['title'] == "The Room"


# Test that is deleting an existing movie
def test_delete_movie():
    test_file = "test_movies.csv"
    with open(test_file, 'r') as file:
        file.read()

    storage = storage_csv.StorageCsv(test_file)

    with patch('builtins.input', return_value='The Room'):
        storage.add_movie()

    previous_data = len(storage.read_data()) #Checking the lenght after I added the movie to be deleted

    with patch('builtins.input', return_value='The Room'):   # Mock the input function to provide "The Room" as input
        storage.delete_movie()
        data = storage.read_data()

        assert len(data) == previous_data - 1

        assert data[-1]['title'] != "The Room"


# Test that is updating an existing movie
def test_update_movie():
    test_file = "test_movies.csv"
    with open(test_file, 'r') as file:
        file.read()

    storage = storage_csv.StorageCsv(test_file)

    with patch('builtins.input', side_effect=["The Moon", "My new note!"]):
        storage.update_movie()

    data = storage.read_data()

    updated_movie = next((movie for movie in data if movie['title'] == "The Moon"), None)
    assert updated_movie is not None
    assert updated_movie['note'] == "My new note!"

pytest.main()


if __name__ == "__main__":
    pytest.main()
