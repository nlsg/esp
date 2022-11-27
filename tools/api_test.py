#!/usr/bin/env python3
import requests
from time import perf_counter
from datetime import datetime as dt
from docer import dict_to_org, pop_keys

ROOT_URL = "http://192.168.43.31:5000/"

request_generator = lambda *calls: (lambda: requests.get(ROOT_URL + call[0], params=call[1])
                         for call in calls)

tee = lambda f, a: (a, f(a))[0]

def chain(*iterables):
    for it in iterables:
        for element in it:
            yield element
            
def benchmark(gen, io, count=1):
    t1 = perf_counter()
    results = list(tee(io, g()) for g in gen for i in range(count))
    t1 = (perf_counter() - t1) * 1000
    return {"resp": {r.url:r for r in results},
            "content": {r.url:r._content for r in results},
            "time": f"{int(t1)}ms",
            "count": f"{count}",
            "average_ms": f"{t1 / count:.3}",
            "request/s": f"{1000 / (t1 / count)}"}

def sum_reports(reports):
    result = dict()
    for n, report in enumerate(reports):
       result[n] = {i:r for i, r in enumerate(report)}
    print(dict_to_org(result, indent=2))
    


stamp = lambda: dt.now().strftime("%Y-%m-%d - %H:%M:%S")

n = 0

def io_function(a):
    global n
    n = n + 1
    print(f"{a} #{n}  ",
          "\n ".join((stamp(), a.url, str(a._content))))

def benchmarking(url, pins, iterations):
    return (benchmark(request_generator(req),
                      io_function,
                      iterations)
            for req in ((url, {"pin":p})
                        for p in pins))

def report_to_org(*tests):
    return sum_reports(chain(
        benchmarking(test[0], test[1], test[2] if len(test) > 2 else 1)
        for test in tests ))

pay = {"get": "api/gpio/set",
       "set": "api/gpio/set",
       "read": "api/gpio/read",
       "ds18": "api/gpio/ds18"}

# report_to_org(pay["get"], list(range(1,35)))
report_to_org(
    (pay["set"], (2, 26)),
    (pay["get"], (2, 26),10),
    (pay["ds18"], (4,),2),
    (pay["read"], (33,),2),
    (pay["get"], (2, 26),10))
