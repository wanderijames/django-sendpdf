"""Sample View for the app"""
# pylint: disable=protected-access
from datetime import datetime
from collections import namedtuple
from django import http
from django.views.generic import View
from django.shortcuts import render
from . topdf import GeneratePDF, ShowPDF, DownloadPDF


def demo_data(qty=2000):
    """Generates data for demonstration purposes

    Args:
        qty (int): The number of rows for test data.

    Returns:
        dict: data containing the context data for the template"""
    headers = [
        "created",
        "direction",
        "reason",
        "transaction_value",
        "transaction_cost",
        "agent_balance"
    ]
    TransRecord = namedtuple("TransRecord", ",".join(headers))
    data = []
    for _ in range(qty):
        data_x_ = TransRecord._make(
            [str(datetime.now().strftime("%y.%m.%d %H:%M")),
             "debit",
             "top_up",
             "1000.00",
             "1000.00",
             "34343.00"
             ])
        data.append(data_x_)
    return {
        "headers": headers,
        "trans": data,
        "names": "John Doe",
        "account": "ACCTX00001",
        "balance": "KES 5454.50",
        "req_date": datetime.now().strftime("%y.%m.%d %H:%M"),
        "period": "1 Day"
    }


class ShowDemo(ShowPDF):
    """Demo for viewing a PDF document inline.

    Once installed and running go to
    `/sendpdf/show/ </sendpdf/show/>`_"""

    pdf_filename = "account_statement"
    pdf_template = "account_statement.html"
    context = demo_data()


class DownloadDemo(DownloadPDF):
    """Demo for downloading a PDF document.

    Once installed and running go to
    `/sendpdf/download </sendpdf/download/>`_"""
    pdf_filename = "account_statement"
    pdf_template = "account_statement.html"
    context = demo_data()


class SendDemo(View):
    """Demo for sending an email with the PDF attachement.

    Make sure you use a valid email addressing for testing.

    Once installed and running go to
    `/sendpdf/send/ </sendpdf/send/>`_"""

    def get(self, *args, **kwargs):
        """Sample view for sending an attachement via email"""
        # pylint: disable=unused-argument,no-self-use
        pdfgen = GeneratePDF(template="account_statement.html")
        pdfgen._make_pdf(ctxt=demo_data(20), filename="account_statement")
        email_ctx = {"name": "John Doe", "month": "April"}
        try:
            pdfgen.send_pdf(
                subject="Monthly statement",
                email_template="statement",
                ctxt=email_ctx,
                to_email=("john@doe.com",))
        except OSError as err:
            return http.HttpResponse("Email not sent: {}".format(err))

        return http.HttpResponse("Email sent")


class TemplateDesign(View):
    """HTML view for the demo template to be used for PDF generation

    Once installed and running go to
    `/sendpdf/ </sendpdf/>`_"""

    def get(self, request):
        """Sample view for displaying what can be generated"""
        params = demo_data(20)
        params["pdf"] = self.request.GET.get("pdf")
        return render(
            request, "sendpdf/docs/account_statement.html", params)
