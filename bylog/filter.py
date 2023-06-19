def format_date(value, fmt='%y/%m/%d'):
    return value.strftime(fmt)

def format_datetime(value, fmt='%Y/%m/%d %p %I:%M'):
    return value.strftime(fmt)