from etl.services.preprocessors.vendor.base import VendorPreprocessor

from etl.services.preprocessors.vendor.reuters import ReutersPreprocessor
from etl.services.preprocessors.vendor.bloomberg import BloombergPreprocessor
from etl.services.preprocessors.vendor.businessdesk import BusinessDeskPreprocessor
from etl.services.preprocessors.vendor.packreport import PackReportPreprocessor


class VendorPreprocessorFactory:

    @staticmethod
    def get_preprocessor(vendor):

        preprocessors = {

            "Reuters": ReutersPreprocessor(),

            "Bloomberg": BloombergPreprocessor(),

            "BusinessDesk": BusinessDeskPreprocessor(),

            "PackReport": PackReportPreprocessor()

        }

        return preprocessors.get(
            vendor,
            VendorPreprocessor()
        )