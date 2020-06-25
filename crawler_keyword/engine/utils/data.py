import re
from pyvi import ViTokenizer
from joblib import load

"""
date format: d/m/y
date_range format: (d/m/y, d/m/y)
check if date is in the date_range
"""
def date_in_range(date, date_range):
    try:
        if date and date_range:
            date_start = date_range[0]
            date_end = date_range[1]
            date_tuple = [int(elem) for elem in reversed(date.split("/"))]
            date_start_tuple = [int(elem) for elem in reversed(date_start.split("/"))]
            date_end_tuple = [int(elem) for elem in reversed(date_end.split("/"))]
            return date_start_tuple < date_tuple < date_end_tuple
        else:
            return True
    except Exception as e:
        print("Error checking date in range "+str(e))
        return True

"""
Remove image, table, html tags from text
"""
def prepare_content(text):
    img_filter = "<img.*?>"
    table_filter = "<table(.|\n)*?</table>"
    tag_filter = "<.*?>"
    linebreak_filter = "\\n"
    result = text
    result = re.sub(img_filter,"",result)
    result = re.sub(table_filter,"",result)
    result = re.sub(tag_filter,"",result)
    result = re.sub(linebreak_filter,"",result)

    return result

def tokenize_content(text):
    return ViTokenizer.tokenize(text)

def sentiment(doc):
    x = [str(doc)]
    model = load('/model/model.pkl')
    pred = model.predict(x)
    result = 'POS' if pred == ['up'] else 'NEG'
    return result