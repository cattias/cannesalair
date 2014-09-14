# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm,\
    PasswordChangeForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django import forms
from account.models import Profil
from core.widgets import MediumTextInput, MediumTextarea
from photologue.models import Photo
from django.core.files.base import ContentFile
from captcha.fields import CaptchaField
from log.models import LogActivity
from account.decorators import login_required
from sortie.models import Activite

###########################
#       User Profil        #
###########################

@login_required
def changepassword(request, template_name="accounts/change_password.html"):
    if request.POST:
        if request.POST.get("pass1"):
            request.user.set_password(request.POST.get("pass1"))
            request.user.save()
        return HttpResponseRedirect(reverse("editprofil"))

    return render_to_response(template_name)


class ProfilForm(forms.ModelForm):
    lieu = forms.CharField(required=False, label='Lieu', widget=MediumTextInput)
    telephone = forms.CharField(required=False, label=u'Téléphone', widget=MediumTextInput)
    siteweb = forms.CharField(required=False, label='Site Web', widget=MediumTextInput)
    signature = forms.CharField(required=False, label='Signature', widget=forms.Textarea(attrs={'rows':'4', 'cols':'50'}))
    custom_background_image = forms.CharField(required=False, label="Votre image de fond perso pour le site", widget=MediumTextInput)
    suivre_les_articles = forms.BooleanField(required=False, label=u'Je veux être informé par mail lorsqu\'un nouvel article est publié')
    suivre_les_sorties = forms.BooleanField(required=False, label=u'Je veux être informé par mail lorsqu\'une nouvelle activité est proposée (quelque soit son type)')
    suivre_les_sorties_partype = forms.ModelMultipleChoiceField(required=False, label=u'Je veux être informé par mail seulement lorsqu\'une nouvelle activité des types choisis est proposée (choix multiples possibles en gardant la touche CTRL ou Pomme sur Mac). Cette option n\'est pas prise en compte si vous avez choisi de suivre n\'importe quel type d\'activité.', queryset=Activite.objects.all(), widget=forms.SelectMultiple(attrs={'size':12,}))
    suivre_les_compterendus = forms.BooleanField(required=False, label=u'Je veux être informé par mail lorsqu\'un nouveau compte-rendu est publié')
    suivre_les_discussions = forms.BooleanField(required=False, label=u'Je veux être informé par mail lorsqu\'une nouvelle discussion sur le forum commence')
    suivre_les_galeries = forms.BooleanField(required=False, label=u'Je veux être informé par mail lorsqu\'une nouvelle galerie est publiée')
    auto_refresh_notif = forms.BooleanField(required=False, label=u'Je veux que les notifications soient marquées comme lues automatiquement quand je vais sur la page correspondante')
    class Meta:
        model = Profil
        fields = ('lieu', 'telephone', 'siteweb', 'signature', 'custom_background_image', 'auto_refresh_notif', 'suivre_les_articles', 'suivre_les_discussions', 'suivre_les_galeries', 'suivre_les_compterendus', 'suivre_les_sorties', 'suivre_les_sorties_partype')
#        exclude = ['user', 'last_known_activity', 'avatar', 'gravatarurl', 'discussions', 'forums', 'sorties', 'articles', 'galeries']

