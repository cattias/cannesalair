# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Profil.auto_refresh_notif'
        db.add_column('account_profil', 'auto_refresh_notif', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Profil.auto_refresh_notif'
        db.delete_column('account_profil', 'auto_refresh_notif')


    models = {
        'account.profil': {
            'Meta': {'object_name': 'Profil'},
            'articles': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'articles_suivis_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['article.Article']"}),
            'auto_refresh_notif': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'avatar': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'avatar_set'", 'null': 'True', 'to': "orm['photologue.Photo']"}),
            'custom_background_image': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'date_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'discussions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'discussions_suivies_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['forum.Thread']"}),
            'forums': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'forums_suivis_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['forum.Forum']"}),
            'galeries': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'galeries_suivies_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['galerie.Galerie']"}),
            'gravatarurl': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_known_activity': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'last_known_activity_set'", 'null': 'True', 'to': "orm['log.LogActivity']"}),
            'lieu': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'signature': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'siteweb': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sorties': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'sorties_suivies_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['sortie.Sortie']"}),
            'suivre_les_articles': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'suivre_les_compterendus': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'suivre_les_discussions': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'suivre_les_galeries': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'suivre_les_sorties': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'telephone': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'article.article': {
            'Meta': {'object_name': 'Article'},
            'auteur': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'auteur_set'", 'to': "orm['auth.User']"}),
            'comments': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'article_comments_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['comment.Comment']"}),
            'contenu': ('django.db.models.fields.TextField', [], {}),
            'date_publication': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'titre': ('django.db.models.fields.TextField', [], {}),
            'titre_slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
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
        'forum.thread': {
            'Meta': {'object_name': 'Thread'},
            'date_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'forum_thread_set'", 'to': "orm['forum.Forum']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'titre': ('django.db.models.fields.TextField', [], {}),
            'titre_slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'})
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
        'log.logactivity': {
            'Meta': {'object_name': 'LogActivity'},
            'contenu': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'qui': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'log_qui_set'", 'to': "orm['auth.User']"}),
            'related_object_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'related_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'log_related_type_set'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'log_type_set'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"})
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
            'reflection_strength': ('django.db.models.fields.FloatField', [], {'default': '0.6'}),
            'sharpness': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'transpose_method': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'})
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
            'Meta': {'object_name': 'Sortie'},
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

    complete_apps = ['account']
