from slamd.common.error_handling import SequentialLearningException, ValueNotSupportedException


class ExperimentPreprocessor:
    @classmethod
    def preprocess(cls, exp):
        cls.filter_apriori_with_thresholds(exp)
        cls.filter_missing_inputs(exp)
        cls.validate_experiment(exp)
        cls.encode_categoricals(exp)
        cls.decide_max_or_min(exp)

    @classmethod
    def validate_experiment(cls, exp):
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

        # Check if a row has either 0 or all targets labelled TODO interferes with unit test?
        # if not all(x in (0, len(exp.target_names)) for x in exp.targets_df.isna().sum()):
        #     raise SequentialLearningException(message='Some rows are partially labelled. '
        #                                               'This is currently not supported.')

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
                raise SequentialLearningException(message=f'All data is already labelled for target {target}.')

    @classmethod
    def encode_categoricals(cls, exp):
        non_numeric_features = exp.features_df.select_dtypes(exclude='number').columns

        for feature in non_numeric_features:
            exp.dataframe[feature], _ = exp.dataframe[feature].factorize()

    @classmethod
    def filter_missing_inputs(cls, exp):
        # TODO Confirm that we want to drop columns, not rows
        #  (Originally, dropping rows was not possible since the operation acted only on features_df)
        #  -> would simply be exp.dataframe.dropna(inplace=True, subset=exp.feature_names)
        # TODO give feedback, open new jira issue
        for col in exp.feature_names:
            if exp.dataframe[col].isna().values.any():
                exp.dataframe.drop(col, axis=1, inplace=True)

    @classmethod
    def decide_max_or_min(cls, exp):
        # TODO find a way to do this non-destructively
        # Multiply the column by -1 if it needs to be minimized
        for (column, value) in zip(exp.target_names + exp.apriori_names,
                                   exp.target_max_or_min + exp.apriori_max_or_min):
            if value == 'min':
                exp.dataframe[column] *= (-1)

    @classmethod
    def filter_apriori_with_thresholds(cls, exp):
        # In the future this function could be handled "live" and non-destructively in label_index and nolabel_index
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
