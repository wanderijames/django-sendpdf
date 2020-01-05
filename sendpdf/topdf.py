"""TO PDF helpers"""
from io import StringIO
from django import http
from django.conf import settings
from django.views.generic import View
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.views.generic.base import TemplateResponseMixin
import pdfkit

# settings.configure() #: I use this during sphinx document generation

WKTHMLTOPDF_PATH = getattr(
    settings, "WKTHMLTOPDF_PATH", "/usr/local/bin/wkhtmltox/bin/wkhtmltopdf")
PDFKIT_CONFIG = pdfkit.configuration(wkhtmltopdf=WKTHMLTOPDF_PATH)

# pylint: disable=too-many-arguments
# pylint:disable=protected-access


class GeneratePDF:
    """PDF generator"""

    data = []
    pdf_options = {"quiet": ""}
    connection = None
    pdf = None
    filename = None

    def __init__(self, template="account_statement.html"):
        self.template = get_template("sendpdf/docs/{}".format(template))

    def _make_pdf(self, ctxt, filename="page"):
        self.filename = filename
        html = self.template.render(ctxt)
        self.pdf = pdfkit.from_file(
            StringIO(html),
            False, options=self.pdf_options, configuration=PDFKIT_CONFIG)
        return self.pdf

    def download(self):
        """download the PDF document generated"""
        response = http.HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = \
            'attachment; filename="{}.pdf"'.format(self.filename)
        response.write(self.pdf)
        return response

    def inline(self):
        """view the in the browser"""
        response = http.HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = \
            'inline; filename="{}.pdf"'.format(self.filename)
        response.write(self.pdf)
        return response

    def send_pdf(
            self,
            subject,
            email_template,
            ctxt,
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL"),
            to_email=("valid_email",),
            **kwargs):
        """Send the PDF to one or more email addresses.

        This method is compliant with the Django's EmailMultiAlternatives.

        This means that `**kwargs` can define the following::
           bcc - which is `bcc = None` by default

           cc - which is `cc = None` by default

           reply_to - which is `reply_to = None` by default

           headers - which is `headers = None` by default

           connection - which is `connection = None` by default

        It is advisable that you set up SMTP settings for an outbound email.

        Args:
           subject (str) - Subject of the email you want to send.

           email_template (str) - The html template that can be access by
           DJango template engine.

           ctxt (dict or Django context object) - Data that is to be populated
           in the `email_template`.

           from_email (Optional[str]) - A valid email address that is allowed
           to send email.
           By default it is defined at the Django settins `DEFAULT_FROM_EMAIL`.

           to_email (tuple) - A tuple of the recipients' email addresses.

        Examples:
           Suppose you want to send generated PDF to `john@doe.com`::
                >>> from django.views.generic import View
                >>> from sendpdf.topdf import GeneratePDF
                >>> class SendDemo(View):
                        def get(self, *args, **kwargs):
                            s = GeneratePDF(template="account_statement.html")
                            s._make_pdf(
                                ctxt=demo_data(20),
                                filename="account_statement")
                            email_ctx = {"name": "John Doe", "month": "April"}
                            s.send_pdf(
                                subject="Monthly statement",
                                email_template="statement",
                                ctxt=email_ctx,
                                to_email=("john@doe.com",))
                            return http.HttpResponse("Email sent")


        """
        message_text = get_template(
            "sendpdf/email/{}.txt".format(email_template)).render(ctxt)
        email_message = EmailMultiAlternatives(
            subject, message_text, from_email, to_email, **kwargs)

        try:
            message_html = get_template(
                "sendpdf/email/{}.html".format(email_template)).render(ctxt)
            email_message.attach_alternative(message_html, 'text/html')
        except TemplateDoesNotExist:
            pass

        email_message.attach(
            filename="{}.pdf".format(self.filename),
            content=self.pdf,
            mimetype="application/pdf")
        email_message.send()


class PDFResponseMixin(TemplateResponseMixin):
    """The base view for PDF generation and view.

    The childs of this object should define a get method,
    assign the following values::
        `pdf_filename` (str) - name of the PDF file to be generated

        `pdf_template` (str) - location of the html template to be
        used for generation of the `pdf_filename`.pdf

        `context` (dict) - The context data to be passed by
        Django template engine to `pdf_template`

    Examples:
        Suppose we want to create a view for viewing PDF document inline::
            >>> from django.views.generic import View
            >>> from sendpdf.topdf import PDFResponseMixin
            >>> class DownloadPDF(PDFResponseMixin, View):
                    pdf_filename = "account_statement"
                    pdf_template = "account_statement.html"
                    context = demo_data()
                    def get(self, request, *args, **kwargs):
                        self.get_pdf()
                        return self.pdfgen.inline()
    """
    pdf_filename = None
    pdf_template = None
    context = {}
    pdfgen = None
    pdf = None

    def get_pdfgen(self):
        """Construct pdf maker"""
        if self.pdfgen is not None:
            return self.pdfgen
        self.pdfgen = GeneratePDF(self.pdf_template)
        return self.pdfgen

    def get_pdf(self):
        """Construct pdf"""
        if self.pdf is not None:
            return self.pdf
        pdfg = self.get_pdfgen()
        self.pdf = pdfg._make_pdf(self.context, self.pdf_filename)
        return self.pdf


class DownloadPDF(PDFResponseMixin, View):
    """The base view for PDF generation and downloading.

    The childs of this object should assign the following values::

        `pdf_filename` (str) - name of the PDF file to be generated

        `pdf_template` (str) - location of the html template to be used
        for generation the `pdf_filename`.pdf

        `context` (dict) - The context data to be passed by
        Django template engine to `pdf_template`

    Examples:
        Suppose we want to create a view for viewing PDF document inline::
            >>> from sendpdf.topdf import DownloadPDF
            >>> class DownloadDemo(DownloadPDF):
                    pdf_filename = "account_statement"
                    pdf_template = "account_statement.html"
                    context = demo_data()
    """
    def get(self, request, *args, **kwargs):
        """Sample view for downloading PDF"""
        # pylint: disable=unused-argument
        self.get_pdf()
        return self.pdfgen.download()


class ShowPDF(PDFResponseMixin, View):
    """The base view for PDF generation and downloading.

    The childs of this object should assign the following values::

        `pdf_filename` (str) - name of the PDF file to be generated

        `pdf_template` (str) - location of the html template to be used
        for generation the `pdf_filename`.pdf

        `context` (dict) - The context data to be passed by
        Django template engine to `pdf_template`

    Examples:
        Suppose we want to create a view for viewing PDF document inline::
            >>> from sendpdf.topdf import ShowPDF
            >>> class ShowDemo(ShowPDF):
                    pdf_filename = "account_statement"
                    pdf_template = "account_statement.html"
                    context = demo_data()
    """
    def get(self, request, *args, **kwargs):
        """Sample pdf for showing PDF"""
        # pylint: disable=unused-argument
        self.get_pdf()
        return self.pdfgen.inline()
