from pandas_datareader import wb
import matplotlib.pyplot as plt

mathces = wb.search('gni.*capita.*const')
 
#grab indicator,country, period I want and load into data frame
df = wb.download(indicator='NY.GNP.PCAP.CD', country=['CL', 'UY', 'HU'], start=1990, end=2010)

#df is "pivoted", pandas' unstack fucntion helps reshape it into something plottable
dfu = df.unstack(level=0)

# a simple matplotlib plot with legend, labels and a title
dfu.plot(); 
plt.legend(loc='best'); 
plt.title("GNI Per Capita ($USD, Atlas Method)"); 
plt.xlabel('Date'); plt.ylabel('GNI Per Capita ($USD, Atlas Method');
plt.show();
