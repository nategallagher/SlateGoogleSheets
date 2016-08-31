# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Address.street'
        db.alter_column('geo_address', 'street', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True))


    def backwards(self, orm):
        
        # Changing field 'Address.street'
        db.alter_column('geo_address', 'street', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))


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
        }
    }

    complete_apps = ['geo']
