from csv import reader
from math import sqrt
from json import dump


def csv_reader(path):
    lst = []
    with open(path, "r") as f_obj:
        rdr = reader(f_obj)
        next(rdr)
        for row in rdr:
            row.pop(0)
            lst.append(row)
    return lst


def sim(u, v):
    numerator = d1 = d2 = 0
    for i in range(len(u)):
        if u[i] == -1 or v[i] == -1:
            continue
        numerator += u[i] * v[i]
        d1 += round(sqrt(u[i] ** 2), 3)
        d2 += round(sqrt(v[i] ** 2), 3)
    return round(numerator / (d1 * d2), 3)


def avg(u):
    avg_u = cnt_u = 0
    for i in range(len(u)):
        if u[i] != -1:
            avg_u += u[i]
            cnt_u += 1
    return round(avg_u / cnt_u, 3)


def kNN(u, numb):
    lst = []
    for k in range(len(u)):
        lst.append(-1)
    if len(u) >= numb:
        u_copy = u.copy()
        u_copy = sorted(u_copy, key=float, reverse=True)
        u_copy = u_copy[:numb]
        for i in range(len(u)):
            for j in range(len(u_copy)):
                if u_copy[j] == u[i]:
                    lst[i] = u[i]
    return lst


def r_u_i(u, i, data, sims_knn):
    n1 = denominator = 0
    for v in range(len(sims_knn)):
        if sims_knn[v] == -1:
            continue
        n1 += sims_knn[v]*(data[v][i] - avg(data[v]))
        denominator += abs(sims_knn[v])
    return round(avg(u) + n1 / denominator, 3)


def recommend(user, data, sims_knn, place, day, new_rnk, not_rnk_film):
    rec = {}
    for v in range(len(sims_knn)):
        if sims_knn[v] != -1:
            for i in range(len(data[0])):
                if data[user][i] == -1 and place[v][i] == ' h' and (day[v][i] == ' Sat' or day[v][i] == ' Sun') \
                        and data[v][i] > avg(data[v]):
                    for l in range(len(not_rnk_film)):
                        if i == not_rnk_film[l]:
                            rec["Movie " + str(i + 1)] = new_rnk[l]
    return rec


def make_json(user, new_rnk, not_rnk_films, recom):
    tmp_lst = {}
    for i in range(len(not_rnk_films)):
        tmp_lst["Movie " + str(not_rnk_films[i] + 1)] = new_rnk[i]
    tmp_lst = {i: tmp_lst[i] for i in sorted(tmp_lst.keys())}
    json_lst = {
        "user": "User" + str(user + 1),
        "1": tmp_lst,
        "2": recom
    }
    return json_lst


def rate_film(user, data, place, day):
    user -= 1
    sims = []
    for j in range(len(data)):
        if user != j and data[user] != -1 and data[j] != -1:
            sims.append(sim(data[user], data[j]))
        else:
            sims.append(-1)

    sims_knn = []
    rnk_all = []
    not_ranked = []
    sims_knn = kNN(sims, 4)

    for i in range(len(data[0])):
        if data[user][i] == -1:
            rank = r_u_i(data[user], i, data_list, sims_knn)
            rnk_all.append(rank)
            not_ranked.append(i)
    recom = recommend(user, data, sims_knn, place_list, day_list, rnk_all, not_ranked)
    json_file = make_json(user, rnk_all, not_ranked, recom)
    print(json_file)
    with open('user.json', 'w') as outfile:
        dump(json_file, outfile)


data_list = csv_reader("data.csv")
day_list = csv_reader("context_day.csv")
place_list = csv_reader("context_place.csv")

for i in range(len(data_list)):
    for j in range(len(data_list[0])):
        data_list[i][j] = int(data_list[i][j])

user_id = int(input("Please enter a user id: "))
rate_film(user_id, data_list, place_list, day_list)


