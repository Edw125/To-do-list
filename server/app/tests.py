# import datetime
#
# from django.conf import settings
# from django.urls import include, path
# from django.utils import timezone
# from rest_framework import status
# from rest_framework.reverse import reverse
# from rest_framework.test import APIClient, APITestCase, URLPatternsTestCase
#
# from mailing.models import Client, MailingList
#
#
# class BaseTestClass(APITestCase, URLPatternsTestCase):
#     import debug_toolbar
#     settings.DEBUG = True
#     urlpatterns = [
#         path("", include("mailing.urls")),
#         path('__debug__/', include(debug_toolbar.urls)),
#     ]
#
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         pass
#
#     def setUp(self):
#         self.unauthorized_client = APIClient()
#
#     def tearDown(self):
#         pass
#
#     @classmethod
#     def tearDownClass(cls):
#         pass
#
#
# class ClientApiTest(BaseTestClass):
#     def setUp(self):
#         super().setUp()
#         self.data = {
#             "phone": "79995552211",
#             "phone_code": "777",
#             "tag": "tag-1",
#             "time_zone": "Europe/Moscow"
#         }
#         self.client = Client.objects.create(**self.data)
#         self.tz = timezone.get_current_timezone()
#
#     def test_create_client(self):
#         """Создание /clients/"""
#         data = {
#             "phone": "79995552255",
#             "phone_code": "999",
#             "tag": "tag-2",
#             "time_zone": "Europe/Moscow"
#         }
#         response = self.unauthorized_client.post(reverse("mailing:clients-list"), data=data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(data.get("phone"), response.json().get("phone"))
#         self.assertEqual(data.get("phone_code"), response.json().get("phone_code"))
#         self.assertEqual(data.get("tag"), response.json().get("tag"))
#
#     def test_update_client(self):
#         """Обновление /clients/{id}/"""
#         data = {
#             "phone_code": "776",
#             "tag": "tag-3",
#             "time_zone": "Europe/Moscow"
#         }
#         response = self.unauthorized_client.patch(
#             reverse("mailing:clients-detail", kwargs={"pk": self.client.id}),
#             data=data
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(data.get("phone_code"), response.json().get("phone_code"))
#         self.assertEqual(data.get("tag"), response.json().get("tag"))
#
#     def test_delete_client(self):
#         """Удаление /clients/{id}/"""
#         response = self.unauthorized_client.delete(
#             reverse("mailing:clients-detail", kwargs={"pk": self.client.id})
#         )
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#
#
# class MailingApiTest(BaseTestClass):
#     def setUp(self):
#         super().setUp()
#         self.tz = timezone.get_current_timezone()
#         self.data = {
#             'text': 'test message',
#             'start_time': datetime.datetime.now(tz=self.tz),
#             'end_time': datetime.datetime.now(tz=self.tz) + datetime.timedelta(days=7),
#             'phone_codes': ['777', '888'],
#             'tags': ['tag-1', 'tag-2']
#         }
#         self.mailing = MailingList.objects.create(**self.data)
#
#     def test_create_mailing(self):
#         """Создание /mailing/"""
#         data = {
#             'text': 'test message',
#             'start_time': str(datetime.datetime.now(tz=self.tz)),
#             'end_time': str(datetime.datetime.now(tz=self.tz) + datetime.timedelta(days=7)),
#             'phone_codes': ['666', '999'],
#             'tags': ['tag-1', 'tag-2']
#         }
#         response = self.unauthorized_client.post(reverse("mailing:mailing-list"), data=data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(data.get("text"), response.json().get("text"))
#         self.assertEqual(data.get("phone_codes"), response.json().get("phone_codes"))
#         self.assertEqual(data.get("tags"), response.json().get("tags"))
#
#     def test_list_mailing(self):
#         """Получение /mailing/"""
#         response = self.unauthorized_client.get(reverse("mailing:mailing-list"))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.json()), 1)
#
#     def test_detail_mailing(self):
#         """Получение /mailing/{id}/"""
#         response = self.unauthorized_client.get(reverse("mailing:mailing-detail", kwargs={"pk": self.mailing.id}))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(self.data.get("text"), response.json().get("text"))
#         self.assertEqual(self.data.get("phone_codes"), response.json().get("phone_codes"))
#         self.assertEqual(self.data.get("tags"), response.json().get("tags"))
#
#     def test_update_mailing(self):
#         """Обновление /mailing/{id}/"""
#         data = {
#             'text': 'other test message',
#             'phone_codes': ['666', '999'],
#             'tags': ['tag-3', 'tag-4']
#         }
#         response = self.unauthorized_client.patch(
#             reverse("mailing:mailing-detail", kwargs={"pk": self.mailing.id}),
#             data=data
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(data.get("text"), response.json().get("text"))
#         self.assertEqual(data.get("phone_codes"), response.json().get("phone_codes"))
#         self.assertEqual(data.get("tags"), response.json().get("tags"))
#
#     def test_delete_mailing(self):
#         """Удаление /mailing/{id}/"""
#         response = self.unauthorized_client.delete(
#             reverse("mailing:mailing-detail", kwargs={"pk": self.mailing.id})
#         )
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
