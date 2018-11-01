from rest_framework.test import APITestCase
import json


class BaseTestCase(APITestCase):
	def get_api_pagination(self, url):
		res = self.client.get(url)
		if res.status_code != 200:
			print(res.content)
		self.assertEqual(res.status_code, 200, msg=res.content)
		data = json.loads(res.content)
		self.assertEqual(data['success'], True)
		return data.get('data', None), data.get('pagination', None)

	def get_api(self, url ,data=None):
		res = self.client.get(url, data)
		if res.status_code != 200:
			print(res.content)
		self.assertEqual(res.status_code, 200, msg=res.content)
		data = json.loads(res.content)
		self.assertEqual(data['success'], True)
		return data.get('data', None)

	def get_api_raw(self, url, verify_status_code=True):
		res = self.client.get(url)
		if verify_status_code:
			if res.status_code != 200:
				print(res.content)
			self.assertEqual(res.status_code, 200, msg=res.content)
		return res

	def post_api_raw(self, url, data, verify_status_code=True):
		res = self.client.post(url, data, format='json')
		if verify_status_code:
			if res.status_code != 200:
				print(res.content)
			self.assertEqual(res.status_code, 200, msg=res.content)
		return res

	def get_api_fail(self, url):
		res = self.client.get(url)
		self.assertEqual(res.status_code, 400)
		data = json.loads(res.content)
		self.assertEqual(data['success'], False)
		return data.get('errors', None)

	def post_api(self, url, data=None):
		res = self.client.post(url, data, format='json')
		if res.status_code != 200:
			print(res.content)
		self.assertEqual(res.status_code, 200, msg=res.content)
		data = json.loads(res.content)
		if data['success'] is False:
			print(data)
		self.assertEqual(data['success'], True)
		return data.get('data', None)

	def post_api_multipart(self, url, data=None):
		res = self.client.post(url, data)
		if res.status_code != 200:
			print(res.content)
		self.assertEqual(res.status_code, 200, msg=res.content)
		data = json.loads(res.content)
		if data['success'] is False:
			print(data)
		self.assertEqual(data['success'], True)
		return data.get('data', None)

	def post_api_fail(self, url, data=None):
		res = self.client.post(url, data, format='json')
		if res.status_code != 400:
			print(res.content)
		self.assertEqual(res.status_code, 400, msg=res.content)
		data = json.loads(res.content)
		self.assertEqual(data['success'], False)
		return data.get('errors', None)
