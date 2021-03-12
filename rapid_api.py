import requests
import json

"""
	Reference link https://rapidapi.com/b2g.corporation/api/amazon24
"""


def request_api(amazon_product_ids):
	"""
		Scraped user count and score of amazon products.
	"""
	data = []
	for product_id in amazon_product_ids:
		url = "https://amazon-product-reviews-keywords.p.rapidapi.com/product/details"
		querystring = {"asin": product_id, "country":"US", "variants":"1", "top":"0"}
		headers = {
					'x-rapidapi-key': "api-key-generated-from-rapid-api",
					'x-rapidapi-host': "amazon-product-reviews-keywords.p.rapidapi.com"
				}
		response = requests.get(url, headers=headers, params=querystring)
		if (200 == response.status_code):
			data = json.loads(response.text)
			user_count = int(data['product']['reviews']['total_reviews'])
			user_orig = float(data['product']['reviews']['rating'])

			data.append({
							"count" : user_count,
							"score" : user_orig,
							"product_id" : product_id
						})
		else:
			print (product_id)
			print ('empty data...')

	return data


if __name__ == "__main__":
	product_ids = []
	request_api(product_ids)
	# you can add function where you can save the scraped data.
	print ('Done!!!')

