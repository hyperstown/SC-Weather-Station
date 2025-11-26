import unicodedata
from decimal import Decimal, ROUND_HALF_UP

def extract_numbers(value):
    clear_value = unicodedata.normalize("NFKD", value)\
        .encode("ascii", "ignore")\
        .decode('ascii').split(" ")[0]
    try:
        return str(
            Decimal(clear_value)
            .quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
        )
    except:
        return "-" if clear_value == "-" else value


def dfilter(lst, **kwargs):
    include = {k: v for k, v in kwargs.items() if not k.endswith("!")}
    exclude = {k[:-1]: v for k, v in kwargs.items() if k.endswith("!")}
    data = [d for d in lst if all(d.get(k) in v for k, v in include.items())]
    data = [d for d in data if all(d.get(k) not in v for k, v in exclude.items())]
    return data
