class Adapter:
	"""
	A generic class for a chainlink external adapter. Encapsulates parsing the POST 
	request, generating errors, and serializing API responses. Need to fill out the
	request_data to integrate with an external API. 
	"""	
	def __init__(self, post_data):
		self.post_data = post_data.get('data')
		self.id = post_data.get('id', '1')
		if self.id is None:
			self.result_error("No id provided")
		else:
			self.request_data()
	
	def request_data(self):
		"""
		Main method for class: where the API is encapsulated.
		Behavior: 
		- makes API call based on request_data.
		- if error: call result_error with appropriate error message.
		- else: call result_success with response data.
		"""
		pass		

	def result_success(self, api_data):
		self.result = {
			'jobRunID': self.id,
			'data': api_data,
			'status': 'success',
			'statusCode': 200,
		}

	def result_error(self, error):
		self.result = {
			'jobRunID': self.id,
			'error': f'There was an error: {error}',
			'status': 'errored',
			'statusCode': 400,
		}

from rfid import RFID
import random

class RFIDAdapter(Adapter):
    DEFAULT_TIMEOUT = 20
    VIRTUAL = True # flag to set when not using a real hardware backend
    VIRTUAL_UIDS = ["F6F8622E", "DEADBEEF", "12345678"]

    def __init__(self, input):
        Adapter.__init__(self, input)
        # sets the rfid interface
        if not self.VIRTUAL:
            self.set_timeout()
            self.rfid = RFID(self.timeout)

    def set_timeout(self):
        # try to get the timeout param
        if self.request_data:
            timeout = self.request_data.get("timeout")
            if timeout is not None:
                self.timeout = timeout
                return
        # otherwise set default
        self.timeout = self.DEFAULT_TIMEOUT

    def request_data(self):
        if not self.VIRTUAL:
            try:
                # runs the rfid scanner
                res = self.rfid.run_scanner()
                if res:
                    # means there was a scan
                    self.result_success({"uid": res})
                else:
                    self.result_error("Timeout")
            except:
                res = self.result_error('No scanner found')
        else:
            # if virtual, just return an arbitrary UID
            self.result_success({"uid": random.choice(self.VIRTUAL_UIDS)})