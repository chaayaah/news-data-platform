from etl.services.preprocessors.vendor.base import VendorPreprocessor


class PackReportPreprocessor(VendorPreprocessor):

    def process(self, root):

        print("Running PackReport Preprocessor...")

        return root