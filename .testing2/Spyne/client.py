import logging
from suds.client import Client as SudsClient

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)

url = 'http://167.205.35.227:5000/test?wsdl'
client = SudsClient(url=url)
r = client.service.test("what")
print r