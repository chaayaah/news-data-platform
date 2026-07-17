from .stage import PipelineStage

from etl.services.preprocessors.pre_generic import PreGeneric
from etl.services.preprocessors.post_generic import PostGeneric
from etl.services.preprocessors.vendor.factory import VendorPreprocessorFactory
from etl.services.xml_parser import XMLParser
from etl.services.validator import Validator


class PreGenericStage(PipelineStage):

    def __init__(self):
        self.processor = PreGeneric()

    def run(self, context):

        print("Running Pre Generic...")

        context.root = self.processor.process(context.root)

        return context


class VendorPreprocessorStage(PipelineStage):

    def run(self, context):

        processor = VendorPreprocessorFactory.get_preprocessor(
            context.vendor
        )

        context.root = processor.process(context.root)

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

        processed = []

        for record in context.records:
            processed.append(
                self.processor.process(record)
            )

        context.records = processed

        return context


class ValidatorStage(PipelineStage):

    def __init__(self, rules):
        self.validator = Validator(rules)

    def run(self, context):

        context.valid_records = []
        context.invalid_records = []

        for record in context.records:

            errors = self.validator.validate(record)

            if errors:

                context.invalid_records.append({
                    "record": record,
                    "errors": errors
                })

            else:

                context.valid_records.append(record)

        return context