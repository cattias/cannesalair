# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'DownloadJob'
        db.create_table('galerie_downloadjob', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('galerie', self.gf('django.db.models.fields.related.ForeignKey')(related_name='galerie_downloadjob_set', to=orm['galerie.Galerie'])),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255)),
            ('is_intreatment', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_treated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('path_to_zip', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('date_treatment', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_creation', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('galerie', ['DownloadJob'])

        # Adding M2M table for field images on 'DownloadJob'
        db.create_table('galerie_downloadjob_images', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('downloadjob', models.ForeignKey(orm['galerie.downloadjob'], null=False)),
            ('photo', models.ForeignKey(orm['galerie.photo'], null=False))
        ))
        db.create_unique('galerie_downloadjob_images', ['downloadjob_id', 'photo_id'])

        # Adding field 'Photo.titre_slug'
        db.add_column('galerie_photo', 'titre_slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=255, unique=True, null=True, blank=True), keep_default=False)

        # Adding field 'Galerie.titre_slug'
        db.add_column('galerie_galerie', 'titre_slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=255, unique=True, null=True, blank=True), keep_default=False)

        # Adding field 'Galerie.is_created'
        db.add_column('galerie_galerie', 'is_created', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Galerie.is_intreatment'
        db.add_column('galerie_galerie', 'is_intreatment', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Galerie.local_path'
        db.add_column('galerie_galerie', 'local_path', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'DownloadJob'
        db.delete_table('galerie_downloadjob')

        # Removing M2M table for field images on 'DownloadJob'
        db.delete_table('galerie_downloadjob_images')

        # Deleting field 'Photo.titre_slug'
        db.delete_column('galerie_photo', 'titre_slug')

        # Deleting field 'Galerie.titre_slug'
        db.delete_column('galerie_galerie', 'titre_slug')

        # Deleting field 'Galerie.is_created'
        db.delete_column('galerie_galerie', 'is_created')

        # Deleting field 'Galerie.is_intreatment'
        db.delete_column('galerie_galerie', 'is_intreatment')

        # Deleting field 'Galerie.local_path'
        db.delete_column('galerie_galerie', 'local_path')


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
        'galerie.downloadjob': {
            'Meta': {'object_name': 'DownloadJob'},
            'date_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_treatment': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'galerie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'galerie_downloadjob_set'", 'to': "orm['galerie.Galerie']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'photo_downloadjob_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['galerie.Photo']"}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_intreatment': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_treated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'path_to_zip': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
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
            'is_created': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_intreatment': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'local_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'sortie': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sortie_galeries_set'", 'null': 'True', 'to': "orm['sortie.Sortie']"}),
            'titre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'titre_slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'galerie.photo': {
            'Meta': {'ordering': "['ordre']", 'object_name': 'Photo'},
            'comments': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'photo_comments_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['comment.Comment']"}),
            'date_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_publication': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'filesize': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'galerie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photos_set'", 'to': "orm['galerie.Galerie']"}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_intreatment': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_linked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_uploaded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'local_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'local_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ordre': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'thumb_local_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'thumb_local_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'titre': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'titre_slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'sortie.activite': {
            'Meta': {'object_name': 'Activite'},
            'activite': ('django.db.models.fields.TextField', [], {}),
            'date_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'sortie.crsortie': {
            'Meta': {'object_name': 'CRSortie'},
            'auteur': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'crsortie_auteur_set'", 'to': "orm['auth.User']"}),
            'compterendu': ('django.db.models.fields.TextField', [], {}),
            'date_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kilometrage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_voitures': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'participants_effectifs': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'peages': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'})
        },
        'sortie.sortie': {
            'Meta': {'ordering': "['-date_debut']", 'object_name': 'Sortie'},
            'activites': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'activites_sortie_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['sortie.Activite']"}),
            'auteur': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sortie_auteur_set'", 'to': "orm['auth.User']"}),
            'canceled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comments': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'sortie_comments_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['comment.Comment']"}),
            'cr': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'compte_rendu_sortie_set'", 'null': 'True', 'to': "orm['sortie.CRSortie']"}),
            'date_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_debut': ('django.db.models.fields.DateTimeField', [], {}),
            'date_fin': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lieu': ('django.db.models.fields.TextField', [], {}),
            'rdv': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'titre': ('django.db.models.fields.TextField', [], {}),
            'titre_slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'typesortie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sortie_type_set'", 'to': "orm['sortie.SortieType']"})
        },
        'sortie.sortietype': {
            'Meta': {'object_name': 'SortieType'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'date_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        }
    }

    complete_apps = ['galerie']
