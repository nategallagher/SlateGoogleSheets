from __future__ import print_function
import httplib2
from httplib2 import Http
import os
import os.path
import json
import datetime

from django.shortcuts import render, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect

from googlesheets.forms import ShipmentForm
from googlesheets.models import Shipment
from googlesheets.models import CredentialsModel
from slate import settings

from apiclient import discovery
from googleapiclient.discovery import build
import oauth2client
from oauth2client import file as oauth2client_file
from oauth2client import client
from oauth2client import tools as oauth2client_tools

from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets, OAuth2WebServerFlow
from oauth2client.contrib.django_orm import Storage

try:
    import argparse
    #flags = argparse.ArgumentParser(parents=[oauth2client_tools.argparser]).parse_args()
    flags = None
except ImportError:
    flags = None

import logging
log = logging.getLogger(__name__)

## warehouse management system software
## WMS
## MRP - Manufacturer Resource Planning


def index(request):
    max_number_of_shipments_to_show = 10
    latest_ship_list = Shipment.objects.all().order_by('-ship_date')[:max_number_of_shipments_to_show]
    return render_to_response('googlesheets/index.html', {'latest_ship_list': latest_ship_list})

def detail(request, ship_id):
    shipment_object = get_object_or_404(Shipment, pk=ship_id)
    return render_to_response('googlesheets/detail.html', {'shipment': shipment_object})

def results(request, ship_id):
    return HttpResponse("You're looking at the results of shipment %s." % ship_id)


APPLICATION_NAME = 'googlesheets'
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
API_KEY = 'AIzaSyB8TddSn7hnjsqxhn4qNL5JXiz_4GxLknY'
API = 'sheets'
API_VERSION = 'v4'
BASE = os.path.dirname(os.path.abspath(__file__))
#CLIENT_SECRET = os.path.join(BASE, "client_secret.json")
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secret.json')

#FLOW = flow_from_clientsecrets(
    #filename=CLIENT_SECRETS,
    #scope='https://www.googleapis.com/auth/spreadsheets',
    #redirect_uri='http://localhost:8000/oauth2callback')

FLOW = OAuth2WebServerFlow(
        client_id="414481533228-kif2tjf0k9q76dfke8n2l2i5ui9eeubf.apps.googleusercontent.com",
        client_secret="GwPe6Oj_WtoOCP2GBQBXV7IE",        
        scope='https://www.googleapis.com/auth/spreadsheets',
        redirect_uri='http://localhost:8000/oauth2callback',
    )


def get_sheetId_by_sheetLabel(service, spreadsheetId, sheetLabel): 
    # gets JSON object for entire spreadsheet
    # converted to dict of lists of dicts of lists, etc.
    # navigate through to get sheetId number

    sheetId = 0
    get_response = service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()

    for i, sheet in enumerate(get_response['sheets']):
        if(sheet['properties']['title'] == sheetLabel): 
            sheetId = sheet['properties']['sheetId']

    return sheetId

def get_firstEmptyRow(service, spreadsheetId, sheetLabel): 
    get_values = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=sheetLabel).execute()
    for i, val in enumerate(get_values['values']):
        if not val:
            return i+1
    return i+2

