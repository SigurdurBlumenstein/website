import blpapi
import pandas as pd
import time 
import datetime
from itertools import islice


def chunks(data, SIZE=10000):
    it = iter(data)
    for i in range(0, len(data), SIZE):
        yield {k:data[k] for k in islice(it, SIZE)}


def is_market_open():
    current_time = datetime.datetime.now().time()
    market_close_time = datetime.time(16, 0)  # 16:00 hours

    return current_time < market_close_time

def sendRequest(session, tickers):
    # Obtain the reference data service
    refDataService = session.getService("//blp/refdata")

    # Create a request for bond data
    request = refDataService.createRequest("ReferenceDataRequest")

    # Add securities to the request
    for ticker in tickers:
        request.getElement("securities").appendValue(f'{ticker}')

    # Add fields to the request
    request.getElement("fields").appendValue("BID")
    request.getElement("fields").appendValue("ASK")
    request.getElement("fields").appendValue("YLD_YTM_BID")
    request.getElement("fields").appendValue("YLD_YTM_ASK")
    request.getElement("fields").appendValue("CPN")
    request.getElement("fields").appendValue("AMT_OUTSTANDING")
    request.getElement("fields").appendValue("CPN_FREQ")
    request.getElement("fields").appendValue("DUR_MID")
    request.getElement("fields").appendValue("DAYS_TO_NEXT_COUPON")
    request.getElement("fields").appendValue("FINAL_MATURITY")
    

    # Send the request
    session.sendRequest(request)

def processResponse(event):
    returndict = {}
    tickerlist = {
                'RIKB 25 0612': 'EH856574@EXCH     Corp', 'RIKB 24 0415': 'BP415428@EXCH     Corp',
                'RIKB 26 1015': 'ZM550820@EXCH     Corp', 'RIKB 28 1115': 'AM216492@EXCH     Corp',
                'RIKB 31 0124': 'EI543139@EXCH     Corp', 'RIKB 42 0217': 'BU935789@EXCH     Corp',
                'RIKS 26 0216': 'AV822915@EXCH     Corp', 'RIKS 30 0701': 'EI719451@EXCH     Corp',
                'RIKS 33 0321': 'EJ106481@EXCH     Corp', 'RIKS 37 0115': 'BT641009@EXCH     Corp',
                'RVKN 35 1': 'LW833191@EXCH     Corp', 'RVK 32 1': 'BO948965@EXCH     Corp',
                'RVK 53 1': 'EJ965736@EXCH     Corp', 'RVKN24 1': 'BR416346@EXCH Corp',
                'RVKNG 40 1': 'BO992153@EXCH Corp', 'RVKG 48 1': 'BO720110@EXCH Corp',
                'OR090546': 'BO924765@EXCH Corp', 'OR180255 GB': 'ZP725965@EXCH Corp',
                'OR020934 GB': 'ZP725685@EXCH Corp', 'OR180242 GB': 'BR384814@EXCH Corp',
                'HFF150224': None, 'HFF150434': None,
                'HFF150644': None, 'LSS150224': None,
                'LSS150434': None, 'LSS151155': None,
                'LSS 39 0303': None, 'ARION CBI 25': None,
                'ARION CBI 29': None, 'ARION CBI 30': None,
                'ARION CBI 48': None, 'LBANK CBI 24': None,
                'LBANK CBI 26': None, 'LBANK CBI 28': None,
                'ISB CBI 24': None, 'ISB CBI 26': None,
                'ISB CBI 28': None, 'ISB CBI 29': None,
                'ISB CBI 30': None, 'REGINN181037 GB': None,
                'REGINN27 GB': None, 'REGINN50 GB': None,
                'ARBO 31 GSB': None, 'FB100366 SB': None,
                'GROSKA 29 GB': None, 'IS Kredit 61 SB': None,
                'LL 010641 GB': None, 'LSS40440 GB': None

                    }
    inv_map = {v: k for k, v in tickerlist.items()}
    for msg in event:
        if event.eventType() == blpapi.Event.RESPONSE:
            securities = msg.getElement("securityData")

            for i in range(securities.numValues()):
                securityData = securities.getValueAsElement(i)
                ticker = securityData.getElementAsString("security")
            
                for field in securityData.getElement("fieldData").elements():
                    field_name = field.name()
                    field_value = field.getValueAsString()
                    if inv_map[str(ticker)] not in returndict.keys():
                        returndict[inv_map[str(ticker)]] = {} 
                    returndict[inv_map[str(ticker)]][str(field_name)] = field_value
    
                    
    return returndict


def main():
    # Input Bloomberg server details
    host = "localhost"
    port = 8194

    # Establish a connection to the Bloomberg Terminal
    sessionOptions = blpapi.SessionOptions()
    sessionOptions.setServerHost(host)
    sessionOptions.setServerPort(port)

    session = blpapi.Session(sessionOptions)
    if not session.start():
        print("Failed to start session.")
        return

    try:
        if not session.openService("//blp/refdata"):
            print("Failed to open //blp/refdata service")
            return
        uppls = {}
        tickerlist = {'RIKB 24 0415': 'BP415428@EXCH     Corp', 'RIKB 25 0612': 'EH856574@EXCH     Corp', 'RIKB 26 1015': 'ZM550820@EXCH     Corp',
                       'RIKB 28 1115': 'AM216492@EXCH     Corp', 'RIKB 31 0124': 'EI543139@EXCH     Corp', 'RIKB 42 0217': 'BU935789@EXCH     Corp', 
                       'RIKS 26 0216': 'AV822915@EXCH     Corp', 'RIKS 30 0701': 'EI719451@EXCH     Corp', 'RIKS 33 0321': 'EJ106481@EXCH     Corp', 
                       'RIKS 37 0115': 'BT641009@EXCH     Corp', 'RVKN 35 1': 'LW833191@EXCH     Corp', 'RVK 32 1': 'BO948965@EXCH     Corp', 
                       'RVK 53 1': 'EJ965736@EXCH     Corp', 'RVKN24 1': 'BR416346@EXCH Corp', 'RVKNG 40 1': 'BO992153@EXCH Corp', 
                       'RVKG 48 1': 'BO720110@EXCH Corp','OR090546': 'BO924765@EXCH Corp', 'OR180255 GB': 'ZP725965@EXCH Corp', 'OR020934 GB': 'ZP725685@EXCH Corp', 
                       'OR180242 GB': 'BR384814@EXCH Corp'}
        for item in chunks(tickerlist, 10):
            tickerlist = item
            sendRequest(session, tickerlist.values())
            # Process received events
            while True:
                event = session.nextEvent()
                retdict = processResponse(event)
                uppls.update(retdict)
                if event.eventType() == blpapi.Event.RESPONSE:
                    break
    

    finally:
        tafla = pd.DataFrame.from_dict(uppls, orient='index')
        tafla.reset_index(inplace=True)
        tafla.rename(columns={'index':"Nafn"}, inplace=True)
        with pd.ExcelWriter('output63.xlsx', engine='openpyxl') as writer:
            tafla.to_excel(writer, sheet_name='Tafla', index=False)
            pd.DataFrame.from_dict(uppls).to_excel(writer, sheet_name='Uppls', index=True)

    print(tafla)
    return [tafla, uppls]


if __name__ == "__main__":
    # while is_market_open:
    main()