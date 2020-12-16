import requests

x = requests.get('https://api.themoviedb.org/3/search/movie?api_key=6427e11274426be9030b97aab51ef6f8&query=Jack+Reacher')

f = x.json()
cantidad = f['total_results']

for i in range (cantidad):
    print(f['results'][i]['title'])



#print(f['results'][1]['title'])