class UserModificationForm(forms.ModelForm):
    first_name = forms.CharField(required=True, label=u'Prénom', widget=MediumTextInput)
    last_name = forms.CharField(required=True, label='Nom', widget=MediumTextInput)
    email = forms.EmailField(required=True, label='Adresse e-mail', widget=MediumTextInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class AvatarForm(forms.Form):
    avatar = forms.ImageField(label='Avatar', required=False, widget = forms.FileInput(attrs={'class':'input-medium'}))
    gravatarurl = forms.CharField(required=False, label='Ou gravatar url', widget=MediumTextInput)

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(user, *args, **kwargs)
        for f in self.fields:
            self.fields[f].required = False
            self.fields[f].widget.attrs['class'] = 'input-medium'

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data.get("old_password")
        password1 = self.data.get('new_password1')
        password2 = self.data.get('new_password2')
        if old_password and not self.user.check_password(old_password):
            raise forms.ValidationError(u"Votre ancien mot de passe est incorrect. Veuillez le rectifier.")
        if not old_password and password1 and password2 and password1 == password2:
            raise forms.ValidationError(u"Votre ancien mot de passe est incorrect. Veuillez le rectifier.")
        return old_password

    def clean_new_password2(self):
        old_password = self.cleaned_data.get("old_password")
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(u"Les deux mots de passe ne correspondent pas.")
        elif old_password:
            if not password1 and not password2:
                raise forms.ValidationError(u"Le nouveau mot de passe ne peut pas être vide.")
            else:
                raise forms.ValidationError(u"Les deux mots de passe ne correspondent pas.")
        return password2

@login_required
def deleteavatar(request):
    p = request.user.get_profile()
    if p.avatar:
        p.avatar.delete()
    p.avatar = None
    p.gravatarurl = None
    p.save()
    return HttpResponseRedirect(reverse("editprofil"))

@login_required
def edit_profil(request, template_name="accounts/edit_profil_form.html"):
    """
    Simple profile form.
    """
    user = request.user
    p = None
    try:
        p = user.get_profile()
    except Profil.DoesNotExist:
        p = Profil(user=user)
        p.save()
    
    if request.POST:
        is_valid = False
        new_user_form = UserModificationForm(request.POST, instance=user)
        new_profil_form = ProfilForm(request.POST, instance=p)
        new_avatar_form = AvatarForm(request.POST)
        new_password_form = CustomPasswordChangeForm(user=user, data=request.POST)
        
        is_valid = new_user_form.is_valid() and new_profil_form.is_valid() and new_avatar_form.is_valid() and new_password_form.is_valid()
        
        if is_valid:
            new_user = new_user_form.save(commit=False)
            new_user.save()

            new_profil = new_profil_form.save(commit=False) 
            new_profil.save()
            
            new_profil.suivre_les_sorties_partype.clear()
            for activite in Activite.objects.filter(pk__in=request.POST.getlist('suivre_les_sorties_partype')):
                new_profil.suivre_les_sorties_partype.add(activite)
            
            if request.POST.get('old_password') and request.POST.get('new_password1') and request.POST.get('new_password1'):
                new_password_form.save()

            p.gravatarurl = new_avatar_form.cleaned_data['gravatarurl']
            title = 'Avatar for user %s' % user.username
            if request.FILES.get('avatar'):
                title_slug = 'avatar-%s' % user.username
                filename = 'avatars/%s' % str(request.FILES.get('avatar'))
                photos = Photo.objects.filter(image=filename)
                photo = None
                if photos.count() > 0:
                    photo = photos[0]
                if not photo:
                    Photo.objects.filter(title_slug=title_slug).delete()
                    photo = Photo(title=title, title_slug=title_slug, is_public=False, tags="avatar")
                    photo.image.save(filename, ContentFile(request.FILES.get('avatar').read()))
                    photo.save()
                p.avatar = photo
            p.save()
            return HttpResponseRedirect(reverse("editprofil"))
        else:
            userform = new_user_form
            profilform = new_profil_form
            avatarform = new_avatar_form
            passwordform = new_password_form
    else:
        userform = UserModificationForm(instance=user)
        profilform = ProfilForm(instance=p)
        avatarform = AvatarForm(initial={'gravatarurl' : p.gravatarurl})
        passwordform = CustomPasswordChangeForm(user=user)

    context = RequestContext(request, {
        'p': p,
        'profilform': profilform,
        'userform': userform,
        'avatarform': avatarform,
        'passwordform': passwordform,
        'full': True,
    })
    return render_to_response(template_name, context)

def edit_profil_subscriptions(request, template_name="accounts/edit_profil_subscriptions.html"):
    """
    Simple profile form.
    """
    context = RequestContext(request, {})
    return render_to_response(template_name, context)
   
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Votre e-mail :', widget=MediumTextInput)
    first_name = forms.CharField(required=True, label='Votre prénom :', widget=MediumTextInput)
    last_name = forms.CharField(required=True, label='Votre nom :', widget=MediumTextInput)
    captcha = CaptchaField()

    def clean_email(self):
        email = self.cleaned_data["email"]
        users = User.objects.filter(email=email)
        if users.count() > 0:
            raise forms.ValidationError(u'Un utilisateur avec cette adresse e-mail existe déjà.')
        else:
            return email

def create_new_user(request, template_name="accounts/user_create_form.html"):
    form = CustomUserCreationForm()
    # if form was submitted, bind form instance.
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user must be active for login to work
            user.is_active = True
            user.email = request.POST.get('email')
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.save()
            p = Profil(user=user)
            p.last_known_activity = LogActivity.getDefault();
            p.save()

            from_email = "Les Cannes A L'air <no-reply@cannesalair.fr>"
            text = "Nouvel inscrit chez les CAL : %s %s (%s)<br><br>L'invalidation du compte peut se faire <a href='http://cannesalair.fr/admin/auth/user/%s/'>ici</a>." % (user.first_name, user.last_name, user.email, user.id)
            to_users = User.objects.filter(groups__name="Admin")
            from core.mail import internal_sendmail
            internal_sendmail(",".join([u.email for u in to_users]), from_email, text, "[CAL] %s vient de s'inscrire sur le site des CAL" % user.username, fail_silently=False)
            return HttpResponseRedirect(reverse("editprofil"))
        
    for f in form.fields:
        if not f == 'captcha':
            form.fields[f].widget.attrs['class'] = 'input-medium'
        form.fields[f].help_text = ""
    return render_to_response(template_name, RequestContext(request, {'form': form,'isstandalone': True,}))

def reset_password(request, template_name="accounts/reset_password_form.html"):
    form = PasswordResetForm()
    # if form was submitted, bind form instance.
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("root"))
    form.fields["email"] = forms.EmailField(label="Votre e-mail", widget=MediumTextInput)
    return render_to_response(template_name, RequestContext(request, {'form': form,}))

