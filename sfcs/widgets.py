from django.conf import settings
from django.contrib.admin.widgets import AdminDateWidget

I18NJS_URL = getattr(settings, 'I18NJS_URL', "i18njs/")
class Date(AdminDateWidget):
    '''
    Wrapper for the AdminDateWidget with missing media. You also have to add:

        (r'^%s' % I18JS_URL, 'django.views.i18n.javascript_catalog')

    to your site's main urls.py.
    '''
    class Media:
        # JSs have to be included in right order, thus:
        extend = False
        js = ("/%s" % I18NJS_URL, settings.ADMIN_MEDIA_PREFIX + "js/core.js",) +\
            AdminDateWidget.Media.js

        # extract approriative content from below CSS if you prefer
        css = {
            'screen': (settings.ADMIN_MEDIA_PREFIX + 'css/forms.css',
                       settings.ADMIN_MEDIA_PREFIX + 'css/global.css',
                       settings.ADMIN_MEDIA_PREFIX + 'css/base.css',
                       ),
        }