import csv


class SimpleDialect(csv.Dialect):
    delimiter = ','
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\n'
    quoting = csv.QUOTE_NONNUMERIC


def write_csv(file, data, headers=None):
    with open(file, "w") as f:
        w = csv.writer(f, dialect=SimpleDialect())
        if headers is not None:
            w.writerow(headers)
        w.writerows(data)


def read_csv(file, headers=None):
    with open(file) as f:
        r = csv.reader(f, dialect=SimpleDialect())
        if headers is None or headers is False:
            return list(r)
        h, *data = r
        if headers is True:
            return h, data
        elif headers in ("ignore", "skip"):
            return data
        else:
            assert h == headers
            return data
