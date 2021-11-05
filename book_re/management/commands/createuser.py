from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from faker import Faker
from book_re import models

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('num', nargs='+', type=int)

    def handle(self, *args, **options):
        #print(options.get('num'))
        number = options.get('num')[0]   # 注意：此处options.get('num')是一个列表
        if number is None:
            number = 5
        password = make_password('123456')
        faker = Faker(locale="En")
        for _ in range(int(number)):
            data = {
                'username': faker.name_male(),
                'mobile': faker.phone_number(),
                'password': password,
                'is_superuser': True,
            }
            try:
                a = User.objects.create(
                    **data
                )
                self.stdout.write("self.style.SUCCESS()")
                a.save()
                b = models.User_cast(user=a)
                b.save()
            except:
                CommandError('创建失败！')
            self.stdout.write(self.style.SUCCESS('Successfully create user "%s"' % faker.name_male()))