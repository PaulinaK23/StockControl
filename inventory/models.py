# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Categories(models.Model):
    cat_id = models.AutoField(db_column='Cat_ID', primary_key=True)  # Field name made lowercase.
    cat_name = models.CharField(db_column='Cat_Name', max_length=100)  # Field name made lowercase.

    def __str__(self):
        return self.cat_name

    class Meta:
        managed = False
        db_table = 'Categories'


class Items(models.Model):
    itm_id = models.AutoField(db_column='Itm_ID', primary_key=True)  # Field name made lowercase.
    itm_name = models.CharField(db_column='Itm_Name', max_length=100)  # Field name made lowercase.
    itm_ean = models.CharField(db_column='Itm_Ean', unique=True, max_length=13, blank=True, null=True)  # Field name made lowercase.
    itm_catid = models.ForeignKey(Categories, models.DO_NOTHING, db_column='Itm_CatID', blank=True, null=True)  # Field name made lowercase.
    itm_uniid = models.ForeignKey('Units', models.DO_NOTHING, db_column='Itm_UniID', blank=True, null=True)  # Field name made lowercase.
    itm_supid = models.ForeignKey('Suppliers', models.DO_NOTHING, db_column='Itm_SupID', blank=True, null=True)  # Field name made lowercase.
    itm_price = models.DecimalField(db_column='Itm_Price', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    itm_minquantity = models.IntegerField(db_column='Itm_MinQuantity', blank=True, null=True)  # Field name made lowercase.
    itm_isactive = models.BooleanField(db_column='Itm_IsActive', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Items'


class Stock(models.Model):
    stk_id = models.AutoField(db_column='Stk_ID', primary_key=True)  # Field name made lowercase.
    stk_itmid = models.ForeignKey(Items, models.DO_NOTHING, db_column='Stk_ItmID', blank=True, null=True)  # Field name made lowercase.
    stk_whsid = models.ForeignKey('Warehouses', models.DO_NOTHING, db_column='Stk_WhsID', blank=True, null=True)  # Field name made lowercase.
    stk_qty = models.IntegerField(db_column='Stk_Qty')  # Field name made lowercase.
    stk_updatedate = models.DateTimeField(db_column='Stk_UpdateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Stock'


class Suppliers(models.Model):
    sup_id = models.AutoField(db_column='Sup_ID', primary_key=True)  # Field name made lowercase.
    sup_name = models.CharField(db_column='Sup_Name', max_length=100)  # Field name made lowercase.
    sup_taxid = models.CharField(db_column='Sup_TaxID', unique=True, max_length=15)  # Field name made lowercase.
    sup_email = models.CharField(db_column='Sup_Email', max_length=100, blank=True, null=True)  # Field name made lowercase.
    sup_phone = models.CharField(db_column='Sup_Phone', max_length=20, blank=True, null=True)  # Field name made lowercase.
    sup_paymentterms = models.CharField(db_column='Sup_PaymentTerms', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sup_address = models.CharField(db_column='Sup_Address', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Suppliers'


class Units(models.Model):
    uni_id = models.AutoField(db_column='Uni_ID', primary_key=True)  # Field name made lowercase.
    uni_name = models.CharField(db_column='Uni_Name', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Units'


class Warehouses(models.Model):
    whs_id = models.AutoField(db_column='Whs_ID', primary_key=True)  # Field name made lowercase.
    whs_name = models.CharField(db_column='Whs_Name', max_length=100)  # Field name made lowercase.
    whs_code = models.CharField(db_column='Whs_Code', max_length=10, blank=True, null=True)  # Field name made lowercase.
    whs_location = models.CharField(db_column='Whs_Location', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Warehouses'
