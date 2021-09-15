from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_style():
    response = client.get("/assets/style.css")
    assert response.status_code == 200


def test_save_lang_find_lang_json():
    response = client.get("/save/lang?content=hello")
    assert response.status_code == 200
    response = client.get("/save/lang?content=hey")
    assert response.status_code == 200
    response = client.get("/save/lang?content=transistor")
    assert response.status_code == 200
    response = client.get("/find/lang/json?content=transistor")
    assert response.json()[0]['content'] == 'transistor'
