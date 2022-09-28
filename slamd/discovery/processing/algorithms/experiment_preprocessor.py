from slamd.common.error_handling import SequentialLearningException


class ExperimentPreprocessor:

    def preprocess(self):


        if len(targets) == 0:
            raise SequentialLearningException('No targets were specified!')



    def _update_prediction_index(self):
        # Selects the rows that have a label for the first target
        # These have a null value in the corresponding column
        self.prediction_index = pd.isnull(self.dataframe[[self.targets[0]]]).to_numpy().nonzero()[0]

    def _update_sample_index(self):
        # Inverse of prediction index - The rows with labels (the training set) are the rest of the rows
        self.sample_index = self.dataframe.index.difference(self.prediction_index)



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



    def _check_target_label_validity(self, training_labels):
        number_of_labelled_targets = training_labels.shape[0]
        if number_of_labelled_targets == 0:
            raise SequentialLearningException('No labels exist. Check your target and apriori columns and ensure '
                                              'your thresholds are set correctly.')
        all_data_is_labelled = self.dataframe.shape[0] == number_of_labelled_targets
        if all_data_is_labelled:
            raise SequentialLearningException('All data is already labelled.')