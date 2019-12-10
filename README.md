#ZFC Web#

ZFC Web is a Django app to conduct Web-based interface for CRISPR screening analysis algorithm [ZFC](https://github.com/wolfsonliu/zfc/).

##Quick start##

1. Add "zfc" to your INSTALLED_APPS setting like this::

```
INSTALLED_APPS = [
    ...
    'zfc',
]
```

2. Include the polls URLconf in your project urls.py like this::

```
path('zfc/', include('zfc.urls')),
```

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/.

