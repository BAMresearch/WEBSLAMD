class DiscoveryService:

    @classmethod
    def list_columns(cls, dataset):
        # Hardcoded response until we have a reliable upload button.
        return [
            'Idx_Sample',
            'SiO2',
            'CaO',
            'SO3',
            'FA (kg/m3)',
            'GGBFS (kg/m3)',
            'Coarse aggregate (kg/m3)',
            'Fine aggregate (kg/m3)',
            'Total aggregates',
            'Na2SiO3', 'Na2O (Dry)',
            'Sio2(Dry)', 'Superplasticizer',
            'water - eff', 'Slump - Target(mm)',
            'CO2(kg/t) - A-priori Information',
            'fc 28-d - Target(MPa)'
        ]
