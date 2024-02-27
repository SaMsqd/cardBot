def make_price_beautiful(price):  # функция для расставдения точек
    rl_price = list(str(price))
    rl_price.reverse()
    res = ""
    for i in range(len(rl_price)):
        if (i + 1) % 3 == 0:
            res += rl_price[i] + "."
        else:
            res += rl_price[i]
    if res[-1] == ".":
        res = res[:-1]
    return res[::-1]


def out_dots(elem):  # функция для удаления точек
    summ = ''
    for i in elem:
        if i in '0123456789':
            summ += i
    return summ

