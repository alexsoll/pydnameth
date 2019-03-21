import abc
import numpy as np
import pandas as pd
from statsmodels import api as sm


class GetStrategy(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_single_base(self, config, items):
        pass

    @abc.abstractmethod
    def get_aux(self, config, item):
        pass

    def get_target(self, config, normed=False):
        target = config.attributes_dict[config.attributes.target]
        if normed:
            target_normed = [(float(x) - min(target)) /
                             (float(max(target)) - float(min(target)))
                             for x in target]
            target = target_normed
        return target


class CPGGetStrategy(GetStrategy):

    def get_single_base(self, config, items):
        rows = [config.base_dict[item] for item in items]
        return config.base_data[np.ix_(rows, config.attributes_indexes)]

    def get_aux(self, config, item):
        return ';'.join(config.cpg_gene_dict[item])


class ResidualsCommonGetStrategy(GetStrategy):

    def get_single_base(self, config, items):
        rows = [config.base_dict[item] for item in items]
        return config.base_data[np.ix_(rows, config.attributes_indexes)]

    def get_aux(self, config, item):
        return CPGGetStrategy.get_aux(self, config, item)


class ResidualsSpecialGetStrategy(GetStrategy):

    def get_single_base(self, config, items):
        cells_dict = config.cells_dict
        exog_df = pd.DataFrame(cells_dict)

        result = np.zeros((len(items), len(config.attributes_indexes)), dtype=np.float32)
        for item_id in range(0, len(items)):
            item = items[item_id]
            row = config.base_dict[item]
            betas = config.base_data[row, config.attributes_indexes]
            endog_dict = {item: betas}
            endog_df = pd.DataFrame(endog_dict)

            reg_res = sm.OLS(endog=endog_df, exog=exog_df).fit()

            residuals = list(map(np.float32, reg_res.resid))

            result[item_id] = residuals

        return result

    def get_aux(self, config, item):
        return CPGGetStrategy.get_aux(self, config, item)


class AttributesGetStrategy(GetStrategy):

    def get_single_base(self, config, items):
        pass

    def get_aux(self, config, item):
        pass
