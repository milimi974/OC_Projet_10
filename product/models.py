import math

import os

import csv

from django.db import models

# Create your models here.
import requests

from master.settings import BASE_DIR
from tools import upload_openfoodfact_cvs, clear_string, str_to_float


class Category(models.Model):
    """ Categories of product
        :argument
        model : parent

    """
    # fields
    name = models.CharField(max_length=255, unique=True)
    # var contain list of categories to save
    list = []
    # contain object instance
    list_object = {}

    # uri
    url_categories = 'https://fr.openfoodfacts.org/categories?json=1'


    def __str__(self):
        return self.name

    def upload(self):
        """ upload all categories """
        response = requests.get(self.url_categories)
        return response.json()

    def get_category_product(self, name):
        """ return a list of category product
            Keyword arguments:
            name -- string category name
        """

    def extract(self, categories_str):
        """ extract categories name from list

            Keyword arguments:
            categories_str -- string of categories elements

        """
        b = self.str_to_list(categories_str)
        if b:
            # merge list and remove duplicate
            self.list = list(set().union(self.list, b))


    def str_to_list(self, strvar):
        """ Return a list of categories object

            Keyword arguments:
            strvar -- string of product elements

        """
        # test type of value if string
        if type(strvar) is str and strvar:
            # Make a list with string
            return [x.strip() for x in strvar.split(',')]
        return False


    def create_categories(self):
        # create categories list
        if self.list:
            for category in self.list:
                category_qs, create = Category.objects.get_or_create(name=category)
                # stock category object by name
                self.list_object[category] = category_qs

    def add_category_list(self, name):
        """add one element name to list
            Keyword arguments:
            name -- string name of category
        """
        # merge list and remove duplicate
        self.list = list(set().union(self.list, list(name)))

    def get_category(self, name):
        """ return category object by name
            :argument
            name : object name

        """
        try:
            self.list_object[name]
            return self.list_object[name]
        except:
            return False

    def reset(self):
        """ reset list """
        self.list = []
        self.list_object = {}


