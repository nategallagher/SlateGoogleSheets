# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Country'
        db.create_table('geo_country', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('geo', ['Country'])

        # Adding model 'State'
        db.create_table('geo_state', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.Country'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('abbr', self.gf('django.db.models.fields.CharField')(max_length=4)),
        ))
        db.send_create_signal('geo', ['State'])

        # Adding model 'City'
        db.create_table('geo_city', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.State'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('geo', ['City'])

        # Adding unique constraint on 'City', fields ['state', 'name']
        db.create_unique('geo_city', ['state_id', 'name'])

        # Adding model 'Address'
        db.create_table('geo_address', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.City'], null=True, blank=True)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
        ))
        db.send_create_signal('geo', ['Address'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'City', fields ['state', 'name']
        db.delete_unique('geo_city', ['state_id', 'name'])

        # Deleting model 'Country'
        db.delete_table('geo_country')

        # Deleting model 'State'
        db.delete_table('geo_state')

        # Deleting model 'City'
        db.delete_table('geo_city')

        # Deleting model 'Address'
        db.delete_table('geo_address')


    models = {
        'geo.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.City']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
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
