import re
import urllib
from django.template.loader import render_to_string



def pagination(object, page_per_view=3, params={}):
    """ return paginate view html
        :argument
        page_per_view : max page selection display
        params : dict options url : add + params on url

    """
    # create paginate view
    more = False
    min_page = 0
    max_page = 0

    page = object.number

    if object.paginator.num_pages < page_per_view:
        max_page = object.paginator.num_pages

    if object.paginator.num_pages > page_per_view:
        min_page = page - 2

        max_page = page + (page_per_view - 2)
        if min_page <= 0:
            min_page = 0
            max_page = max_page + 1

        if page == object.paginator.num_pages:
            min_page = page - page_per_view

        if max_page > object.paginator.num_pages:
            max_page = object.paginator.num_pages

        if max_page < object.paginator.num_pages:
            more = max_page + 1
            if more > object.paginator.num_pages:
                more = False
    url = ''
    if params and params['url']:
        for key, value in  params['url'].items():
           url += '&{}={}'.format(key, value)


    context = {
        'total_page': range(min_page, max_page),
        'more': more,
        'paginate': object.paginator.num_pages > 0,
        'object': object,
        'url':url
    }
    return render_to_string('partials/pagination.html', context)


def upload_openfoodfact_cvs():
    """ That function simply download csv file source to local """
    csv_uri = 'http://world.openfoodfacts.org/data/fr.openfoodfacts.org.products.csv'
    try:
        urllib.request.urlretrieve(csv_uri, './product/uploads/food.csv')
        return True
    except:
        raise ("Can't upload csv file!")

def upload_location(instance, filename):
    """ return upload format location"""
    return "%$/%s" %(instance.id, filename)

def clear_string(text):
    """ escape ' """
    # remove special char
    text = re.sub('r"[^a-zA-Z %., 0-9€_\-()@áàâäãåçéèêëíìîïñóòôöõúùûüýÿæœÁÀÂÄÃÅÇÉÈÊËÍÌÎÏÑÓÒÔÖÕÚÙÛÜÝŸÆŒ\'\"]"g', "", str(text))
    # remove extra space
    text = re.sub('r"\s+"g', " ", text)
    # remove "
    text = re.sub('r"[\"]"g', "'", text)
    # escape '
    text = re.sub('r"[\']"g', "\\'", text)
    return text



def str_to_float(s):
    try:
        return float(s)
    except ValueError:
        return float('0')

