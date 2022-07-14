from typing import Dict
import yaml
import pathlib

class Pricing:
    """This class handles the input of discounts, tax rax and calculation of order price
    
        Attributes:
            discounts (dict(str, float)): dictionary of discount rates. keys are assumed to be strings of floating numbers
            tax_rates (dict(str, float)): dictionary of tax rates per region
    """

    def __init__(self, discounts: Dict[str, float] = None, tax_rates: Dict[str, float] = None, discounts_path: str = None, tax_rates_path: str = None):
        """Constructs an instance from paths or dictionaries

            Accepts either paths or dictionaries for discounts and tax rates.

            By default assumes the data for discounts and tax rates is present in /config/discounts.yaml and /config/tax_rates.yaml.
            Data quality is assumed. No checking is done

            Parameters:
                discounts_path (str): path string for discounts.yaml. defaults to /config/discounts.yaml
                tax_rates_path (str): path string for tax_rates.yaml. defaults to /config/tax_rates.yaml
                discounts (dict(str, float)): dictionary of discount rates. keys are assumed to be strings of floating numbers
                tax_rates (dict(str, float)): dictionary of tax rates per region
        """

        # if dictionaries are present they are used (e.g. unit testing)
        if discounts is not None and tax_rates is not None:
            self.discounts = discounts
            self.tax_rates = tax_rates
            return

        # loading discounts data from paths
        if discounts_path is None:
            self.discounts_path = ( pathlib.Path(__file__) / '../config/discounts.yaml').resolve()
        else:
            self.discounts_path = pathlib.Path(discounts_path)
        
        try:
            discounts_text = self.discounts_path.read_text()
        except Exception as orig:
            raise Exception('Could not open discounts.yaml', orig)

        try:
            self.discounts = yaml.safe_load(discounts_text)
        except Exception as orig:
            raise Exception('Could not parse discounts.yaml', orig)
            
        # loading tax rates data from paths
        if tax_rates_path is None:
            self.tax_rates_path = ( pathlib.Path(__file__) / '../config/tax_rates.yaml').resolve()
        else:
            self.tax_rates_path = pathlib.Path(tax_rates_path)

        try:
            tax_rates_text = self.tax_rates_path.read_text()
        except Exception as orig:
            raise Exception('Could not open tax_rates.yaml', orig)

        try:
            self.tax_rates = yaml.safe_load(tax_rates_text)
        except Exception as orig:
            raise Exception('Could not parse tax_rates.yaml', orig)
 

    def calculate(self, num_items: int, price_per_item: float, tax_region_code: str) -> float:
        '''Calculates the order price

            Calculates the order price, applies discount based on the discount brackets and tax based on tax region

            Parameters:
                num_items (int): number of items in the order
                price_per_item (float): price per item
                tax_region_code (str): string code of tax region
            
            Returns:
                total_amount (float): total amount after discount and  tax
        '''

        # Checking for the correct types and values of inputs
        if not isinstance(num_items, int):
            raise TypeError(f'num_items must be of type int. received {type(num_items)}')
        elif num_items <= 0:
            raise ValueError(f'num_items must be positive. received {num_items}')

        if not isinstance(price_per_item, (int, float)):
            raise TypeError(f'price_per_item must be of type numeric. received {type(price_per_item)}')
        elif price_per_item <= 0:
            raise ValueError(f'price_per_item must be positive. received {price_per_item}')

        if tax_region_code not in self.tax_rates:
            raise ValueError(f'tax_region_code must be in {self.tax_rates.keys()}. received {tax_region_code}')
        
        # amount before discount and taxes
        amount = num_items * price_per_item

        discount_amount = amount*(self.__calculate_discount_percent(amount) / 100.0)

        pretax_amount = amount - discount_amount

        tax_amount = pretax_amount * (self.tax_rates[tax_region_code] / 100.0)

        total_amount = pretax_amount + tax_amount

        return total_amount

    
    def __calculate_discount_percent(self, amount: float) -> float:
        '''Private method to calculate discount percent based on amount

            Runs in O(n_disc*log(n_disc)) time with O(n_disc) extra space
            where n_disc is the number of discount breakpoints.
            Discount is supposed to be in the correct format, no input validation is done

            Parameters:
                amount (float): the amount for which the discount percent is calculated

            Returns:
                discount_percent (float): discount percent 
        '''
        # no discounts are provided
        if len(self.discounts) == 0:
            return 0

        # checking if the amount is within any of the discount brackets:
        # The brackets are sorted first. Ascending order guarantees the correctness of the method, 
        # since there are 3 mutually exclusive cases: less than the min, larger than the max, and within a bracket.

        # 1. calculating discount_brackets in ascending order
        discounts_list = [(float(key), float(value)) for key, value in self.discounts.items()]
        discounts_list.sort(key=lambda tup: tup[0])

        # checking if below minimum or above maximum
        if amount < discounts_list[0][0]:
            return 0
        elif amount >= discounts_list[-1][0]:
            return discounts_list[-1][1]

        # 2. iterating over the intermediate discount brackets
        for i in range(1, len(discounts_list)):
            if discounts_list[i-1][0] <= amount < discounts_list[i][0]:
                return discounts_list[i-1][1]
            
        

        


disc = {'1000': 3, '5000': 5, '7000': 7, '10000': 10}
tax = {'AB': 5, 'ON': 13, 'QC': 14.975, 'MI': 6, 'DE': 0}

# p = Pricing()
# p = Pricing(discounts_path=r"config\discounts.yaml", tax_rates_path=r"config\tax_rates.yaml")
p = Pricing(discounts=disc,tax_rates=tax)

print(p.calculate(12,212.5,'AB'))
print(p.calculate(14,1008.42,'QC'))
