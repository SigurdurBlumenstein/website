import QuantLib as ql
from datetime import date
from bloomtest import * 
from datetime import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta as rd


def calculate_macaulay_duration(final_maturity, coupon, mid_yield, face_value=100.0):
    today = datetime.today()
    dates = []
    while(final_maturity > today):
        dates.append(final_maturity)
        final_maturity = final_maturity - rd(years=1)
    dates.reverse()

    T = []
    for date in dates:
        between = date - today
        T.append(between.days/365)
    coupons = [coupon] * (len(T) - 1)
    coupons.append(coupon + face_value)

    PV = []
    for i in range(len(coupons)):
        pv = coupons[i] / ((1 + (mid_yield / 100))**T[i])
        PV.append(pv)

    PV_T = []
    for i in range(len(PV)):
        pv_t = PV[i] * T[i]
        PV_T.append(pv_t)
    mac_dur = sum(PV_T) / sum(PV)
    return mac_dur

k = calculate_macaulay_duration(datetime(2037,1,15), 1, 2.33)
print(k)

def find_dur_and_yield():
    # data = {
    #     'Nafn': [
    #         'RIKB 24 0415', 'RIKB 25 0612', 'RIKB 26 1015', 'RIKB 28 1115',
    #         'RIKB 31 0124', 'RIKB 42 0217', 'RIKS 26 0216', 'RIKS 30 0701',
    #         'RIKS 33 0321', 'RIKS 37 0115'
    #     ],
    #     'BID': [
    #         98.220000, 98.775000, 96.930000, 91.070000,
    #         97.410000, 80.200000, 96.225000, 102.450000,
    #         102.500000, 84.260000
    #     ],
    #     'ASK': [
    #         98.310000, 98.915000, 97.140000, 91.310000,
    #         97.870000, 80.950000, 96.440000, 102.860000,
    #         103.040000, 84.980000
    #     ],
    #     'YLD_YTM_BID': [
    #         10.005134, 8.899408, 8.018118, 7.249595,
    #         6.977909, 6.374167, 3.402787, 2.827737,
    #         2.688334, 2.426246
    #     ],
    #     'YLD_YTM_ASK': [
    #         9.608227, 8.789011, 7.928399, 7.185373,
    #         6.891682, 6.292187, 3.291426, 2.758645,
    #         2.622383, 2.354674
    #     ],
    #     'CPN': [
    #         2.500000, 8.000000, 6.750000, 5.000000,
    #         6.500000, 4.500000, 1.500000, 3.250000,
    #         3.000000, 1.000000
    #     ],
    #     'AMT_OUTSTANDING': [
    #         89387762192.000000, 109762963000.000000, 54195400000.000000, 113464801519.000015,
    #         124632500000.000000, 58012000000.000000, 83592700000.000000, 78683199659.000000,
    #         79393919842.000000, 52978600000.000000
    #     ],
    #     'CPN_FREQ': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #     'DUR_MID': [
    #         0.231950, 1.332494, 2.559747, 4.354014,
    #         5.486403, 11.489590, 2.029690, 5.621442,
    #         7.588543, 12.078951
    #     ],
    #     'DAYS_TO_NEXT_COUPON': [91, 149, 274, 305, 9, 33, 32, 168, 66, 366],
    #     'FINAL_MATURITY': [
    #         '2024-04-15', '2025-06-12', '2026-10-15', '2028-11-15',
    #         '2031-01-24', '2042-02-17', '2026-02-16', '2030-07-01',
    #         '2033-03-21', '2037-01-15'
    #     ]
    # }
    # # Convert the dictionary into a DataFrame
    # tafla = pd.DataFrame(data)
    [tafla, dicti] = main()
    dic = {}
    for ind in tafla.index:
        bid = tafla['BID'][ind]
        ask = tafla['ASK'][ind]
        if pd.isna(bid) == False and pd.isna(ask) == False:
            if tafla['Nafn'][ind] not in dic.keys():
                dic[tafla['Nafn'][ind]] = {}
            dic[tafla['Nafn'][ind]]['Mid Price'] = (float(tafla['BID'][ind])+float(tafla['ASK'][ind]))/2 
            dic[tafla['Nafn'][ind]]['Final Maturity'] = datetime.strptime(tafla['FINAL_MATURITY'][ind], "%Y-%m-%d")
            dic[tafla['Nafn'][ind]]['Coupon Frequency'] = tafla['CPN_FREQ'][ind]
            dic[tafla['Nafn'][ind]]['Coupon'] = tafla['CPN'][ind]
            dic[tafla['Nafn'][ind]]['Mid Yield'] = (float(tafla['YLD_YTM_BID'][ind])+float(tafla['YLD_YTM_ASK'][ind]))/2 

    result = {}
    for key in dic.keys():
        final_maturity = dic[key]['Final Maturity']
        coupon = dic[key]['Coupon']
        coupon = float(coupon)
        mid_yield = dic[key]['Mid Yield']
        print(coupon , mid_yield)
        print(type(coupon) , type(mid_yield))
        face_value = 100  # Assuming a face value of 100
        macaulay_duration = calculate_macaulay_duration(final_maturity, coupon, mid_yield, face_value)
        
        # Store the Macaulay Duration in the result dictionary
        result[key] = macaulay_duration
        
    return result

fm = find_dur_and_yield()
for key, value in fm.items():
    print(key, value)

# Calculate YTM
# market_yield = fixed_rate_bond.bondYield(market_price, ql.ActualActual(ql.ActualActual.ISDA), ql.Compounded, frequency)
# print("Market yield", market_yield)
# print("Mid yield", mid_yield) 
# Calculate duration