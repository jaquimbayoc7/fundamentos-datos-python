import urllib.request, json

API_KEY = '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'

queries = [
    'streamflow forecasting SARIMA ARIMA time series river discharge prediction',
    'Holt-Winters exponential smoothing hydrological forecasting water discharge',
    'Prophet Facebook forecasting streamflow river flow prediction',
    'daily streamflow prediction comparison machine learning statistical models',
    'Colombia IDEAM river discharge analysis time series hydrology',
    'missing data imputation hydrological time series interpolation',
    'seasonal decomposition STL river flow stationarity ADF KPSS',
    'SARIMA vs Prophet water resources forecasting comparison metrics RMSE',
]

all_results = []
seen_urls = set()

for q in queries:
    data = json.dumps({
        'api_key': API_KEY,
        'query': q,
        'search_depth': 'advanced',
        'max_results': 5,
        'include_domains': [
            'sciencedirect.com', 'springer.com', 'mdpi.com',
            'tandfonline.com', 'wiley.com', 'nature.com',
            'researchgate.net', 'ieeexplore.ieee.org', 'hindawi.com',
            'journals.ametsoc.org',
        ],
    }).encode('utf-8')

    req = urllib.request.Request(
        'https://api.tavily.com/search',
        data=data,
        headers={'Content-Type': 'application/json'},
    )
    try:
        resp = urllib.request.urlopen(req, timeout=20)
        body = json.loads(resp.read().decode('utf-8'))
        for r in body.get('results', []):
            url = r.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                all_results.append({
                    'title': r.get('title', ''),
                    'url': url,
                })
    except Exception as e:
        print("Error en query [{}]: {}".format(q[:50], e))

print("=" * 80)
print("ARTICULOS ENCONTRADOS: {}".format(len(all_results)))
print("=" * 80)
for i, art in enumerate(all_results[:25], 1):
    t = art['title']
    u = art['url']
    print("{}. {}".format(i, t))
    print("   {}".format(u))
    print()
