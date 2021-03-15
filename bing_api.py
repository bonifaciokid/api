import requests

"""
	Bing browser will take many days to crawl your webpage, google takes around 3.
	The best way is to send your page URL through their API.
	https://www.bing.com/webmasters/url-submission-api
"""


api_key = "your-api-key-generated-by-bing"
headers = {"Content-Type": "application/json", "charset": "utf-8"}
data = {
			"siteUrl":"https://yourwebsite.com/",
			"urlList": ['your', 'list', 'of', 'URL']
		}
request = requests.post('https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlBatch?apikey={}'.format(api_key), headers=headers, json=data)
response = request.status_code

if response == 200:
	print ('success!!!')
else:
	print ('error')
	print (response.text)

