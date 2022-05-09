from django.contrib.auth.models import User


def authenticate(client):
    user = User.objects.create_user(
        'dummyuser', 'dummy@email.com', 'dummypassword')
    client.force_authenticate(user=user)
