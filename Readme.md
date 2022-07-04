# Basic operation

Check every N seconds:
- For each share
  - Get last price
  - Set sell order STOP LOSS - e.g. 1% 
    - If sold, remember sell price
    - Set buy price = sold price - SOMETHING - fees
  - Set sell order if share + 3%
    - Set buy order if price drops

