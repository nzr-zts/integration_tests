# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-02-20 12:09
from __future__ import unicode_literals

import yaml
from django.db import migrations, models


def add_type_to_provider(apps, schema_editor):
    from cfme.utils.conf import cfme_data
    Provider = apps.get_model("appliances", "Provider")  # noqa
    for provider in Provider.objects.using(schema_editor.connection.alias).all():
        # Need to replicate the functionality from the model here
        provider_data = yaml.load(provider.object_meta_data).get('provider_data')
        if not provider_data:
            provider_data = cfme_data.get("management_systems", {}).get(provider.id, {})
        provider_type = provider_data.get('type', None)
        if provider_type is not None:
            provider.provider_type = provider_type
            provider.save(update_fields=['provider_type'])


class Migration(migrations.Migration):

    dependencies = [
        ('appliances', '0042_openshift_appliances_support'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='provider_type',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.RunPython(add_type_to_provider),
    ]