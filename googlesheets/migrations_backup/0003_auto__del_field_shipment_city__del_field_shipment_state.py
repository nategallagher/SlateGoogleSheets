# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Shipment.city'
        db.delete_column('googlesheets_shipment', 'city_id')

        # Deleting field 'Shipment.state'
        db.delete_column('googlesheets_shipment', 'state_id')


    def backwards(self, orm):
        # Adding field 'Shipment.city'
        db.add_column('googlesheets_shipment', 'city',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.City'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Shipment.state'
        db.add_column('googlesheets_shipment', 'state',
                      self.gf('django.db.models.fields.related.ForeignKey')(default='California', to=orm['geo.State']),
                      keep_default=False)


    models = {
        'geo.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.City']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'})
        },
        'geo.city': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('state', 'name'),)", 'object_name': 'City'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.State']"})
        },
        'geo.country': {
            'Meta': {'ordering': "['name']", 'object_name': 'Country'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'geo.state': {
            'Meta': {'ordering': "('name',)", 'object_name': 'State'},
            'abbr': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'googlesheets.shipment': {
            'Meta': {'object_name': 'Shipment'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Address']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ship_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['googlesheets']