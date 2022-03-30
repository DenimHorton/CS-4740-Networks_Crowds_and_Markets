class EndPointWorker:
    '''
    '''
    def __init__(self, end_point):
        self.end_point = end_point 
        self.worker_thread = None
        self.running = False

    def start(self):
        self._log('Started thread')
