import wolframalpha

appid = "74PH97-WLV3Y3G8XR"
client = wolframalpha.Client(appid)

res = client.query('temperature in State College, PA now')

print(next(res.results).text[:5])
