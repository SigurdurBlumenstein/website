import pandas as pd 
from bloomtest import *

def calculate_weights(length_smaller, length_larger, length_corporate):
    """
    Calculate the weights based on bond lengths.
    Ensure that weighted length of two bonds is the same as the corporate bond length.
    """
    if length_smaller == length_larger:
        # Avoid division by zero in case both lengths are equal
        return 0.5, 0.5

    weight_1 = (length_corporate - length_larger) / (length_smaller - length_larger)
    weight_2 = 1 - weight_1
    return weight_1, weight_2



def credit_spread():
    [data, tafla] = main()
    overdtryggd_rikisbref = ["RIKB 24 0415", "RIKB 25 0612", "RIKB 26 1015", "RIKB 28 1115", "RIKB 31 0124", "RIKB 42 0217"]
    overdtryggt_fyrirtaekja = ["RVKN 35 1", "ARION CB 24", "ARION CB 27", "LBANK CB 25", "LBANK CB 27", "LBANK CB 29", "ISB CB 27", "ISB CBF 27", "ARION 24 1020 GB", "ARION 25 1222 GB", "BRIM 221026 GB", "ISB GB 25 1126", "ISB GB 25 1126", "ISB GB 27 1122", "ISB GBF 27 1122", "KVIKA 24 1216 GB", "KVIKA 25 1201 GB", "LSB280829 GB", "OR161126 GB", "OR161126 GB", "OR180242 GB", "RVKN 24 1", "RVKNG 40 1"]
    rikisbref= {}
    for ind in data.index: 
        if data['Nafn'][ind] in overdtryggd_rikisbref:
            years = data['DUR_MID'][ind]
            try:
                bid_price = data['BID'][ind]
                ask_price = data['ASK'][ind]
                bid_yield = data['YLD_YTM_BID'][ind]
                ask_yield = data['YLD_YTM_ASK'][ind]
                mid_yield = (float(bid_yield)+float(ask_yield))/2
                if data['Nafn'][ind] not in rikisbref.keys():
                    rikisbref[data['Nafn'][ind]] = {}
                rikisbref[data['Nafn'][ind]]['Bid Price'] = bid_price
                rikisbref[data['Nafn'][ind]]['Ask Price'] = ask_price
                rikisbref[data['Nafn'][ind]]['Duration'] = years
                rikisbref[data['Nafn'][ind]]['Bid Yield'] = bid_yield
                rikisbref[data['Nafn'][ind]]['Ask Yield'] = ask_yield 
                rikisbref[data['Nafn'][ind]]['Mid Yield'] = mid_yield  
            except KeyError:
                pass
            



    rikisbref_df = pd.DataFrame.from_dict(rikisbref, orient="index")

    print(rikisbref_df)
            


    fyrirtaeki = {}
    for ind in data.index: 
        if data['Nafn'][ind] in overdtryggt_fyrirtaekja:
            years = data['DUR_MID'][ind]
            try:
                bid_price = data['BID'][ind]
                ask_price = data['ASK'][ind]
                years = data['DUR_MID'][ind]
                bid_yield = data['YLD_YTM_BID'][ind]
                ask_yield = data['YLD_YTM_ASK'][ind]
                mid_yield = (float(bid_yield)+float(ask_yield))/2
                if data['Nafn'][ind] not in rikisbref.keys():
                    fyrirtaeki[data['Nafn'][ind]] = {}
                fyrirtaeki[data['Nafn'][ind]]['Bid Price'] = bid_price
                fyrirtaeki[data['Nafn'][ind]]['Ask Price'] = ask_price
                fyrirtaeki[data['Nafn'][ind]]['Duration'] = years
                fyrirtaeki[data['Nafn'][ind]]['Bid Yield'] = bid_yield
                fyrirtaeki[data['Nafn'][ind]]['Ask Yield'] = ask_yield 
                fyrirtaeki[data['Nafn'][ind]]['Mid Yield'] = mid_yield
            except KeyError:
                pass



    fyrirtaeki_df = pd.DataFrame.from_dict(fyrirtaeki, orient="index")

    print(fyrirtaeki_df)




    krofur = {}
    less = {}
    for j1 in fyrirtaeki.keys(): 
        maxval = 0
        for ind in rikisbref.keys():
            if j1 not in krofur.keys():
                krofur[j1] = {}
            if float(rikisbref[ind]['Duration']) > maxval and float(rikisbref[ind]['Duration']) <= float(fyrirtaeki[j1]['Duration']):
                maxval = float(rikisbref[ind]['Duration'])
                bref = ind
                krafa = float(rikisbref[ind]['Mid Yield'])
        krofur[j1]['Lengd fyrirtækjabréfs'] = float(fyrirtaeki[j1]['Duration'])
        krofur[j1]['Krafa fyrirtækjabréfs'] = float(fyrirtaeki[j1]['Mid Yield'])
        krofur[j1]['Bréf sem er styttra'] = bref
        krofur[j1]['Lengd'] = maxval 
        krofur[j1]['Krafa'] = krafa 



    krofur_df = pd.DataFrame.from_dict(krofur)
    krofur_df = krofur_df.T
    print(krofur_df)



    krafa2 = {}
    for j1 in fyrirtaeki.keys():
        minval =  25 
        go = False 
        for ind in rikisbref.keys():
            for test in rikisbref.keys():
                if float(rikisbref[test]['Duration']) >= float(fyrirtaeki[j1]['Duration']):
                    go = True 
                    break
            if j1 not in krafa2.keys():
                krafa2[j1] = {}
            if go == True:
                if float(rikisbref[ind]['Duration']) < minval and float(rikisbref[ind]['Duration']) >= float(fyrirtaeki[j1]['Duration']):
                    minval = float(rikisbref[ind]['Duration'])
                    bref = ind
                    krafa = float(rikisbref[ind]['Mid Yield'])
                krafa2[j1]['Lengd fyrirtækjabréfs'] = float(fyrirtaeki[j1]['Duration'])
                krafa2[j1]['Krafa fyrirtækjabréfs'] = float(fyrirtaeki[j1]['Mid Yield'])
                krafa2[j1]['Bréf sem er lengra'] = bref
                krafa2[j1]['Lengd'] = minval 
                krafa2[j1]['Krafa'] = krafa 
            elif go == False:
                minval = krofur[j1]['Lengd']
                bref = krofur[j1]['Bréf sem er styttra']
                krafa = krofur[j1]['Krafa']
                krafa2[j1]['Lengd fyrirtækjabréfs'] = float(fyrirtaeki[j1]['Duration'])
                krafa2[j1]['Krafa fyrirtækjabréfs'] = float(fyrirtaeki[j1]['Mid Yield'])
                krafa2[j1]['Bréf sem er lengra'] = bref 
                krafa2[j1]['Lengd'] = minval 
                krafa2[j1]['Krafa'] = krafa



    krafa2_df = pd.DataFrame.from_dict(krafa2)
    krafa2_df = krafa2_df.T
    print(krafa2_df)
    finalkrofudict = krofur_df.join(krafa2_df, lsuffix = '_Minni', rsuffix ='_Stærri')
    finalkrofudict = finalkrofudict.reset_index()

    vigtir = {}
    for ind in finalkrofudict.index:
        length_smaller = finalkrofudict['Lengd_Minni'][ind]
        length_larger = finalkrofudict['Lengd_Stærri'][ind]
        length_corporate = finalkrofudict['Lengd fyrirtækjabréfs_Minni'][ind]

        w1, w2 = calculate_weights(length_smaller, length_larger, length_corporate)

        vigtir[ind] = {
            'Vigt 1': w1,
            'Vigt 2': w2,
            'Vigtuð krafa': w1 * finalkrofudict['Krafa_Minni'][ind] + w2 * finalkrofudict['Krafa_Stærri'][ind],
            'Credit Spread': finalkrofudict['Krafa fyrirtækjabréfs_Stærri'][ind] - (w1 * finalkrofudict['Krafa_Minni'][ind] + w2 * finalkrofudict['Krafa_Stærri'][ind])
        }


    vigtir_df = pd.DataFrame.from_dict(vigtir)
    vigtir_df = vigtir_df.transpose()
    final1 = finalkrofudict.join(vigtir_df)
    final1 = final1.drop('Lengd fyrirtækjabréfs_Stærri', axis=1)
    final1 = final1.drop('Lengd fyrirtækjabréfs_Minni', axis=1)
    final1 = final1.drop('Krafa fyrirtækjabréfs_Stærri', axis=1)
    print(final1)

    lokatafla = []

    for ind in final1.index: 
        lokatafla.append([final1['index'][ind], final1['Vigtuð krafa'][ind], final1['Krafa fyrirtækjabréfs_Minni'][ind], final1['Credit Spread'][ind]])
    print(lokatafla)


    ########################################################################################################## 

    verdtryggd_rikisbref = ["RIKS 26 0216", "RIKS 30 0701", "RIKS 33 0321", "RIKS 37 0115"]
    verdtryggt_fyrirtaekja = ["HFF150224", "HFF150434", "HFF150644", "LSS150224", "LSS150434", "LSS151155", "LSS 39 0303", "OR020934 GB", "OR090546", "OR180255 GB", "RVK 32 1", "RVK 53 1", "ARION CBI 25", "ARION CBI 29", "ARION CBI 30", "ARION CBI 48", "LBANK CBI 24", "LBANK CBI 26", "LBANK CBI 28", "ISB CBI 24", "ISB CBI 26", "ISB CBI 28", "ISB CBI 29", "ISB CBI 30", "REGINN181037 GB", "REGINN27 GB", "REGINN50 GB", "RVKG 48 1", "ARBO 31 GSB", "FB100366 SB", "GROSKA 29 GB", "IS Kredit 61 SB", "LL 010641 GB", "LSS40440 GB" ]
    rikisbref= {}
    for ind in data.index: 
        if data['Nafn'][ind] in verdtryggd_rikisbref:
            years = data['DUR_MID'][ind]
            try:
                bid_price = data['BID'][ind]
                ask_price = data['ASK'][ind]
                bid_yield = data['YLD_YTM_BID'][ind]
                ask_yield = data['YLD_YTM_ASK'][ind]
                mid_yield = (float(bid_yield)+float(ask_yield))/2
                if data['Nafn'][ind] not in rikisbref.keys():
                    rikisbref[data['Nafn'][ind]] = {}
                rikisbref[data['Nafn'][ind]]['Bid Price'] = bid_price
                rikisbref[data['Nafn'][ind]]['Ask Price'] = ask_price
                rikisbref[data['Nafn'][ind]]['Duration'] = years
                rikisbref[data['Nafn'][ind]]['Bid Yield'] = bid_yield
                rikisbref[data['Nafn'][ind]]['Ask Yield'] = ask_yield 
                rikisbref[data['Nafn'][ind]]['Mid Yield'] = mid_yield  
            except KeyError:
                pass
            



    rikisbref_df = pd.DataFrame.from_dict(rikisbref, orient="index")

    print(rikisbref_df)
            


    fyrirtaeki = {}
    for ind in data.index: 
        if data['Nafn'][ind] in verdtryggt_fyrirtaekja:
            years = data['DUR_MID'][ind]
            try:
                bid_price = data['BID'][ind]
                ask_price = data['ASK'][ind]
                years = data['DUR_MID'][ind]
                bid_yield = data['YLD_YTM_BID'][ind]
                ask_yield = data['YLD_YTM_ASK'][ind]
                mid_yield = (float(bid_yield)+float(ask_yield))/2
                if data['Nafn'][ind] not in rikisbref.keys():
                    fyrirtaeki[data['Nafn'][ind]] = {}
                fyrirtaeki[data['Nafn'][ind]]['Bid Price'] = bid_price
                fyrirtaeki[data['Nafn'][ind]]['Ask Price'] = ask_price
                fyrirtaeki[data['Nafn'][ind]]['Duration'] = years
                fyrirtaeki[data['Nafn'][ind]]['Bid Yield'] = bid_yield
                fyrirtaeki[data['Nafn'][ind]]['Ask Yield'] = ask_yield 
                fyrirtaeki[data['Nafn'][ind]]['Mid Yield'] = mid_yield
            except KeyError:
                pass



    fyrirtaeki_df = pd.DataFrame.from_dict(fyrirtaeki, orient="index")

    print(fyrirtaeki_df)




    krofur = {}
    less = {}
    for j1 in fyrirtaeki.keys(): 
        maxval = 0
        for ind in rikisbref.keys():
            if j1 not in krofur.keys():
                krofur[j1] = {}
            if float(rikisbref[ind]['Duration']) > maxval and float(rikisbref[ind]['Duration']) <= float(fyrirtaeki[j1]['Duration']):
                maxval = float(rikisbref[ind]['Duration'])
                bref = ind
                krafa = float(rikisbref[ind]['Mid Yield'])
        krofur[j1]['Lengd fyrirtækjabréfs'] = float(fyrirtaeki[j1]['Duration'])
        krofur[j1]['Krafa fyrirtækjabréfs'] = float(fyrirtaeki[j1]['Mid Yield'])
        krofur[j1]['Bréf sem er styttra'] = bref
        krofur[j1]['Lengd'] = maxval 
        krofur[j1]['Krafa'] = krafa 



    krofur_df = pd.DataFrame.from_dict(krofur)
    krofur_df = krofur_df.T
    print(krofur_df)



    krafa2 = {}
    for j1 in fyrirtaeki.keys():
        minval =  25 
        go = False 
        for ind in rikisbref.keys():
            for test in rikisbref.keys():
                if float(rikisbref[test]['Duration']) >= float(fyrirtaeki[j1]['Duration']):
                    go = True 
                    break
            if j1 not in krafa2.keys():
                krafa2[j1] = {}
            if go == True:
                if float(rikisbref[ind]['Duration']) < minval and float(rikisbref[ind]['Duration']) >= float(fyrirtaeki[j1]['Duration']):
                    minval = float(rikisbref[ind]['Duration'])
                    bref = ind
                    krafa = float(rikisbref[ind]['Mid Yield'])
                krafa2[j1]['Lengd fyrirtækjabréfs'] = float(fyrirtaeki[j1]['Duration'])
                krafa2[j1]['Krafa fyrirtækjabréfs'] = float(fyrirtaeki[j1]['Mid Yield'])
                krafa2[j1]['Bréf sem er lengra'] = bref
                krafa2[j1]['Lengd'] = minval 
                krafa2[j1]['Krafa'] = krafa 
            elif go == False:
                minval = krofur[j1]['Lengd']
                bref = krofur[j1]['Bréf sem er styttra']
                krafa = krofur[j1]['Krafa']
                krafa2[j1]['Lengd fyrirtækjabréfs'] = float(fyrirtaeki[j1]['Duration'])
                krafa2[j1]['Krafa fyrirtækjabréfs'] = float(fyrirtaeki[j1]['Mid Yield'])
                krafa2[j1]['Bréf sem er lengra'] = bref 
                krafa2[j1]['Lengd'] = minval 
                krafa2[j1]['Krafa'] = krafa



    krafa2_df = pd.DataFrame.from_dict(krafa2)
    krafa2_df = krafa2_df.T
    print(krafa2_df)
    finalkrofudict = krofur_df.join(krafa2_df, lsuffix = '_Minni', rsuffix ='_Stærri')
    finalkrofudict = finalkrofudict.reset_index()

    vigtir = {}
    for ind in finalkrofudict.index:
        length_smaller = finalkrofudict['Lengd_Minni'][ind]
        length_larger = finalkrofudict['Lengd_Stærri'][ind]
        length_corporate = finalkrofudict['Lengd fyrirtækjabréfs_Minni'][ind]

        w1, w2 = calculate_weights(length_smaller, length_larger, length_corporate)

        vigtir[ind] = {
            'Vigt 1': w1,
            'Vigt 2': w2,
            'Vigtuð krafa': w1 * finalkrofudict['Krafa_Minni'][ind] + w2 * finalkrofudict['Krafa_Stærri'][ind],
            'Credit Spread': finalkrofudict['Krafa fyrirtækjabréfs_Stærri'][ind] - (w1 * finalkrofudict['Krafa_Minni'][ind] + w2 * finalkrofudict['Krafa_Stærri'][ind])
        }


    vigtir_df = pd.DataFrame.from_dict(vigtir)
    vigtir_df = vigtir_df.transpose()
    final2 = finalkrofudict.join(vigtir_df)
    final2 = final2.drop('Lengd fyrirtækjabréfs_Stærri', axis=1)
    final2 = final2.drop('Lengd fyrirtækjabréfs_Minni', axis=1)
    final2 = final2.drop('Krafa fyrirtækjabréfs_Stærri', axis=1)
    print(final2)

    lokatafla2 = []
    for ind in final2.index: 
        lokatafla2.append([final2['index'][ind], final2['Vigtuð krafa'][ind], final2['Krafa fyrirtækjabréfs_Minni'][ind], final2['Credit Spread'][ind]])
    lokatafla2 = lokatafla2 + lokatafla
    return lokatafla2