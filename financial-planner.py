#!/usr/bin/env python
# coding: utf-8

# # Unit 5 - Financial Planning

# In[2]:


# Initial imports
import os
import requests
import pandas as pd
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
from MCForecastTools import MCSimulation

get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


# Load .env enviroment variables
load_dotenv()


# ## Part 1 - Personal Finance Planner

# ### Collect Crypto Prices Using the `requests` Library

# In[4]:


# Set current amount of crypto assets
# YOUR CODE HERE!
my_btc = 1.2
my_eth = 5.3


# In[5]:


# Crypto API URLs
btc_url = "https://api.alternative.me/v2/ticker/Bitcoin/?convert=CAD"
eth_url = "https://api.alternative.me/v2/ticker/Ethereum/?convert=CAD"


# In[18]:


# Fetch current BTC price
# YOUR CODE HERE!
btc_request_data = requests.get(btc_url)
btc_data = btc_request_data.json()
btc_price_CAD = btc_data['data']['1']['quotes']['CAD']['price']

# Fetch current ETH price
# YOUR CODE HERE!
eth_request_data = requests.get(eth_url)
eth_data = eth_request_data.json()
eth_price_CAD = eth_data['data']['1027']['quotes']['CAD']['price']


# Compute current value of my crpto
# YOUR CODE HERE!
my_btc_value = my_btc * btc_price_CAD
my_eth_value = my_eth * eth_price_CAD

# Print current crypto wallet balance
print(f"The current value of your {my_btc} BTC is ${my_btc_value:0.2f}")
print(f"The current value of your {my_eth} ETH is ${my_eth_value:0.2f}")


# ### Collect Investments Data Using Alpaca: `SPY` (stocks) and `AGG` (bonds)

# In[34]:


# Set current amount of shares
my_agg = 200
my_spy = 50


# In[35]:


# Set Alpaca API key and secret
# YOUR CODE HERE!
alpaca_api_key = os.getenv("ALPACA_API_KEY")
alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")

# Create the Alpaca API object
# YOUR CODE HERE!
api = tradeapi.REST(
    alpaca_api_key,
    alpaca_secret_key,
    api_version = "v2"
)


# In[36]:


# Format current date as ISO format
# YOUR CODE HERE!
start_date = pd.Timestamp("2017-01-01", tz="America/New_York").isoformat()
end_date = pd.Timestamp.today("America/New_York").isoformat()

# Set the tickers
tickers = ["AGG", "SPY"]

# Set timeframe to '1D' for Alpaca API
timeframe = "1D"

# Get current closing prices for SPY and AGG
# (use a limit=1000 parameter to call the most recent 1000 days of data)
# YOUR CODE HERE!
df_tickers = api.get_barset(
    tickers,
    timeframe,
    start = start_date,
    end = end_date,
    limit=1000
).df

# Preview DataFrame
# YOUR CODE HERE!
df_tickers


# In[37]:


# Pick AGG and SPY close prices
# YOUR CODE HERE!
agg_close_price = df_tickers.iloc[-1]['AGG']['close']
spy_close_price = df_tickers.iloc[-1]['SPY']['close']

# Print AGG and SPY close prices
print(f"Current AGG closing price: ${agg_close_price}")
print(f"Current SPY closing price: ${spy_close_price}")


# In[38]:


# Compute the current value of shares
# YOUR CODE HERE!
my_spy_value = spy_close_price * my_spy
my_agg_value = agg_close_price * my_agg

# Print current value of shares
print(f"The current value of your {my_spy} SPY shares is ${my_spy_value:0.2f}")
print(f"The current value of your {my_agg} AGG shares is ${my_agg_value:0.2f}")


# ### Savings Health Analysis

# In[40]:


# Set monthly household income
# YOUR CODE HERE!
monthly_income = 12000

# Consolidate financial assets data
# YOUR CODE HERE!
savings_dict = {'crypto' : [my_btc_value + my_eth_value], 'shares' : [my_spy_value + my_agg_value]}

# Create savings DataFrame
# YOUR CODE HERE!
df_savings = pd.DataFrame.from_dict(savings_dict, orient='index')
df_savings.columns = ['amount']
# Display savings DataFrame
display(df_savings)


# In[45]:


# Plot savings pie chart
# YOUR CODE HERE!
df_savings.plot(kind="pie", subplots=True, title="Personal Savings Chart", figsize=[8,5])


# In[51]:


# Set ideal emergency fund
emergency_fund = monthly_income * 3

# Calculate total amount of savings
# YOUR CODE HERE!
total_savings = df_savings.sum()

# Validate saving health
# YOUR CODE HERE!
if total_savings['amount'] > emergency_fund:
    print(f"Congratulations!! You have total savings of ${total_savings['amount']:.2f} which is more than enough for an emergency.")
elif total_savings['amount'] < emergency_fund:
    print(f"You have total savings of ${total_savings['amount']:.2f}. You still require ${emergency_fund - total_savings['amount']:.2f} more to have enough funds for an emergency.")
else:
    print(f"Congratulations!! You have enough funds for an emergency.")


# ## Part 2 - Retirement Planning
# 
# ### Monte Carlo Simulation

# In[52]:


# Set start and end dates of five years back from today.
# Sample results may vary from the solution based on the time frame chosen
start_date = pd.Timestamp('2016-05-01', tz='America/New_York').isoformat()
end_date = pd.Timestamp('2021-05-01', tz='America/New_York').isoformat()


# In[55]:


# Get 5 years' worth of historical data for SPY and AGG
# (use a limit=1000 parameter to call the most recent 1000 days of data)
# YOUR CODE HERE!
df_stock_data = api.get_barset(
    tickers,
    timeframe,
    start = start_date,
    end = end_date,
    limit=1000
).df

