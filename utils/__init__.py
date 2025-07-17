import yaml 


def load_config(path):
    with open(path , 'r') as fp:
        data = yaml.safe_load(fp) 
    return data 