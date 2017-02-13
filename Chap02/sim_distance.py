from math import sqrt


def sim_distance(prefs, person1, person2):
    share = []
    for film in prefs[person1]:
        if film in prefs[person2]:
            share.append(film)
    sum = 0
    for film in share:
        len = pow(prefs[person1][film] - prefs[person2][film], 2)
        sum += len
    distance = 1.0 / (1.0 + sqrt(sum))
    return distance


print(sim_distance(critics, 'Lisa Rose', 'Gene Seymour'))
