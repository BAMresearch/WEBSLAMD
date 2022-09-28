from slamd.common.error_handling import SequentialLearningException


class ExperimentPreprocessor:
    @classmethod
    def preprocess(cls, exp):
        cls._validate_experiment(exp)
        cls._filter_apriori_with_thresholds(exp)
        cls._encode_categoricals(exp)
        cls._filter_missing_inputs(exp)
        cls._decide_max_or_min(exp)

    @classmethod
    def _validate_experiment(cls, exp):
        # TODO Think of more sensible errors we could throw
        if len(exp.target_names) == 0:
            raise SequentialLearningException('No targets were specified!')
        for value in exp.target_max_or_min + exp.apriori_max_or_min:
            if value not in ['min', 'max']:
                raise SequentialLearningException(f'Invalid value for max_or_min, got {value}')

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
        exp.dataframe.dropna(inplace=True, subset=exp.feature_names, axis=1)

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




    @classmethod
    def _normalize_data(cls, exp):
        # TODO average over categoricals?
        # TODO turn into "normalize dataframe" instead?
        # Subtract the mean and divide by the standard deviation of each column
        for col in exp.dataframe.columns:
            std = exp.dataframe[col].std()

            if std == 0:
                std = 1

            pass
        # std = self.features_df.std().apply(lambda x: x if x != 0 else 1)
        # self.features_df = (self.features_df - self.features_df.mean()) / std
        #
        # std = self.target_df.std().apply(lambda x: x if x != 0 else 1)
        # self.target_df = (self.target_df - self.target_df.mean()) / std
        #
        # std = self.apriori_df.std().apply(lambda x: x if x != 0 else 1)
        # self.apriori_df = (self.apriori_df - self.apriori_df.mean()) / std



    def apply_weights_to_apriori_values(self):
        apriori_for_predicted_rows = self.apriori_df.iloc[self.prediction_index].to_numpy()

        for w in range(len(self.apriori_weights)):
            apriori_for_predicted_rows[w] *= self.apriori_weights[w]
        # Sum the apriori values row-wise for the case that there are several of them
        # We need to simply add their contributions in that case
        return apriori_for_predicted_rows.sum(axis=1)