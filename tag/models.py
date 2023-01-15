from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify
from random import SystemRandom
import string


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    # Relação genérica
    # Representação do model que queremos encaixar
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # Representação do ID da linha do model descrito acima
    object_id = models.CharField()
    # Campo que representa a relação genérica conhece os campos acima
    content_object = GenericForeignKey('content_type')

    def save(self, *args, **kwargs):
        if not self.slug:
            rand_letters = ''.join(
                SystemRandom().choices(
                    string.ascii_letters + string.digits,
                    k=5,
                )
            )
            self.slug = slugify(f'{self.name}-{rand_letters}')
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
