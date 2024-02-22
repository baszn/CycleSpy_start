from cyclespy.verifier import ResultVerifier, CortexM3Ruleset

"""
When the recordings are done the results can be verified by a model. The 'ResultVerifier' will
help with importing the results and enriching them with extra columns. It will also shift the Cycle column to the
right position. When the results are enriched, the 'verify_results(...)' function can be called that will evaluate
the results against a Ruleset. For now only a CortexM3Ruleset is available. This will add a 'expected_cycles' column
to the results and a 'holds_to_spec' column to evaluate if the model matches the actual results. These columns will
be used to calculate the percentage of correct predictions by the 'print_results()' function.

Most of these functions will return the (modified) dataset as a pandas dataframe. It is possible to export these
dataframes to for example a CSV file by using the pandas 'to_csv()' function. 
"""
if __name__ == '__main__':
    for i in range(0, 7):
        verifier = ResultVerifier.load_csv_from_results_directory("combination_test_small", "lpc1768", i)
        verifier.enrich_results()
        results = verifier.verify_results(CortexM3Ruleset())
        # results.to_csv(...)
        verifier.print_results()
