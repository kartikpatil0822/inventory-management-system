from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


async def setup_function():
    client.post("/items/", json={"itemname": "item2", "itemdesc": "This is item 2"})
    client.post("/items/", json={"itemname": "item1", "itemdesc": "This is item 1"})


def teardown_function():
    # Clean up the items created for the tests
    client.delete("/items/1")
    client.delete("/items/2")


def test_get_item_return_200_status_code():
    setup_function()
    response = client.get("/items/5")
    assert response.status_code == 200
    assert response.json() == {"item_name": "item2", "item_desc": "This is item 2"}
    teardown_function()


def test_get_item_return_404_status_code():
    response = client.get("/items/78")
    assert response.status_code == 404
    assert response.json() == {"error": "404: Item not found"}


def test_update_item_return_200_status_code():
    setup_function()
    response = client.put("/items/2", json={"itemname": "marker", "itemdesc": "black marker pen"})
    breakpoint()
    assert response.status_code == 200
    assert response.json() == {"item_name": "marker", "item_desc": "black marker pen"}
    teardown_function()


def test_update_item_return_404_status_code():
    response = client.put("/items/78", json={"itemname": "marker", "itemdesc": "black marker pen"})
    assert response.status_code == 404
    assert response.json() == {"error": "404: Item not found"}


def test_delete_item_return_200_status_code():
    setup_function()
    response = client.delete("/items/1")
    assert response.status_code == 200
    assert response.json() == {'message': 'Item Deleted Successfully'}
    teardown_function()


def test_delete_item_return_404_status_code():
    response = client.delete("/items/78")
    assert response.status_code == 404
    assert response.json() == {"error": "404: Item not found"}


def test_post_item_return_201_status_code():
    response = client.post("/items/", json={"itemname": "pen", "itemdesc": "blue pen"})
    assert response.status_code == 201
    assert response.json() == {"item_name": "pen", "item_desc": "blue pen"}


def test_post_item_return_400_status_code():
    response = client.post("/items/", json={"itemname": "pen", "itemdesc": "blue pen"})
    assert response.status_code == 400
    assert response.json() == {'error': 'Item already exists.'}
