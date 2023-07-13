import networkx as nx
import requests
import matplotlib.pyplot as plt
from networkx.algorithms import community

token = 'vk1.a.eDKZtV3ZGDHVsdwDo0bT5EFWg_SXHHBKhOU9KqdThm5shCSbf-C4_D6To2V_G3NQLXTfAWYmsqFdJiZRwpZ0dvLSzofFwz8sBLEQj2Ccz1JrVgE4KpH5njJ8ES8a-y2ywsIHXz0SqC1N09pKgtEQuKdbUN3VK8lm8Lan1L_OQBkZp8BzAbBsjS-mUXRFYs8OQn6zwQBS6RQnp2TeiV7wjQ'

# список др
url = 'https://api.vk.com/method/friends.get'
params = {
    'access_token': token,
    'user_id': '623495939',
    'count': 5,
    'v': '5.131'
}
response = requests.get(url, params=params).json()

if 'response' in response:
    friends = response['response']['items']

    # новый граф + вершина выбранного пол-ля
    user_id = '623495939'
    G = nx.Graph()
    G.add_node(user_id)

    # вершины и ребра для др 1 ур-ня
    for friend_id in friends:
        G.add_node(friend_id)
        G.add_edge(user_id, friend_id)

        # список др 1 ур-ня
        url = 'https://api.vk.com/method/friends.get'
        params = {
            'access_token': token,
            'user_id': friend_id,
            'count': 30,
            'v': '5.131'
        }
        response = requests.get(url, params=params).json()

        if 'response' in response:
            # вершины и ребра для др 2 ур-ня
            second_level_friends = response['response']['items']
            for second_friend_id in second_level_friends:
                # если 2 ур-нь уже есть в 1 ур-не, то не добавляем
                if second_friend_id not in friends:
                    G.add_node(second_friend_id)
                    G.add_edge(friend_id, second_friend_id)

    # фун-ия для отображения графа
    nx.draw_networkx(G, with_labels=True, node_size=2000, pos=nx.circular_layout(G))

    # кластер
    communities = list(community.asyn_lpa_communities(G))

    # цвета кластер
    color_map = []
    for node in G.nodes():
        for i, community in enumerate(communities):
            if node in community:
                color_map.append(i)
                break
    node_size = [2000 for _ in range(len(G.nodes()))]
    node_color = [color_map[i] for i in range(len(G.nodes()))]

    # фун-ия для отображения кластер
    nx.draw_networkx(G, with_labels=True, pos=nx.circular_layout(G), node_color=node_color, node_size=node_size, cmap=plt.cm.tab20)

    plt.show()

else:
    print('Не удалось получить список друзей')