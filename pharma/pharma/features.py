from dateutil import parser
from datetime import datetime

from scrapy.utils.trackref import NoneType

def clean_date(date_raw):

    class GermanParserInfo(parser.parserinfo):
        MONTHS = [
            ('Jan', 'Januar', 'Jänner', 'January', 'Jan.'),
            ('Feb', 'Februar', 'February', 'Feb.'),
            ('Mär', 'Mrz', 'März', 'March', 'Mar'),
            ('Apr', 'April'),
            ('Mai', 'May'),
            ('Jun', 'Juni', 'June'),
            ('Jul', 'Juli', 'July'),
            ('Aug', 'August'),
            ('Sep', 'Sept', 'September'),
            ('Okt', 'Oktober', 'October', 'Oct.', 'Oct'),
            ('Nov', 'November'),
            ('Dez', 'Dezember', 'December', 'Dec.', 'Dec'),
        ]

    if date_raw == " von ":
        date_raw = datetime.today().strftime("%d-%m-%Y")
    elif type(date_raw) == NoneType:
        date_raw = datetime.today().strftime("%d-%m-%Y")

    date = date_raw.replace('/', '.')
    # date = parse(date)
    date = parser.parse(date, GermanParserInfo())
    date = date.strftime("%d-%m-%Y")
    date = datetime.strptime(date, '%d-%m-%Y')

    return date