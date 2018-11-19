def TWANOVA(data,x1,x2,y):
    
  import pandas as pd
  from statsmodels.graphics.factorplots import interaction_plot
  from scipy import stats

  # import the data
  data = pd.read_csv(data, sep='\t', header = (0))

  '''Input - csv with data, independent factor 1,2; dependent factor (as col names, string);
  Calculating sum of squares (SS):
  Total (SSt), Between-Groups (SSb) for each factor, 
  Within-Group (Error or SSw)
  and interaction SSi variability. 
  SSt = SSx1+SSx2+SSi+SSw
  Adopted from https://www.marsja.se/three-ways-to-carry-out-2-way-anova-with-python/'''
  
  # Grand mean
  grand_mean = data[y].mean()

  # SS total 
  SSt = sum((data[y] - grand_mean)**2)
  
  # SS for factors x1 and x2
  SSx1 = sum([(data[y][data[x1] ==e].mean()-grand_mean)**2 for e in data[x1]])
  SSx2 = sum([(data[y][data[x2] ==e].mean()-grand_mean)**2 for e in data[x2]])
  
  # SS within (error/residual)
  SSw=0   
  for i in range(len(data[y])):
      str_x1=data[x1][i]
      str_x2=data[x2][i]
      SSw=SSw+((data[y][i]-data[y][(data[x1]==str_x1) & (data[x2]==str_x2)].mean())**2)     
      
  # SS interaction
  SSi = SSt-SSx1-SSx2-SSw

  # degrees of freedom
  N = len(data[y])
  df_x1 = len(data[x1].unique()) - 1 # levels of factor -1 
  df_x2 = len(data[x2].unique()) - 1
  df_i = df_x1*df_x2
  df_w = N - (len(data[x1].unique())*len(data[x2].unique()))
  
  # mean squares
  MS_x1 = SSx1/df_x1
  MS_x2 = SSx2/df_x2
  MS_i = SSi/df_i
  MS_w = SSw/df_w

  # F-ratio
  f_x1 = MS_x1/MS_w
  f_x2 = MS_x2/MS_w
  f_i = MS_i/MS_w

  # p-values
  p_x1 = stats.f.sf(f_x1, df_x1, df_w)
  p_x2 = stats.f.sf(f_x2, df_x2, df_w)
  p_i = stats.f.sf(f_i, df_i, df_w)
  
  #printing results
  results = {'SS':[SSx1, SSx2,SSi,SSw],
           'df':[df_x1,df_x2,df_i,df_w],
           'F':[f_x1,f_x2,f_i,'NaN'],
           'PR(>F)':[p_x1,p_x2,p_i,'NaN']}
  columns=['SS', 'df', 'F', 'PR(>F)']
 
  table = pd.DataFrame(results, columns=columns,
                          index=['Genotype', 'Treatment', 
                          'GenotypexTreatment', 'Residual'])
  print(table)  
  
  # interaction plot
  fig = interaction_plot(data[x1], data[x2], data[y],
             colors=['red','blue'], markers=['D','^'], ms=10)

  # post-hoc Tukey's test
  x1_x2 = []
  for i in range(len(data[y])):
      x1_x2.append(data[x1][i] +'_'+ data[x2][i])
      
  from statsmodels.stats.multicomp import pairwise_tukeyhsd
  print (pairwise_tukeyhsd(data[y], x1_x2,alpha=0.05))






  
