import unicodedata

def extract_numbers(value):
    if str(value).strip().startswith('--'):
        raise ValueError("Empty data")
    try:
        return float(
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode('ascii').split(" ")[0]
        )
    except:
        return value


def dfilter(lst, **kwargs):
    include = {k: v for k, v in kwargs.items() if not k.endswith("!")}
    exclude = {k[:-1]: v for k, v in kwargs.items() if k.endswith("!")}
    data = [d for d in lst if all(d.get(k) in v for k, v in include.items())]
    data = [d for d in data if all(d.get(k) not in v for k, v in exclude.items())]
    return data
