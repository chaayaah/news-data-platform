from etl.services.pipeline.stages import (
    PreGenericStage,
    VendorPreprocessorStage,
    ParserStage,
    PostGenericStage,
    ValidatorStage,
)


class PipelineFactory:

    STAGES = {
        "pre_generic": PreGenericStage,
        "vendor_preprocessor": VendorPreprocessorStage,
        "parser": ParserStage,
        "post_generic": PostGenericStage,
        "validator": ValidatorStage,
    }

    @classmethod
    def build_pipeline(cls, stage_names, rules):

        from etl.services.pipeline.pipeline import Pipeline

        pipeline = Pipeline()

        for stage_name in stage_names:

            stage_class = cls.STAGES.get(stage_name)

            if stage_class is None:
                raise ValueError(f"Unknown pipeline stage: {stage_name}")

            if stage_name == "validator":
                pipeline.add_stage(stage_class(rules))
            else:
                pipeline.add_stage(stage_class())

        return pipeline