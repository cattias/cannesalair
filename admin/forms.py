'''
Created on 29 avr. 2012

@author: Marc
'''
from admin.siteconfig import load_site_config
from django import forms
from djblets.siteconfig.forms import SiteSettingsForm

class GeneralSettingsForm(SiteSettingsForm):
    """
    Admin Part
    """
    site_admin_name = forms.CharField(
        label="Name",
        required=True)
    site_admin_email = forms.EmailField(
        label="E-Mail",
        required=True)
    
    """
    Webmaster Part
    """
    conf_webmaster_mail = forms.EmailField(
        label="Mail",
        required=True)

    """
    Google Part
    """
    google_calendar_email = forms.EmailField(
        label="Calendar E-Mail",
        required=False)
    google_calendar_password = forms.CharField(
        label="Calendar Password",
        required=False)
    google_analytics_account = forms.CharField(
        label="Analytics Account",
        required=False)
    google_analytics_domain = forms.CharField(
        label="Analytics Domain",
        required=False)



    """
    Imgur Part
    """
    imgur_auth_anon_key = forms.CharField(
        label="Authentication Anon Key",
        required=False)
    imgur_auth_consumer_key = forms.CharField(
        label="Authentication Consumer Key",
        required=False)
    imgur_auth_consumer_secret = forms.CharField(
        label="Authentication Consumer Secret",
        required=False)
    imgur_account = forms.CharField(
        label="Account",
        required=False)
    imgur_password = forms.CharField(
        label="Password",
        required=False)
    imgur_signin_url = forms.CharField(
        label="Sign-in URL",
        required=False)
    imgur_api_endpoint = forms.CharField(
        label="Api Endpoint",
        required=False)
    imgur_api_version = forms.CharField(
        label="Api Version",
        required=False)
    imgur_api_account = forms.CharField(
        label="Api Account",
        required=False)
    imgur_api_format = forms.CharField(
        label="Api Format",
        required=False)

    """
    Site Part
    """
    site_config_path = forms.ChoiceField(
        label="config_path",
        required=True,
        choices=(('default', 'Cannes A L\'Air'),
                 ('musical_choir', 'Chorale',)))
    site_activite_en_premier = forms.BooleanField(
        label="'Activites' tab in first",
        required=False)
    site_background_image = forms.CharField(
        label="Background Image",
        required=False)
    site_id = forms.IntegerField(
        label="Site ID",
        required=False)


    class Meta:
        fieldsets = (
            {
                'title': "Admin",
                'description': "Information about the administrator of this site",
                'fields': ('site_admin_name', 'site_admin_email',),
            },
            {
                'title': "Webmaster",
                'description': "Information about the webmaster of this site",
                'fields': ('conf_webmaster_mail',),
            },
            {
                'title': "Google",
                'description': "Information about google account",
                'fields': ('google_calendar_email', 'google_calendar_password', 'google_analytics_account', 'google_analytics_domain',),
            },
            {
                'title': "Imgur",
                'description': "Information about Imgur account",
                'fields': ('imgur_auth_anon_key', 'imgur_auth_consumer_key', 'imgur_auth_consumer_secret', 'imgur_account',
                           'imgur_password', 'imgur_signin_url', 'imgur_api_endpoint', 'imgur_api_version',
                           'imgur_api_account', 'imgur_api_format',),
            },
            {
                'title': "Site",
                'description': "Information about this site",
                'fields': ('site_config_path', 'site_activite_en_premier', 'site_background_image', 'site_id',),
            },
        )

    def save(self):
        super(GeneralSettingsForm, self).save()
        load_site_config()
