from django.db import models


# --------------------CDCs----------------------------------------
class CDCs(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, verbose_name='ОКД', default='', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'ОКД'
        verbose_name_plural = 'ОКД'
        ordering = ['name']

# --------------------ClueAttrs----------------------------------------
class ClueAttrs(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, verbose_name='Описание', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Значащий атрибут'
        verbose_name_plural = 'Значащие атрибуты'
        ordering = ['name']

# --------------------DataObjects----------------------------------------
class DataObjects(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, verbose_name='Объект данных', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Объект данных логического узла'
        verbose_name_plural = 'Объекты данных логического узла'
        ordering = ['name']

# --------------------Datasets----------------------------------------
class Datasets(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, verbose_name='Датасет', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Датасет'
        verbose_name_plural = 'Датасеты'
        ordering = ['name']


# --------------------Statuses----------------------------------------
class Statuses(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, verbose_name='Статусы сигнала', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус сигнала'
        verbose_name_plural = 'Статусы сигнала'
        ordering = ['name']

# --------------------Signals----------------------------------------
class Signals(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, verbose_name='Сигналы', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Перечень сигналов'
        verbose_name_plural = 'Перечни сигналов'
        ordering = ['name']


# -------------------------------------------------------------------
# --------------------LNobject----------------------------------------
class LNobject(models.Model):
    CUS_CHOICES = [
        ('+', '+'),
        ('-', '-')
    ]
    RAS_CHOICES = [
        ('+', '+'),
        ('-', '-'),
        ('П', 'П')
    ]
    SIG_CHOICES = [
        ('Внутр', 'Внутренний сигнал'),
        ('ВнутрШтрих', 'Внутренний штриховой'),
        ('-', 'Без прорисовки')
    ]
    id = models.AutoField(primary_key=True)
    data_object = models.ForeignKey(DataObjects, on_delete=models.CASCADE, verbose_name='Объект данных')
    cdc = models.ForeignKey(CDCs, on_delete=models.CASCADE, verbose_name='ОКД')
    signal = models.ForeignKey(Signals, on_delete=models.CASCADE, verbose_name='Сигнал', null=True, default='<не задан>')
    status = models.ForeignKey(Statuses, on_delete=models.CASCADE, verbose_name='Статус сигнала', blank=True, null=True)
    clue_attr = models.ForeignKey(ClueAttrs, on_delete=models.CASCADE, verbose_name='Значащий атрибут', default='<не задан>')
    func_group = models.IntegerField(verbose_name='Функ. группа', default=-1)
    cus = models.CharField(max_length=1, choices=CUS_CHOICES, default='-', verbose_name='ЦУС')
    rdu = models.CharField(max_length=1, choices=CUS_CHOICES, default='-', verbose_name='РДУ')
    ras = models.CharField(max_length=1, choices=RAS_CHOICES, default='-', verbose_name='РАС')
    dataset = models.ForeignKey(Datasets, on_delete=models.CASCADE, verbose_name='Датасет', blank=True, null=True)
    sgras_name = models.CharField(max_length=64, verbose_name='Обозначение РАС/Уставка', blank=True)
    signal_type = models.CharField(max_length=32, choices=SIG_CHOICES, default='-', verbose_name='Тип сигнала (чертеж)')
    signal_number = models.IntegerField(verbose_name='Номер выхода (чертеж)', default=0)

    def __str__(self):
        return str(self.data_object)

    class Meta:
        verbose_name = 'Объект логического узла'
        verbose_name_plural = 'Объекты логических узлов'
        ordering = ['data_object']

    @property
    def get_dataset(self):
        if self.dataset:
            return self.dataset
        else:
            return "<Чертеж>"

# --------------------LogicNodesTypes----------------------------------------
class LogicNodesTypes(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, verbose_name='Имя типа ЛУ', unique=True)
    description = models.TextField(max_length=1024, blank=True, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип логического узла'
        verbose_name_plural = 'Типы логических узлов'
        ordering = ['name']

# --------------------Switch----------------------------------------
class Switch(models.Model):
    SW_CHOICES = [
        ('SW.2', 'SW.2'),
        ('SW.3', 'SW.3')
    ]
    sw_type = models.CharField(max_length=4, choices=SW_CHOICES, default='SW.2', verbose_name='Тип')
    short_name = models.CharField(max_length=32, verbose_name='Краткое обозначение')
    description = models.TextField(max_length=1024, verbose_name='Назначение', blank=True)

    def __str__(self):
        return self.sw_type

    class Meta:
        verbose_name = 'Переключатель'
        verbose_name_plural = 'Переключатели'
        ordering = ['sw_type']


# --------------------Input----------------------------------------
class Input(models.Model):
    SW_CHOICES = [
        ('SW.2', 'SW.2'),
        ('SW.2', 'SW.2'),
        ('-', '-')
    ]
    name = models.CharField(max_length=4, verbose_name='Обозначение входа (напр.: С1, А4)')
    sw_type = models.CharField(max_length=4, choices=SW_CHOICES, default='-', verbose_name='Тип переключателя')
    sw_name = models.CharField(max_length=32, verbose_name='Обозначение переключателя', blank=True)
    description = models.CharField(max_length=128, verbose_name='Описание входа (напр.: АСУ / Режим работы)')

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Вход'
        verbose_name_plural = 'Входы'
        ordering = ['description']




# --------------------LogicNodeInstantiated----------------------------------------
class LogicNodeInstantiated(models.Model):
    id = models.AutoField(primary_key=True)
    short_name = models.CharField(max_length=64, verbose_name='Краткое имя', unique=True)
    full_name = models.CharField(max_length=128, verbose_name='Полное имя', blank=True)
    ln_prefix = models.CharField(max_length=32, verbose_name='Префикс ЛУ', blank=True)
    class_name = models.CharField(max_length=4, verbose_name='Класс')
    instance = models.IntegerField(verbose_name='Номер экземпляра', blank=True, null=True)
    ln_type = models.ForeignKey(LogicNodesTypes, on_delete=models.CASCADE, verbose_name='Тип ЛУ', null=True)
    def __str__(self):
        return str(self.short_name)

    class Meta:
        verbose_name = 'Экземпляр логического узла'
        verbose_name_plural = 'Экземпляр логического узла'
        ordering = ['short_name']

    @property
    def get_instance(self):
        if self.instance:
            return self.instance
        else:
            return "-"

# --------------------SwitchesAndLNs----------------------------------------
class SwitchesAndLNs(models.Model):
    id = models.AutoField(primary_key=True)
    switch = models.ForeignKey(Switch, on_delete=models.CASCADE, verbose_name='Переключатель', null=True)
    ln = models.ForeignKey(LogicNodeInstantiated, on_delete=models.CASCADE, verbose_name='Экземпляр лог. узла', null=True)

    def __str__(self):
        return self.switch

    class Meta:
        verbose_name = 'Переключатель в составе ФБ'
        verbose_name_plural = 'Переключатели в составе ФБ'
        ordering = ['switch']

# --------------------InputsAndLNs----------------------------------------
class InputsAndLNs(models.Model):
    id = models.AutoField(primary_key=True)
    input = models.ForeignKey(Input, on_delete=models.CASCADE, verbose_name='Переключатель', null=True)
    ln = models.ForeignKey(LogicNodeInstantiated, on_delete=models.CASCADE, verbose_name='Экземпляр лог. узла', null=True)

    def __str__(self):
        return self.input

    class Meta:
        verbose_name = 'Вход в составе ФБ'
        verbose_name_plural = 'Входы составе ФБ'
        ordering = ['input']

'''
# --------------------LNobjConnections--УДАЛИТЬ--------------------------------------
class LNobjConnections(models.Model):
    id = models.AutoField(primary_key=True)
    ln_inst = models.ForeignKey(LogicNodeInstantiated, on_delete=models.CASCADE, verbose_name='Экземпляр логического узла', null=True)
    ln_obj = models.ForeignKey(LNobject, on_delete=models.CASCADE, verbose_name='Объект лог. узла', null=True)

    def __str__(self):
        return str(self.ln_inst)

    class Meta:
        verbose_name = ' -Удалить- Связь между экземплярами логических узлов и объектами'
        verbose_name_plural = '-Удалить- Связи между экземплярами логических узлов и объектами'
        ordering = ['ln_inst']
'''
# --------------------LNtypeObjConnections----------------------------------------
class LNtypeObjConnections(models.Model):
    id = models.AutoField(primary_key=True)
    ln_type = models.ForeignKey(LogicNodesTypes, on_delete=models.CASCADE, verbose_name='Тип логического узла', null=True)
    ln_obj = models.ForeignKey(LNobject, on_delete=models.CASCADE, verbose_name='Объект лог. узла', null=True)

    def __str__(self):
        return str(self.ln_type)

    class Meta:
        verbose_name = 'Связь между типом логического узла и объектами'
        verbose_name_plural = 'Связи между типами логических узлов и объектами'
        ordering = ['ln_type']


# --------------------LogicDevices----------------------------------------
class LogicDevices(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, verbose_name='Обозначение логического устройства', unique=True)
    fb_name = models.CharField(max_length=128, verbose_name='Обозначение функционального блока', unique=True)
    description = models.TextField(max_length=1024, blank=True, verbose_name='Назначение логического устройства (ФБ)')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Логическое устройство'
        verbose_name_plural = 'Логические устройства'
        ordering = ['name']

# --------------------LDLNconnections----------------------------------------
class LDLNconnections(models.Model):
    id = models.AutoField(primary_key=True)
    ld = models.ForeignKey(LogicDevices, on_delete=models.CASCADE, verbose_name='Логическое устройство', null=True)
    ln = models.ForeignKey(LogicNodeInstantiated, on_delete=models.CASCADE, verbose_name='Экземпляр лог. узла', null=True)

    def __str__(self):
        return str(self.ld)

    class Meta:
        verbose_name = 'Связь между логическими устройствами и экземплярами логических узлов'
        verbose_name_plural = 'Связи между логическими устройствами и экземплярами логических узлов'
        ordering = ['ld']


# --------------------Terminals----------------------------------------
class Terminals(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, verbose_name='Обозначение ИЭУ', unique=True)
    description = models.TextField(max_length=1024, blank=True, verbose_name='Назначение ИЭУ')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'ИЭУ'
        verbose_name_plural = 'ИЭУ'
        ordering = ['name']

# --------------------PhDLDconnections----------------------------------------
class PhDLDconnections(models.Model):
    id = models.AutoField(primary_key=True)
    ied = models.ForeignKey(Terminals, on_delete=models.CASCADE, verbose_name='Физическое устройство', null=True)
    ld = models.ForeignKey(LogicDevices, on_delete=models.CASCADE, verbose_name='Логическое устройство', null=True)

    def __str__(self):
        return str(self.ied)

    class Meta:
        verbose_name = 'Связь между физическими и логическими устройствами'
        verbose_name_plural = 'Связи между физическими и логическими устройствами'
        ordering = ['ied']

# --------------------Cabinets----------------------------------------
class Cabinets(models.Model):
    name = models.CharField(max_length=64, verbose_name='Обозначение шкафа', primary_key=True)
    terminal1 = models.ForeignKey(Terminals, related_name='ied1_set', on_delete=models.PROTECT, verbose_name='ИЭУ1', max_length=64, null=True)
    terminal2 = models.ForeignKey(Terminals, related_name='ied2_set', on_delete=models.PROTECT, verbose_name='ИЭУ2', max_length=64, blank=True, null=True)
    terminal3 = models.ForeignKey(Terminals, related_name='ied3_set', on_delete=models.PROTECT, verbose_name='ИЭУ3', max_length=64, blank=True, null=True)
    description = models.TextField(max_length=1024, verbose_name='Назначение шкафа')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Шкаф'
        verbose_name_plural = 'Шкафы'
        ordering = ['name']
    # чтобы пустые поля не выводились как None!
    @property
    def get_terminal2(self):
        if self.terminal2:
            return self.terminal2
        else:
            return ""
    @property
    def get_terminal3(self):
        if self.terminal3:
            return self.terminal3
        else:
            return ""

