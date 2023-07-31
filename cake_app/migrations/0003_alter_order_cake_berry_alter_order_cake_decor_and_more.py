# Generated by Django 4.1.7 on 2023-07-30 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cake_app', '0002_alter_berries_price_alter_berries_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cake_berry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='cake_app.berries', verbose_name='Ягоды'),
        ),
        migrations.AlterField(
            model_name='order',
            name='cake_decor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='cake_app.decors', verbose_name='Декор'),
        ),
        migrations.AlterField(
            model_name='order',
            name='cake_form',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='cake_app.forms', verbose_name='Форма торта'),
        ),
        migrations.AlterField(
            model_name='order',
            name='cake_size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='cake_app.sizes', verbose_name='Количество уровней торта'),
        ),
        migrations.AlterField(
            model_name='order',
            name='cake_topping',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='cake_app.toppings', verbose_name='Топпинг'),
        ),
        migrations.AlterField(
            model_name='sizes',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Количество уровней торта'),
        ),
    ]