import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

class tTest:
   
    colors = ['w','g'] # class vars
    edgecolor = 'g'
        
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
        
        self.outliers = outliers_df # for removing outliers (outliers())
        self.stats = dict_stats # for creating bar graph (bar_graph())
        
        # exporting results
        df_stats = pd.DataFrame.from_dict(dict_stats, orient = 'index')
        df_stats_ordered = df_stats.reindex(categories_order)
        file_name = self.title+'_descr_stats.csv'
        df_stats_ordered.to_csv(file_name)
        
        # plotting histogram
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
        df = len(df[yVar])-2
        print ('t_statistics:',tstat,'df:',df,' p_value:',pvalue)
        
        # exporting results
        tTest_stats_dict = {'t_statistics':tstat,'df':df,'p_value':pvalue}
        tTest_stats = pd.DataFrame.from_dict(tTest_stats_dict, 
                                             orient = 'index')
        file_name = self.title+'tTest_stats.csv'
        tTest_stats.to_csv(file_name)
        
        return tTest_stats
    
    def bar_graph(self):
        df = self.dataframe 
        x_labels = self.categories_order
        xVar, yVar  = self.dataframe.columns.values
        colors = tTest.colors
        edgecolor = tTest.edgecolor
        
        # boxplot with scatter
        fig = plt.figure()
        
        y_axis = []
        for i in range(len(x_labels)): 
            values = list(df[yVar][df[xVar] == x_labels[i]])
            y_axis.append(values)
        
        position_scatter_loc = [x-0.3 for x in list(range(1,len(y_axis)+1,1))]
        position_scatter_jitter = []
        for i in range(len(y_axis)):
            position_scatter_jitter.append(np.random.normal(position_scatter_loc[i],
                                                   0.05,len(y_axis[i])))
        for i in range(len(y_axis)): 
            plt.scatter(position_scatter_jitter[i], y_axis[i],c = 'k', alpha = 0.5, 
                        label = None, zorder = 2)    
                
        box =  plt.boxplot(y_axis, labels = x_labels, patch_artist=True, zorder = 1) 
        plt.tick_params(labelsize=18)
        for patch, color in zip(box['boxes'], colors):
            patch.set(color = color, linewidth=2)
            patch.set_edgecolor(edgecolor)  
        for median in box['medians']:
            median.set(color='#b2df8a', linewidth=2)
        for whisker in box['whiskers']:
            whisker.set(linewidth=2) 
        for cap in box['caps']:
            cap.set(linewidth=2)              
        fig.show()
        # fig save
        fig_name = self.title + '_boxplot_graph.tiff'
        fig.savefig(fig_name, dpi = 300)
        
        # scatter and bar graph (mean,sem)   
        # getting stats
        self.descr_stats()
        dict_stats = self.stats
        mean = []
        sem = []
        labels = []        
        for key in dict_stats:
            mean.append(dict_stats[key]['mean'])
            sem.append(dict_stats[key]['sem'])
            labels.append(key)
            
        # plotting figures    
        plt.rcParams["font.weight"] = "bold"
        plt.rcParams['axes.linewidth'] = 2     
        
        fig = plt.figure(figsize=(3, 5))
        ax = plt.subplot(111)    
        
        # setting position of bars and scatter on x-axis
        position_bar = list(range(1,len(y_axis)+1,1))
        position_scatter = []
        for i in range(len(y_axis)):
            position_scatter.append(np.random.normal(position_bar[i],
                                                   0.1,len(y_axis[i])))
        # plotting graphs        
        ax.bar(position_bar,mean,yerr = sem, color = colors,
               edgecolor = edgecolor, lw = 2, zorder = 1)
        for i in range(len(y_axis)): 
            ax.scatter(position_scatter[i], y_axis[i],c = 'k', alpha = 0.5, 
                       zorder = 2, label = None)
        # axis formatting
        y_max = max(df[yVar])
        ax.set_yticks(np.arange(0,y_max+(y_max/4),y_max/4))
        ax.set_xticks(position_bar)
        ax.set_xticklabels(labels)
        ax.tick_params(labelsize=18)
        ax.tick_params(axis = 'x',length = 0)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        
        fig.show()
        # fig save
        fig.tight_layout()
        fig_name = self.title + '_bar_graph.tiff'
        fig.savefig(fig_name, dpi = 300)
        
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
    
    

        
    
