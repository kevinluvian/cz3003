from api.models import Crisis, CrisisStatus
from api.utils.tests import BaseTestCase
from cz3003backend.settings import FIRE_KEY, CMC_KEY


class CMSEndpointTest(BaseTestCase):
	def setUp(self):
		self.client.login(username='user1', password='123123123')

	def test_cms_integration(self):
		# get all crisis
		data = self.get_api('/api/crisis/')
		# assert 0
		self.assertEqual(len(data), 0)

		# create a new crisis, using fire key, assert fail
		new_crisis_data = {
			'location': 'Singapore 1',
			'detail': 'detail',
			'assigned_agency': 'fire department'
		}
		self.post_api_fail('/api/crisis/create/', {'key': FIRE_KEY, **new_crisis_data})
		# create a new crisis, using cmc key, assert success
		data = self.post_api('/api/crisis/create/', {'key': CMC_KEY, **new_crisis_data})
		# get all crisis
		data = self.get_api('/api/crisis/')
		# assert 1
		self.assertEqual(len(data), 1)
		crisis1 = Crisis.objects.get()
		# create a new crisis, using cmc key, assert success
		data = self.post_api('/api/crisis/create/', {'key': CMC_KEY, **new_crisis_data})
		# get all crisis
		data = self.get_api('/api/crisis/')
		# assert 2
		self.assertEqual(len(data), 2)
		crisis2 = Crisis.objects.all().exclude(id=crisis1.id).get()

		# edit crisis, using fire key, assert fail
		edit_crisis_data = {
			'location': 'Singapore 1 edit',
			'detail': 'detail edit',
		}
		self.post_api_fail('/api/crisis/{}/edit/'.format(crisis1.id), {'key': FIRE_KEY, **edit_crisis_data})
		# edit crisis, using cmc key, assert success
		self.post_api('/api/crisis/{}/edit/'.format(crisis1.id), {'key': CMC_KEY, **edit_crisis_data})
		# get all crisis
		data = self.get_api('/api/crisis/{}/'.format(crisis1.id))
		# assert edited
		self.assertEqual(data['location'], edit_crisis_data['location'])
		self.assertEqual(data['detail'], edit_crisis_data['detail'])

		# update crisis 1 action
		self.post_api('/api/crisis/{}/create_action_update/'.format(crisis1.id), {'key': CMC_KEY, 'description': 'fire dept on the way'})
		# get all crisis
		data = self.get_api('/api/crisis/')
		# assert updated on crisis 1
		self.assertEqual(len(data[0]['action_updates']), 1)
		self.assertEqual(data[0]['action_updates'][0]['description'], 'fire dept on the way')
		# assert no change on crisis 2
		self.assertEqual(len(data[1]['action_updates']), 0)
		# update crisis 1 action
		self.post_api('/api/crisis/{}/create_action_update/'.format(crisis1.id), {'key': CMC_KEY, 'description': 'fire dept arrived'})
		# get all crisis
		data = self.get_api('/api/crisis/')
		# assert updated on crisis 1
		self.assertEqual(len(data[0]['action_updates']), 2)
		self.assertEqual(data[0]['action_updates'][0]['description'], 'fire dept on the way')
		self.assertEqual(data[0]['action_updates'][1]['description'], 'fire dept arrived')
		# assert no change on crisis 2
		self.assertEqual(len(data[1]['action_updates']), 0)
		# update crisis 2 action
		self.post_api('/api/crisis/{}/create_action_update/'.format(crisis2.id), {'key': CMC_KEY, 'description': 'fire dept on the way 2'})
		# get all crisis
		data = self.get_api('/api/crisis/')
		# assert no change on crisis 1
		self.assertEqual(len(data[0]['action_updates']), 2)
		self.assertEqual(data[0]['action_updates'][0]['description'], 'fire dept on the way')
		self.assertEqual(data[0]['action_updates'][1]['description'], 'fire dept arrived')
		# assert updated on crisis 2
		self.assertEqual(len(data[1]['action_updates']), 1)
		self.assertEqual(data[1]['action_updates'][0]['description'], 'fire dept on the way 2')

		# edit crisis status, using fire key, assert fail
		self.post_api_fail('/api/crisis/{}/update_status/'.format(crisis1.id), {'key': FIRE_KEY, 'status': CrisisStatus.COMPLETED})
		# edit crisis status, using cmc key, assert success
		self.post_api('/api/crisis/{}/update_status/'.format(crisis1.id), {'key': CMC_KEY, 'status': CrisisStatus.COMPLETED})
		# get all crisis
		data = self.get_api('/api/crisis/')
		# assert updated on crisis 1
		self.assertEqual(data[0]['id'], crisis1.id)
		self.assertEqual(data[0]['status'], CrisisStatus.COMPLETED)
		# assert no change on crisis 2
		self.assertEqual(data[1]['status'], CrisisStatus.IN_PROGRESS)

		# notify public
		self.post_api('/api/crisis/{}/notify_public/'.format(crisis2.id), {'key': CMC_KEY, 'description': 'notification to public'})
		# assert success
