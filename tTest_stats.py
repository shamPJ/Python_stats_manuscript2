import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

class tTest:
   
    colors = ['w','g'] # class vars
    edge_col = 'g'
        
    def __init__(self,csv_file,xVar, yVar, xVar_order = None):
        
        """
        Takes as input name of csv file (string) and returns dataframe.
        Specify independent (xVar) and dependent (yVar) variables (as list 
        with one string element). Order of xVar categories (e.g. wt,ko vs 
        ko,wt) in the stats tables could be specifyed if list of str is given.
        CSV files with different delimiters could be read by using
        'sep = None, engine = 'python'' expression.
        """        
        self.title = csv_file.split('.')[0]       
        df = pd.read_csv(csv_file, sep = None, engine = 'python')
        self.dataframe = df[[xVar,yVar]]
        self.categories_order = xVar_order
       
    def descr_stats(self):
        """
        Returns for each xVar category - sample number, mean, std, sem and
        outliers number.
        Outliers defined as  H3*2*step < values < H1*2*step
        H1 and H3 - 1st and 3rd quartiles, step = 1.5*IQR
        IQR (interquantile range) = H3 - H1       
        """
       
        df = self.dataframe
        xVar, yVar  = self.dataframe.columns.values
        categories_order = self.categories_order
        
        if categories_order == None:
             categories_order = set(df[xVar])
        
        dict_stats = {}
        for e in categories_order:
           temp_df = df[df[xVar] == e]
           H1, H3 = temp_df[yVar].quantile(q=0.25),\
                    temp_df[yVar].quantile(q=0.75)
           step = 1.5*(H3 - H1)
           
           sample_number = len(temp_df[yVar])
           mean = temp_df[yVar].mean()
           std = temp_df[yVar].std()
           sem = temp_df[yVar].sem()
           
           outliers_df = temp_df[(temp_df[yVar] < H1-2*step) | 
                                   (temp_df[yVar] > H3+2*step)]
           outliers_number = len(outliers_df[yVar])
           
           temp_dict = {'sample_number': sample_number,'mean': mean,'std': std,
                        'sem': sem, 'outliers': outliers_number}
           dict_stats[e] = temp_dict
        
        self.outliers = outliers_df
        
        df_stats = pd.DataFrame.from_dict(dict_stats, orient = 'index')
        df_stats_ordered = df_stats.reindex(categories_order)
        file_name = self.title+'descr_stats.csv'
        df_stats_ordered.to_csv(file_name)
        
        for e in categories_order:
            hist = np.histogram(df[yVar][df[xVar] == e])
            plt.hist(df[yVar][df[xVar] == e], bins='auto', label = e)
        plt.legend()    
        plt.show()
        
        return df_stats_ordered
        
    def tTest_stats(self):
        df = self.dataframe 
        xVar, yVar  = self.dataframe.columns.values
        categories_order = self.categories_order
        tstat, pvalue = stats.ttest_ind(df[yVar][df[xVar] == categories_order[0]],
                                        df[yVar][df[xVar] == categories_order[1]])
        print ('t_statistics:',tstat,' p_value:',pvalue)
        #{'t_statistics':tstat,'p_value':pvalue}
        #return 
    
    def bar_graph(self):
        df = self.dataframe 
        x_labels = self.categories_order
        xVar, yVar  = self.dataframe.columns.values
        y_axis = [df[yVar][df[xVar] == x_labels[0]],
                     df[yVar][df[xVar] == x_labels[1]]]        
        x1, x2 = np.random.normal(0.7, 0.1, len(y_axis[0])),\
                 np.random.normal(1.7, 0.1, len(y_axis[1])), 
              
        plt.scatter([x1,x2],y_axis)
        plt.boxplot(y_axis)
    
    def outliers(self):
        
        """
        """
        #self.outliers = outliers_df
        pass
    
    def rm_outliers(self):
        
        """ 
        Takes as input dataframe and returns new dataframe with outliers
        removed.Outliers removed from yVar for each group separately 
        (groups defined by xVar).
        Outliers defined as  H3*2*step < values < H1*2*step
        H1 and H3 - 1st and 3rd quartiles, step = 1.5*IQR
        IQR (interquantile range) = H3 - H1
        """
        
        pass
    
    

        
    
