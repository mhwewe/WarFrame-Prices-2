from operator import itemgetter
import requests

base_url = "https://api.warframe.market/v1/items/"

def orders(item_link):
    if " " in item_link:
        item_link = item_link.replace(" ", "_")
        url = f"{base_url}{item_link}/orders"
    else:
        item_link = f"{item_link}_prime_set"
        url = f"{base_url}{item_link}/orders"

    try:
        response = requests.get(url)
    except Exception:
        response = False
    if response:
        raw = response.json()
        orders_list: list = []
        for i in raw['payload']['orders']:
            orders_dict: dict = {'order_type': i['order_type'],
                                 'platinum': i['platinum'],
                                 'quantity': i['quantity'],
                                 'reputation': i['user']['reputation'],
                                 'avatar': i['user']['avatar'],
                                 'ingame_name': i['user']['ingame_name'],
                                 'status': i['user']['status'],
                                 'creation_date': i['creation_date']}
            if orders_dict['status'] == "ingame":
                orders_list.append(orders_dict)
        orders_list = sorted(orders_list, key=itemgetter('platinum'))
        buy_list: list = []
        sell_list: list = []

        for i in orders_list:
            if i['order_type'] == 'buy':
                buy_list.append(i)
            else:
                sell_list.append(i)

        orders_dict = {'buy': buy_list, 'sell': sell_list}
        return orders_dict
    else:
        orders_dict: dict = {'order_type': 'fail',
                             'platinum': 'fail',
                             'quantity': 'fail',
                             'reputation': 'fail',
                             'avatar': 'fail',
                             'ingame_name': 'fail',
                             'status': 'fail',
                             'creation_date': 'fail'}
        buy_list = []
        sell_list = []

        orders_dict = {'buy': buy_list, 'sell': sell_list}
        return orders_dict