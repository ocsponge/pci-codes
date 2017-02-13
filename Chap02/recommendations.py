# 一个涉及影评者及其对几部影片评分情况的字典
critics = {
    'Lisa Rose': {'Lady in the water': 2.5, 'Snakes on a plane': 3.5, 'Just my luck': 3.0, 'Superman returns': 3.5,
                  'You, me and Dupree': 2.5, 'The night listener': 3.0},
    'Gene Seymour': {'Lady in the water': 3.0, 'Snakes on a plane': 3.5, 'Just my luck': 1.5, 'Superman returns': 5.0,
                     'The night listener': 3.0, 'You, me and Dupree': 3.5},
    'Michael Phillips': {'Lady in the water': 2.5, 'Snakes on a plane': 3.0, 'Superman returns': 3.5,
                         'The night listener': 4.0},
    'Claudia Puig': {'Snakes on a plane': 3.5, 'Just my luck': 3.0, 'The night listener': 4.5, 'Superman returns': 4.0,
                     'You, me and Dupree': 2.5},
    'Mick Lasalle': {'Lady in the water': 3.0, 'Snakes on a plane': 4.0, 'Just my luck': 2.0, 'Superman returns': 3.0,
                     'The night listener': 3.0, 'You, me and Dupree': 2.0},
    'Jack Matthews': {'Lady in the water': 3.0, 'Snakes on a plane': 4.0, 'The night listener': 3.0,
                      'Superman returns': 5.0, 'You, me and Dupree': 3.5},
    'Toby': {'Snakes on a plane': 4.5, 'You, me and Dupree': 1.0, 'Superman returns': 4.0}}

from math import sqrt

# 欧几里德距离
def sim_distance(prefs, person1, person2):
    share = {}
    for film in prefs[person1]:
        if film in prefs[person2]:
            share[film] = 1
    # 二者没有共同之处
    if len(share) == 0:
        return 0

    sum_of_squares = sum(
        [pow(prefs[person1][film] - prefs[person2][film], 2) for film in share])

    distance = 1.0 / (1.0 + sum_of_squares)
    return distance

# 皮尔逊相关系数
def sim_pearson(prefs, p1, p2):
    share = {}
    for film in prefs[p1]:
        if film in prefs[p2]:
            share[film] = 1
    # 二者没有共同之处
    if len(share) == 0:
        return 0
    sumxy = sum([prefs[p1][film] * prefs[p2][film] for film in share])
    sumx = sum([prefs[p1][film] for film in share])
    sumy = sum([prefs[p2][film] for film in share])
    sumxx = sum([prefs[p1][film] * prefs[p1][film] for film in share])
    sumyy = sum([prefs[p2][film] * prefs[p2][film] for film in share])
    n = len(share)

    den = sqrt((sumxx - sumx * sumx / n) * (sumyy - sumy * sumy / n))
    if den == 0:
        return 0
    pearson = (sumxy - sumx * sumy / n) / den
    return pearson

# 寻找最佳匹配者
# 返回结果的个数和相似度函数均为可选函数
def topmatches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other)
              for other in prefs if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]

# 利用所有他人的评价进行加权平均，为某人提供建议
def getrec(prefs, person, similarity=sim_pearson):
    simsum = {}
    totals = {}
    for other in prefs:
        if other == person:
            continue
        sim = similarity(prefs, person, other)
        if sim <= 0:
            continue
        for film in prefs[other]:
            if film not in prefs[person] or prefs[person][film] == 0:
                totals.setdefault(film, 0)
                totals[film] += sim * prefs[other][film]
                simsum.setdefault(film, 0)
                simsum[film] += sim

    ranking = [(total / simsum[film], film) for film, total in totals.items()]
    ranking.sort()
    ranking.reverse()
    return ranking

# 交换行和列
def transformPrefs(prefs):
    result = {}
    for k, v in prefs.items():
        for item in v:
            result.setdefault(item, {})
            result[item][k] = prefs[k][item]
    return result

# 构造数据集
def calculateSimilarItems(prefs, n=10):
    result = {}
    movies = transformPrefs(prefs)
    c = 0
    for film in movies:
        c += 1
        if c % 100 == 0:
            print('%d/%d' % (c, len(movies)))  # 更新进度
        result[film] = topmatches(movies, film, n=n, similarity=sim_distance)
    return result

# 基于物品的协作型过滤
def getrecbyitems(prefs, result, user):
    simsum = {}
    totals = {}
    for item, v in prefs[user].items():
        for (sim, item2) in result[item]:
            if item2 in prefs[user]:
                continue
            simsum.setdefault(item2, 0)
            simsum[item2] += sim
            totals.setdefault(item2, 0)
            totals[item2] += sim * v
    ranking = [(total / simsum[item], item) for item, total in totals.items()]
    ranking.sort()
    ranking.reverse()
    return ranking

# 加载movielen数据集
def loadmovielens(path='/home/ocsponge/文档/pythonwork/Recommendation'):
    movies = {}
    for line in open(path + '/u.item'):
        (id, title) = line.split('|')[0:2]
        movies[id] = title  # 影片id对应其名称

    prefs = {}
    for line in open(path + '/u.data'):
        (user, movieid, rating, time) = line.split('\t')
        prefs.setdefault(user, {})
        prefs[user][movies[movieid]] = float(rating)
    return prefs

prefs = loadmovielens()
itemsim=calculateSimilarItems(prefs,n=50)
list1 = getrecbyitems(prefs,itemsim, '87')[0:30]
for (k, v) in list1:
    print('%.1f,%s' % (k, v))