def submit_to_googlesheets(request,post_data): 
    log.debug("made it to submit_to_googlesheets")
    # search through validated posted data from form
    # convert any non-None, non-String value to a String
    for key, value in post_data.iteritems():
        if value is not None:
            if (key == 'state'):
                # if state object then submit the abbreviation for the state
                log.debug("state value type: ")
                log.debug(type(value))
                log.debug("state value.abbr type: ")
                log.debug(type(value.abbr))
                #post_data[key] = str(value)
            elif not isinstance(value, basestring):
                # if any other python object or int, etc. then convert to string for submission to spreadsheet 
                post_data[key] = str(value)


    storage = Storage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid == True:
        log.debug("submit_to_googlesheets: credential is None or credential.invalid == True")
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, request.user)
        authorize_url = FLOW.step1_get_authorize_url()

        return HttpResponseRedirect(authorize_url)

    else:
        log.debug("submit_to_googlesheets: else")
        http = httplib2.Http()
        http = credential.authorize(http)
        service = build(API, API_VERSION, http=http)
        
        spreadsheetId = '1j2_ZjzoMGzR2e6m-UbscK1xJiV58vX92rupEiRwQvD4'
        sheetId = get_sheetId_by_sheetLabel(service,spreadsheetId, 'Fulfillment Spreadsheet')
        rangeName = 'Fulfillment Spreadsheet!A2:E'

        current_row_num = get_firstEmptyRow(service, spreadsheetId, 'Fulfillment Spreadsheet')
        insert_row_data =   {
                                "requests": 
                                [
                                {
                                    "insertDimension": 
                                    {
                                        "range": 
                                        {
                                            "sheetId": sheetId,
                                            "dimension": "ROWS",
                                            "startIndex": "%d" % (current_row_num-1), 
                                            "endIndex": "%d" % (current_row_num)
                                        },
                                        "inheritFromBefore": True
                                    }
                                }
                                ]
                            }

        test_input_data =   {
                              "majorDimension": "ROWS",
                              "values": [
                                [
                                    "=COUNTIFS($D$3:$D$3022,$D%s)" % (current_row_num),     ## Units in Order   
                                    "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now()), ## Timestamp
                                    post_data['order_date'],            ## Date of Order
                                    post_data['order_number'],   ## Order Number
                                    post_data['dealer_name'],   ## Dealer Name
                                    post_data['customer_name'],   ## Customer Name
                                    post_data['street_address'],   ## Shipping Address
                                    post_data['city'],   ## City
                                    post_data['state'].abbr,   ## State
                                    post_data['zip'],   ## Zip
                                    post_data['country'],   ## Country
                                    post_data['customer_phone'],   ## Customer Phone
                                    post_data['customer_email'],   ## Customer Email
                                    post_data['sku_number'],   ## SKU
                                    post_data['model_type'],   ## Model
                                    post_data['item_condition'],   ## Item condition
                                    post_data['unit_number'],   ## Number of Units
                                    post_data['po_number'],   ## PO #
                                    post_data['slate_invoice_number'],   ## Slate Invoice #
                                    post_data['priority'],   ## Priority
                                    post_data['order_notes'],   ## Notes
                                    post_data['promised_date'],   ## Is there a promised date?
                                    post_data['ship_number'],   ## Ship Number - Sales
                                    "",   ## Proj. Ship Week
                                    "",   ## Proj. Ship Week Notes
                                    "",   ## Actual Ship Number
                                    post_data['billing_address'],   ## Billing address
                                    post_data['addtl_ship_info'],   ## Add additional shipping info if you like.
                                    post_data['addtl_notes'],   ## Additional notes
                                    post_data['warranty_date'],   ## Warranty Exp Date
                                    "",   ## Serial Number
                                    "",   ## Tracking
                                    "",   ## NAILED IT
                                    "",   ## OK to ship?
                                    '=if(AG%s="x",D%s,"")' % (current_row_num, current_row_num)     ## Order Counter Formula
                                ]
                              ],
                            }

        service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body=insert_row_data).execute()
        service.spreadsheets().values().append(spreadsheetId=spreadsheetId,
            range='Fulfillment Spreadsheet', body=test_input_data, valueInputOption='USER_ENTERED').execute()
        return None


@login_required
def entershipment(request):

    if request.POST:
        data_list = [
            'city',
            'state',
            'zip',
            'ship_date'
        ]
        form = ShipmentForm(request.POST)
        if form.is_valid():
            log.debug('ShipmentForm form: is_valid is True.')


            redirect_response = submit_to_googlesheets(request,form.cleaned_data)


            for key, value in request.POST.iteritems():
                try:
                    i = data_list.index(key)
                except:
                    i = 0
                debug_value = 'views.entershipment: POST data: %03d. %s => %s' % (i, key, value)
                log.debug(debug_value)
            form.save()

            if (redirect_response == None):
                return HttpResponseRedirect('/googlesheets/')
            else: 
                return redirect_response
                form = ShipmentForm()
                context = {
                    'form': form,
                    'user': request.user
                }
                template='googlesheets/entershipment.html'
                return render(request, template, context)
    else:
        form = ShipmentForm()
    context = {
        'form': form,
        'user': request.user
    }
    template='googlesheets/entershipment.html'
    return render(request, template, context)


@login_required
def auth_return(request):
    log.debug("made it to auth_return")
    if not xsrfutil.validate_token(settings.SECRET_KEY, request.REQUEST['state'], request.user):
        log.debug("auth_return: user: %s" % request.user)
        log.debug("auth_return: state: %s" % request.REQUEST['state'])
        log.debug("auth_return: SECRET_KEY: %s" % settings.SECRET_KEY)
        log.debug("auth_return: API_KEY: %s" % API_KEY)
        log.debug("auth_return: HttpResponseBadRequest")
        return  HttpResponseBadRequest()
    credential = FLOW.step2_exchange(request.REQUEST)
    storage = Storage(CredentialsModel, 'id', request.user, 'credential')
    storage.put(credential)
    log.debug("auth_return: credential", credential)
    log.debug("auth_return: HttpResponseRedirect")
    return None