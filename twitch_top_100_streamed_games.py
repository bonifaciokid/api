import requests
import json
import csv
import boto3
from botocore.client import Config
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class TwitchTopStreamedGames():


	"""
		In this example, we will scraped and saved top streamed games in Twitch. We will crawl game_id, game_name and viewers count. Saving scraped data to s3 and appending twitch top streamed games to googlesheet.

		You can find your AUTH_KEY through requests.
		req = requests.post("https://id.twitch.tv/oauth2/token?client_id={0}&client_secret={1}&grant_type=client_credentials".format(YOUR_CLIENT_ID, TWITCH_SECRET_KEY))
		print (req.body) and find your authorization key

	"""

	# get all top 100 streams from viewer_count in Twitch 
	def twitch_top_streamed_games(self):
		client_id = "TWITCH_API_CLIENT_ID"
		auth_key = "AUTHORIZATIO_KEY"
		headers = {'Client-ID' : client_id, 'Authorization': "Bearer YOUR_AUTH_KEY".format(auth_key
			)}
		query = 'streams?first=100'
		base_url = "https://api.twitch.tv/helix/"
		url = base_url + query
		response = requests.get(url, headers=headers)
		current_time = datetime.datetime.now()
		timestamp = current_time.timestamp()
		response_json = response.json()
		data = response_json['data']
		game_list = [game['game_name'] for game in data]
		game_names = list(set(game_list))
		print (game_names)

		return [data, timestamp]


	# make a csv file from scraped data 
	def file_to_csv(self, response):
		"""
			get unique game from the list and adding streamers and viewer count per game.
		"""
		data = response[0]
		timestamp = str(int(response[1]))
		unique_games = [game['game_id'] for game in data]
		game_ids = list(set(unique_games))

		final_data = []
		for game_id in game_ids:
			viewer_count = 0
			streamer_count = 0
			game_name = ''
			for info in data:
				if game_id == info['game_id']:
					viewer_count+=info['viewer_count']
					streamer_count+=1
					game_name = info['game_name']
			final_data.append([game_id, game_name, viewer_count, streamer_count, timestamp])

		if final_data:
			self.append_to_gsheet(final_data)#append new data to google sheet
			file_name = '{}.csv'.format(timestamp)
			columns = ['game_id', 'game_name', 'viewer_count', 'streamer_count', 'timestamp']
			with open('csv/' + file_name,'w') as w:
				writer=csv.writer(w)
				writer.writerow(columns)
				for itm in final_data:
					writer.writerow(itm)

			return file_name
		else:
			print ('No scraped data...')


	# upload csv file to s3 bucket
	def upload_python_objects(self, file_name):
		aws_access_key = "AWS_ACCESS_KEY"
		aws_secret_key= "AWS_SECRET_KEY"
		bucket_name = 'BUCKET_NAME'
		directory = 'csv/' + file_name
		print (file_name)
		print ('uploading file to s3 bucket ' , bucket)
		s3 = boto3.resource(
								's3',
								aws_access_key_id=aws_access_key,
								aws_secret_access_key=aws_secret_key,
								config=Config(signature_version='s3v4')
							)
		s3.meta.client.upload_file(directory, bucket_name, file_name, ExtraArgs={"ContentType":'application/csv', "ACL":'public-read'})


	# add new data to google sheet
	def append_to_gsheet(self, data):
		work_sheet = "google-sheet-name"
		scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
		credentials = ServiceAccountCredentials.from_json_keyfile_name('/path/to/file/client_credentials.json', scopes=scope)
		client = gspread.authorize(credentials)
		sheet = client.open(work_sheet).sheet1
		sheet.append_rows(data)
		print ('new data sheet added...')


if __name__ == "__main__":
	twitch = TwitchTopStreamedGames()
	response = twitch.twitch_top_streamed_games()
	saved_data = twitch.file_to_csv(response)
	upload = twitch.upload_python_objects(saved_data)

	print ('Done...')
