from etl.services.preprocessors.vendor.base import VendorPreprocessor


class BloombergPreprocessor(VendorPreprocessor):

    def process(self, root):

        print("Running Bloomberg Preprocessor...")

        return root