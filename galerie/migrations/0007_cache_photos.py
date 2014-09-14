# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from galerie.models import Galerie
from galerie import sync_galerie_from_imgur

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        for g in Galerie.objects.all():
            sync_galerie_from_imgur(g)


    def backwards(self, orm):
        "Write your backwards methods here."


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'comment.comment': {
            'Meta': {'object_name': 'Comment'},
            'auteur': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comment_auteur_set'", 'to': "orm['auth.User']"}),
            'contenu': ('django.db.models.fields.TextField', [], {}),
            'date_publication': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'galerie.galerie': {
            'Meta': {'object_name': 'Galerie'},
            'auteur': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'auteur_galerie_set'", 'to': "orm['auth.User']"}),
            'comments': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'galerie_comments_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['comment.Comment']"}),
            'date_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_publication': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imgur_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'titre': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'galerie.photo': {
            'Meta': {'ordering': "['ordre']", 'object_name': 'Photo'},
            'comments': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'photo_comments_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['comment.Comment']"}),
            'date_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_publication': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'galerie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photos_set'", 'to': "orm['galerie.Galerie']"}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_uploaded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'local_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ordre': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'thumb_local_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'titre': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['galerie']