class ContactForm(forms.Form):
    qui = forms.ChoiceField(required=True, label='Qui voulez-vous contacter ? ', choices=[('Admin', 'Le Webmaster'), ('CA', 'Le Conseil d\'Administration'), ('Bureau', 'Le Bureau')])
    nom = forms.CharField(required=True, label='Votre nom :', widget=MediumTextInput)
    email = forms.EmailField(required=True, label='Votre e-mail :', widget=MediumTextInput)
    sujet = forms.CharField(required=True, label='Le sujet de votre message :', widget=MediumTextInput)
    message = forms.CharField(required=True, label='Votre message :', widget=MediumTextarea)
    captcha = CaptchaField()

class ContactAuthForm(forms.Form):
    qui = forms.ChoiceField(required=True, label='Qui voulez-vous contacter ? ', choices=[('Admin', 'Le Webmaster'), ('CA', 'Le Conseil d\'Administration'), ('Bureau', 'Le Bureau')])
    sujet = forms.CharField(required=True, label='Le sujet de votre message :', widget=MediumTextInput)
    message = forms.CharField(required=True, label='Votre message :', widget=MediumTextarea)

def contact_us(request, template_name="accounts/contact_form.html"):
    if request.user.is_authenticated():
        form = ContactAuthForm()
    else:
        form = ContactForm()
    # if form was submitted, bind form instance.
    if request.method == 'POST':
        if request.user.is_authenticated():
            form = ContactAuthForm(request.POST)
        else:
            form = ContactForm(request.POST)
        if form.is_valid():
            qui = request.POST.get('qui')
            if request.user.is_authenticated():
                from_email = "%s <%s>" % (request.user.username, request.user.email)
            else:
                from_email = "%s <%s>" % (request.POST['nom'], request.POST['email'])
            to_users = User.objects.filter(groups__name=qui)
            from core.mail import internal_sendmail
            internal_sendmail(",".join([u.email for u in to_users]), from_email, request.POST['message'], "[Contact CAL] %s" % request.POST['sujet'], fail_silently=False)
            return render_to_response("accounts/contact_form_sent.html", RequestContext(request, {}))
    return render_to_response(template_name, RequestContext(request, {'form': form,}))
