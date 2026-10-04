"""Redraw the adopted external benchmark panels from archived plot inputs."""
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'generated'
OUT.mkdir(exist_ok=True)
DS='GSIM'
sep=pd.read_csv(ROOT/f'data/external/{DS}/panels_ab_separation.csv',float_precision='round_trip')
plot=pd.read_csv(ROOT/f'data/external/{DS}/panel_c_four_line_values.csv',float_precision='round_trip')
features=list(dict.fromkeys(sep.feature))
metrics=['silhouette','calinski_harabasz','gap']
specs=[('MatchedK5','Knoben','MatchedK5','AUDIOSK5 vs KnobenK5','#1A6633','-'),
       ('ClassMean','Koppen','ClassMean','AUDIOS vs Köppen','#EB912E','--'),
       ('ClassMean','Knoben','ClassMean','AUDIOS vs Knoben','#7ACD78','--'),
       ('ClassMean','Knoben','MatchedK5','AUDIOS vs KnobenK5','#1A6633','--')]
plt.rcParams.update({'font.family':['Times New Roman','DejaVu Serif'],'font.size':11,'axes.titlesize':11.5,'axes.labelsize':11.5,
                    'xtick.labelsize':10.7,'ytick.labelsize':10.7,'axes.linewidth':.7,'pdf.fonttype':42,'savefig.facecolor':'white'})
fig=plt.figure(figsize=(8.4,6.2),facecolor='white');axes=[]
cmap=LinearSegmentedColormap.from_list('signed_difference',['#D65A18','#FFFFFF','#2A9D73'])
limits={'silhouette':.25,'calinski_harabasz':100.,'gap':.5}
norms={metric:Normalize(-limit,limit) for metric,limit in limits.items()}
for col,comp in enumerate(['Koppen','Knoben']):
    ax=fig.add_axes([.11+col*.485,.765,.375,.155]);axes.append(ax)
    matrix=sep[sep.comparator==comp].pivot(index='metric',columns='feature',values='delta_continuous_minus_comparator').reindex(index=metrics,columns=features)
    assert not matrix.isna().any().any()
    for row,metric in enumerate(metrics):
        values=matrix.loc[metric].to_numpy()
        assert np.abs(values).max()<=limits[metric]
        ax.imshow(values[None,:],cmap=cmap,norm=norms[metric],aspect='auto',interpolation='nearest',
                  extent=(-.5,17.5,row+.5,row-.5))
    ax.set_xlim(-.5,17.5);ax.set_ylim(2.5,-.5)
    ax.set_xticks(range(18),features,rotation=50,ha='right',rotation_mode='anchor')
    ax.set_yticks(range(3),['Silhouette','CH','Gap'])
    ax.set_xticks(np.arange(-.5,18,1),minor=True);ax.set_yticks(np.arange(-.5,3,1),minor=True)
    ax.grid(which='minor',color='#DDDDDD',linewidth=.35);ax.tick_params(which='both',length=0,pad=5)
    for spine in ax.spines.values():spine.set_color('#777777');spine.set_linewidth(.5)
    ax.set_title(f'({chr(97+col)}) GSIM — '+('Köppen' if comp=='Koppen' else comp),loc='left',pad=8)
for i,(metric,label) in enumerate(zip(metrics,['ΔSilhouette','ΔCH','ΔGap'])):
    cax=fig.add_axes([.15+i*.29,.608,.21,.015])
    cb=fig.colorbar(plt.cm.ScalarMappable(norm=norms[metric],cmap=cmap),cax=cax,orientation='horizontal',
                    ticks=[-limits[metric],0,limits[metric]])
    cb.outline.set_linewidth(.5)
    cb.ax.tick_params(labelsize=10.7,length=2,pad=2)
    cb.ax.set_title(label,fontsize=10.7,pad=5)
ax=fig.add_axes([.11,.145,.86,.37]);axes.append(ax)
for variant,baseline,bvariant,label,color,style in specs:
    values=plot[plot.label==label].set_index('feature').loc[features,'relative_rmse_improvement_percent']
    ax.plot(range(18),values,label=label,color=color,linestyle=(0,(4,2.8)) if style=='--' else style,linewidth=1.5,marker='o',markersize=3.5,
            markerfacecolor='white',markeredgewidth=1.1,zorder=3)
low=min(-5,np.floor(plot.relative_rmse_improvement_percent.min()/5)*5-5)
high=np.ceil(plot.relative_rmse_improvement_percent.max()/5)*5+10
ax.set_ylim(low,high);ax.set_xlim(-.5,17.5)
ax.set_xticks(range(18),features,rotation=50,ha='right',rotation_mode='anchor')
ax.set_ylabel('RMSE improvement (%)');ax.set_xlabel('Hydrological signatures',labelpad=6)
ax.set_title('(c) GSIM hydrological signature prediction',loc='left',pad=10)
ax.axhline(0,color='#777777',linewidth=.8)
ax.grid(color='#E5E5E5',linewidth=.5)
ax.legend(loc='upper left',ncol=2,frameon=False,borderaxespad=.25,
          fontsize=10.7,handlelength=3.2,columnspacing=1.0,labelspacing=.2)
fig.canvas.draw();renderer=fig.canvas.get_renderer()
for ax in axes:
    for text in ax.get_xticklabels()+ax.get_yticklabels()+[ax.title,ax.xaxis.label,ax.yaxis.label]:
        if not text.get_text():continue
        box=text.get_window_extent(renderer)
        assert fig.bbox.contains(box.x0,box.y0) and fig.bbox.contains(box.x1,box.y1),text.get_text()
fig.savefig(OUT/'Figure8.png',dpi=300)
fig.savefig(OUT/'Figure8.pdf');plt.close(fig)
print('Rendered', DS)
