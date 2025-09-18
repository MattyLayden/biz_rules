from rest_framework import serializers
from .models import Object, CharacterForm, IntegerForm, FloatForm, TextForm, BooleanForm, DateForm, URLForm

FORM_MODELS = [CharacterForm, IntegerForm, FloatForm, TextForm, BooleanForm, DateForm, URLForm]

class ObjectSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    class Meta:
        model = Object
        fields = ['data']  

    def get_data(self, obj):
        result = {}
        for form_model in FORM_MODELS:
            forms = form_model.objects.filter(object=obj)
            for form in forms:
                result[form.field.name] = form.value
        return result