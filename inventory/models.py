# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from datetime import datetime
from django.db import transaction
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db.models import Sum, F  # Import Sum i F dla agregacji

class Categories(models.Model):
    cat_id = models.AutoField(db_column='Cat_ID', primary_key=True)  # Field name made lowercase.
    cat_name = models.CharField(db_column='Cat_Name', max_length=100, db_collation='Polish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Categories'

    def __str__(self):
        return self.cat_name


class Items(models.Model):
    itm_id = models.AutoField(db_column='Itm_ID', primary_key=True)  # Field name made lowercase.
    itm_name = models.CharField(db_column='Itm_Name', max_length=100, db_collation='Polish_CI_AS')  # Field name made lowercase.
    itm_ean = models.CharField(db_column='Itm_Ean', unique=True, max_length=13, db_collation='Polish_CI_AS', blank=False, null=False)  # Field name made lowercase.
    itm_catid = models.ForeignKey(Categories, models.DO_NOTHING, db_column='Itm_CatID', blank=True, null=True)  # Field name made lowercase.
    itm_uniid = models.ForeignKey('Units', models.DO_NOTHING, db_column='Itm_UniID', blank=True, null=True)  # Field name made lowercase.
    itm_supid = models.ForeignKey('Suppliers', models.DO_NOTHING, db_column='Itm_SupID', blank=True, null=True)  # Field name made lowercase.
    itm_price = models.DecimalField(db_column='Itm_Price', max_digits=10, decimal_places=2, blank=False, null=False)  # Field name made lowercase.
    itm_minquantity = models.IntegerField(db_column='Itm_MinQuantity', blank=True, null=True, default=0)  # Field name made lowercase.
    itm_isactive = models.BooleanField(db_column='Itm_IsActive', blank=True, null=True)  # Field name made lowercase.
    itm_insertedby = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        db_column='Itm_InsertedBy',
        related_name='items_created'
    )
    itm_insertdate = models.DateTimeField(db_column='Itm_InsertDate', default=now)
    itm_updatedby = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        db_column='Itm_UpdatedBy',
        blank=True,
        null=True,
        related_name='items_updated'
    )
    itm_updateddate = models.DateTimeField(db_column='Itm_UpdateDate', blank=True, null=True)

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)


        if not user or not user.is_authenticated:
            user = User.objects.get(username='sysadmin')

        current_time = now()  # Użyj timezone-aware daty

        if not self.pk:  # Nowy rekord
            self.itm_insertedby = user
            self.itm_insertdate = current_time
            self.itm_updatedby = user
            self.itm_updateddate = current_time
        else:  # Aktualizacja rekordu
            self.itm_updatedby = user
            self.itm_updateddate = current_time

        super().save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'Items'

    def __str__(self):
        return self.itm_name


class Stock(models.Model):
    stk_id = models.AutoField(db_column='Stk_ID', primary_key=True)  # Field name made lowercase.
    stk_itmid = models.ForeignKey(Items, models.DO_NOTHING, db_column='Stk_ItmID', blank=True, null=True)  # Field name made lowercase.
    stk_whsid = models.ForeignKey('Warehouses', models.DO_NOTHING, db_column='Stk_WhsID', blank=True, null=True)  # Field name made lowercase.
    stk_qty = models.IntegerField(db_column='Stk_Qty', default=0)  # Field name made lowercase.
    stk_updatedate = models.DateTimeField(db_column='Stk_UpdateDate', blank=True, null=True)  # Field name made lowercase.
    stk_insertdate = models.DateTimeField(db_column='Stk_InsertDate', default=now)  # Data dodania
    stk_insertedby = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        db_column='Stk_InsertedBy',
        related_name='stock_created'
    )  # Użytkownik, który dodał wpis

    stk_updatedby = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        db_column='Stk_UpdatedBy',
        blank=True,
        null=True,
        related_name='stock_updated'
    )  # Użytkownik, który edytował wpis

    class Meta:
        managed = False  # Django nie będzie zarządzało tabelą
        db_table = 'Stock'  # Nazwa tabeli w bazie

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)

        if not user or not user.is_authenticated:
            user = User.objects.get(username='sysadmin')  # Domyślny użytkownik systemowy

        current_time = now()  # Aktualny timestamp

        if not self.pk:  # Nowy rekord
            self.stk_insertedby = user
            self.stk_insertdate = current_time
            self.stk_updatedby = user
            self.stk_updatedate = current_time
        else:  # Aktualizacja rekordu
            self.stk_updatedby = user
            self.stk_updatedate = current_time

        super().save(*args, **kwargs)

