import StringIO
from django import http
from django.conf import settings
from django.views.generic import View
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.views.generic.base import TemplateResponseMixin
import pdfkit

path_wkthmltopdf = getattr(
    settings, "WKTHMLTOPDF_PATH", "/usr/local/bin/wkhtmltox/bin/wkhtmltopdf")
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)


class GeneratePDF:

    data = []
    pdf_options = {"quiet": ""}
    connection = None
    pdf = None
    filename = None

    def __init__(self, template="statement.html"):
        self.template = get_template("sendpdf/docs/{}".format(template))

    def _make_pdf(self, ctxt, filename="page"):
        self.filename = filename
        html = self.template.render(ctxt)
        self.pdf = pdfkit.from_file(
            StringIO.StringIO(html.encode("UTF-8")), False, options=self.pdf_options, configuration=config)
        return self.pdf

    def download(self):
        response = http.HttpResponse(content_type='application/pdf')
        response[
            'Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(self.filename)
        response.write(self.pdf)
        return response

    def inline(self):
        response = http.HttpResponse(content_type='application/pdf')
        response[
            'Content-Disposition'] = 'inline; filename="{}.pdf"'.format(self.filename)
        response.write(self.pdf)
        return response

    def send_pdf(self, subject, email_template, ctxt, from_email=settings.DEFAULT_FROM_EMAIL,
                 to=("wanderi@wanderi.me",), **kwargs):
        message_text = get_template(
            "sendpdf/email/{}.txt".format(email_template)).render(ctxt)
        email_message = EmailMultiAlternatives(
            subject, message_text, from_email, to, **kwargs)

        try:
            message_html = get_template(
                "sendpdf/email/{}.html".format(email_template)).render(ctxt)
            email_message.attach_alternative(message_html, 'text/html')
        except TemplateDoesNotExist:
            pass

        email_message.attach(
            filename="{}.pdf".format(self.filename), content=self.pdf, mimetype="application/pdf")
        email_message.send()


class PDFResponseMixin(TemplateResponseMixin):
    pdf_filename = None
    pdf_template = None
    context = {}
    pdfgen = None
    pdf = None

    def get_pdfgen(self):
        if self.pdfgen is not None:
            return self.pdfgen
        self.pdfgen = GeneratePDF(self.pdf_template)
        return self.pdfgen

    def get_pdf(self):
        if self.pdf is not None:
            return self.pdf
        pdfg = self.get_pdfgen()
        self.pdf = pdfg._make_pdf(self.context, self.pdf_filename)
        return self.pdf


class DownloadPDF(PDFResponseMixin, View):
    def get(self, request, *args, **kwargs):
        self.get_pdf()
        return self.pdfgen.download()


class ShowPDF(PDFResponseMixin, View):
    def get(self, request, *args, **kwargs):
        self.get_pdf()
        return self.pdfgen.inline()
