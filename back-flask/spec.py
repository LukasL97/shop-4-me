import json

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Blueprint


spec = APISpec(
    title='Shop4Me API',
    version='0.0.1',
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
    openapi_version='3.0.2'
)


class DocumentedBlueprint(Blueprint):
    """
    Flask Blueprint which documents every view function defined in it.

    Copied from https://github.com/marshmallow-code/apispec-webframeworks/blob/bf161bf5b9853df6c206d8f4a3187521cbada3cc/apispec_webframeworks/flask.py
    """

    def __init__(self, name, import_name):
        super(DocumentedBlueprint, self).__init__(name, import_name)
        self.documented_view_functions = []
        self.spec = spec

    def route(self, rule, document=True, **options):
        """If document is set to True, the route will be added to the spec.
        :param bool document: Whether you want this route to be added to the spec or not.
        """

        def decorator(f):
            if document and f not in self.documented_view_functions:
                self.documented_view_functions.append(f)
            return super(DocumentedBlueprint, self).route(rule, **options)(f)

        return decorator

    def register(self, app, options, first_registration=False):
        """Register current blueprint in the app. Add all the view_functions to the spec."""
        super(DocumentedBlueprint, self).register(app, options, first_registration=first_registration)
        with app.app_context():
            for f in self.documented_view_functions:
                self.spec.path(view=f)


TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Swagger UI</title>
  <link href="https://fonts.googleapis.com/css?family=Open+Sans:400,700|Source+Code+Pro:300,600|Titillium+Web:400,600,700" rel="stylesheet">
  <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/swagger-ui.css" >
  <style>
    html
    {
      box-sizing: border-box;
      overflow: -moz-scrollbars-vertical;
      overflow-y: scroll;
    }
    *,
    *:before,
    *:after
    {
      box-sizing: inherit;
    }
    body {
      margin:0;
      background: #fafafa;
    }
  </style>
</head>
<body>
<div id="swagger-ui"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/swagger-ui-bundle.js"> </script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/swagger-ui-standalone-preset.js"> </script>
<script>
window.onload = function() {
  var spec = %s;
  // Build a system
  const ui = SwaggerUIBundle({
    spec: spec,
    dom_id: '#swagger-ui',
    deepLinking: true,
    presets: [
      SwaggerUIBundle.presets.apis,
      SwaggerUIStandalonePreset
    ],
    plugins: [
      SwaggerUIBundle.plugins.DownloadUrl
    ],
    layout: "StandaloneLayout"
  })
  window.ui = ui
}
</script>
</body>
</html>
"""

def get_spec_as_html():
    return TEMPLATE % json.dumps(spec.to_dict())
