from datetime import datetime
from collections import namedtuple
from django import http
from django.views.generic import View
from django.template import RequestContext
from django.shortcuts import render_to_response
from .topdf import GeneratePDF, ShowPDF, DownloadPDF


def demo_data(qty=2000):
    headers = ["created", "direction", "reason", "transaction_value", "transaction_cost", "agent_balance"]
    TransRecord = namedtuple("TransRecord", ",".join(headers))
    data = []
    for x in xrange(qty):
        data.append(TransRecord._make([str(datetime.now().strftime("%y.%m.%d %H:%M")), "debit", "top_up", "1000.00", "1000.00", "34343.00"]))
    return {"headers": headers, "trans": data}


class ShowDemo(ShowPDF):
    pdf_filename = "account_statement"
    pdf_template = "account_statement.html"
    context = demo_data()


class DownloadDemo(DownloadPDF):
    pdf_filename = "account_statement"
    pdf_template = "account_statement.html"


class SendDemo(View):

    def get(self, *args, **kwargs):
        s = GeneratePDF(template="account_statement.html")
        s._make_pdf(ctxt=demo_data(20), filename="account_statement")
        email_ctx = {"name": "James Wanderi", "month": "April"}
        s.send_pdf(subject="Monthly statement", email_template="statement", ctxt=email_ctx, to=("wanderi@wanderi.me",))
        return http.HttpResponse("Email sent")


class TemplateDesign(View):
    def get(self, request):
        params = demo_data(20)
        params["pdf"] = self.request.GET.get("pdf")
        return render_to_response("sendpdf/docs/account_statement.html", RequestContext(request, params))
