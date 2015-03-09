# django-fast-sync
A Django app which helps you to import a lot of data with raw SQL

```
Important: This library only supports Postgres (common for Django projects)!
```

# Example

Let's say you have this model in the app 'booking':

```
class Category(models.Model):
  category_id = models.IntegerField()
  name = models.CharField(max_length=255)
```

and you want to import about 1000000 categories fast.
You get a list of dictionaries from you REST API or different database which looks like this:

```
[
  {
    'category_id': 2,
    'name': 'light'
  },
  {
    'category_id': 3,
    'name': 'heavy'
  },
  ...
]
```

Then you can import my package and just use:
```
from django_fast_sync.fast_sync import FastSync

fast_sync = FastSync(my_data_list, 'category_id', 'booking_category')
# FastSync(list_of_data, primary_field_name, table_name)
and then run
fast_sync.start_sync()
```

Note: You can also do it in a transaction (which makes it more faster)

```
from django.db.transaction import *

from django_fast_sync.fast_sync import FastSync

fast_sync = FastSync(my_data_list, 'category_id', 'booking_category')
# FastSync(list_of_data, primary_field_name, table_name)
and then run
set_autocommit(False)
fast_sync.start_sync()
commit()
set_autocommit(True)
```
