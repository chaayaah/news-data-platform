import time

from etl.services.logger import Logger


class Pipeline:

    def __init__(self):

        self.logger = Logger.get_logger()
        self.stages = []

    def add_stage(self, stage):

        self.stages.append(stage)

    def run(self, context):

        self.logger.info("Pipeline Started")

        pipeline_start = time.perf_counter()

        for stage in self.stages:

            stage_name = stage.__class__.__name__

            try:

                self.logger.info(f"Starting {stage_name}")

                start = time.perf_counter()

                context = stage.run(context)

                elapsed = time.perf_counter() - start

                self.logger.info(
                    f"Finished {stage_name} ({elapsed:.4f} sec)"
                )

            except Exception as e:

                context.failed_stage = stage_name
                context.error = str(e)

                self.logger.exception(
                    f"{stage_name} failed"
                )

                break

        total = time.perf_counter() - pipeline_start

        self.logger.info("========== Pipeline Summary ==========")
        self.logger.info(
            f"Files Processed : {context.metrics['files_processed']}"
        )
        self.logger.info(
            f"Records Processed : {context.metrics['records_processed']}"
        )
        self.logger.info(
            f"Valid Records : {context.metrics['valid_records']}"
        )
        self.logger.info(
            f"Invalid Records : {context.metrics['invalid_records']}"
        )
        self.logger.info(f"Elapsed : {total:.4f} sec")

        if context.failed_stage:
            self.logger.error(
                f"Pipeline Failed at {context.failed_stage}"
            )
            self.logger.error(
                f"Reason: {context.error}"
            )
        else:
            self.logger.info("Pipeline Finished Successfully")

        return context