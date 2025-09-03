from .validator import validator_data
def processor_data(data):
    if(validator_data(data)):
            return f'Processed Data:{data}'
    return 'invalid Data'