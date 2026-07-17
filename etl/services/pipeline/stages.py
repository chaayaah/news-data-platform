from etl.services.preprocessors.pre_generic import PreGeneric
from etl.services.preprocessors.post_generic import PostGeneric

from etl.services.preprocessors.vendor.factory import VendorPreprocessorFactory

from etl.services.xml_parser import XMLParser
from etl.services.validator import Validator

from etl.services.pipeline.stage import PipelineStage
from etl.services.logger import Logger

logger = Logger.get_logger()


class PreGenericStage(PipelineStage):

    def __init__(self):
        self.processor = PreGeneric()

    def run(self, context):

        context.root = self.processor.process(context.root)

        return context


class VendorPreprocessorStage(PipelineStage):

    def run(self, context):

        preprocessor = VendorPreprocessorFactory.get_preprocessor(
            context.vendor
        )

        context.root = preprocessor.process(
            context.root
        )

        return context


class ParserStage(PipelineStage):

    def __init__(self):
        self.parser = XMLParser()

    def run(self, context):

        context.records = self.parser.parse(
            context.root,
            context.mapping
        )

        return context


class PostGenericStage(PipelineStage):

    def __init__(self):
        self.processor = PostGeneric()

    def run(self, context):

        context.records = self.processor.process(
            context.records
        )

        return context


class ValidatorStage(PipelineStage):

    def __init__(self, rules):

        self.validator = Validator(rules)

    def run(self, context):

        context.valid_records, context.invalid_records = (
            self.validator.validate(context.records)
        )

        # Pipeline metrics
        context.metrics["files_processed"] = 1
        context.metrics["records_processed"] = len(context.records)
        context.metrics["valid_records"] = len(context.valid_records)
        context.metrics["invalid_records"] = len(context.invalid_records)

        return context