from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='no',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='menu',
            name='no',
            field=models.CharField(max_length=5, unique=True),
        ),
    ]
