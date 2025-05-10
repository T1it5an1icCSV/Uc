from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('store', '0001_initial'),  # Укажите последнюю миграцию, которая есть у вас
    ]

    operations = [
        # Добавляем slug полям для Category и Product
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, null=True, unique=True, verbose_name='URL'),
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, null=True, unique=True, verbose_name='URL'),
        ),
        # Изменяем поле postal_code в Order
        migrations.AlterField(
            model_name='order',
            name='postal_code',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Почтовый индекс'),
        ),
    ] 