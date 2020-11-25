from json.decoder import JSONDecodeError
import datetime
import requests

"""
Count the number of friends by user ID and sort them by year.
"""

ACCESS_TOKEN = 'b5663bd6b5663bd6b5663bd6dbb5132556bb566b5663bd6eadb39a4e0afc5ef5bb51782'  # server key
API_URL = 'https://api.vk.com/method'
V = '5.71'  # version of API VK


def get_user_id(user_id):
    """
    Take user ID by nickname.
    :param user_id: nickname or id
    :return: id
    """
    resp = requests.get(f"{API_URL}/users.get", params={
        'access_token': ACCESS_TOKEN,
        'user_ids': user_id,
        'v': V
    })
    try:
        resp = resp.json()
        resp = resp['response']
        resp = resp[0]
        return resp['id']
    except (JSONDecodeError, KeyError):
        pass


def get_friends(user_id):
    """
    Take list of friends by user's id
    :param user_id: user's id
    :return: list of friends
    """
    resp = requests.get(f"{API_URL}/friends.get", params={
        'access_token': ACCESS_TOKEN,
        'user_id': user_id,
        'fields': 'bdate',
        'v': V
    })

    try:
        resp = resp.json()
        resp = resp['response']
        return resp['items']
    except (JSONDecodeError, KeyError):
        pass


def calc_age(user_id):
    """
    Calculate age of every person and return a list of couples (<age>, <number of friends with this age>),
    sorted in descending order by the second key (number of friends) and ascending by the first key (age).
    :param user_id: user's id
    :return:list of age and count of it
    """
    us_id = get_user_id(user_id)
    friends = get_friends(us_id)
    my_list = list()
    for friend in friends:
        try:
            my_list.append(friend['bdate'])
        except KeyError:
            continue
    dates = list()

    for data in my_list:
        try:
            #dates.append(data.split('.')[2])
            year = (datetime.datetime.now().date() - datetime.datetime.strptime(data, '%d.%m.%Y').date())
            dates.append(int(year.days/365))
        except (IndexError, ValueError):
            continue

    years = dict()
    for date in dates:
        years.setdefault(date, 0)
        years[date] += 1
    return sorted(years.items(), key=lambda v: (v[1], -v[0]), reverse=True)


if __name__ == '__main__':
    res = calc_age('sten_CF')
    print(res)
