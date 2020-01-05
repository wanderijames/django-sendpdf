========
Sendpdf
========

Sendpdf is a simple Django app that can be used to generate PDF documents from html templates.

It can handle images and css very well. The generated PDF can then be displayed in the browser for printing and saving.

Alternatively, one can send the PDF to one or many email addresses.

It has been tested with Django==1.9.

Detailed documentation is in the `official page <http://django-sendpdf.readthedocs.io/en/latest>`_.

Quick start
--------------

1. Install django-sendpdf:

.. code-block:: bash

  $ pip install django-sendpdf

2. Install wkhtmltopdf:

* Debian/Ubuntu:

.. code-block:: bash

  $ sudo apt-get install wkhtmltopdf

**Warning!** Version in debian/ubuntu repos have reduced functionality (because it compiled without the wkhtmltopdf QT patches), such as adding outlines, headers, footers, TOC etc. To use this options you should install static binary from `wkhtmltopdf <http://wkhtmltopdf.org/>`_ site or you can use `this script <https://github.com/JazzCore/python-pdfkit/blob/master/travis/before-script.sh>`_.

* Windows and other options: check wkhtmltopdf `homepage <http://wkhtmltopdf.org/>`_ for binary installers


3. Add "sendpdf" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'sendpdf',
    )

4. In your Django settings add the location of wkhtmltopdf, default location is **/usr/local/bin/wkhtmltox/bin/wkhtmltopdf**, like this::

    WKTHMLTOPDF_PATH = "/usr/local/bin/wkhtmltopdf"

4. Include the sendpdf URLconf in your project urls.py like this::

    path(r'^sendpdf/', include('sendpdf.urls', namespace='sendpdf')),

5. Run `python manage.py runserver` to see some demos:

    `Template example <http://127.0.0.1:8000/sendpdf/>`_

    `View PDF inline <http://127.0.0.1:8000/sendpdf/show/>`_

    `Dewnload PDF <http://127.0.0.1:8000/sendpdf/download/>`_

    `Send PDF <http://127.0.0.1:8000/sendpdf/send/>`_
