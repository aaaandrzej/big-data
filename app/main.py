from app.bl.df_processing import AirportFinding
from app.core.ports import import_cities, import_airports, import_cc_codes, cc_codes_processor, \
    airport_matching_processor, result_to_file_saver, result_to_dynamodb_saver, result_to_file_and_dynamodb_saver

if __name__ == '__main__':

    bl = AirportFinding(import_cities, import_airports, import_cc_codes, cc_codes_processor, airport_matching_processor,
                        result_to_file_and_dynamodb_saver)

    bl.process()
