import requests
from bs4 import BeautifulSoup



def get_html(link, file):
    r = requests.get(link).text
    return r

def get_field(soup, find_tag, param_dict=None):
    try:
        field = soup.find(find_tag, param_dict).text
    except AttributeError:
        field = '...'
    return field


def get_info(parse_text):
    soup = BeautifulSoup(parse_text, 'html.parser')

    title = get_field(soup, 'title')
    bath = get_field(soup, 'li', {'class': 'parnv'})
    seats = get_field(soup, 'li', {'class': 'mes'})
    bas = get_field(soup, 'li', {'class': 'bas'})
    price = get_field(soup, 'span', {'class': 'kr'})
    adress = get_field(soup, 'li', {'class': 'adr'})


    info = {'title': title,
                'fields': {
                    'bath': bath,
                    'bas': bas,
                    'seats': seats,
                    'price': price,
                    'adress': adress
                }
    }
    return info

    # with open(file, 'w', encoding='utf-8') as f:
    #     f.write(r.text)


def main():
    link1 = 'http://www.saunaminska.info/na-zamkovoi.htm'
    proc = get_info(get_html(link1, 'file1.txt'))

    print(proc['title'], end='\n\n')
    for k, v in proc['fields'].items():
        print(f'{k} - {v}')

if __name__ == '__main__':
    main()
