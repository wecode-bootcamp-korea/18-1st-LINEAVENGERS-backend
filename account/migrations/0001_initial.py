

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_id', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=300)),
                ('name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=11)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('email', models.CharField(max_length=50)),
                ('image_url', models.URLField(max_length=2000, null=True)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
