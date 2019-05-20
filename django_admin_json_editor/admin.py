import json

from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class JSONEditorWidget(forms.Widget):
    template_name = 'django_admin_json_editor/editor.html'

    def __init__(self, schema, collapsed=True, sceditor=False, editor_options=None):
        super(JSONEditorWidget, self).__init__()
        self._schema = schema
        self._collapsed = collapsed
        self._sceditor = sceditor
        self._editor_options = editor_options or {}

    def render(self, name, value, attrs=None, renderer=None):
        print("[ GIT ] django-admin-json-editor/ admin.py - JSONEditorWidget - render()")
        print("[ GIT ] django-admin-json-editor/ admin.py - JSONEditorWidget - name:" + name)
        print(value)
        print(type(value))
        # value = value.replace('</script>','')
        # value = '{"logo": "https://s3-us-west-2.amazonaws.com/images.happyreturns.com/outerknown/outerknown-logo.png", "favicon": "https://s3-us-west-2.amazonaws.com/images.happyreturns.com/outerknown/outerknown-favicon.png", "primary_color": "#333333", "background_img": "https://s3-us-west-2.amazonaws.com/images.happyreturns.com/outerknown/outerknown-background-desktop.png", "item_list_message": "For international orders or to request an exception, please email customer care at customercare@outerknown.com or chat us.", "primary_dark_color": "#222222", "order_number_message": "Please enter the Order ID found in your email or your packing slip (first 5 numbers)", "background_img_mobile": "https://s3-us-west-2.amazonaws.com/images.happyreturns.com/outerknown/outerknown-background-mobile.png"}'
        # Maybe remove javascript section from the value dict here
        # Nope - don't want to hard code delete or it will be removed from the db`
        # if value and "javascript" in value:
            # del value["javascript"]

        if callable(self._schema):
            schema = self._schema(self)
        else:
            schema = self._schema

        print("[ GIT ] django-admin-json-editor/ admin.py - render() - 1" )
        schema['title'] = ' '
        schema['options'] = {'collapsed': int(self._collapsed)}

        print("[ GIT ] django-admin-json-editor/ admin.py - render() - 2" )
        editor_options = {
            'theme': 'bootstrap3',
            'iconlib': 'fontawesome4',
            'schema': schema,
        }
        editor_options.update(self._editor_options)

        print("[ GIT ] django-admin-json-editor/ admin.py - render() - 3" )
        edit = json.dumps(editor_options)
        print("Edit")
        print(edit)
        # editor_options is the theme, iconlib, schema, options

        print("[ GIT ] django-admin-json-editor/ admin.py - render() - 4" )
        context = {
            'name': name,
            'data': value,
            'sceditor': int(self._sceditor),
            'editor_options': json.dumps(editor_options),
        }
        print("[ GIT ] django-admin-json-editor/ admin.py - render() - 5" )
        return mark_safe(render_to_string(self.template_name, context))

    @property
    def media(self):
        css = {
            'all': [
                'django_admin_json_editor/bootstrap/css/bootstrap.min.css',
                'django_admin_json_editor/fontawesome/css/font-awesome.min.css',
                'django_admin_json_editor/style.css',
            ]
        }
        js = [
            'django_admin_json_editor/jquery/jquery.min.js',
            'django_admin_json_editor/bootstrap/js/bootstrap.min.js',
            'django_admin_json_editor/jsoneditor/jsoneditor.min.js',
        ]
        if self._sceditor:
            css['all'].append('django_admin_json_editor/sceditor/themes/default.min.css')
            js.append('django_admin_json_editor/sceditor/jquery.sceditor.bbcode.min.js')
        return forms.Media(css=css, js=js)
