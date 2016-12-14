from datetime import datetime
from collections import namedtuple
from django import http
from django.views.generic import View
from django.template import RequestContext
from django.shortcuts import render_to_response
from topdf import GeneratePDF, ShowPDF, DownloadPDF


def demo_data(qty=2000):
    """Generates data for demonstration purposes

    Args:
        qty (int): The number of rows for test data.

    Returns:
        dict: data containing the context data for the template"""
    headers = ["created", "direction", "reason",
               "transaction_value", "transaction_cost", "agent_balance"]
    TransRecord = namedtuple("TransRecord", ",".join(headers))
    data = []
    for x in xrange(qty):
        data.append(TransRecord._make([str(datetime.now().strftime(
            "%y.%m.%d %H:%M")), "debit", "top_up", "1000.00", "1000.00", "34343.00"]))
    return {"headers": headers, "trans": data, "names": "John Doe", "account": "ACCTX00001", "balance": "KES 5454.50",
            "req_date": datetime.now().strftime("%y.%m.%d %H:%M"), "period": "1 Day"}


class ShowDemo(ShowPDF):
    """Demo for viewing a PDF document inline.

    Once installed and running go to `http://127.0.0.1:8000/sendpdf/show/ <http://127.0.0.1:8000/sendpdf/show/>`_"""

    pdf_filename = "account_statement"
    pdf_template = "account_statement.html"
    context = demo_data()


class DownloadDemo(DownloadPDF):
    """Demo for downloading a PDF document.

    Once installed and running go to `http://127.0.0.1:8000/sendpdf/download <http://127.0.0.1:8000/sendpdf/download/>`_"""
    
    pdf_filename = "account_statement"
    pdf_template = "account_statement.html"


class SendDemo(View):
    """Demo for sending an email with the PDF attachement.

    Make sure you use a valid email addressing for testing.

    Once installed and running go to `http://127.0.0.1:8000/sendpdf/send/ <http://127.0.0.1:8000/sendpdf/send/>`_"""

    def get(self, *args, **kwargs):
        s = GeneratePDF(template="account_statement.html")
        s._make_pdf(ctxt=demo_data(20), filename="account_statement")
        email_ctx = {"name": "John Doe", "month": "April"}
        s.send_pdf(subject="Monthly statement", email_template="statement",
                   ctxt=email_ctx, to=("john@doe.com",))
        return http.HttpResponse("Email sent")


class TemplateDesign(View):
    """HTML view for the demo template to be used for PDF generation

    Once installed and running go to `http://127.0.0.1:8000/sendpdf/ <http://127.0.0.1:8000/sendpdf/>`_"""

    def get(self, request):
        params = demo_data(20)
        params["pdf"] = self.request.GET.get("pdf")
        return render_to_response("sendpdf/docs/account_statement.html", RequestContext(request, params))
