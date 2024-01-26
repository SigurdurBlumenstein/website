##Verðtryggð og óverðtryggð kúrva
import QuantLib as ql
import numpy as np
from dur_yield import *


data = {'RIKB 25 0612': [1.3864295689983808, 0.0903354627625228], 'RIKB 24 0415': [0.2622950819672131, 0.1003460222363472], 
        'RIKB 26 1015': [2.600965223551949, 0.08039818873405458], 'RIKB 28 1115': [4.39492731291943, 0.07313195868676504], 
        'RIKB 31 0124': [5.8467823722019, 0.07006805157557225], 'RIKB 42 0217': [12.052603461552339, 0.06380813660621643], 
        'RIKS 26 0216': [2.083298532793428, 0.03433820395469666], 'RIKS 30 0701': [5.943803944861205, 0.027731483983993534], 
        'RIKS 33 0321': [8.182722337279037, 0.026546119928359993], 'RIKS 37 0115': [12.182722688848974, 0.024178357362747198], 
        'RVKN 35 1': [7.918775048838153, 0.07624127205483008], 'RVK 32 1': [7.86838328076303, 0.034300989580154435], 
        'RVK 53 1': [17.669758614459305, 0.03713076543807983], 'RVKG 48 1': [18.338448312084683, 0.03143909296989442], 
        'OR180255 GB': [21.16844356194149, 0.030683523511886607], 'OR020934 GB': [9.772840151154885, 0.0280449776172638], 
        'OR180242 GB': [11.853913329621976, 0.06312596440315246]}

# data = find_dur_and_yield()


def forward_rate():
    overd_fram_curve = {}
    durations = []
    ytms = []
    keys = []
    for key, value in data.items():
        if(key[:4] == "RIKB"):
            durations.append(value[0])
            ytms.append(value[1])
            keys.append(key[:7])
    combined = list(zip(durations, ytms, keys))
    combined.sort(key=lambda x: x[0])
    for i in range(len(combined) - 1):
        tem_duration1, tem_ytm1, tem_nafn = combined[i]
        temp = []
        temp.append([tem_duration1, tem_ytm1 * 100])
        for x in range(i, len(combined) - 1):
            duration1, ytm1, nafn = combined[i]
            duration2, ytm2, nafn2 = combined[x + 1]
            forward = ((((1 + ytm2) ** duration2) / ((1 + ytm1) ** duration1)) ** (1 / (duration2 - duration1)) - 1) * 100
            temp.append([duration2 , forward])
        overd_fram_curve[nafn] = temp
    return overd_fram_curve

def forward_rate_verdtryggt():
    overd_fram_curve = {}
    durations = []
    ytms = []
    keys = []
    for key, value in data.items():
        if(key[:4] == "RIKS"):
            durations.append(value[0])
            ytms.append(value[1])
            keys.append(key[:7])
    combined = list(zip(durations, ytms, keys))
    combined.sort(key=lambda x: x[0])
    for i in range(len(combined) - 1):
        tem_duration1, tem_ytm1, tem_nafn = combined[i]
        temp = []
        temp.append([tem_duration1, tem_ytm1 * 100])
        for x in range(i, len(combined) - 1):
            duration1, ytm1, nafn = combined[i]
            duration2, ytm2, nafn2 = combined[x + 1]
            forward = ((((1 + ytm2) ** duration2) / ((1 + ytm1) ** duration1)) ** (1 / (duration2 - duration1)) - 1) * 100
            temp.append([duration2 , forward])
        overd_fram_curve[nafn] = temp
    return overd_fram_curve


# def cubic_spline_interpolate_forward_rates(forward_rates):
#     # Sort the items by durations
#     sorted_items = sorted(forward_rates.items(), key=lambda item: item[0])
#     durations = np.array([item[0] for item in sorted_items])
#     rates = np.array([item[1] for item in sorted_items])

#     # Create a cubic spline interpolation function
#     cs = CubicSpline(durations, rates, bc_type='natural')

#     # Estimate the forward rates for each year from 1 to 10
#     interpolated_forward_rates = {f"Years {year}": cs(year) for year in range(1, 11)}

#     return interpolated_forward_rates

fm = forward_rate()
print("Forward Rates:", fm)


# fm = forward_rate_verdtryggt()
# print("Forward Rates:", fm)
# interpolated_fm = cubic_spline_interpolate_forward_rates(fm)
# for key, value in interpolated_fm.items():
#     print(key, f"{value:.4f}") 

    