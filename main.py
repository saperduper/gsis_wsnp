from google.appengine.ext.webapp import template
from suds.client import Client
from webapp2 import RequestHandler, WSGIApplication
from xml.etree import cElementTree
from xml2Dict.xml2Dict import XmlDictConfig
import os

WSDL_URL = 'https://www1.gsis.gr/wsgsis/RgWsBasStoixN/RgWsBasStoixNSoapHttpPort?wsdl'
SERVICE_URL = 'https://www1.gsis.gr/wsgsis/RgWsBasStoixN/RgWsBasStoixNSoapHttpPort'
NULL = "{'{http://www.w3.org/2001/XMLSchema-instance}nil': '1'}"
RgWsBasStoixNRtUser_TYPE = 'ns0:RgWsBasStoixNRtUser'
GenWsErrorRtUser_TYPE = 'ns0:GenWsErrorRtUser'

class AfmHandler(RequestHandler):
    def get(self, afm):
        client = Client(url = WSDL_URL, location = SERVICE_URL, retxml = True)
        # prepare the request
        pBasStoixNRec_out = client.factory.create(RgWsBasStoixNRtUser_TYPE)
        pBasStoixNRec_out.afm = ' '
        pErrorRec_out = client.factory.create(GenWsErrorRtUser_TYPE)
        pErrorRec_out.errorDescr = ' '
        pErrorRec_out.errorCode = ' '
        # call the service
        reply = client.service.rgWsBasStoixN(pAfm = afm,
                                            pBasStoixNRec_out = pBasStoixNRec_out,
                                            pCallSeqId_out = 0,
                                            pErrorRec_out = pErrorRec_out)
        # reply as xml
        xml = cElementTree.XML(reply)
        # xml -> dict
        dictionary = XmlDictConfig(xml)
        # check for errors
        error = dictionary.get('Body').get('rgWsBasStoixNResponse').get('pErrorRec_out')
        error_desc = error.get('errorDescr')

        # in case of no errors, error_desc is dict
        if type(error_desc) is unicode:
            template_values = {
                'error_message': error_desc
            }
            path = os.path.join(os.path.dirname(__file__), 'templates/error.html')
        else:
            # fetch the details
            details = dictionary.get('Body').get('rgWsBasStoixNResponse').get('pBasStoixNRec_out')
            template_values = {
                'name': details.get('onomasia'),
                'address': details.get('postalAddress'),
                'city': details.get('parDescription'),
                'number': details.get('postalAddressNo'),
                'tk': details.get('postalZipCode'),
                'telephone': details.get('firmPhone'),
                'fax': details.get('firmFax'),
                'afm': details.get('afm'),
                'doy': details.get('doy'),
                'doyDescr': details.get('doyDescr')
            }
            path = os.path.join(os.path.dirname(__file__), 'templates/result.html')

        content = template.render(path, template_values)
        self.response.out.write(str(content.encode('utf-8')))

app = WSGIApplication([
    (r'/(\d{9})', AfmHandler),
])

def main():
    app.run()

if __name__ == '__main__':
    main()
