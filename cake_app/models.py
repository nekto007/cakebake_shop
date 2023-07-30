from django.db import models
from django.db.models import F, Sum
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone


class CakeCategory(models.Model):
    title = models.CharField(
        'название категории',
        max_length=100
    )
    image = models.ImageField(
        'изображение для категории',
        null=True,
        blank=True
    )

    class Meta():
        verbose_name = 'категория торта'
        verbose_name_plural = 'категории тортов'

    def __str__(self):
        return self.title


class CatalogCake(models.Model):
    title = models.CharField(
        'название торта',
        max_length=100
    )
    description = models.TextField('описание торта')
    category = models.ForeignKey(
        CakeCategory,
        on_delete=models.CASCADE,
        related_name='cakes',
        verbose_name='категория торта'
    )
    price = models.DecimalField(
        'цена',
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )
    image = models.ImageField('изображение торта')

    class Meta():
        verbose_name = 'торт из каталога'
        verbose_name_plural = 'каталог тортов'

    def __str__(self):
        return self.title


class ComponentType(models.Model):
    title = models.CharField(
        'название типа',
        max_length=100
    )

    class Meta():
        verbose_name = 'тип компонента'
        verbose_name_plural = 'типы компонентов'

    def __str__(self):
        return self.title


class Component(models.Model):
    title = models.CharField(
        'название компонента',
        max_length=100
    )
    component_type = models.ForeignKey(
        ComponentType,
        on_delete=models.CASCADE,
        related_name='components',
        verbose_name='тип компонента'
    )
    price = models.DecimalField(
        'цена',
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )

    class Meta():
        verbose_name = 'компонент'
        verbose_name_plural = 'компоненты'

    def __str__(self):
        return self.title


class Bakery(models.Model):
    title = models.CharField(
        'название кондитерской',
        max_length=100
    )
    address = models.CharField(
        'адрес кондитерской',
        max_length=250
    )
    contact_phone = PhoneNumberField(
        verbose_name='номер телефона кондитерской',
        region='RU'
    )

    class Meta():
        verbose_name = 'пекарня'
        verbose_name_plural = 'пекарни'

    def __str__(self):
        return self.title


class OrderQuerySet(models.QuerySet):
    def fetch_with_total_price(self):
        orders_ids = [order.id for order in self]
        with_cakes_price_qs = Order.objects.filter(id__in=orders_ids).annotate(
            total_price=Sum(
                F('cakes__price')*F('cakes__quantity')
            )
        )
        with_components_price_qs = Order.objects.filter(id__in=orders_ids).annotate(
            total_price=Sum(
                F('components__price')*F('components__quantity')
            )
        )
        ids_and_cakes_price = dict(with_cakes_price_qs.values_list('id', 'total_price'))
        print(ids_and_cakes_price)
        ids_and_components_price = dict(with_components_price_qs.values_list('id', 'total_price'))
        print(ids_and_components_price)
        for order in self:
            component_total_price = 0
            cakes_total_price = 0
            if ids_and_components_price[order.id]:
                component_total_price = ids_and_components_price[order.id]
            if ids_and_cakes_price[order.id]:
                cakes_total_price = ids_and_cakes_price[order.id]
            order.total_price = component_total_price + cakes_total_price
        return self


class Order(models.Model):
    ORDER_STATUSES = [
        ('PLACED', 'Оформлен'),
        ('DELIVERED', 'Доставляется'),
        ('COMPLETE', 'Готов к выдаче'),
        ('TAKEN', 'Получен')
    ]
    RECEIPT_METHODS = [
        ('DELIVERY', 'Доставка'),
        ('PICKUP', 'Самовывоз')
    ]

    status = models.CharField(
        'статус заказа',
        max_length=15,
        choices=ORDER_STATUSES,
        default='PLACED',
        db_index=True
    )
    client_name = models.CharField(
        'имя клиента',
        max_length=100
    )
    phonenumber = PhoneNumberField(
        verbose_name='номер телефона',
        region='RU'
    )
    email = models.EmailField(
        verbose_name='почта клиента'
    )
    comment = models.TextField(
        'комментарий к заказу',
        blank=True
    )
    inscription = models.TextField(
        'надпись на торт',
        blank=True,
    )
    order_receipt_method = models.CharField(
        'Способ получения заказа',
        max_length=15,
        choices=RECEIPT_METHODS,
        default='PICKUP',
        db_index=True
    )
    bakery = models.ForeignKey(
        Bakery,
        on_delete=models.SET_NULL,
        related_name='orders',
        verbose_name='кондитерская для самовывоза',
        null=True,
        blank=True
    )
    address = models.CharField(
        'адрес доставки',
        max_length=250,
        blank=True
    )
    delivery_datetime = models.DateTimeField(
        'дата и время доставки',
        db_index=True,
        null=True,
        blank=True,
    )
    delivered_at = models.DateTimeField(
        'доставили',
        null=True,
        blank=True,
        db_index=True
    )
    delivery_comment = models.TextField(
        'комментарий курьеру',
        blank=True
    )
    created_at = models.DateTimeField(
        'заказ зарегестрирован',
        default=timezone.now,
        db_index=True
    )
    completed_at = models.DateTimeField(
        'заказ выполнен',
        null=True,
        blank=True,
        db_index=True
    )

    objects = OrderQuerySet.as_manager()

    class Meta():
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Заказ № {self.id}. {self.client_name}, телефон - {self.phonenumber}'


class OrderComponents(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='components',
        verbose_name='заказ'
    )
    component = models.ForeignKey(
        Component,
        on_delete=models.SET_NULL,
        related_name='order_components',
        verbose_name='компонент торта',
        null=True,
        blank=True
    )
    quantity = models.PositiveIntegerField(
        'количество',
        validators=[MinValueValidator(1)],
        default=1
    )
    price = models.DecimalField(
        'цена в заказе',
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )

    class Meta():
        verbose_name = 'ингридиенты в заказе'
        verbose_name_plural = 'ингридиенты в заказе'


class OrderCatalogCakes(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='cakes',
        verbose_name='заказ'
    )
    catalog_cake = models.ForeignKey(
        CatalogCake,
        on_delete=models.SET_NULL,
        related_name='order_cakes',
        verbose_name='торт из каталога',
        null=True,
        blank=True
    )
    quantity = models.PositiveIntegerField(
        'количество',
        validators=[MinValueValidator(1)],
        default=1
    )
    price = models.DecimalField(
        'цена в заказе',
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )

    class Meta():
        verbose_name = 'торты из каталога в заказе'
        verbose_name_plural = 'торты из каталога в заказе'
