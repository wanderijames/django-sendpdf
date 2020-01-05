from django.test import TestCase
from topdf import GeneratePDF


class SendpdfTestCase(TestCase):

    def test_pdf_generatable(self):

        gen = GeneratePDF()
        gen._make_pdf({})
        self.assertEqual('Able', 'Able')
