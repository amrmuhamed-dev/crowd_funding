# Generated by Django 4.2.2 on 2023-06-23 23:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fundraising', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='compaign_categ',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='fundraising.project_compaign'),
        ),
        migrations.AlterField(
            model_name='image',
            name='compaign_img',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='fundraising.project_compaign'),
        ),
    ]
