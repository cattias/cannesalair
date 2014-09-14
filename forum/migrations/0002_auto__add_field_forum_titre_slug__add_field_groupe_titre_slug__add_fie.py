# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Forum.titre_slug'
        db.add_column('forum_forum', 'titre_slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=255, unique=True, null=True, blank=True), keep_default=False)

        # Adding field 'Groupe.titre_slug'
        db.add_column('forum_groupe', 'titre_slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=255, unique=True, null=True, blank=True), keep_default=False)

        # Adding field 'Thread.titre_slug'
        db.add_column('forum_thread', 'titre_slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=255, unique=True, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Forum.titre_slug'
        db.delete_column('forum_forum', 'titre_slug')

        # Deleting field 'Groupe.titre_slug'
        db.delete_column('forum_groupe', 'titre_slug')

        # Deleting field 'Thread.titre_slug'
        db.delete_column('forum_thread', 'titre_slug')


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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'forum.forum': {
            'Meta': {'object_name': 'Forum'},
            'commentaire': ('django.db.models.fields.TextField', [], {}),
            'date_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'groupe': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'groupe_forum_set'", 'to': "orm['forum.Groupe']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moderateurs': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'forum_moderateur_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'ordre': ('django.db.models.fields.IntegerField', [], {}),
            'titre': ('django.db.models.fields.TextField', [], {}),
            'titre_slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'forum.groupe': {
            'Meta': {'object_name': 'Groupe'},
            'date_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordre': ('django.db.models.fields.IntegerField', [], {}),
            'titre': ('django.db.models.fields.TextField', [], {}),
            'titre_slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'forum.message': {
            'Meta': {'object_name': 'Message'},
            'auteur': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'auteur_message_set'", 'to': "orm['auth.User']"}),
            'contenu': ('django.db.models.fields.TextField', [], {}),
            'date_publication': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'thread_message_set'", 'to': "orm['forum.Thread']"})
        },
        'forum.thread': {
            'Meta': {'object_name': 'Thread'},
            'date_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'forum_thread_set'", 'to': "orm['forum.Forum']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'titre': ('django.db.models.fields.TextField', [], {}),
            'titre_slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['forum']
