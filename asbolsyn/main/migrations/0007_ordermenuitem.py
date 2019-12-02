# Generated by Django 2.1.1 on 2019-11-24 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderMenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.MenuItem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='order_menu_items', to='main.Order')),
            ],
        ),
    ]