class ManageDB(models.Manager):

    # object for create all categories or shops
    categories = Category()
    # list of product to save
    products = []



    # update database with data from OpenFoodFact API
    def update_db(self, qty=500, qtyc=500,upload=False, api=False):
        """ create products
            Keyword arguments:
            qty -- int total product to create
            qtyc -- int total category to create
            upload -- boolean use csv file
            api -- boolean use json file
        """
        if upload :
            upload_openfoodfact_cvs()
            return self.add_by_upload_file(qty)
        if api:
            return self.add_by_api(qty, qtyc)

    def add_by_api(self, qty, qtyc):
        """ create products
            Keyword arguments:
            qty -- int total product to create
            qtyc -- int total category to create
        """
        # read all products
        read_all = False
        if qty == -1:
            read_all = True

        # counter
        counter_p = 0
        counter_c = 0
        total_product = 0
        # create all categories
        categories = self.categories.upload()

        # config for save all categories
        if qtyc == -1:
            # read total entries
            qtyc = int(categories['count'])

        for category in categories['tags']:

            # get category from db
            category_qs, create = Category.objects.get_or_create(name=category['name'])
            # check if category is create
            # format url
            url = category['url']+'/{}.json'
            page = 1
            max = False
            # read all products
            if qty == -1:
                qty = int(category['products'])

            # while max page doesn't reach
            while not max:
                request_url = url.format(str(page))
                # get json list from remote
                response = requests.get(request_url)
                json_object = response.json()

                # if no products exit loop
                if len(json_object['products']) == 0:
                    total_product += counter_p
                    counter_p = 0
                    max = True
                else:
                    for product in json_object['products']:
                        data = self.format_product(product)
                        counter_p += Product.add(data, category_qs)
                        if counter_p == qty and not read_all:
                            break
                    # change page
                    page += 1
                # if total product reached reset counter then exit loop
                if counter_p == qty and not read_all:
                    total_product += counter_p
                    counter_p = 0
                    # if update category and product reached inc category counter
                    if not create:
                        counter_c += 1
                    max = True
            # if new category inc counter
            if create:
                counter_c += 1
                # if total product not reached in a category reset anyway
                if counter_p < qty:
                    total_product += counter_p
                    counter_p = 0
            # if total category reached exit loop
            if counter_c == qtyc:
                break


        return 'Total entry : ' + str(counter_c * total_product)

        # create product by category

    def format_product(self, json):
        """ return a a dict of product field data
            Keyword arguments:
            json -- dict product data
        """
        return {
            'link': json.get('url'),
            'name': clear_string(json.get('product_name')),
            'nutri_code': json.get('nutrition_grade_fr'),
            'picture': json.get('image_front_url'),
            'fat': str_to_float(json.get('nutriments', {}).get('fat_100g', 'NA')),
            'saturated_fat': str_to_float(json.get('nutriments', {}).get('saturated-fat_100g', 'NA')),
            'sugars': str_to_float(json.get('nutriments', {}).get('sugars_100g', 'NA')),
            'salt': str_to_float(json.get('nutriments', {}).get('salt_100g', 'NA')),
        }

    def add_by_upload_file(self, qty):
        # total entry save
        entry = -1
        loop = 1
        if qty > 500:
            loop = math.floor(qty / 500)
            qty = 500

        # Read Csv file from url
        filename = os.path.join(BASE_DIR, 'product/uploads/food.csv')
        with open(filename, newline='', encoding='utf-8') as csvfile:
            # Associating header with value in a dictionary
            reader = csv.DictReader(csvfile, delimiter='\t')
            if qty == -1:
                qty = sum(1 for row in reader)

            # Max line to save
            save_qty = 0


            # Start loop to read each line
            for row in reader:
                # Create a list of food object for each line
                if row['product_name'] and row['code']:
                    # format product
                    self.add_product_list({
                        'link': row['url'],
                        'name': clear_string(row['product_name']),
                        # 'description': row['ingredients_text'],
                        'nutri_code': row['nutrition_grade_fr'],
                        'picture': row['image_url'],
                        'categories': self.categories.str_to_list(row['categories_fr']),
                        # 'shops': self.shops.str_to_list(row['stores']),

                        'fat': row['fat_100g'],
                        'saturated_fat': row['saturated-fat_100g'],
                        'sugars': row['sugars_100g'],
                        'salt': row['salt_100g'],
                    })

                    # add categories to object
                    self.categories.extract(row['categories_fr'])
                    # add shops to object
                    # self.shops.extract(row['stores'])
                    save_qty += 1
                    entry += 1
                    if loop > 0 and save_qty > qty+1:
                        # create all categories
                        self.categories.create_categories()

                        # create all shops
                        # self.shops.create_shops()

                        # create all product
                        self.create_products()
                        # reset data
                        save_qty = 0
                        loop -= 1
                        self.reset_components()

                    if loop == 1:
                        break

            if qty < 500:
                # create all categories
                self.categories.create_categories()

                # create all shops
                # self.shops.create_shops()

                # create all product
                self.create_products()
            return 'Total entry : '+ str(entry)

    def reset_components(self):
        # reset all components
        self.categories.reset()
        self.shops.reset()
        self.products = []

    def create_products(self):
        """ method create a list of product
            do before create_products():
            self.add_product_list()

            # add on by one entry
            self.categories.add_category_list()
            self.shops.add_shop_list()

            # create all categories / shops
            self.categories.create_categories()
            self.shops.create_shops()

        :return:
        """
        # create all product
        for p in self.products:

            # check if product exist in DB
            # product_qs = Product.objects.filter()
            product = dict(p)

            categories = product.get('categories')
            # shops =  product.get('shops')
            del product['categories']
            # del product['shops']

            product_qs, created = Product.objects.update_or_create(
                name=product.get('name'),
                defaults=product,
            )

            self.add_product_categories(product_qs, categories)
            # self.add_product_shops(product_qs, shops)

    def add_product_list(self, params):
        """add one element product  to list
           Keyword arguments:
           params -- dict key : name field, value : value of field
        """
        self.products.append(params)

    def add_product_categories(self, product, categories):
        """ add all product categories
            Keyword argument:
            product : qs product object
            categories : list category name
        """
        if categories:
            # list for bulk add
            objs = []
            # add product category
            for category in categories:
                category_qs = self.categories.get_category(category)
                if category_qs:
                    # if category exist test if relation already exist
                    qs = product.categories.filter(pk=category_qs.id)
                    if not qs.exists():
                        # if no relation add to list for bulk
                        objs.append(category_qs)
            if objs:
                # bulk add categories
                product.categories.add(*objs)

    def add_product_shops(self, product, shops):
        """ add all product shops
           Keyword argument:
           product : qs product object
           shops : list shop name
        """
        if shops :
            # list for bulk add
            objs = []
            # add product shop
            for shop in shops:
                shop_qs = self.shops.get_shop(shop)
                if shop_qs:
                    # if shop exist test if relation already exist
                    qs = product.shops.filter(pk=shop_qs.id)
                    if not qs.exists():
                        # if no relation add to list for bulk
                        objs.append(shop_qs)
            if objs:
                # bulk add shop
                product.shops.add(*objs)



class Product(models.Model):
    """ Product class
        :argument
        model : parent

    """

    # fields
    name = models.CharField(max_length=255, blank=False)
    # description = models.TextField()
    nutri_code = models.CharField(max_length=1, null=True)
    link = models.CharField(max_length=255, null=True)
    picture = models.URLField(max_length=255, null=True)
    """ image = models.ImageField(upload_to=upload_location,
                                null=True,
                                blank=True,
                                width_field="width_field",
                                height_field="height_field",
                                )
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)
    """
    create_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name='products', blank=True)

    # nutritional for 100g
    fat = models.DecimalField(max_digits=5, decimal_places=2, default=000.00)
    saturated_fat = models.DecimalField(max_digits=5, decimal_places=2, default=000.00)
    sugars = models.DecimalField(max_digits=5, decimal_places=2, default=000.00)
    salt = models.DecimalField(max_digits=5, decimal_places=2, default=000.00)


    objects = ManageDB()


    def __str__(self):
        return self.name

    @classmethod
    def add(cls, data, category):
        """ create or update product
            :argument
            data  : dict category params
            category : object category
        """
        product = dict(data)
        product_qs, created = Product.objects.update_or_create(
            name=product.get('name'),
            defaults=product,
        )
        # test if relation already exist
        qs = product_qs.categories.filter(pk=category.id)
        if not qs.exists():
            product_qs.categories.add(category)

        if created:
            return 1
        return 0