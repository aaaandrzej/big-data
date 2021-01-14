class AirportFinding:
    def __init__(self,
                 cities_importer,
                 airport_importer,
                 cc_codes_importer,
                 cc_codes_processor,
                 airport_matching_processor,
                 result_saver):
        self._cities_importer = cities_importer
        self._airport_importer = airport_importer
        self._cc_codes_importer = cc_codes_importer
        self._cc_codes_processor = cc_codes_processor
        self._airport_matching_processor = airport_matching_processor
        self._result_saver = result_saver

    def process(self):
        df = self._cities_importer()
        country_info = self._cc_codes_importer()
        df = self._cc_codes_processor(df, country_info)
        print('prep done')

        airports = self._airport_importer()
        result = self._airport_matching_processor(df, airports)
        print('processing done')

        self._result_saver(result)
        print('all done')
