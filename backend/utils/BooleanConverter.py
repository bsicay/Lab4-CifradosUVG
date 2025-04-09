from werkzeug.routing import BaseConverter

class BooleanConverter(BaseConverter):
    def to_python(self, value):
        return value.lower() in ('true', '1', 't', 'yes')
    
    def to_url(self, value):
        return str(int(bool(value)))