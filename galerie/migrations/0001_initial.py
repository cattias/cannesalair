# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Galerie'
        db.create_table('galerie_galerie', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('imgur_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('auteur', self.gf('django.db.models.fields.related.ForeignKey')(related_name='auteur_galerie_set', to=orm['auth.User'])),
            ('titre', self.gf('django.db.models.fields.TextField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('date_publication', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('galerie', ['Galerie'])

        # Adding M2M table for field comments on 'Galerie'
        db.create_table('galerie_galerie_comments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('galerie', models.ForeignKey(orm['galerie.galerie'], null=False)),
            ('comment', models.ForeignKey(orm['comment.comment'], null=False))
        ))
        db.create_unique('galerie_galerie_comments', ['galerie_id', 'comment_id'])


    def backwards(self, orm):
        
        # Deleting model 'Galerie'
        db.delete_table('galerie_galerie')

        # Removing M2M table for field comments on 'Galerie'
        db.delete_table('galerie_galerie_comments')


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
            'date_publication': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imgur_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'titre': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['galerie']
