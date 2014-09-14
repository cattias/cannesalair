# encoding: utf-8
from south.v2 import DataMigration
from sortie.models import SortieType

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        SortieType(name="Sortie", code="sortie").save()
        SortieType(name="Stage", code="stage").save()
        SortieType(name="Soiree", code="soiree").save()


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
        'sortie.activite': {
            'Meta': {'object_name': 'Activite'},
            'activite': ('django.db.models.fields.TextField', [], {}),
            'date_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'sortie.participant': {
            'Meta': {'object_name': 'Participant'},
            'date_update': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'qui': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'participant_user_set'", 'to': "orm['auth.User']"}),
            'sortie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'participant_sortie_set'", 'to': "orm['sortie.Sortie']"}),
            'statut': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'sortie.sortie': {
            'Meta': {'object_name': 'Sortie'},
            'activites': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'activites_sortie_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['sortie.Activite']"}),
            'auteur': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sortie_auteur_set'", 'to': "orm['auth.User']"}),
            'comments': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'sortie_comments_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['comment.Comment']"}),
            'compterendu': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_debut': ('django.db.models.fields.DateTimeField', [], {}),
            'date_fin': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lieu': ('django.db.models.fields.TextField', [], {}),
            'rdv': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'titre': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'sortie.sortietype': {
            'Meta': {'object_name': 'SortieType'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'date_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        }
    }

    complete_apps = ['sortie']
