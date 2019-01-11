# to_buy = 5
# resource_state = {"OIL": 16, "URANIUM": 4, "GAS": 18, "COAL": 23}
# what = 'GAS'


def how_much_to_buy(resource_state, to_buy, what):

    bin_dic = {'COAL': [[9, 0], [9, 0],  [8, 0], [8, 0],  [7, 0], [7, 0],
                [6, 0], [6, 0], [6, 0], [5, 0], [5, 0], [5, 0],  [4, 0], [4, 0], [4, 0],  [3, 0], [3, 0],
                [3, 0], [3, 0], [2, 0], [2, 0], [2, 0], [2, 0], [1, 0], [1, 0], [1, 0], [1, 0]],
    'GAS': [[8, 0], [8, 0], [8, 0], [7, 0], [7, 0], [7, 0],
                [6, 0], [6, 0], [6, 0], [5, 0], [5, 0], [5, 0],  [4, 0], [4, 0], [4, 0],  [3, 0], [3, 0],
                [3, 0],  [2, 0], [2, 0], [2, 0],  [1, 0], [1, 0], [1, 0]],
    'OIL':[[9, 0], [9, 0], [9, 0], [9, 0], [8, 0], [8, 0],  [7, 0], [7, 0], [6, 0],
                [6, 0], [5, 0], [5, 0],  [4, 0], [4, 0],  [3, 0], [3, 0],
                 [2, 0], [2, 0],  [1, 0], [1, 0]],
    'URANIUM': [[9, 0], [9, 0],  [8, 0], [8, 0],  [7, 0], [7, 0],  [6, 0],
                  [5, 0],  [4, 0], [3, 0],  [2, 0],  [1, 0]]}

    if to_buy > resource_state[what]:
        return "sorry only "+ str(resource_state[what])+' ' + what +" to buy"

    def fill_bin(what):
        for i in range(resource_state[what]):
            bin_dic[what][i][1] = 1

    fill_bin(what)
    monies = [a[0]*a[1] for a in bin_dic[what] if a[1]>0]
    run_sum = 0
    for i in range(len(monies)-1, len(monies)- to_buy-1, -1):
        run_sum += monies[i]
    return run_sum

#print(how_much_to_buy(resource_state, to_buy, what))