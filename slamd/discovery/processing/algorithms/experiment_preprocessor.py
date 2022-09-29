from slamd.common.error_handling import SequentialLearningException, ValueNotSupportedException


class ExperimentPreprocessor:
    @classmethod
    def preprocess(cls, exp):
        cls._filter_apriori_with_thresholds(exp)
        cls._filter_missing_inputs(exp)
        cls._validate_experiment(exp)
        cls._encode_categoricals(exp)
        cls._decide_max_or_min(exp)

    @classmethod
    def _validate_experiment(cls, exp):
        # TODO Think of more sensible errors we could throw

        # TODO We should not be carrying these strings around
        if exp.model not in ['Statistics-based model (Gaussian Process Regression)',
                             'AI Model (lolo Random Forest)']:
            raise ValueNotSupportedException(message=f'Invalid model: {exp.model}')

        if len(exp.target_names) == 0:
            raise SequentialLearningException('No targets were specified!')
        for value in exp.target_max_or_min + exp.apriori_max_or_min:
            if value not in ['min', 'max']:
                raise SequentialLearningException(f'Invalid value for max_or_min, got {value}')

        # TODO Implement this validation function formerly called by regressor functions
        # nan_counts = list(self.target_df.isna().sum())
        #
        # previous_count = nan_counts[0]
        # for j in range(1, len(nan_counts)):
        #     if nan_counts[1] != previous_count:
        #         raise SequentialLearningException('Targets used are labelled for differing rows.')
        #     previous_count = nan_counts[j]

        # Check if a row has either 0 or all targets labelled
        if not all(x in (0, len(exp.target_names)) for x in exp.targets_df.isna().sum()):
            raise SequentialLearningException(message='Some rows are partially labelled. '
                                                      'This is currently not supported.')

        # TODO Implement the validation checks from this function. Needs to run AFTER filter apriori
        #
        # @classmethod
        # def _check_target_label_validity(cls, training_labels):
        #     number_of_labelled_targets = training_labels.shape[0]
        #     if number_of_labelled_targets == 0:
        #         raise SequentialLearningException('No labels exist. Check your target and apriori columns and ensure '
        #                                           'your thresholds are set correctly.')
            # all_data_is_labelled = exp.dataframe.shape[0] == number_of_labelled_targets
            # if all_data_is_labelled:
            #     raise SequentialLearningException('All data is already labelled.')

        # TODO Implement this validation check for the random forest regressor
        # if self.dataframe.loc[:, self.targets[i]].count() <= 1:
        #     raise ValueNotSupportedException(message=f'The given dataset does not contain enough training data '
        #                                              f'in column {self.targets[i]}. Please ensure that there are '
        #                                              f'at least 2 data points that are not filtered out by '
        #                                              f'apriori thresholds.')
        for target, count in zip(exp.target_names, exp.targets_df.count()):
            if exp.model == 'AI Model (lolo Random Forest)' and count <= 1:
                raise ValueNotSupportedException(
                    message=f'Not enough labelled values for target: {target}. The Random Forest Regressor '
                            f'requires at least 2 labelled values, but only {count} was/were found. '
                            f'Please ensure that there are at least 2 data points that are not filtered out '
                            f'by the apriori thresholds.'
                )
            elif exp.model == 'Statistics-based model (Gaussian Process Regression)' and count < 1:
                raise ValueNotSupportedException(
                    message=f'Not enough labelled values for target: {target}. The Gaussian Process Regressor '
                            f'requires at least 1 labelled value, but none were found. '
                            f'Please ensure that there is at least 1 data points that is not filtered out '
                            f'by the apriori thresholds.'
                )
            elif count == len(exp.targets_df.index):
                raise SequentialLearningException(message='All data is already labelled.')

    @classmethod
    def _encode_categoricals(cls, exp):
        # TODO The previous version of this function used to do a dropna (axis=1) on features_df.
        #  This has been moved to _filter_missing_inputs
        non_numeric_features = exp.features_df.select_dtypes(exclude='number').columns

        for feature in non_numeric_features:
            exp.dataframe[feature], _ = exp.dataframe[feature].factorize()

    @classmethod
    def _filter_missing_inputs(cls, exp):
        # TODO Confirm that we want to drop columns, not rows
        #  (Originally, dropping rows was not possible since the operation acted only on features_df)
        #  -> would simply be exp.dataframe.dropna(inplace=True, subset=exp.feature_names)
        # TODO Technically this is modifying a dataframe as we are iterating over it which is not really clean
        #  not really an issue here but still...
        for col in exp.feature_names:
            if exp.dataframe[col].isna().values.any():
                exp.dataframe.drop(col, axis=1, inplace=True)

    @classmethod
    def _decide_max_or_min(cls, exp):
        # TODO find a way to do this non-destructively
        # Multiply the column by -1 if it needs to be minimized
        for (column, value) in zip(exp.target_names+exp.apriori_names, exp.target_max_or_min+exp.apriori_max_or_min):
            if value == 'min':
                exp.dataframe[column] *= (-1)

    @classmethod
    def _filter_apriori_with_thresholds(cls, exp):
        # TODO This function could be handled "live" and non-destructively in label_index and nolabel_index
        for (column, value, threshold) in zip(exp.apriori_names, exp.apriori_max_or_min, exp.apriori_thresholds):
            if threshold is None:
                continue

            # index of rows in which all target columns are nan
            nodata_index = exp.targets_df.isna().all(axis=1)
            if value == 'max':
                # Get dataframe mask based on threshold value and nodata_index.
                # Apply mask to dataframe. Get index of values to drop.
                # Use new index to drop values from original dataframe.
                exp.dataframe.drop(exp.dataframe[(exp.dataframe[column] < threshold) & nodata_index].index, inplace=True)
            else:
                exp.dataframe.drop(exp.dataframe[(exp.dataframe[column] > threshold) & nodata_index].index, inplace=True)

        exp.dataframe.reset_index(drop=True, inplace=True)


