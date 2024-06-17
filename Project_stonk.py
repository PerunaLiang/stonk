import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
#msft = yf.Ticker("MSFT")
#hist = msft.history(period="max")
#print(hist)

#Get company data
def get_companydata(ticker):
    companydata = yf.Ticker(ticker)
    hist = companydata.history(period="max")
    return hist

#Graph of price over time


def price_time(ticker):
    hist = get_companydata(ticker)
    hist['Close'].plot(color ='#661b43')
    plt.ylabel('Price(USD)')
    plt.suptitle('Price over time (USD) '+ ticker, fontsize=16)
    plt.show() 



#Percent change per day
def pct_day(ticker):
    hist = get_companydata(ticker)
    hist['pct_change'] =  hist['Close'].pct_change()
    pct_changegraph = hist['Close'].pct_change()*100
    pct_changegraph.plot(color=['#26bbaa'])
    plt.ylabel('Percent change per day')
    plt.suptitle('Percent change per day '+ ticker, fontsize=16)
    plt.show()
    print(hist['pct_change'].mean()*100, 'Mean % change per day')
    print(hist['pct_change'].std()*100, 'standard deviation of % change per day)')




#Yearly percent change
def year_change(ticker):
    hist = get_companydata(ticker)
    hist['pct_change'] =  hist['Close'].pct_change()
    hist['yearthingpct'] = hist['pct_change'].rolling(window=253).mean()
    yeargraph=hist['yearthingpct']*100
    yeargraph.plot(color=['#26bcaa'])
    plt.ylabel('Percent change per year')
    plt.suptitle('Percent change per year '+ ticker, fontsize=16)
    plt.show()
    print('Mean % change per year', hist['yearthingpct'].mean()*100)
    print('Standard deviation of % change per year', hist['yearthingpct'].std()*100)
    
    mean = hist['yearthingpct'].mean()*100
    std = hist['yearthingpct'].std()*100

    if mean >= 0.1:
        print('The stonko is moving')
    elif mean <0.1:
        print('no')
    
    if std >= 1:
        print('Fluctuating stonk')
    elif std <1:
        print('Less fluctuating')
    


def stonk_study(ticker):
    price_time(ticker)
    pct_day(ticker)
    year_change(ticker)

stonk_study("MSFT")




