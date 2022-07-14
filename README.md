# Test Project
## Introduction
We have a network of vendors who re-sell our products. We wish to provide them an application to calculate the total cost of an order.
The app needs to give volume discounts and include sales tax.
Another system will accept input from the user, and will call this component with 3 inputs:
- number of items
- price per item
- 2-letter province/state code

The application should output the total price. The total price is calculated by:
- calculate the total cost for the items
- deduct discount based on the quantity
- add sales tax based on the province/state code

The following tables give the discount rate and tax rates:

*Discounts Table:*
| Order Value | Discount Rate |
| ----------- | ------------- |
| $1000 | 3 % |
| $5000 | 5 % | 
| $7000 | 7 % |
| $10000 | 10 % |

*Tax Rate Table:*
| Province | Tax Rate |
| ----------- | ------------- |
| AB | 5 % |
| ON | 13 % | 
| QC | 14.975 % |
| MI | 6 % |
| DE | 0 % |

## Quick Start
1. Make sure Python 3.7+ is installed
2. Make sure dependencies are installed:
    - `pytest` can be installed via `pip install pytest`
    - `pyyaml` can be installed via `pip install pyyaml`
3. Run test using ```pytest``` from the root directory
4. See docstrings for further reference

## Furter improvements:
- Add logging
- Implement input data quality checks
- Refactor test (e.g. use mocks for files, performance testing with random data, etc.)
- Investigate alternative algorithms for range arithmetic (e.g. Interval Tree)