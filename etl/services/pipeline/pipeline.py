from .context import PipelineContext


class Pipeline:

    def __init__(self):
        self.stages = []

    def add_stage(self, stage):
        self.stages.append(stage)

    def run(self, context: PipelineContext):

        for stage in self.stages:
            context = stage.run(context)

        return context