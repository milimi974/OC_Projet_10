 import argparse

from django.core.management.base import BaseCommand, CommandError
from product.models import Product

class Command(BaseCommand):
    help = 'Update database'

    def add_arguments(self, parser):
        parser.add_argument('--product',  type=int)
        parser.add_argument('--category',  type=int)
        parser.add_argument('--upload',  type=self.str2bool)
        parser.add_argument('--api',  type=self.str2bool)

    def handle(self, *args, **options):
        return Product.objects.update_db(qty=options['product'], qtyc=options['category'],upload=options['upload'], api=options['api'])

    def str2bool(self, v):
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')
