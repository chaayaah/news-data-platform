class PipelineContext:

    def __init__(self):

        self.vendor = None
        self.mapping = None
        self.root = None

        self.records = []
        self.valid_records = []
        self.invalid_records = []

        self.metadata = {}

        self.metrics = {
            "files_processed": 0,
            "records_processed": 0,
            "valid_records": 0,
            "invalid_records": 0,
        }

        self.failed_stage = None
        self.error = None