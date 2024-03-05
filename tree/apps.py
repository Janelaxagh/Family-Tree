from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TreeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tree'
    verbose_name = _('Древо')
