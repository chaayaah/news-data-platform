from etl.services.mapping_loader import MappingLoader
from etl.services.validator import Validator
from etl.services.config import Config

from etl.services.pipeline.stages import (
    PreGenericStage,
    VendorPreprocessorStage,
    ParserStage,
    PostGenericStage,
    ValidatorStage,
)


class ServiceContainer:

    def __init__(self):

        rules = Config.load("validation.json")

        self.mapping_loader = MappingLoader()

        self.validator = Validator(rules)

        self.stages = {
            "pre_generic": PreGenericStage(),
            "vendor_preprocessor": VendorPreprocessorStage(),
            "parser": ParserStage(),
            "post_generic": PostGenericStage(),
            "validator": ValidatorStage(
                self.validator
            ),
        }