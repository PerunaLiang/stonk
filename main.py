from typing import Optional
from PIL.Image import Image
from fastapi import FastAPI
from numpy import histogram_bin_edges
#Fast API is a library

import pandas as pd
import matplotlib.pyplot as plt
from starlette.responses import HTMLResponse
import yfinance as yf



doggo = FastAPI()

# http://127.0.0.1:8000/docs
# display swagger documentaion



@doggo.get("/", response_class=HTMLResponse)
def homepage():

    html = f'''

     
      <style>
     * {{color:black;
        font-family:arial}}
    p {{
        color:#d3e5e8
    }}

    a
    {{text-decoration: none;}}

    label {{
        color:#d3e5e8
    }}
    
      input {{
          border: none;
          border:solid 1px #ccc;
          border-radius: 5px;
      }}  

      #box {{
      height: 20px;
      text-align:center;
        border: 2px solid #d3e5e8
      }}

      #box:hover {{
      background-color:rgba(128, 140, 200, 0.5)}}

      </style>

    
    <p> Enter the ticker and column </p>

     <a href="https://uk.finance.yahoo.com/lookup/" target="_blank">
     <div>
        <p id="box"> Ticker lookup search </p>
        </a>
    <br>
    <form action="/graph1/" >
    <label for="ticker">Choose ticker:</label>
    <input name="ticker" id="ticker" type="text" placeholder="Ticker"></input>

    <br>
    <br>

    <label for="column">Choose column:</label>
    <select id="column" name="column" >
    <option value="High">High</option>
    <option value="Low">Low</option>    
    <option value="Close">Close</option>
    <option value="Volume">Volume</option>
    <option value="Dividends">Dividends</option>
    <option value="Stock Splits">Stock Splits</option>
    </select>

   
    
    <button>Enter</button>
    </form>

    

    
   
    ''' 
    return html

# Need to use {{ double}} as if you use a f"string it thinks it is refering to a python

# (f"http://127.0.0.1:8000/basic/?ticker={ticker}&column={column})
 

@doggo.get("/basic/")
def get_companydata(ticker: str, column: str):
    ticker = ticker.upper().strip()
    column = column.capitalize().strip()
    companydata = yf.Ticker(ticker)
    hist = companydata.history(period="12mo")
    print(hist)
    
    return hist[column]

# would be good to have a option to select the timeframe you want

@doggo.get("/showcolumns/")
def get_columns(ticker: str):
    ticker = ticker.upper().strip()
    companydata = yf.Ticker(ticker)
    hist = companydata.history(period="max")
    print(hist)

    return list(hist.columns)
# websites take basic/primitive datatypes e.g they cannot deal with dataframes
# hence columns names needs to converted to a list

# @doggo.get("/graph1/?ticker={ticker}&column={column}", response_class=HTMLResponse)
# fastAPI does this for you so it can reference your parameters immediately


@doggo.get("/graph1/", response_class=HTMLResponse)


def price_time(ticker, column):
    plt.clf() #this clears the graph for previous ticker shown
    ticker = ticker.upper().strip()
    column = column.capitalize().strip()
    hist = get_companydata(ticker, column)
    fig = hist.plot(color ='#3a7f9e')
    plt.ylabel('Price(USD)')
    plt.suptitle(ticker + ' USD over time for ' + column, fontsize=16)
    #plt.show() 
    img = fig2img(fig)
    html = f'''
    
    <img src=\'data:image/png;base64,{img}\' width="400px" >
    <form action="/" method="get">
    <br>
    <button>Start again</button>
    </form>
    ''' 
    return html 

def fig2img(fig):
    """Convert a Matplotlib figure to a PIL Image and return it"""
    import io
    from PIL import Image
    import base64
    tmpfile = io.BytesIO()
    #This below is saving to memory instead of as a file savefig('ye.png') tmpfile is a psuedofile memory location
    fig.figure.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    return encoded



    
# Percent change per day
@doggo.get("/graph2/", response_class=HTMLResponse)
def pct_day(ticker, column):
    plt.clf()
    hist = get_companydata(ticker, column)
    pct_changegraph = hist.pct_change()*100
    fig = pct_changegraph.plot(color=['#26bbaa'])
    plt.ylabel('Percent change per day')
    plt.suptitle('Percent change per day '+ ticker, fontsize=16)
    #plt.show()

    img_pctday = fig2img(fig)
    html = f'''
    <img src=\'data:image/png;base64,{img_pctday}\'>
    <form action="" method="get">
    <input name="ticker"></input>
    <input name="column"></input>
    <button>No</button>
    </form>
   
    ''' 
    return html

    # print(hist['pct_change'].mean()*100, 'Mean % change per day')
    # print(hist['pct_change'].std()*100, 'standard deviation of % change per day)')

@doggo.get("/graph3/")
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
    

@doggo.get("/everything/")
def stonk_study(ticker):
    price_time(ticker)
    pct_day(ticker)
    year_change(ticker)
    
@doggo.get("/inputtest", response_class=HTMLResponse)
def dsa(foo: str = None):
    return f"""
    <form action="" method="get">
    <input name="foo"></input>
    <button>Enter</button>
    </form>
    <p>{foo}</p>
    """

#uvicorn name_of_file:fastAPI_variable --reload

#uvicorn main:doggo --reload
#put that in terminal below 
# Example http://127.0.0.1:8000/basic/?ticker=MSFT&column=Close

# Error loading ASGI app. Could not import module "main".
# pwd - print working directory
# ls - to list the filed
# cd NameofFile 
# then go onto the file the main.py is in 