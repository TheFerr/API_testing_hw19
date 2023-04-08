from ..api import PetFriends
from ..settings import valid_email, valid_password
import os
import random

pf = PetFriends()


def test_wrong_credentials(email='555@555.55', passw='555'):
    status, answer = pf.get_api_key(email, passw)
    assert status == 403
    assert 'Forbidden' in answer


def test_empty_credentials(email='', passw=''):
    status, answer = pf.get_api_key(email, passw)
    assert status == 403
    assert 'Forbidden' in answer


def test_bad_filter_string(filter='mypets'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    stat, result = pf.get_list_of_pets(auth_key, filter)
    assert stat == 500
    assert 'Error' in result


def test_wrong_auth_key_create_simple(auth_key_str='_'):
    stat, result = pf.create_new_pet_simple({"key": auth_key_str}, name='Vassily', animal_type='cat', age='3')
    assert stat == 403
    assert 'auth_key' in result


def test_create_pet_simple_empty_properties(name='', animal_type='', age=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_new_pet_simple(auth_key, name, animal_type, age)
    # print(result)
    assert status == 200
    assert 'created_at' in result
    assert len(result['id']) > 10
    assert result['pet_photo'] == ''


def test_add_photo_by_id(name='', animal_type='', age='', photo='images\cat1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.create_new_pet_simple(auth_key, name, animal_type, age)
    stat, res_add_ph = pf.add_photo(auth_key, result['id'], pet_photo)
    # print(res_add_ph)
    assert stat == 200
    assert len(res_add_ph['pet_photo']) > 1000

def test_delete_pet_others():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.get_list_of_pets(auth_key, '')
    st, result = pf.delete_pet(auth_key,result['pets'][0]['id'])
    assert st == 403

def test_delete_pet_random_id():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_id = "habrakadabra_" + str(random.uniform(0.0,1000000.0)) + "_hmm"
    # print(pet_id)
    st, result = pf.delete_pet(auth_key,pet_id)
    assert st == 404

def test_delete_pet_wrongauth():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.get_list_of_pets(auth_key, 'my_pets')
    auth_key = { "key": "____" }
    # print(pet_id)
    st, result = pf.delete_pet(auth_key,result['pets'][0]['id'])
    assert st == 403

def test_update_pet_wrong_id():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    petid = "abrakadabra_" + str(random.uniform(0.0, 1000000.0)) + "_hmm"
    # print(petid)
    status, result = pf.update_pet_info(auth_key, petid, 'Kot', 'vass', '5')
    assert status == 400
    assert "Pet with this id" in result