class Suppliers(models.Model):
    sup_id = models.AutoField(db_column='Sup_ID', primary_key=True)  # Field name made lowercase.
    sup_name = models.CharField(db_column='Sup_Name', max_length=100, db_collation='Polish_CI_AS')  # Field name made lowercase.
    sup_taxid = models.CharField(db_column='Sup_TaxID', unique=True, max_length=15, db_collation='Polish_CI_AS', blank=False, null=False)  # Field name made lowercase.
    sup_email = models.CharField(db_column='Sup_Email', max_length=100, db_collation='Polish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sup_phone = models.CharField(db_column='Sup_Phone', max_length=20, db_collation='Polish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sup_paymentterms = models.CharField(db_column='Sup_PaymentTerms', max_length=50, db_collation='Polish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sup_address = models.CharField(db_column='Sup_Address', max_length=200, db_collation='Polish_CI_AS', blank=True, null=True)  # Field name made lowercase.

    sup_isactive = models.BooleanField(db_column='Sup_IsActive', default=True)  # Pole aktywności dostawcy
    sup_insertedby = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        db_column='Sup_InsertedBy',
        related_name='suppliers_created'
    )
    sup_insertdate = models.DateTimeField(db_column='Sup_InsertDate', default=now)
    sup_updatedby = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        db_column='Sup_UpdatedBy',
        blank=True,
        null=True,
        related_name='suppliers_updated'
    )
    sup_updateddate = models.DateTimeField(db_column='Sup_UpdateDate', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Suppliers'

    def __str__(self):
        return self.sup_name

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)

        if not user or not user.is_authenticated:
            user = User.objects.get(username='sysadmin')

        current_time = now()  # Pobranie bieżącego czasu

        if not self.pk:  # Nowy rekord
            self.sup_insertedby = user
            self.sup_insertdate = current_time
            self.sup_updatedby = user
            self.sup_updateddate = current_time
        else:  # Aktualizacja rekordu
            self.sup_updatedby = user
            self.sup_updateddate = current_time

        super().save(*args, **kwargs)


