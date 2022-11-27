import os.path

from app.pets_api import PetFriends
from app.settings import valid_email, valid_password
import os

pet_friends = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и сам ключ"""

    status, result = pet_friends.get_api_key(email, password)

    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем, что запрос возвращает непустой список питомцев"""

    _, auth_key = pet_friends.get_api_key(valid_email, valid_password)
    status, result = pet_friends.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name="Рыся", animal_type="рысь", age=2, pet_photo="images/ryska.jpg"):
    """Проверяем возможность добавления нового питомца с корректными данными"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pet_friends.get_api_key(valid_email, valid_password)
    status, result = pet_friends.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_delete_self_pet_successful():
    """Проверяем возможность удаления питомца"""

    _, auth_key = pet_friends.get_api_key(valid_email, valid_password)
    _, my_pets = pet_friends.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pet_friends.add_new_pet(auth_key, 'Мурка', 'кошка', 1, 'image/murka.jpg')
        _, my_pets = pet_friends.get_list_of_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']
    status, _ = pet_friends.delete_pet(auth_key, pet_id)

    _, my_pets = pet_friends.get_list_of_pets(auth_key, 'my_pets')

    assert status == 200
    assert pet_id not in my_pets.values()


def test_update_my_pet_successful(name='Жучка', animal_type="собака", age=3):
    """Проверяем возможность обновления информации о питомце"""

    _, auth_key = pet_friends.get_api_key(valid_email, valid_password)
    _, my_pets = pet_friends.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pet_friends.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception('Pets not found.')


# Негативное тестирование:

def test_get_api_key_for_invalid_email(email="incorrect@incorrect", password=valid_password):
    """ Проверяем, что запрос api ключа при вводе неверного email отбивает с ошибкой"""

    status, result = pet_friends.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result


def test_get_api_key_for_empty_email(email="", password=valid_password):
    """ Проверяем, что запрос api ключа при вводе пустого email отбивает с ошибкой"""

    status, result = pet_friends.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result


def test_get_api_key_for_invalid_password(email=valid_email, password="12345"):
    """ Проверяем, что запрос api ключа при вводе неверного пароля отбивает с ошибкой"""

    status, result = pet_friends.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result


def test_get_api_key_for_empty_password(email=valid_email, password=""):
    """ Проверяем, что запрос api ключа при вводе пустого пароля отбивает с ошибкой"""

    status, result = pet_friends.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result


def test_add_new_pet_with_invalid_age(name="Мурка", animal_type="кошка",
                                      age=9783827382738, pet_photo="images/murka.jpg"):
    """Проверяем, что добавление питомца с невалидным возрастом возвращает ошибку"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pet_friends.get_api_key(valid_email, valid_password)
    status, result = pet_friends.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400


def test_add_new_pet_with_invalid_photo(name="Мурка", animal_type="кошка", age=1, pet_photo="images/cat.jpg"):
    """Проверяем, что добавление питомца с некорректным фото возвращает ошибку"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pet_friends.get_api_key(valid_email, valid_password)
    status, result = pet_friends.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400


def test_add_new_pet_without_name(name="", animal_type="кошка", age=1, pet_photo="images/murka.jpg"):
    """Проверяем, что добавление питомца с пустым именем невозможно"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pet_friends.get_api_key(valid_email, valid_password)
    status, result = pet_friends.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400


def test_add_new_pet_without_animal_type(name="Мурка", animal_type="", age=2, pet_photo="images/murka.jpg"):
    """Проверяем, что добавление питомца с пустым типом возвращает ошибку"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pet_friends.get_api_key(valid_email, valid_password)
    status, result = pet_friends.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400


def test_update_my_pet_with_the_same_data(name="Мурка", animal_type="кошка", age=1):
    """Проверяем, что обновление информации о питомце с теми же данными невозможно"""

    _, auth_key = pet_friends.get_api_key(valid_email, valid_password)
    _, my_pets = pet_friends.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pet_friends.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 400
