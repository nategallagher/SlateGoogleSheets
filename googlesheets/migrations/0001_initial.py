# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Shipment'
        db.create_table('googlesheets_shipment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.Address'], null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.State'])),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.City'], null=True, blank=True)),
        ))
        db.send_create_signal('googlesheets', ['Shipment'])


    def backwards(self, orm):
        # Deleting model 'Shipment'
        db.delete_table('googlesheets_shipment')


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
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.City']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.State']"})
        }
    }

    complete_apps = ['googlesheets']