#%%
import pandas as pd
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64

# Power verisini oku
power = pd.read_csv('/Users/berkanyuce/Desktop/Workintech/Kişisel Projeler/interview1/ML/power_usage_2016_to_2020.csv')

# Verinin boyutunu al
n = power.shape[0]

# DateTime sütununu oluştur
p1 = pd.Series(range(n), pd.period_range('2016-06-01 00:00:00', freq='1H', periods=n))
power['DateTime'] = p1.to_frame().index

# DateTime sütununu indeks olarak ayarla
power = power.set_index('DateTime')

# Saatlik veriyi günlük olarak toplamak için yeniden örnekle
daily_power = power.resample('D').sum()

# Günlük toplamların dataframe'indeki tarih sütununun adını değiştirebilirsiniz
daily_power.index.name = 'Date'

# Weather verisini oku
weather = pd.read_csv('/Users/berkanyuce/Desktop/Workintech/Kişisel Projeler/interview1/ML/weather_2016_2020_daily.csv')

# Weather verisinin boyutunu al
m = weather.shape[0]

# Date sütununu oluştur
p2 = pd.Series(range(m), pd.period_range('2016-06-01', freq='1D', periods=m))
weather['Date'] = p2.to_frame().index

# Weather verisini belirli bir süreye indir
weather = weather[:1498]

# Weather verisini Date sütununu indeks olarak ayarla
weather = weather.set_index('Date')

# Daily_power veri setindeki sütunları weather veri setine ekle
weather = weather.join(daily_power, how='left', lsuffix='_weather', rsuffix='_power')

# Birleştirilmiş veriyi görüntüle (ilk 5 gün için)
print(weather.head())




# Calculate HDD
# HDD = (65 F - Tm) Here; Tm =  Average daily temp
# If Tm > 65 F (Base Tempeture), HDD = 0. 
# Resource: https://mrcc.purdue.edu/CLIMATE/Station/Daily/degreeday_description.html

# HDD Calculation
weather['HDD'] = weather['Temp_avg'].apply(lambda Tm: max(65 - Tm, 0))


# Calculate CDD
# CDD = (Tm - 65 F) Burada; Tm = Average daily temp
# If Tm ≤ 65 F (Base Tempeture) , CDD = 0. 
# Resource: https://mrcc.purdue.edu/CLIMATE/Station/Daily/degreeday_description.html

# CDD Calculation
weather['CDD'] = weather['Temp_avg'].apply(lambda Tm: max(Tm - 65, 0))


# Correlation matrix
correlation_matrix = weather.corr()

# Show correlation matrix
# print(correlation_matrix)

# Visualize correlation matrix with heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=.5)
plt.title("Correlation Matrix")
plt.show()

#%%

# Independent features
X = weather[['Temp_max', 'Temp_avg', 'Temp_min', 'Dew_max', 'Dew_avg', 'Dew_min',
          'Hum_max', 'Hum_avg', 'Hum_min', 'Wind_max', 'Wind_avg', 'Wind_min',
          'Press_max', 'Press_avg', 'Press_min', 'Precipit', 'day_of_week_weather', 'HDD', 'CDD']]

# Dependent features. It calculates for HDD and CDD seperately
Y = weather[['Value (kWh)']]

# Function for backward elimination
def backward_elimination(Y, X):
    # Add constant term
    X = sm.add_constant(X)
    # Create the model
    model = sm.OLS(Y, X).fit()
    # Get p-values
    p_values = model.pvalues
    # Threshold value
    threshold = 0.05
    # Drop the feature if the largest p-value is greater than the threshold
    while p_values.max() > threshold:
        max_p_value_index = p_values.argmax()
        X = X.drop(X.columns[max_p_value_index], axis=1)
        model = sm.OLS(Y, X).fit()
        p_values = model.pvalues
    return model

# Build the model and check p-values (for HDD)
model = backward_elimination(Y, X)


# Print the results
print("Model Summary:")
print(model.summary())

#%%

# Get the values ​​predicted by the model
predicted_values = model.predict()

# Get actual values
actual_values = Y.values

# Draw a graph showing the relationship between predicted and actual values
plt.figure(figsize=(10, 6))
plt.scatter(actual_values, predicted_values, color='blue', alpha=0.5)
plt.plot(actual_values, actual_values, color='red', linestyle='--')
plt.title('Gerçek vs. Tahmin Edilen  Değerleri')
plt.xlabel('Gerçek  Değerleri')
plt.ylabel('Tahmin Edilen CDD Değerleri')
plt.grid(True)
plt.show()

