import requests
import allure

from tests.endpoints import Endpoints
from tests.helps import get_token


@allure.suite('Проверка получения заказов')
class TestGetOrder:

    @allure.title('Проверка получения заказов авторизованного пользователя')
    def test_get_orders_authorization_user_success(self):
        token = get_token()
        response = requests.get(Endpoints.url + Endpoints.orders, headers={'authorization': token})
        assert response.status_code == 200 and 'orders' in response.text

    @allure.title('Проверка получения заказов неавторизованным пользователем')
    def test_get_orders_not_authorization_user_error(self):
        response = requests.get(Endpoints.url + Endpoints.orders)
        assert response.status_code == 401 and response.text == '{"success":false,"message":"You should be authorised"}'

