import requests
import argparse
import logging
import json
from collections import defaultdict

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', datefmt='%Y-%m-%d:%H:%M:%S', level=logging.INFO)

parser = argparse.ArgumentParser('Processing')
parser.add_argument('-c', '--config', help='json configuration path to be used by stress client', type=str)
logger = logging.getLogger('Stress')

class Stress:
    def __init__(self, config_path='./config.json'):
        try:
            with open(config_path, 'r') as f:
                self.config_dict = json.load(f)
        except Exception as e:
            logger.error(e)
            logger.exception(e)
    def create_headers(self, token):
        headers = {
                'Authorization': 'Bearer {}'.format(token),
                'Content-Type': 'application/json'
                }
        return headers
    def get_request(self, url, req_headers):
        request_obj = requests.get(url, headers=req_headers)
        response_dict = request_obj.json()
        logger.info(response_dict)
    def post_request(self, url, body, headers):
        request_obj = requests.post(url, body, headers)
        response_dict = request_obj.json()
        logger.info(response_dict)
    def show_config(self):
        logger.info(json.dumps(self.config_dict))
    def process_requests(self):
        for each_request_object in self.config_dict['requests']:
            logger.info(each_request_object)
            request_headers = self.config_dict['config']['headers'][each_request_object['headers']]
            if each_request_object['type'] == 'get':
                self.get_request(each_request_object['url'], json.dumps(request_headers)),
            elif each_request_object['type'] == 'post':
                self.post_request(each_request_object['url'], each_request_object['body'], request_headers)
            else:
                logger.erro('problem parsing request object {}'.format(each_request_object))
if __name__ == '__main__':
    args = parser.parse_args()
    if args.config:
        stress_client = Stress(args.config)
    else:
        stress_client = Stress()
    # stress_client.show_config()
    stress_client.process_requests()
    # if args.config:
        # logging.info(args.config)
    # else:
        # logging.info('please provide a configuration')
