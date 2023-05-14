import requests
import pytest


# Проверка, что счетчик работает и выводит корректное количество пивоварен. Проверяю через количество элементов в списке
@pytest.mark.parametrize("count", [1, 100, 200],
                         ids=['one_breweries_list', 'one_hundred_breweries_list',
                              'two_hundred_breweries_list'])
def test_count_number_of_breweries(count):
    response = requests.get(f"https://api.openbrewerydb.org/v1/breweries?per_page={count}")
    assert response.json()
    assert response.status_code == 200
    assert len(response.json()) == count


# получение разных типов пивоварен
@pytest.mark.parametrize("type_breweries",
                         ["micro", "nano", "regional", "brewpub", "large", "planning", "bar", "contract", "proprietor",
                          "closed"],
                         ids=["micro_breweries", "nano_breweries", "regional_breweries", "brewpub_breweries",
                              "large_breweries", "planning_breweries", "bar_breweries", " contract_breweries",
                              "proprietor_breweries", "closed_breweries"])
def test_get_types_breweries(type_breweries):
    response = requests.get(f"https://api.openbrewerydb.org/v1/breweries?by_type={type_breweries}&per_page=10")
    assert response.json()
    assert response.status_code == 200
    for brewery in response.json():
        assert brewery.get("brewery_type") == type_breweries


# Проверка, что с некорректным типом будет возвращено 400 Bad Request с описанием ошибки
@pytest.mark.parametrize("incorrect_type", ["nano123", " ", None, 123],
                         ids=['incorrect_string_type', "space", "None_type", "int_type"])
def test_check_incorrect_type(incorrect_type):
    response = requests.get(f"https://api.openbrewerydb.org/v1/breweries?by_type={incorrect_type}")
    assert response.json()
    assert response.status_code == 400
    assert "errors" in response.json()
    assert "Brewery type must include one of these types: [\"micro\", \"nano\", \"regional\", \"brewpub\", \"large\", \"planning\", \"bar\", \"contract\", \"proprietor\", \"closed\"]" in \
           response.json()["errors"]


# Проверка, что переключение страниц работает и ответ на следующей отличается
@pytest.mark.parametrize("page", [1, 2, 3, 10], ids=["first_page", "second_page", "third_page", "tenth_page"])
def test_diff_api_response_at_page(page):
    response = requests.get(f"https://api.openbrewerydb.org/v1/breweries?page={page}&per_page=10")
    previous_page = None
    for current_page in response.json():
        if current_page is not None:
            assert current_page != previous_page
        previous_page = current_page


# Запрашиваю рандомную пивоварню, записываю id и вызываю метод получения пивоварни через этот id и сравниваю ответы на совпадение
def test_get_brewery_by_random_id():
    response = requests.get("https://api.openbrewerydb.org/v1/breweries/random")
    assert response.status_code == 200
    brewery_random = response.json()[0]
    brewery_id = brewery_random["id"]

    response = requests.get(f"https://api.openbrewerydb.org/v1/breweries/{brewery_id}")
    assert response.status_code == 200
    brewery_by_id = response.json()

    assert brewery_random == brewery_by_id
