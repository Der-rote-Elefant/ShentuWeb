from django.db import models

# Create your models here.

class StrategyType(models.Model):
    strategy_type = models.CharField(max_length=32)