import requests
import pytest


# Перебираю через параметризацию значения возвращаемых картинок с собаками. 1, 3 и 50 изображений
@pytest.mark.parametrize('count', [1, 3, 50], ids=['one_message', 'three_messages', 'fifty_messages'])
def test_count_number_of_messages(count):
    response = requests.get(f"https://dog.ceo/api/breeds/image/random/{count}")
    assert response.json()
    assert len(response.json()["message"]) == count
    assert response.status_code == 200


# проверка, что приходит 200 ОК и параметр status принимает значение success для 1, 3 и 50 изображений
@pytest.mark.parametrize('count', [1, 3, 50], ids=['one_message', 'three_messages', 'fifty_messages'])
def test_200_success_code_response(count):
    response = requests.get(f"https://dog.ceo/api/breeds/image/random/{count}")
    assert response.json()
    assert response.status_code == 200
    assert response.json()["status"] == "success"


# проверка того, что для счетчика >50 изображений возвращается только 50 согласно доке
def test_max_50_number_of_message():
    response = requests.get("https://dog.ceo/api/breeds/image/random/51")
    assert len(response.json()["message"]) == 50
    assert response.json()
    assert response.status_code == 200


# Проверка, что метод рандомной генерации работает и при двух вызовах метода картинки не повторяются
def test_image_urls_not_equal():
    url = "https://dog.ceo/api/breeds/image/random"

    # первый картинка
    response_first_image = requests.get(url)
    json_first_image = response_first_image.json()
    message_first_image = json_first_image["message"]

    # вторая
    response_second_image = requests.get(url)
    json_second_image = response_second_image.json()
    message_second_image = json_second_image["message"]

    # Сравниваем, что значения параметра message не равны
    assert message_first_image != message_second_image

#Проверяю, что генерируется рандомная картинка с породой
def test_randon_breeds_image():
    response = requests.get("https://dog.ceo/api/breed/african/images/random")
    json = response.json()
    assert "message" in json
    assert json["message"] != ""
    assert json["status"] == "success"
    assert response.status_code == 200
