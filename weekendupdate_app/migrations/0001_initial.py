# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Archive'
        db.create_table('weekendupdate_app_archive', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=255)),
            ('edition', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('weekendupdate_app', ['Archive'])


    def backwards(self, orm):
        # Deleting model 'Archive'
        db.delete_table('weekendupdate_app_archive')


    models = {
        'weekendupdate_app.archive': {
            'Meta': {'object_name': 'Archive'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'edition': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['weekendupdate_app']