import pytest
from django.test import RequestFactory
from django.urls import reverse

from sdap.users.api.views import UserViewSet
from sdap.users.models import User

from django.core import mail
from rest_framework import status
from rest_framework.test import APITestCase

pytestmark = pytest.mark.django_db


class ProjectCRUDTest(APITestCase):

    # user endpoints needed
    register_url = "/api/v1/users/"
    activate_url = "/api/v1/users/activation/"
    resend_verification_url = "/api/v1/users/resend_activation/"
    login_url = "/api/v1/token/login/"
    user_details_url = "/api/v1/users/"

    # project endpoints needed
    crud_project = "/api/v1/projects/"
    selected_project = "/api/v1/projects/1/"


    # user information
    user_data = {
        "email": "test@example.com", 
        "username": "test_user", 
        "password": "verysecret"
    }
    login_data = {
        "email": "test@example.com", 
        "password": "verysecret"
    }

    #project information
    project = {
        "title":"TestProject",
        "description":"My test project",
        "organism":"Human",
        "assembly":"hg38",
        "tissue":"Liver",
        "sample_number":20,
        "application":"BRB-sequencing",
    }

    def test_create_project_with_registered_user(self):
        # register the new user
        response = self.client.post(self.register_url, self.user_data, format="json")
        # expected response 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # expected one email to be send
        self.assertEqual(len(mail.outbox), 1)
        
        # parse email to get uid and token
        email_lines = mail.outbox[0].body.splitlines()
        # you can print email to check it
        #print(mail.outbox[0].subject)
        #print(mail.outbox[0].body)
        activation_link = [l for l in email_lines if "/activate/" in l][0]
        uid, token = activation_link.split("/")[-2:]
        
        # verify email
        data = {"uid": uid, "token": token}
        response = self.client.post(self.activate_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # login to get the authentication token
        response = self.client.post(self.login_url, self.login_data, format="json")
        self.assertTrue("auth_token" in response.json())
        token = response.json()["auth_token"]
        
        ###############################################
        #            USER Validation                  #
        ###############################################
        # set token in the header
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        # get user details
        response = self.client.get(self.user_details_url, format="json")

        ###############################################
        #            Project creation                 #
        ###############################################
        response = self.client.post(self.crud_project, self.project, format="json")
        # expected response 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    
    def test_create_project_no_registered_user(self):

        ###############################################
        #            Project creation                 #
        ###############################################
        response = self.client.post(self.crud_project, self.project, format="json")
        # expected response 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_project_with_registered_user(self):
        # register the new user
        response = self.client.post(self.register_url, self.user_data, format="json")
        # expected response 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # expected one email to be send
        self.assertEqual(len(mail.outbox), 1)
        
        # parse email to get uid and token
        email_lines = mail.outbox[0].body.splitlines()
        # you can print email to check it
        #print(mail.outbox[0].subject)
        #print(mail.outbox[0].body)
        activation_link = [l for l in email_lines if "/activate/" in l][0]
        uid, token = activation_link.split("/")[-2:]
        
        # verify email
        data = {"uid": uid, "token": token}
        response = self.client.post(self.activate_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # login to get the authentication token
        response = self.client.post(self.login_url, self.login_data, format="json")
        self.assertTrue("auth_token" in response.json())
        token = response.json()["auth_token"]
        
        ###############################################
        #            USER Validation                  #
        ###############################################
        # set token in the header
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        ###############################################
        #            Project creation                 #
        ###############################################
        response = self.client.post(self.crud_project, self.project, format="json")
        # expected response 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        updated_project = {
            "title":"New TestProject",
            "description":"My test project",
            "organism":"Human",
            "assembly":"hg38",
            "tissue":"Liver",
            "sample_number":20,
            "application":"BRB-sequencing",
        }
        response = self.client.put('/api/v1/projects/1/', data=updated_project, format='json',)
        response = self.client.get(self.selected_project,format='json')
        # expected response 
        self.assertEqual(response.status_code, status.HTTP_200_OK)