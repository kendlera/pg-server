


pg_cities = [["Istanbul", "Ankara", 9.0], ["Istanbul", "Sofia", 13.0], ["Istanbul", "Izmir", 8.0], ["Istanbul", "Bucuresti", 13.0], ["Bremen", "Rhein-Main", 9.0], ["Bremen", "Kobenhavn", 12.0], ["Bremen", "Vlaanderen", 10.0], ["Bremen", "Randstad", 8.0], ["Bremen", "Berlin", 6.0], ["Rhein-Ruhr", "Rhein-Main", 3.0], ["Rhein-Ruhr", "Vlaanderen", 4.0], ["Rhein-Ruhr", "Paris", 10.0], ["Rhein-Ruhr", "Stuttgart", 5.0], ["London", "Vlaanderen", 15.0], ["London", "Paris", 16.0], ["London", "Randstad", 18.0], ["London", "Birmingham", 4.0], ["Athina", "Tirane", 16.0], ["Athina", "Sofia", 17.0], ["Bordeaux", "Barcelona", 15.0], ["Bordeaux", "Lyon", 12.0], ["Bordeaux", "Marseille", 12.0], ["Bordeaux", "Paris", 12.0], ["Bordeaux", "Madrid", 16.0], ["Zagreb", "Wien", 8.0], ["Zagreb", "Munchen", 14.0], ["Zagreb", "Milano", 17.0], ["Zagreb", "Beograd", 9.0], ["Zagreb", "Budapest", 7.0], ["Madrid", "Lisboa", 13.0], ["Madrid", "Barcelona", 14.0], ["Birmingham", "Glasgow", 13.0], ["Birmingham", "Dublin", 15.0], ["Vlaanderen", "Paris", 7.0], ["Vlaanderen", "Rhein-Main", 6.0], ["Vlaanderen", "Randstad", 4.0], ["Praha", "Katowice", 8.0], ["Praha", "Warszawa", 11.0], ["Praha", "Berlin", 7.0], ["Praha", "Wien", 7.0], ["Praha", "Rhein-Main", 10.0], ["Praha", "Munchen", 8.0], ["Kyjiv", "Kharkiv", 9.0], ["Kyjiv", "Odessa", 9.0], ["Kyjiv", "Warszawa", 14.0], ["Kyjiv", "Katowice", 18.0], ["Kyjiv", "Minsk", 10.0], ["Kyjiv", "Budapest", 21.0], ["Rhein-Main", "Stuttgart", 3.0], ["Rhein-Main", "Berlin", 10.0], ["Rhein-Main", "Munchen", 6.0], ["Milano", "Zurich", 11.0], ["Milano", "Roma", 19.0], ["Milano", "Munchen", 16.0], ["Milano", "Marseille", 13.0], ["Milano", "Lyon", 11.0], ["Tirane", "Napoli", 25.0], ["Tirane", "Sofia", 13.0], ["Tirane", "Beograd", 15.0], ["Katowice", "Wien", 8.0], ["Katowice", "Warszawa", 5.0], ["Katowice", "Budapest", 11.0], ["Berlin", "Warszawa", 11.0], ["Berlin", "Kobenhavn", 15.0], ["Tallinn", "Riga", 7.0], ["Tallinn", "Sankt-Peterburg", 9.0], ["Riga", "Minsk", 8.0], ["Riga", "Moskwa", 18.0], ["Riga", "Sankt-Peterburg", 13.0], ["Riga", "Warszawa", 12.0], ["Munchen", "Zurich", 8.0], ["Munchen", "Stuttgart", 4.0], ["Munchen", "Wien", 9.0], ["Warszawa", "Minsk", 10.0], ["Warszawa", "Kobenhavn", 25.0], ["Odessa", "Kharkiv", 13.0], ["Odessa", "Bucuresti", 10.0], ["Odessa", "Budapest", 25.0], ["Glasgow", "Dublin", 17.0], ["Sofia", "Beograd", 11.0], ["Sofia", "Bucuresti", 9.0], ["Stuttgart", "Zurich", 5.0], ["Stuttgart", "Paris", 14.0], ["Izmir", "Ankara", 10.0], ["Oslo", "Stockholm", 13.0], ["Oslo", "Kobenhavn", 17.0], ["Kharkiv", "Moskwa", 15.0], ["Kharkiv", "Minsk", 16.0], ["Lyon", "Zurich", 14.0], ["Lyon", "Marseille", 8.0], ["Lyon", "Paris", 11.0], ["Minsk", "Moskwa", 14.0], ["Budapest", "Bucuresti", 16.0], ["Budapest", "Wien", 5.0], ["Budapest", "Beograd", 10.0], ["Beograd", "Bucuresti", 12.0], ["Beograd", "Napoli", 18.0], ["Sankt-Peterburg", "Moskwa", 14.0], ["Sankt-Peterburg", "Helsinki", 11.0], ["Roma", "Napoli", 7.0], ["Paris", "Zurich", 14.0], ["Helsinki", "Stockholm", 21.0], ["Kobenhavn", "Stockholm", 18.0], ["Marseille", "Barcelona", 11.0]]
my_city_info = {'Rhein-Main', 'Berlin', 'Praha'}
players_cities = {'Rhein-Main', 'Berlin', 'Praha', 'Minsk', 'Riga', 'Warszawa', 'Bordeaux', 'Lyon', 'Paris'}





def generate_pg_graph(game_board):
    """included countries list:  color, nodes, edges and costs  returns game_graph"""

    def make_link(G, node1, node2, cost):
        if node1 not in G:
            G[node1] = {}
        (G[node1])[node2] = cost
        if node2 not in G:
            G[node2] = {}
        (G[node2])[node1] = cost
        return G

    G = {}
    for (x,y,z) in game_board: make_link(G,x,y,z)
    return G

start_board = generate_pg_graph(pg_cities)







def choose_cheapest_cities(start_board, player, player_token):
    players_cities = []
    for p in all_city_info['info']['name']:
        for c in city_info['info']['name'][p]['cities']:
            players_cities.append(c)
    best_start_cities = ['Rhein-Main', 'Vlaanderen', 'Praha', 'Munchen', 'Berlin', 'Warszawa']
    if len(my_cities) == 0:
        for c in best_start_cities:
            if c not in players_cities:
                return c
    else:
        first_poss_cities_to_gen = []
        second_poss_cities_to_gen = []
        third_poss_cities_to_gen = []

        for c in my_city_info:
            for nc in start_board[c]:
                first_poss_cities_to_gen.append([nc, start_board[c][nc]])
        for nc in first_poss_cities_to_gen:
            for nnc in start_board[nc[0]]:
                second_poss_cities_to_gen.append([nnc, nc[1] + start_board[nc[0]][nnc]])
        for nnc in second_poss_cities_to_gen:
            for nnnc in start_board[nnc[0]]:
                third_poss_cities_to_gen.append([nnnc, nnc[1] + start_board[nnc[0]][nnnc]])

        all_poss_cities = first_poss_cities_to_gen + second_poss_cities_to_gen + third_poss_cities_to_gen
        legal_cities = []

        for c in all_poss_cities:
            if c[0] not in players_cities:
                legal_cities.append(c)

        def second(elem):
            return elem[1]

        legal_cities.sort(key=second)
        return  legal_cities[0][0]

#print(choose_cheapest_cities(start_board, players_cities, my_city_info))
