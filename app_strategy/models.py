from django.db import models


# Create your models here.

class StrategyType(models.Model):
    strategy_type = models.CharField(max_length=32)


class StrategyInfo(models.Model):
    name = models.CharField(max_length=32)
    info = models.TextField()
    create_time = models.DateField(auto_now_add=True, null=True)
    type = models.ForeignKey('StrategyType', on_delete=models.DO_NOTHING, to_field='id', null=True)



class StrategyTradePositionList(models.Model):
    create_date = models.DateTimeField(null=True)
    code = models.CharField(max_length=16)
    position = models.IntegerField()
    direction = models.IntegerField()
    strategy = models.ForeignKey('StrategyInfo', on_delete=models.CASCADE, to_field='id', null=True)