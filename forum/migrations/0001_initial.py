# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Groupe'
        db.create_table('forum_groupe', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titre', self.gf('django.db.models.fields.TextField')()),
            ('ordre', self.gf('django.db.models.fields.IntegerField')()),
            ('date_creation', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('forum', ['Groupe'])

        # Adding model 'Forum'
        db.create_table('forum_forum', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titre', self.gf('django.db.models.fields.TextField')()),
            ('groupe', self.gf('django.db.models.fields.related.ForeignKey')(related_name='groupe_forum_set', to=orm['forum.Groupe'])),
            ('commentaire', self.gf('django.db.models.fields.TextField')()),
            ('ordre', self.gf('django.db.models.fields.IntegerField')()),
            ('date_creation', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('forum', ['Forum'])

        # Adding M2M table for field moderateurs on 'Forum'
        db.create_table('forum_forum_moderateurs', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('forum', models.ForeignKey(orm['forum.forum'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('forum_forum_moderateurs', ['forum_id', 'user_id'])

        # Adding model 'Thread'
        db.create_table('forum_thread', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titre', self.gf('django.db.models.fields.TextField')()),
            ('forum', self.gf('django.db.models.fields.related.ForeignKey')(related_name='forum_thread_set', to=orm['forum.Forum'])),
            ('date_creation', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('forum', ['Thread'])

        # Adding model 'Message'
        db.create_table('forum_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('auteur', self.gf('django.db.models.fields.related.ForeignKey')(related_name='auteur_message_set', to=orm['auth.User'])),
            ('contenu', self.gf('django.db.models.fields.TextField')()),
            ('thread', self.gf('django.db.models.fields.related.ForeignKey')(related_name='thread_message_set', to=orm['forum.Thread'])),
            ('date_publication', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('forum', ['Message'])


    def backwards(self, orm):
        
        # Deleting model 'Groupe'
        db.delete_table('forum_groupe')

        # Deleting model 'Forum'
        db.delete_table('forum_forum')

        # Removing M2M table for field moderateurs on 'Forum'
        db.delete_table('forum_forum_moderateurs')

        # Deleting model 'Thread'
        db.delete_table('forum_thread')

        # Deleting model 'Message'
        db.delete_table('forum_message')


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
            'titre': ('django.db.models.fields.TextField', [], {})
        },
        'forum.groupe': {
            'Meta': {'object_name': 'Groupe'},
            'date_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordre': ('django.db.models.fields.IntegerField', [], {}),
            'titre': ('django.db.models.fields.TextField', [], {})
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
            'titre': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['forum']
