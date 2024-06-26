# Generated by Django 5.0.1 on 2024-04-13 07:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studygroup', '0005_chatroommember_is_admin_chatroommember_is_approved'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='num_resources',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(choices=[('IMAGE', 'Image'), ('VIDEO', 'Video'), ('LINK', 'Link')], default='LINK', max_length=10)),
                ('image', models.ImageField(blank=True, upload_to='chatroom_resources/images/')),
                ('video_url', models.URLField(blank=True)),
                ('link', models.URLField(blank=True)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('chatroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studygroup.chatroom')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
