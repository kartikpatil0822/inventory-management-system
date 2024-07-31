import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def setup_function():
    """
    Setup function to initialize data required for testing the APIs.

    This function creates two items in the database, which will be used
    for testing various endpoints. It posts two items to the /items/ endpoint.
    """
    client.post("/items/", json={"itemname": "item1", "itemdesc": "This is item 1"})
    client.post("/items/", json={"itemname": "item2", "itemdesc": "This is item 2"})


@pytest.mark.order(1)
def test_get_item_return_200_status_code():
    """
    Test to verify the GET /items/{item_id} endpoint returns status code 200.

    This test fetches an item by ID and checks if the response status code is 200.
    It also verifies the returned JSON data matches the expected item details.
    """
    setup_function()
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == {"item_name": "item1", "item_desc": "This is item 1"}


@pytest.mark.order(2)
def test_get_item_return_404_status_code():
    """
    Test to verify the GET /items/{item_id} endpoint returns status code 404.

    This test attempts to fetch a non-existent item by ID and checks if
    the response status code is 404. It also verifies the error message.
    """
    response = client.get("/items/78")
    assert response.status_code == 404
    assert response.json() == {"error": "404: Item not found"}


@pytest.mark.order(3)
def test_update_item_return_200_status_code():
    """
    Test to verify the PUT /items/{item_id} endpoint returns status code 200.

    This test updates an existing item by ID and checks if the response
    status code is 200. It also verifies the returned JSON data matches the
    updated item details.
    """
    response = client.put("/items/2", json={"itemname": "item3", "itemdesc": "This is item 3"})
    assert response.status_code == 200
    assert response.json() == {"item_name": "item3", "item_desc": "This is item 3"}


@pytest.mark.order(4)
def test_update_item_return_404_status_code():
    """
    Test to verify the PUT /items/{item_id} endpoint returns status code 404.

    This test attempts to update a non-existent item by ID and checks if
    the response status code is 404. It also verifies the error message.
    """
    response = client.put("/items/78", json={"itemname": "item3", "itemdesc": "This is item 3"})
    assert response.status_code == 404
    assert response.json() == {"error": "404: Item not found"}


@pytest.mark.order(5)
def test_delete_item_return_200_status_code():
    """
    Test to verify the DELETE /items/{item_id} endpoint returns status code 200.

    This test deletes an existing item by ID and checks if the response
    status code is 200. It also verifies the success message in the response.
    """
    response = client.delete("/items/2")
    assert response.status_code == 200
    assert response.json() == {'message': 'Item Deleted Successfully'}


@pytest.mark.order(6)
def test_delete_item_return_404_status_code():
    """
    Test to verify the DELETE /items/{item_id} endpoint returns status code 404.

    This test attempts to delete a non-existent item by ID and checks if
    the response status code is 404. It also verifies the error message.
    """
    response = client.delete("/items/2")
    assert response.status_code == 404
    assert response.json() == {"error": "404: Item not found"}


@pytest.mark.order(7)
def test_post_item_return_201_status_code():
    """
    Test to verify the POST /items/ endpoint returns status code 201.

    This test creates a new item and checks if the response status code is 201.
    It also verifies the returned JSON data matches the created item details.
    """
    response = client.post("/items/", json={"itemname": "item4", "itemdesc": "This is item 4"})
    assert response.status_code == 201
    assert response.json() == {"item_name": "item4", "item_desc": "This is item 4"}


@pytest.mark.order(8)
def test_post_item_return_400_status_code():
    """
    Test to verify the POST /items/ endpoint returns status code 400.

    This test attempts to create an item that already exists and checks if
    the response status code is 400. It also verifies the error message.
    """
    response = client.post("/items/", json={"itemname": "item4", "itemdesc": "This is item 4"})
    assert response.status_code == 400
    assert response.json() == {'error': 'Item already exists.'}