class Units(models.Model):
    uni_id = models.AutoField(db_column='Uni_ID', primary_key=True)  # Field name made lowercase.
    uni_name = models.CharField(db_column='Uni_Name', max_length=10, db_collation='Polish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Units'

    def __str__(self):
        return self.uni_name


class Warehouses(models.Model):
    whs_id = models.AutoField(db_column='Whs_ID', primary_key=True)  # Field name made lowercase.
    whs_name = models.CharField(db_column='Whs_Name', max_length=100, db_collation='Polish_CI_AS')  # Field name made lowercase.
    whs_code = models.CharField(db_column='Whs_Code', max_length=10, db_collation='Polish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    whs_location = models.CharField(db_column='Whs_Location', max_length=100, db_collation='Polish_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Warehouses'

    def __str__(self):
        return self.whs_name


class Statuses(models.Model):
    sta_id = models.AutoField(primary_key=True, db_column='Sta_ID')
    sta_name = models.CharField(max_length=100, db_column='Sta_Name', verbose_name="Nazwa statusu")

    def __str__(self):
        return self.sta_name

    class Meta:
        managed = False
        db_table = 'Statuses'
        verbose_name = "Status"
        verbose_name_plural = "Statusy"


# class Orders(models.Model):
#     ord_id = models.AutoField(primary_key=True, db_column='Ord_ID')
#     ord_date = models.DateTimeField(
#         db_column='Ord_Date',
#         verbose_name="Data zamówienia",
#         default=datetime.now  # Ustaw domyślną wartość na bieżącą datę i czas
#     )
#     ord_statusid = models.ForeignKey('Statuses', on_delete=models.CASCADE, db_column='Ord_StatusID', related_name='orders', verbose_name="Status")
#     ord_whsid = models.ForeignKey('Warehouses', on_delete=models.CASCADE, db_column='Ord_WhsID', related_name='orders', verbose_name="Magazyn")
#     ord_total = models.DecimalField(db_column='Ord_Total', max_digits=10, decimal_places=2, default=0.00)
#     ord_supid = models.ForeignKey('Suppliers', on_delete=models.SET_NULL, db_column='Ord_SupID', null=True, blank=True, related_name='orders', verbose_name="Dostawca")
#     ord_number = models.CharField(max_length=50, db_column='Ord_Number', null=True, blank=True, verbose_name="Numer zamówienia")
#
#     def __str__(self):
#         return f"{self.ord_number or 'Zamówienie'} ({self.ord_date.strftime('%Y-%m-%d')})"
#
#     class Meta:
#         managed = False
#         db_table = 'Orders'
#         verbose_name = "Zamówienie"
#         verbose_name_plural = "Zamówienia"
#
#
#     def save(self, *args, **kwargs):
#         # Wyliczanie wartości `Ord_Total`
#         if self.pk:  # Sprawdza, czy zamówienie już istnieje
#             total = OrderItems.objects.filter(oit_ordid=self.pk).aggregate(
#                 total=models.Sum(models.F('oit_quantity') * models.F('oit_price'))
#             )['total'] or 0  # Domyślnie 0, jeśli brak pozycji
#             self.ord_total = total
#
#         super().save(*args, **kwargs)  # Wywołanie oryginalnej metody `save`
#
#
# class OrderItems(models.Model):
#     oit_id = models.AutoField(primary_key=True, db_column='Oit_ID', verbose_name="Numer pozycji")  # Klucz główny, identity
#     oit_ordid = models.ForeignKey(
#         'Orders',
#         on_delete=models.CASCADE,
#         db_column='Oit_OrdID',
#         related_name='order_items',
#         verbose_name="Zamówienie"
#     )
#     oit_itmid = models.ForeignKey(
#         'Items',
#         on_delete=models.CASCADE,
#         db_column='Oit_ItmID',
#         related_name='order_items',
#         verbose_name="Produkt"
#     )
#     oit_quantity = models.IntegerField(db_column='Oit_Quantity', verbose_name="Ilość")
#     oit_price = models.DecimalField(max_digits=10, decimal_places=2, db_column='Oit_Price', verbose_name="Cena jednostkowa")
#
#     def __str__(self):
#         return f"{self.oit_itmid} - {self.oit_quantity} szt."
#
#     class Meta:
#         managed = False  # Tabela zarządzana zewnętrznie
#         db_table = 'OrderItems'
#         verbose_name = "Pozycja zamówienia"
#         verbose_name_plural = "Pozycje zamówienia"
#
class Orders(models.Model):
    ord_id = models.AutoField(primary_key=True, db_column='Ord_ID')
    ord_date = models.DateTimeField(
        db_column='Ord_Date',
        verbose_name="Data zamówienia",
        default=datetime.now  # Domyślnie ustawiona bieżąca data i czas
    )
    ord_statusid = models.ForeignKey(
        'Statuses',
        on_delete=models.CASCADE,
        db_column='Ord_StatusID',
        related_name='orders',
        verbose_name="Status"
    )
    ord_whsid = models.ForeignKey(
        'Warehouses',
        on_delete=models.CASCADE,
        db_column='Ord_WhsID',
        related_name='orders',
        verbose_name="Magazyn"
    )
    ord_total = models.DecimalField(
        db_column='Ord_Total',
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Łączna wartość"
    )
    ord_supid = models.ForeignKey(
        'Suppliers',
        on_delete=models.SET_NULL,
        db_column='Ord_SupID',
        null=True,
        blank=True,
        related_name='orders',
        verbose_name="Dostawca"
    )
    ord_number = models.CharField(
        max_length=50,
        db_column='Ord_Number',
        null=True,
        blank=True,
        verbose_name="Numer zamówienia"
    )

    def __str__(self):
        return f"{self.ord_number or 'Zamówienie'} ({self.ord_date.strftime('%Y-%m-%d')})"

    def save(self, *args, **kwargs):
        # Wyliczanie total z pozycji zamówienia
        total = OrderItems.objects.filter(oit_ordid=self.pk).aggregate(
            total=Sum(F('oit_quantity') * F('oit_price'))
        )['total'] or 0
        self.ord_total = total
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'Orders'
        verbose_name = "Zamówienie"
        verbose_name_plural = "Zamówienia"


class OrderItems(models.Model):
    oit_id = models.AutoField(primary_key=True, db_column='Oit_ID')
    oit_ordid = models.ForeignKey(
        Orders,
        on_delete=models.CASCADE,
        db_column='Oit_OrdID',
        related_name='order_items',
        verbose_name="Zamówienie"
    )
    oit_itmid = models.ForeignKey(
        'Items',
        on_delete=models.CASCADE,
        db_column='Oit_ItmID',
        related_name='order_items',
        verbose_name="Produkt"
    )
    oit_quantity = models.IntegerField(db_column='Oit_Quantity', verbose_name="Ilość")
    oit_price = models.DecimalField(max_digits=10, decimal_places=2, db_column='Oit_Price', verbose_name="Cena jednostkowa")

    def __str__(self):
        return f"{self.oit_itmid} - {self.oit_quantity} szt."

    class Meta:
        db_table = 'OrderItems'
        verbose_name = "Pozycja zamówienia"
        verbose_name_plural = "Pozycje zamówienia"

class Objects(models.Model):
    obj_id = models.AutoField(primary_key=True, db_column='Obj_ID')
    obj_name = models.CharField(max_length=100, unique=True, db_column='Obj_Name')

    def __str__(self):
        return self.obj_name

    class Meta:
        db_table = 'Objects'


class Attachments(models.Model):
    att_id = models.BigAutoField(primary_key=True)  # Główne ID załącznika
    att_objecttypeid = models.ForeignKey(
        Objects,
        on_delete=models.CASCADE,
        db_column='Att_ObjectTypeID',
        verbose_name='Typ obiektu'
    )
    att_objid = models.PositiveIntegerField(db_column='Att_ObjID')  # ID powiązanego obiektu
    att_file = models.FileField(upload_to='attachments/', db_column='Att_File')  # Ścieżka do pliku
    att_description = models.CharField(max_length=255, null=True, blank=True, db_column='Att_Description')  # Opis
    att_insertdate = models.DateTimeField(auto_now_add=True, db_column='Att_InsertDate')  # Data dodania
    att_insertedby = models.CharField(max_length=50, null=True, blank=True, db_column='Att_InsertedBy')  # Kto dodał

    class Meta:
        db_table = 'Attachments'
        indexes = [
            models.Index(fields=['att_objecttypeid', 'att_objid'], name='IX_Attachments_ObjectType')  # Indeks
        ]

    def __str__(self):
        return f"Attachment {self.att_id}: {self.att_file.name}"


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, db_collation='Polish_CI_AS')

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)



class AuthPermission(models.Model):
    name = models.CharField(max_length=255, db_collation='Polish_CI_AS')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, db_collation='Polish_CI_AS')

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128, db_collation='Polish_CI_AS')
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, db_collation='Polish_CI_AS')
    first_name = models.CharField(max_length=150, db_collation='Polish_CI_AS')
    last_name = models.CharField(max_length=150, db_collation='Polish_CI_AS')
    email = models.CharField(max_length=254, db_collation='Polish_CI_AS')
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(db_collation='Polish_CI_AS', blank=True, null=True)
    object_repr = models.CharField(max_length=200, db_collation='Polish_CI_AS')
    action_flag = models.SmallIntegerField()
    change_message = models.TextField(db_collation='Polish_CI_AS')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, db_collation='Polish_CI_AS')
    model = models.CharField(max_length=100, db_collation='Polish_CI_AS')

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255, db_collation='Polish_CI_AS')
    name = models.CharField(max_length=255, db_collation='Polish_CI_AS')
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40, db_collation='Polish_CI_AS')
    session_data = models.TextField(db_collation='Polish_CI_AS')
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
