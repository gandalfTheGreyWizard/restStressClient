import requests
import argparse
import logging

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', datefmt='%Y-%m-%d:%H:%M:%S', level=logging.INFO)

parser = argparse.ArgumentParser('Processing')
parser.add_argument('-c', '--config', help='json configuration path to be used by stress client', type=str)
logger = logging.getLogger('Stress')

class Utils:
    def create_headers(token):
        headers = {
                'Authorization': 'Bearer {}'.format(token),
                'Content-Type': 'application/json'
                }
        return headers
    def get_request(url, token):
        request_header = create_headers(token)
        request_obj = requests.get()

class Stress:
    def __init__(self, config_path):
        self.config_path = config_path

if __name__ == '__main__':
    args = parser.parse_args()
    if args.config:
        logging.info(args.config)
    else:
        logging.info('please provide a configuration')
