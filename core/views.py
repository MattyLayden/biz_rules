import json

from django.views.generic import View
from django.http import JsonResponse, HttpResponseNotAllowed

from . import models

from rest_framework import generics
from .models import Object
from .serializers import ObjectSerializer


class ObjectListAPIView(generics.ListAPIView):
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer

class ImportResult:
    def __init__(self):
        self.created = 0
        self.updated = 0
        self.errors = []

        self.service_id = 0

        self.ticket_ids = []
        self.updated_ticket_ids = []

    def __str__(self):
        if self.errors:
            return ', '.join(self.errors)

        return ', '.join([
            f"Service: {self.service_id}",
            f"tickets created: {self.created} ({self.ticket_ids})",
            f"updated: {self.updated} ({self.updated_ticket_ids})",
        ])


class CustomerAPI(View):
    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(["POST"])

    def build_ticket(self, service: models.Service, obj: models.Object, payload: dict, result: ImportResult) -> JsonResponse:
        for field_data in payload.get("fields", []):
            lookup = {k:v for k, v in {
                "object": obj,
                "name": field_data["name"],
                "form_type": field_data.get("type"),
                "description": field_data.get("description"),
            }.items() if v}

            field, _ = models.Field.objects.get_or_create(**lookup)

            if field.form_type == models.Field.CHAR:
                form, _ = models.CharacterForm.objects.get_or_create(object=obj, field=field)
                form.value = field_data["value"]
                form.save()

            elif field.form_type == models.Field.TEXT:
                form, _ = models.TextForm.objects.get_or_create(object=obj, field=field)
                form.value = field_data["value"]
                form.save()

            elif field.form_type == models.Field.INTEGER:
                form, _ = models.IntegerForm.objects.get_or_create(object=obj, field=field)
                form.value = field_data["value"]
                form.save()

            elif field.form_type == models.Field.FLOAT:
                form, _ = models.FloatForm.objects.get_or_create(object=obj, field=field)
                form.value = field_data["value"]
                form.save()

            elif field.form_type == models.Field.BOOLEAN:
                form, _ = models.BooleanForm.objects.get_or_create(object=obj, field=field)
                form.value = field_data["value"]
                form.save()

            else:
                result.errors += f"{field.form_type} does not exist"


    def post(self, request, *args, **kwargs):
        json_payload = json.loads(request.body)

        if not json_payload.get("service"):
            return JsonResponse({"msg": "Error: No service provided!"})

        service_name = json_payload["service"]
        service, _ = models.Service.objects.get_or_create(name=service_name)

        import_result = ImportResult()
        import_result.service_id = service.id

        for payload in json_payload.get("objects"):
            if "human_id" in payload:
                obj = models.Object.load(payload['human_id'])
                import_result.updated += 1
                import_result.updated_ticket_ids.append(obj.id)

            else:
                obj = models.Object(service=service)
                obj.save()
                import_result.created += 1
                import_result.ticket_ids.append(obj.id)

            self.build_ticket(service, obj, payload, import_result)

        return JsonResponse({"result": str(import_result)})
