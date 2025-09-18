import os
import requests
from dotenv import load_dotenv
from datetime import datetime

from core.models import (Service, Object, Field, IntegerForm, FloatForm, CharacterForm, TextForm, BooleanForm, DateForm, URLForm)

load_dotenv()  

API_KEY = os.getenv("POKEMON_API_KEY")

HEADERS = {"X-Api-Key": API_KEY}


def main():
    service_name = "Pokemon"
    service, created = Service.objects.get_or_create(name=service_name)

    
    id_field = Field.objects.get_or_create(service=service, name="id", defaults={"form_type": Field.CHAR})[0]
    name_field = Field.objects.get_or_create(service=service, name="name", defaults={"form_type": Field.CHAR})[0]
    hp_field = Field.objects.get_or_create(service=service, name="hp", defaults={"form_type": Field.INTEGER})[0]
    types_field = Field.objects.get_or_create(service=service, name="types", defaults={"form_type": Field.TEXT})[0]
    evolvesTo_field = Field.objects.get_or_create(service=service, name="evolvesTo", defaults={"form_type": Field.TEXT})[0]
    date_field = Field.objects.get_or_create(service=service, name="releaseDate", defaults={"form_type": Field.DATE})[0]

   
    image_fields = {}
    for size in ["small", "large"]:
        image_fields[size] = Field.objects.get_or_create(service=service, name=f"{size}_image_field", defaults={"form_type": Field.URL})[0]

    
    holo_fields = {}
    for price_type in ["low", "mid", "high"]:
        holo_fields[price_type] = Field.objects.get_or_create(service=service, name=f"holofoil_price_{price_type}_field", defaults={"form_type": Field.FLOAT})[0]

    
    attack_fields = {}
    for i in range(1, 6):
        attack_fields[i] = {
            "name": Field.objects.get_or_create(service=service, name=f"attack_{i}_name_field", defaults={"form_type": Field.CHAR})[0],
            "energy_cost": Field.objects.get_or_create(service=service, name=f"attack_{i}_energy_cost_field", defaults={"form_type": Field.INTEGER})[0],
            "damage": Field.objects.get_or_create(service=service, name=f"attack_{i}_damage_field", defaults={"form_type": Field.CHAR})[0],
            "text": Field.objects.get_or_create(service=service, name=f"attack_{i}_text_field", defaults={"form_type": Field.TEXT})[0],
        }

    
    weakness_fields = {}
    for i in range(1, 6):
        weakness_fields[i] = {
            "type": Field.objects.get_or_create(service=service, name=f"weakness{i}_type_field", defaults={"form_type": Field.CHAR})[0],
            "value": Field.objects.get_or_create(service=service, name=f"weakness{i}_value_field", defaults={"form_type": Field.CHAR})[0],
        }

    
    url = "https://api.pokemontcg.io/v2/cards?page=1&pageSize=25"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    cards = response.json().get("data", [])

    for card in cards:
        obj = Object(service=service)
        obj.save()

        ### Character forms
        if "id" in card:
            CharacterForm.objects.create(object=obj, field=id_field, value=card["id"])
        if "name" in card:
            CharacterForm.objects.create(object=obj, field=name_field, value=card["name"])

        ### Integer forms
        if "hp" in card and card["hp"].isdigit():
            IntegerForm.objects.create(object=obj, field=hp_field, value=int(card["hp"]))

        ### Text forms
        if "types" in card:
            TextForm.objects.create(object=obj, field=types_field, value=", ".join(card["types"]))
        if "evolvesTo" in card:
            TextForm.objects.create(object=obj, field=evolvesTo_field, value=", ".join(card["evolvesTo"]))

        ### Date form
        release_date_str = card.get("set", {}).get("releaseDate")
        if release_date_str:
            release_date = datetime.strptime(release_date_str, "%Y/%m/%d").date()
            DateForm.objects.create(object=obj, field=date_field, value=release_date)

        ### URL forms
        for size, url_val in card.get("images", {}).items():
            field_instance = image_fields.get(size)
            if field_instance:
                URLForm.objects.create(object=obj, field=field_instance, value=url_val)

        ### Float forms 
        holofoil_prices = card.get("tcgplayer", {}).get("prices", {}).get("holofoil", {})
        for price_type in ["low", "mid", "high"]:
            price_value = holofoil_prices.get(price_type)
            field_instance = holo_fields.get(price_type)
            if price_value is not None and field_instance:
                FloatForm.objects.create(object=obj, field=field_instance, value=price_value)

        
        for i, attack in enumerate(card.get("attacks", []), start=1):
            if i in attack_fields:
                CharacterForm.objects.create(object=obj, field=attack_fields[i]["name"], value=attack.get("name", ""))
                IntegerForm.objects.create(object=obj, field=attack_fields[i]["energy_cost"], value=attack.get("convertedEnergyCost", 0))
                CharacterForm.objects.create(object=obj, field=attack_fields[i]["damage"], value=attack.get("damage", ""))
                TextForm.objects.create(object=obj, field=attack_fields[i]["text"], value=attack.get("text", ""))

        
        for i, weakness in enumerate(card.get("weaknesses", []), start=1):
            if i in weakness_fields:
                CharacterForm.objects.create(object=obj, field=weakness_fields[i]["type"], value=weakness.get("type", ""))
                CharacterForm.objects.create(object=obj, field=weakness_fields[i]["value"], value=weakness.get("value", ""))

    pass