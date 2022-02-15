from django.db import models
from stdimage.models import StdImageField
from datetime import datetime

# SIGNALS
from django.db.models import signals
from django.template.defaultfilters import slugify

# Create your models here.
class Base(models.Model):
    created = models.DateField('Data de criação', auto_now_add=True)
    modified = models.DateField('Data de Atualização', auto_now=True)
    active = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True

class Brand(Base):
    brand = models.CharField('Marca', max_length=10)

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
    
    def __str__(self):
        return self.brand

class CarModel(Base):
    brand = models.ForeignKey(Brand, related_name='modelo', on_delete=models.CASCADE)
    model = models.CharField("Modelo", max_length=100)

    class Meta:
        verbose_name = 'Modelo'
        verbose_name_plural = 'Modelos'
    
    def __str__(self):
        return self.model


class Car(Base):
    CATEGORY_CHOICES = (
        ('Hatch', 'Hatch'),
        ('Minivan', 'Minivan'),
        ('Perua', 'Perua'),
        ('Picape', 'Picape'),
        ('Picape C. Dupla', 'Picape C. Dupla'),
        ('SUV', 'SUV'),
        ('Seda', 'Sedã')
    )
    
    COLOR_CHOICES = (
        ('Amarelo', 'Amarelo'),
        ('Azul', 'Azul'),
        ('Branco', 'Branco'),
        ('Preto', 'Preto'),
        ('Vermelho', 'Vermelho'),
        ('Cinza', 'Cinza'),
        ('Bege', 'Bege'),
        ('Vinho', 'Vinho'),
        ('Verde', 'Verde'),
        ('Marrom', 'Marrom'),
    )

    EXCHANGE_CHOICES = {
        ('Manual', 'Manual'),
        ('Automatico', 'Automático'),
        ('CVT', 'CVT'),
        ('Semi-automatico', 'Semi-automático'),
    }

    FUEL_CHOICES = (
        ('Gasolina', 'Gasolina'),
        ('Diesel', 'Diesel'),
        ('A/G', 'Á/G'),
        ('Alcool', 'Álcool'),
    )

    DOORS_CHOICES = tuple([(str((i)), str(i)) for i in range(2, 6)]) # gera a quantidade de portas entre 2 e 5 portas
    YEAR_CHOICES = tuple([(datetime.today().year-i, datetime.today().year-i) for i in range(0, 23)]) # gera os anos desde 2022 até 2000
    
    # FIELDS 
    new = models.BooleanField('Novo', default=True)
    kms = models.PositiveIntegerField('Kms Rodados', default=0)
    year = models.PositiveIntegerField('Ano', choices=YEAR_CHOICES, default=datetime.today().year)
    price = models.DecimalField('Preço', max_digits=8, decimal_places=2)
    color = models.CharField('Cor', max_length=9, choices=COLOR_CHOICES, default="Branco")
    brand = models.ForeignKey(Brand, related_name='marca', on_delete=models.CASCADE)
    model = models.ForeignKey(CarModel, related_name='modelo', on_delete=models.CASCADE)
    category = models.CharField('Categoria', max_length=15, choices=CATEGORY_CHOICES, default="Hatch")
    exchange = models.CharField('Câmbio', max_length=15, choices=EXCHANGE_CHOICES, default='Manual')
    fuel = models.CharField('Combustível', max_length=10, choices=FUEL_CHOICES, default='Gasolina')
    doors = models.CharField('Portas', max_length=1, choices=DOORS_CHOICES, default='1')
    image = StdImageField('Imagem', upload_to='carros', variations={'thumb': (290, 220)})
    slug = models.SlugField('Slug', max_length=100, blank=True, editable=False)

    class Meta:
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'
    
    def __str__(self):
        return str(self.model) #self.car


def car_pre_save(signal, instance, sender, **kwargs):
    if instance.kms != 0 and instance.new:
        instance.new = False
    if instance.price < 0:
        instance.price = -instance.price

    instance.slug = slugify(instance.model)

signals.pre_save.connect(car_pre_save, sender=Car)