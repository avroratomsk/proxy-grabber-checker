from multiprocessing import Pool

import requests
import time


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


start = time.time()


def get_location(proxy):
    proxy = {
        "http": f'socks4://{proxy}',
        "https": f'socks4://{proxy}'
    }

    if proxy['https'] != '':
        try:
            response = requests.get('https://whoer.net/v2/geoip2-city', headers={'Accept': 'application/json'}, proxies=proxy, timeout=5)
            response_json = response.json()

            # if str(response_json['country_code']) == 'RU':
            if str(response_json['subdivision1_name']) != 'None' or str(response_json['city_name']) != 'None':

                location = str(response_json['subdivision1_name']).replace('́с', 'с') + '|' + str(response_json['city_name']).replace('́с', 'с')

                print(color.BOLD + color.GREEN + "✔ " + color.END + color.BOLD + proxy['https'] + color.END + " (" + color.CYAN + str(response_json['subdivision1_name']).replace('́с', 'с') + color.END + ', ' + str(response_json['city_name']).replace('́с', 'с') + ")")

                f = open('./result_socks4.txt', 'a', encoding="utf-8")
                f.write(str(proxy['https']) + '|' + location + '\r')
        except Exception as e:
            print(color.BOLD + color.RED + "X " + color.END + color.BOLD + proxy['https'] + color.END)


def get_proxy_list():
    proxies = []
    with open('./socks4.txt', "r", encoding="utf-8") as file:
        for line in file:
            try:
                proxies.append(line.replace('\n', ''))
            except Exception as e:
                pass

    return proxies


if __name__ == '__main__':
    proxy_list = get_proxy_list()

    print(color.BOLD + "› Запущена проверка " + color.END + color.YELLOW + str(len(proxy_list)) + color.END + color.BOLD + " прокси" + color.END)

    f = open('./result_socks4.txt', 'w+', encoding="utf-8")
    f.write('')

    p = Pool(15)
    p.map(get_location, proxy_list)

    proxies = []
    with open('./result_socks4.txt', "r", encoding="utf-8") as file:
        for line in file:
            try:
                proxies.append(line.replace('\n', ''))
            except Exception as e:
                pass

    end = time.time() - start

    print()
    print(color.BOLD + 'Результат проверки:' + color.END)
    print(color.BOLD + color.CYAN + "• " + color.END + "Время выполнения {} сек.".format(str(end)))
    print(color.BOLD + color.CYAN + "• " + color.END + "Проверено " + color.YELLOW + str(len(proxy_list)) + color.END + " прокси")
    print(color.BOLD + color.CYAN + "   ¬ " + color.END + "Из них " + color.GREEN + str(len(proxies)) + color.END + " валидных")
    print(color.BOLD + color.CYAN + "   ¬ " + color.END + "И " + color.RED + str(len(proxy_list) - len(proxies)) + color.END + " не рабочих")
