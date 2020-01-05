from django.test import TestCase
from sendpdf.topdf import GeneratePDF


class SendpdfTestCase(TestCase):

    def test_pdf_generatable(self):

        gen = GeneratePDF()
        gen._make_pdf({})
