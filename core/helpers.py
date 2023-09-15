from datetime import datetime


def transform_time(input_time_str):
    output_time_str = ''
    try:
        input_datetime = datetime.strptime(input_time_str, "%m/%d/%Y %I:%M %p")
        output_time_str = input_datetime.strftime("%Y-%m-%dT%H:%M:%S.%f0Z")
        return output_time_str
    except:
        return output_time_str