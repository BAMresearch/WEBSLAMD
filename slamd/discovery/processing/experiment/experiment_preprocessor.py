from slamd.common.error_handling import SequentialLearningException, ValueNotSupportedException, \
    SlamdUnprocessableEntityException
from slamd.discovery.processing.experiment.experiment_model import ExperimentModel


class ExperimentPreprocessor:

    @classmethod
    def preprocess(cls, exp):
        cls.filter_apriori_with_thresholds_and_update_orig_data(exp)
        cls.filter_missing_inputs(exp)
        cls.validate_experiment(exp)
        cls.encode_categoricals(exp)

    @classmethod
    def validate_experiment(cls, exp):
        if exp.model not in [ExperimentModel.GAUSSIAN_PROCESS.value, ExperimentModel.RANDOM_FOREST.value]:
            raise ValueNotSupportedException(message=f'Invalid model: {exp.model}')

        if len(exp.target_names) == 0:
            raise SequentialLearningException('No targets were specified!')

        if not (len(exp.target_names) == len(exp.target_weights) == len(exp.target_thresholds) ==
                len(exp.target_max_or_min)):
            raise SlamdUnprocessableEntityException(message='Target names, weights, thresholds, and max_or_min '
                                                            'parameters do not have the same length.')
        elif not (len(exp.apriori_names) == len(exp.apriori_weights) == len(exp.apriori_thresholds) ==
                  len(exp.apriori_max_or_min)):
            raise SlamdUnprocessableEntityException(message='Apriori names, weights, thresholds, and max_or_min '
                                                            'parameters do not have the same length.')

        for value in exp.target_max_or_min + exp.apriori_max_or_min:
            if value not in ['min', 'max']:
                raise SequentialLearningException(f'Invalid value for max_or_min, got {value}')

        for target, count in zip(exp.target_names, exp.targets_df.count()):
            if exp.model == ExperimentModel.RANDOM_FOREST.value and count <= 1:
                raise ValueNotSupportedException(
                    message=f'Not enough labelled values for target: {target}. The Random Forest Regressor '
                            f'requires at least 2 labelled values, but only {count} was/were found. '
                            f'Please ensure that there are at least 2 data points that are not filtered out '
                            f'by the apriori thresholds.'
                )
            elif exp.model == ExperimentModel.GAUSSIAN_PROCESS.value and count < 1:
                raise ValueNotSupportedException(
                    message=f'Not enough labelled values for target: {target}. The Gaussian Process Regressor '
                            f'requires at least 1 labelled value, but none were found. '
                            f'Please ensure that there is at least 1 data point that is not filtered out '
                            f'by the a priori information thresholds.'
                )
            elif count == len(exp.targets_df.index):
                raise SequentialLearningException(message=f'All data is already labelled for target {target}.')

    @classmethod
    def encode_categoricals(cls, exp):
        non_numeric_features = exp.features_df.select_dtypes(exclude='number').columns

        for feature in non_numeric_features:
            exp.dataframe[feature], _ = exp.dataframe[feature].factorize()

    @classmethod
    def filter_missing_inputs(cls, exp):
        for col in exp.feature_names:
            if exp.dataframe[col].isna().values.any():
                exp.dataframe.drop(col, axis=1, inplace=True)
                exp.feature_names.remove(col)

    @classmethod
    def filter_apriori_with_thresholds_and_update_orig_data(cls, exp):
        # In the future this function could be handled "live" and non-destructively in index_all_labelled and index_none_labelled
        for (column, value, threshold) in zip(exp.apriori_names, exp.apriori_max_or_min, exp.apriori_thresholds):
            if threshold is None:
                continue

            # index of rows in which all target columns are nan
            nodata_index = exp.targets_df.isna().all(axis=1)
            if value == 'max':
                # Get dataframe mask based on threshold value and nodata_index.
                # Apply mask to dataframe. Get index of values to drop.
                # Use new index to drop values from original dataframe.
                exp.dataframe.drop(
                    exp.dataframe[(exp.dataframe[column] < threshold) & nodata_index].index,
                    inplace=True
                )
            else:
                exp.dataframe.drop(
                    exp.dataframe[(exp.dataframe[column] > threshold) & nodata_index].index,
                    inplace=True
                )

        exp.dataframe.reset_index(drop=True, inplace=True)
        exp.orig_data = exp.dataframe.copy()
