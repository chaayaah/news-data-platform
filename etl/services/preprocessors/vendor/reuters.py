from etl.services.preprocessors.vendor.base import VendorPreprocessor


class ReutersPreprocessor(VendorPreprocessor):

    def process(self, root):

        print("Running Reuters Preprocessor...")

        return root