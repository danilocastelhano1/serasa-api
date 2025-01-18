import uuid

from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Farm(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Productor(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cpf_cnpj = models.CharField(max_length=18, unique=True)
    name = models.CharField(max_length=100)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    total_area = models.DecimalField(max_digits=10, decimal_places=2)
    agricultural_area = models.DecimalField(max_digits=10, decimal_places=2)
    vegetation_area = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.farm.name}"


class Season(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    productor = models.ForeignKey(Productor, on_delete=models.CASCADE, related_name="seasons")
    year = models.PositiveIntegerField()

    def __str__(self):
        return f"Season {self.year} - {self.productor.farm.name}"


class Culture(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="cultures")
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} - Season {self.season.year}"
