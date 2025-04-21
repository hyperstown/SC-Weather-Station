from urllib.request import urlopen
from .parser import HTMLParser2
from .utils import extract_numbers, dfilter
from . import settings


def sensor_values(request):
    response = urlopen(settings.SOURCE_DATA_URL)
    content = response.read().decode("utf-8")
    # with open("./temp/table.html") as file:
    #     content = file.read()
    parser = HTMLParser2(content)

    table_data = []
    rows = parser.get_elements_by_tag_name('tr')
    # Extract headers from the first row (if <th> exists)
    headers = [header.data.lower() for header in rows[0].children]
    # Extract data from remaining rows
    for row in rows[1:]:  # Skip header row
        values = [extract_numbers(cell.data) for cell in row.children if cell.tag == 'td']
        if len(values) != len(headers):
            continue
        row_dict = dict(zip(headers, values))  # Match values to headers
        table_data.append(row_dict)

    data = table_data

    if request.query_params:
        data = dfilter(data, **request.query_params)

    return [
        {"sensordatavalues": data} # keep same as community api
    ]

    