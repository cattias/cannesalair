# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Categorie'
        db.create_table('matos_categorie', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('date_creation', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('matos', ['Categorie'])

        # Adding model 'SousCategorie'
        db.create_table('matos_souscategorie', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('categorie', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sous_cat_set', to=orm['matos.Categorie'])),
            ('date_creation', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('matos', ['SousCategorie'])

        # Adding model 'Matos'
        db.create_table('matos_matos', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titre', self.gf('django.db.models.fields.TextField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('categorie', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='sous_cat_matos_set', null=True, to=orm['matos.SousCategorie'])),
            ('prix_neuf', self.gf('django.db.models.fields.FloatField')()),
            ('date_achat', self.gf('django.db.models.fields.DateField')()),
            ('photos', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='matos_photos_set', null=True, to=orm['photologue.Gallery'])),
            ('date_creation', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('matos', ['Matos'])

        # Adding model 'Emprunt'
        db.create_table('matos_emprunt', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('qui', self.gf('django.db.models.fields.related.ForeignKey')(related_name='emprunteur_set', to=orm['auth.User'])),
            ('quoi', self.gf('django.db.models.fields.related.ForeignKey')(related_name='matos_emprunt_set', to=orm['matos.Matos'])),
            ('lieu', self.gf('django.db.models.fields.TextField')()),
            ('statut', self.gf('django.db.models.fields.CharField')(default='V', max_length=1)),
            ('date_debut', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_fin', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_creation', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('matos', ['Emprunt'])


    def backwards(self, orm):
        
        # Deleting model 'Categorie'
        db.delete_table('matos_categorie')

        # Deleting model 'SousCategorie'
        db.delete_table('matos_souscategorie')

        # Deleting model 'Matos'
        db.delete_table('matos_matos')

        # Deleting model 'Emprunt'
        db.delete_table('matos_emprunt')


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
        'matos.categorie': {
            'Meta': {'object_name': 'Categorie'},
            'date_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        'matos.emprunt': {
            'Meta': {'object_name': 'Emprunt'},
            'date_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_debut': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_fin': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lieu': ('django.db.models.fields.TextField', [], {}),
            'qui': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'emprunteur_set'", 'to': "orm['auth.User']"}),
            'quoi': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'matos_emprunt_set'", 'to': "orm['matos.Matos']"}),
            'statut': ('django.db.models.fields.CharField', [], {'default': "'V'", 'max_length': '1'})
        },
        'matos.matos': {
            'Meta': {'object_name': 'Matos'},
            'categorie': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sous_cat_matos_set'", 'null': 'True', 'to': "orm['matos.SousCategorie']"}),
            'date_achat': ('django.db.models.fields.DateField', [], {}),
            'date_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photos': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'matos_photos_set'", 'null': 'True', 'to': "orm['photologue.Gallery']"}),
            'prix_neuf': ('django.db.models.fields.FloatField', [], {}),
            'titre': ('django.db.models.fields.TextField', [], {})
        },
        'matos.souscategorie': {
            'Meta': {'object_name': 'SousCategorie'},
            'categorie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sous_cat_set'", 'to': "orm['matos.Categorie']"}),
            'date_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        'photologue.gallery': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'Gallery'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'photos': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'galleries'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['photologue.Photo']"}),
            'tags': ('tagging.fields.TagField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'title_slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'photologue.photo': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'Photo'},
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'crop_from': ('django.db.models.fields.CharField', [], {'default': "'center'", 'max_length': '10', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'effect': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'photo_related'", 'null': 'True', 'to': "orm['photologue.PhotoEffect']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'title_slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'view_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'photologue.photoeffect': {
            'Meta': {'object_name': 'PhotoEffect'},
            'background_color': ('django.db.models.fields.CharField', [], {'default': "'#FFFFFF'", 'max_length': '7'}),
            'brightness': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'color': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'contrast': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'filters': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'reflection_size': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'reflection_strength': ('django.db.models.fields.FloatField', [], {'default': '0.59999999999999998'}),
            'sharpness': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'transpose_method': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'})
        }
    }

    complete_apps = ['matos']
