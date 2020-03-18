""" Samsung info fetcher """
import json
import re

from requests import get


def fetch_devices():
    """Fetch models from gplay cerification data"""
    try:
        data = get('https://raw.githubusercontent.com/androidtrackers/'
                   'certified-android-devices/master/by_brand.json').json()
        samsung = data['Samsung']
        devices = {}
        for item in samsung:
            name = item['name']
            if not name:
                continue
            model = item['model']
            if 'samsung-' in model.lower():
                model = re.sub('SAMSUNG-', '', model, re.IGNORECASE)
            devices.update({model: name})
        with open("../data/devices_info.json", 'w', encoding='utf-8') as output:
            json.dump(devices, output, ensure_ascii=False, indent=1)
    except json.decoder.JSONDecodeError:
        return


def main():
    """Main function"""
    fetch_devices()


if __name__ == '__main__':
    main()
