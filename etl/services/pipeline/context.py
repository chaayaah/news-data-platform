class PipelineContext:
    """
    Shared object passed through every pipeline stage.
    """

    def __init__(self):
        # General
        self.vendor = None
        self.mapping = None

        # XML
        self.root = None

        # Parsed records
        self.records = []

        # Validation
        self.valid_records = []
        self.invalid_records = []

        # Metadata
        self.metadata = {}