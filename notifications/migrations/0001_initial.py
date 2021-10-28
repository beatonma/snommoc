# Generated by Django 2.2.6 on 2019-11-09 22:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TaskNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=80, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
            ],
            options={
                'permissions': [('view_notification', 'Can view notifications generated by tasks'), ('dismiss_notification', 'Can dismiss notifications generated by tasks')],
            },
        ),
    ]
