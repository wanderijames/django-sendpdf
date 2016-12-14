.. _getting_started:


***************
Getting started
***************

.. _introduction:

Introduction
============

As a developer I have had problems in PDF generation in the past, and I thought someone out there needs a helping hand.

Sendpdf is an app that enables you to generate PDF documents from predefined html templates. Design your PDF with the tools that we all love and know how to use perfectly well: HTML and CSS.

.. _installing_app:

Intalling Django-sendpdf
========================

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

4. In your Django settings add the location of wkhtmltopdf, if you download the binary or follow the above guide then the location would be '/usr/local/bin/wkhtmltox/bin/wkhtmltopdf' which you don't have to define its PATH explicitly as below, like this::

    WKTHMLTOPDF_PATH = "wkhtmltopdf/path/here"

4. Include the sendpdf URLconf in your project urls.py like this::

    url(r'^sendpdf/', include('sendpdf.urls', namespace='sendpdf')),


5. Test if the app can run without any errors::

    python manage.py test sendpdf


.. _pdfgenerator:

sendpdf.topdf.py
=================

.. automodule:: sendpdf.sendpdf.topdf
    :members:

.. _views:

sendpdf.views.py
================

.. automodule:: sendpdf.sendpdf.views
    :members:



