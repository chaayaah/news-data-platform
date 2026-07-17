class PipelineStage:
    """
    Base class for all pipeline stages.
    """

    def run(self, context):
        raise NotImplementedError(
            "Pipeline stages must implement run()."
        )