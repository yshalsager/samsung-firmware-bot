""" Samsung regions/models fetcher """
import json

from requests import get


def fetch_regions():
    """Fetch regions from samdb"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest', 'Connection': 'keep-alive',
        'Referer': 'https://samdb.org/firmware/', 'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
    try:
        data = get('https://samdb.org/ajax/regions?model=', headers=headers).json()
        regions = [i['text'].split(' ')[0] for i in data['results'][1:]]
        return regions
    except json.decoder.JSONDecodeError:
        return


def fetch_models():
    """Fetch models from sammobile"""
    try:
        data = get('https://www.sammobile.com/wp-content/themes/sammobile-5/'
                   'templates/fw-page/ajax/ajax.models.php?search').json()
        models = [i['id'] for i in data]
        return models
    except json.decoder.JSONDecodeError:
        return


def write_file(filename, data):
    """Write regions to a file"""
    with open(filename, 'w') as output:
        json.dump(data, output)


def main():
    """Main function"""
    regions = fetch_regions()
    if regions:
        write_file('regions.json', regions)
    models = fetch_models()
    if models:
        write_file('models.json', models)


if __name__ == '__main__':
    main()
