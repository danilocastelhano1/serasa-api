import logging

from django.db import transaction
from rest_framework import serializers
from validate_docbr import CNPJ
from validate_docbr import CPF

from .models import Culture
from .models import Farm
from .models import Productor
from .models import Season

logger = logging.getLogger(__name__)

cpf = CPF()
cnpj = CNPJ()


class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = [
            "name",
        ]


class CultureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Culture
        fields = [
            "name",
        ]


class SeasonSerializer(serializers.ModelSerializer):
    cultures = CultureSerializer(many=True, required=True)

    class Meta:
        model = Season
        fields = ["year", "cultures"]


class ProductorSerializer(serializers.ModelSerializer):
    seasons = SeasonSerializer(many=True, required=True)
    farm = FarmSerializer(many=False, required=True)

    class Meta:
        model = Productor
        fields = [
            "id",
            "cpf_cnpj",
            "name",
            "city",
            "state",
            "farm",
            "total_area",
            "agricultural_area",
            "vegetation_area",
            "seasons",
        ]

    def validate_total_area(self, value):
        """
        Validates that the sum of the areas does not exceed the total area.
        """
        logger.info("Start validating total_area")

        agricultural_area = self.initial_data.get("agricultural_area", 0)
        vegetation_area = self.initial_data.get("vegetation_area", 0)
        total_area = value or 0

        if (agricultural_area + vegetation_area) > total_area:
            logger.error("Validate total_area raised")

            raise serializers.ValidationError(
                "The sum of the 'agricultural_area' and 'vegetation_area' areas cannot exceed the total_area."
            )
        return total_area

    def validate_cpf_cnpj(self, value):
        """
        Validates the CPF or CNPJ.
        """
        value: str = "".join(v for v in value if v.isdigit())
        logger.info("Start validating cpf_cnpj %s", value)

        if len(value) == 11:  # CPF
            if not cpf.validate(value):
                logger.error("Invalid CPF")
                raise serializers.ValidationError("Invalid CPF.")
        elif len(value) == 14:  # CNPJ
            if not cnpj.validate(value):
                logger.error("Invalid CNPJ")
                raise serializers.ValidationError("Invalid CNPJ.")
        else:
            logger.error("Invalid CPF or CNPJ")
            raise serializers.ValidationError("CPF or CNPJ is invalid.")

        if not self.instance and Productor.objects.filter(cpf_cnpj=value).exists():
            raise serializers.ValidationError("CPF or CNPJ Already exists.")

        return value

    @staticmethod
    def store_season_and_culture(productor, seasons_data):
        for season_data in seasons_data:
            cultures_data = season_data.pop("cultures")
            season, _ = Season.objects.get_or_create(productor_id=productor.id, **season_data)

            for culture_data in cultures_data:
                Culture.objects.get_or_create(season_id=season.id, **culture_data)

    @transaction.atomic
    def create(self, validated_data):
        logger.info("Start creating a productor with these validated_data %s", validated_data)

        seasons_data = validated_data.pop("seasons")
        farm_data = validated_data.pop("farm")

        farm, _ = Farm.objects.get_or_create(**farm_data)
        validated_data["farm"] = farm

        productor = super(ProductorSerializer, self).create(validated_data)

        self.store_season_and_culture(productor, seasons_data)
        logger.debug("Created successfully")
        return productor

    @transaction.atomic
    def update(self, instance, validated_data):
        logger.info("Start updating a productor with these validated_data %s", validated_data)

        seasons_data = validated_data.pop("seasons")
        farm_data = validated_data.pop("farm")
        farm, _ = Farm.objects.get_or_create(**farm_data)
        validated_data["farm"] = farm
        productor = super(ProductorSerializer, self).update(instance, validated_data)

        instance.seasons.all().delete()
        self.store_season_and_culture(productor, seasons_data)
        logger.debug("Updated successfully")
        return productor
