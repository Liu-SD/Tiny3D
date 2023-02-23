import argparse
import json

def parse_config():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", default=None, type=str,
                        help="The config json file.")
    parser.add_argument("--list_modules", action='store_true',
                        help="The configuration options of given module type.")
    parser.add_argument("--doc", default=None, type=str,
                        help="Show the module's document string.")
    args = parser.parse_args()
    if args.config is not None:
        with open(args.config) as f:
            pipline = json.load(f)
    else:
        pipline = None
    return args, pipline
