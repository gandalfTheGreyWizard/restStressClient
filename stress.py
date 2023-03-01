import requests
import argparse
import logging
import json
import math
from collections import defaultdict
from p_tqdm import p_map

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', datefmt='%Y-%m-%d:%H:%M:%S', level=logging.INFO)

parser = argparse.ArgumentParser('Processing')
parser.add_argument('-c', '--config', help='json configuration path to be used by stress client', type=str)
parser.add_argument('-n', '--num_cpu', help='number of processing threads to be used', type=int)
parser.add_argument('-s', '--sample_len', help='length of the query sample to be stress tested with', type=int)
logger = logging.getLogger('Stress')

class Stress:
    def __init__(self, config_path='./config.json'):
        try:
            with open(config_path, 'r') as f:
                self.config_dict = json.load(f)
        except Exception as e:
            logger.error(e)
            logger.exception(e)
    def show_config(self):
        logger.info(json.dumps(self.config_dict))
    def export_requests(self, num_reqs):
        self.requests_to_process = []
        current_length = len(self.config_dict['requests'])
        iterations = math.floor(num_reqs / current_length)
        temp_dict_arr = []
        for i in range(0, current_length):
            self.config_dict['requests'][i]['headers'] = self.config_dict['config']['headers'][self.config_dict['requests'][i]['headers']]
            temp_dict_arr += [self.config_dict['requests'][i]] * iterations
        utility_object = Utils()
        response_objects = p_map(utility_object.process_requests, temp_dict_arr, num_cpus=64)
        print(response_objects)

class Utils:
    def __init__(self):
        self.session = requests.Session()
    def get_request(self, url, req_headers):
        request_obj = self.session.get(url, headers=req_headers)
        return request_obj
        # logger.info(response_dict)
    def post_request(self, url, body, headers):
        request_obj = self.session.post(url, body, headers)
        return request_obj
        # logger.info(response_dict)
    def process_requests(self, each_request_object):
        if each_request_object['type'] == 'get':
            return self.get_request(each_request_object['url'], each_request_object['headers'])
        elif each_request_object['type'] == 'post':
            return self.post_request(each_request_object['url'], each_request_object['body'], each_request_object['headers'])
        else:
            logger.erro('problem parsing request object {}'.format(each_request_object))

if __name__ == '__main__':
    args = parser.parse_args()
    utils_object = Utils()
    if args.config:
        stress_client = Stress(args.config)
    else:
        stress_client = Stress()
    # stress_client.show_config()
    stress_client.export_requests(args.sample_len)
    # if args.config:
        # logging.info(args.config)
    # else:
        # logging.info('please provide a configuration')
