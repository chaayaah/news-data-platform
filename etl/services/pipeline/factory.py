from etl.services.pipeline.stages import (
    PreGenericStage,
    VendorPreprocessorStage,
    ParserStage,
    PostGenericStage,
    ValidatorStage,
)


class PipelineFactory:

    @classmethod
    def build_pipeline(cls, stage_names, stages):

        from etl.services.pipeline.pipeline import Pipeline

        pipeline = Pipeline()

        for stage_name in stage_names:

            stage = stages.get(stage_name)

            if stage is None:
                raise ValueError(
                    f"Unknown pipeline stage: {stage_name}"
                )

            pipeline.add_stage(stage)

        return pipeline