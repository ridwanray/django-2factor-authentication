import factory
import pyotp
from django.contrib.auth.models import User
from faker import Faker
from faker.providers import file
from user.models import User

fake = Faker()
fake.add_provider(file)

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        
    email = factory.Sequence(lambda n: 'person{}@example.com'.format(n))
    password = factory.PostGenerationMethodCall('set_password','passer@@@111')
    otp_base32 = pyotp.random_base32()
    qr_code = fake.file_path(depth=3, category='image')

    