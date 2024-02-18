import requests

API_URL = 'http://127.0.0.1:8000/'


def fill_users():
    url = 'https://dummyjson.com/users?limit=5&&select=username,email,password'
    resp = requests.get(url)
    if resp.status_code == 200:
        for item in resp.json()['users']:
            data = {
                "username": item['username'],
                "email": item['email'],
                "password": item['password']
            }
            requests.post(API_URL + 'users/', json=data)


def fill_products():
    url = 'https://dummyjson.com/products?limit=10&&select=title,description,price'
    resp = requests.get(url)
    if resp.status_code == 200:
        for item in resp.json()["products"]:
            data = {
                "title": item['title'],
                "description": item['description'],
                "price": item['price']
            }
            requests.post(API_URL + 'product/', json=data)