# Display sample data
df_stock_data.head()


# In[63]:


# Configuring a Monte Carlo simulation to forecast 30 years cumulative returns
# YOUR CODE HERE!
MC_stock = MCSimulation(
    portfolio_data = df_stock_data,
    weights = [.40,.60],
    num_simulation = 500,
    num_trading_days = 252*30
)


# In[64]:


# Printing the simulation input data
# YOUR CODE HERE!
MC_stock.portfolio_data.head()


# In[65]:


# Running a Monte Carlo simulation to forecast 30 years cumulative returns
# YOUR CODE HERE!
MC_stock.calc_cumulative_return()


# In[66]:


# Plot simulation outcomes
# YOUR CODE HERE!
MC_stock.plot_simulation()


# In[68]:


# Plot probability distribution and confidence intervals
# YOUR CODE HERE!
MC_stock.plot_distribution()


# ### Retirement Analysis

# In[69]:


# Fetch summary statistics from the Monte Carlo simulation results
# YOUR CODE HERE!
MC_stock_summary = MC_stock.summarize_cumulative_return()

# Print summary statistics
# YOUR CODE HERE!
print(MC_stock_summary)


# ### Calculate the expected portfolio return at the `95%` lower and upper confidence intervals based on a `$20,000` initial investment.

# In[70]:


# Set initial investment
initial_investment = 20000

# Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes of our $20,000
# YOUR CODE HERE!
ci_lower = round(MC_stock_summary[8]*initial_investment,2)
ci_upper = round(MC_stock_summary[9]*initial_investment,2)

# Print results
print(f"There is a 95% chance that an initial investment of ${initial_investment} in the portfolio"
      f" over the next 30 years will end within in the range of"
      f" ${ci_lower} and ${ci_upper}")


# ### Calculate the expected portfolio return at the `95%` lower and upper confidence intervals based on a `50%` increase in the initial investment.

# In[71]:


# Set initial investment
initial_investment = 20000 * 1.5

# Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes of our $30,000
# YOUR CODE HERE!
ci_lower = round(MC_stock_summary[8]*initial_investment,2)
ci_upper = round(MC_stock_summary[9]*initial_investment,2)

# Print results
print(f"There is a 95% chance that an initial investment of ${initial_investment} in the portfolio"
      f" over the next 30 years will end within in the range of"
      f" ${ci_lower} and ${ci_upper}")


# ## Optional Challenge - Early Retirement
# 
# 
# ### Five Years Retirement Option

# In[72]:


# Configuring a Monte Carlo simulation to forecast 5 years cumulative returns
# YOUR CODE HERE!
MC_stock_5 = MCSimulation(
    portfolio_data = df_stock_data,
    weights = [.40,.60],
    num_simulation = 500,
    num_trading_days = 252*5
)


# In[73]:


# Running a Monte Carlo simulation to forecast 5 years cumulative returns
# YOUR CODE HERE!
MC_stock_5.calc_cumulative_return()


# In[74]:


# Plot simulation outcomes
# YOUR CODE HERE!
MC_stock_5.plot_simulation()


# In[75]:


# Plot probability distribution and confidence intervals
# YOUR CODE HERE!
MC_stock_5.plot_distribution()


# In[79]:


# Fetch summary statistics from the Monte Carlo simulation results
# YOUR CODE HERE!
MC_stock_5_summary = MC_stock_5.summarize_cumulative_return()

# Print summary statistics
# YOUR CODE HERE!
print(MC_stock_5_summary)


# In[81]:


# Set initial investment
# YOUR CODE HERE!
initial_investment = 50000
# Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes of our $60,000
# YOUR CODE HERE!
ci_lower_five = round(MC_stock_5_summary[8]*initial_investment,2)
ci_upper_five = round(MC_stock_5_summary[9]*initial_investment,2)

# Print results
print(f"There is a 95% chance that an initial investment of ${initial_investment} in the portfolio"
      f" over the next 5 years will end within in the range of"
      f" ${ci_lower_five} and ${ci_upper_five}")


# ### Ten Years Retirement Option

# In[82]:


# Configuring a Monte Carlo simulation to forecast 10 years cumulative returns
# YOUR CODE HERE!
MC_stock_10 = MCSimulation(
    portfolio_data = df_stock_data,
    weights = [.40,.60],
    num_simulation = 500,
    num_trading_days = 252*10
)


# In[83]:


# Running a Monte Carlo simulation to forecast 10 years cumulative returns
# YOUR CODE HERE!
MC_stock_10.calc_cumulative_return()


# In[84]:


# Plot simulation outcomes
# YOUR CODE HERE!
MC_stock_10.plot_simulation()


# In[85]:


# Plot probability distribution and confidence intervals
# YOUR CODE HERE!
MC_stock_10.plot_distribution()


# In[86]:


# Fetch summary statistics from the Monte Carlo simulation results
# YOUR CODE HERE!
MC_stock_10_summary = MC_stock_10.summarize_cumulative_return()

# Print summary statistics
# YOUR CODE HERE!
print(MC_stock_10_summary)


# In[87]:


# Set initial investment
# YOUR CODE HERE!
initial_investment = 50000

# Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes of our $60,000
# YOUR CODE HERE!
ci_lower_ten = round(MC_stock_10_summary[8]*initial_investment,2)
ci_upper_ten = round(MC_stock_10_summary[9]*initial_investment,2)

# Print results
print(f"There is a 95% chance that an initial investment of ${initial_investment} in the portfolio"
      f" over the next 10 years will end within in the range of"
      f" ${ci_lower_ten} and ${ci_upper_ten}")


# In[ ]:




