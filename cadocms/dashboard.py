"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'yardgear.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name
from django.conf import settings

class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """
    columns = 2
    
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        
        self.children.append(modules.ModelList(
            _('Site Content'),
            collapsible=False,
            column=1,
            #css_classes=('collapse closed',),
            exclude=('cadocms.*', 'django.contrib.*', 'djcelery.*', 'ajax_upload.*'),
        ))
        
        """
        self.children.append(modules.ModelList(
            _('Tasks'),
            collapsible=False,
            column=1,
            #css_classes=('collapse closed',),
            models=('djcelery.*', ),
        ))
        """
        
        
        self.children.append(modules.ModelList(
            _('CMS Content'),
            collapsible=False,
            column=1,
            #css_classes=('collapse closed',),
            models=('cadocms.*', 'django.contrib.*', ),
        ))
        
        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Actions'),
            column=2,
            collapsible=False,
            children=[
                {
                    'title': _('Moderation'),
                    'url': '/admin/moderation/',
                    'external': False,
                },
                {
                    'title': _('FileBrowser'),
                    'url': '/admin/filebrowser/browse/',
                    'external': False,
                },
                {
                    'title': _('Admin Manual'),
                    'url': '/admin/manual/',
                    'external': False,
                },
                {
                    'title': _('Clear Cache'),
                    'url': '/admin/clearcache/',
                    'external': False,
                }
            ] + settings.CADO_EXTRA_ADMIN_LINKS
        ))
        
        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Help'),
            column=2,
            collapsible=False,
            children=[
                {
                    'title': _('Admin Manual'),
                    'url': '/admin/manual/',
                    'external': True,
                },
            ]
        ))
        
        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=5,
            collapsible=False,
            column=2,
        ))
        


