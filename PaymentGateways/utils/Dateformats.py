import datetime


def dateToMilliseconds(date):
    dt_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    # Convert the datetime object to a timestamp in seconds
    timestamp_seconds = int(dt_obj.timestamp())

    # Convert to milliseconds
    timestamp_milliseconds = timestamp_seconds * 1000
    return timestamp_milliseconds
