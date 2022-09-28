from slamd.common.error_handling import SequentialLearningException


class ExperimentPreprocessor:
    @classmethod
    def preprocess(cls, exp):
        cls._encode_categoricals(exp)
        cls.decide_max_or_min(exp)

        if len(targets) == 0:
            raise SequentialLearningException('No targets were specified!')






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



    @classmethod
    def _encode_categoricals(cls, exp):
        # TODO The previous version of this function used to do a dropna (axis=1) on features_df.
        #  This should be done in a separate function
        non_numeric_features = exp.features_df.select_dtypes(exclude='number').columns

        for feature in non_numeric_features:
            exp.dataframe[feature], _ = exp.dataframe[feature].factorize()



    def filter_apriori_with_thresholds(self, df):
        for (column, value, threshold) in zip(self.apriori_columns, self.apriori_max_or_min, self.apriori_thresholds):
            if value not in ['min', 'max']:
                raise SequentialLearningException(f'Invalid value for max_or_min, got {value}')
            if threshold is None:
                continue

            # index of rows in which all target columns are nan
            nodata_index = df[self.targets].isna().all(axis=1)
            if value == 'max':
                # Get dataframe mask based on threshold value and nodata_index.
                # Apply mask to dataframe. Get index of values to drop.
                # Use new index to drop values from original dataframe.
                df.drop(df[(df[column] < threshold) & nodata_index].index, inplace=True)
            else:
                df.drop(df[(df[column] > threshold) & nodata_index].index, inplace=True)

        return df.reset_index(drop=True)



    def apply_weights_to_apriori_values(self):
        apriori_for_predicted_rows = self.apriori_df.iloc[self.prediction_index].to_numpy()

        for w in range(len(self.apriori_weights)):
            apriori_for_predicted_rows[w] *= self.apriori_weights[w]
        # Sum the apriori values row-wise for the case that there are several of them
        # We need to simply add their contributions in that case
        return apriori_for_predicted_rows.sum(axis=1)

    def decide_max_or_min(self, df, columns, max_or_min):
        # Multiply the column by -1 if it needs to be minimized
        for (column, value) in zip(columns, max_or_min):
            if value not in ['min', 'max']:
                raise SequentialLearningException(f'Invalid value for max_or_min, got {value}')
            if value == 'min':
                df[column] *= (-1)