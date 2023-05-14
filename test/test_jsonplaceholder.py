import json

import requests
import pytest

PATCH_URL = "https://jsonplaceholder.typicode.com/posts/100"


# Проверка, что для каждого id из параметров возвращается пост с соответствующим id
@pytest.mark.parametrize("id_post", [1, 5, 10, 20, 50],
                         ids=["one_post", "five_post", "ten_post", "twenty_post", "fifty_post"])
def test_check_id_post(id_post):
    response = requests.get(f"https://jsonplaceholder.typicode.com/posts/{id_post}")
    assert response.status_code == 200
    assert response.json()["id"] == id_post


# Проверка, что работает фильтр по userid
@pytest.mark.parametrize("user_id", [1, 3, 5, 10], ids=["first_user", "third_user", "fiftieth_user", " tenth_user"])
def test_check_user_id(user_id):
    response = requests.get(f"https://jsonplaceholder.typicode.com/posts?userId={user_id}")
    assert response.status_code == 200
    post_in_user_id = response.json()
    for post in post_in_user_id:
        assert post["userId"] == user_id


# Проверка создания поста и проверка на соответствие полей в ответе API
def test_creating_and_check_post():
    payload = {"title": "test_Zakhvatov", "body": "MTT", "userId": 77}
    headers = {'Content-type': 'application/json; charset=UTF-8'}
    response = requests.post("https://jsonplaceholder.typicode.com/posts", data=json.dumps(payload), headers=headers)
    assert response.status_code == 201
    assert response.json()
    assert response.json()["title"] == "test_Zakhvatov"
    assert response.json()['body'] == "MTT"
    assert response.json()['userId'] == 77


# patch и delete поста через фикстуру вначале
def test_patch_and_delete_post(patch_post):
    assert patch_post.status_code == 200
    assert patch_post.json()["title"] == "test_Zakhvatov_patch"

    headers = {'Content-type': 'application/json; charset=UTF-8'}
    response = requests.delete(PATCH_URL, headers=headers)
    assert response.status_code == 200


# Апдейт поста
def test_update_and_check_post():
    payload = {"title": "test_Zakhvatov", "body": "update", "userId": 999, "id": 500}
    headers = {'Content-type': 'application/json; charset=UTF-8'}
    response = requests.put("https://jsonplaceholder.typicode.com/posts/1", data=json.dumps(payload), headers=headers)
    assert response.status_code == 200
    assert response.json()
    assert response.json()["title"] == "test_Zakhvatov"
    assert response.json()['body'] == "update"
    assert response.json()['userId'] == 999
