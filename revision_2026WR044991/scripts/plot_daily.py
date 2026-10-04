"""Redraw Figures 9 and S17 from archived, already-screened score tables.
This entry point does not reconstruct daily discharge or rerun donor selection.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, FixedLocator, MaxNLocator
from matplotlib.cbook import boxplot_stats
from matplotlib.patches import Patch
from matplotlib.scale import SymmetricalLogTransform
ROOT = Path(__file__).resolve().parents[1]
F = ROOT/'generated'
F.mkdir(exist_ok=True)
def read(p): return pd.read_csv(p, float_precision='round_trip')
def load_scores(filename):
    parts=[]
    for name in ['Figure9','FigureS17']:
        frame=read(ROOT/f'data/daily/{name}/{filename}')
        # Each archived row is repeated once per plotted metric.
        clean=frame.drop(columns='plotted_metric').drop_duplicates()
        assert not clean.duplicated(['window','basin_id','method']).any()
        parts.append(clean)
    return pd.concat(parts,ignore_index=True)
d=load_scores('boxplot_source_values.csv')
p=load_scores('paired_source_values.csv')
refs=[]
for name, window in [('Figure9','subsequent_2016_2020'),('FigureS17','unified_1981_2015')]:
    frame=read(ROOT/f'data/daily/{name}/plotted_statistics.csv').rename(columns={
        'median_paired_difference':'median_difference_favor_AUDIOS',
        'audios_5th_percentile':'AUDIOS_p05','knoben_5th_percentile':'baseline_p05',
        'audios_better_percent':'AUDIOS_win_pct'})
    refs.append(frame.assign(window=window,scope='common_targets',comparison='AUDIOSK5 vs KnobenK5'))
summ=pd.concat(refs,ignore_index=True)
def pack_swarm(y, diameter, max_width):
    """Deterministic collision avoidance in display coordinates; y never changes."""
    order=np.argsort(y,kind="stable")
    placed=[];offsets=np.empty(len(y))
    for i in order:
        neighbours=[(xj,yj) for xj,yj in placed if abs(y[i]-yj)<diameter]
        candidates=[0.]
        for xj,yj in neighbours:
            dx=np.sqrt(max(0.,diameter**2-(y[i]-yj)**2))+1e-8
            candidates.extend([xj+dx,xj-dx])
        preferred=1 if len(placed)%2==0 else -1
        candidates.sort(key=lambda x:(abs(x),-preferred*x))
        chosen=None
        for x in candidates:
            if abs(x)>max_width:continue
            if all((x-xj)**2+(y[i]-yj)**2>=diameter**2-1e-7 for xj,yj in neighbours):
                chosen=x;break
        if chosen is None:return None
        offsets[i]=chosen;placed.append((chosen,y[i]))
    if len(y)>1:
        dist=(offsets[:,None]-offsets[None,:])**2+(y[:,None]-y[None,:])**2
        np.fill_diagonal(dist,np.inf)
        assert dist.min()>=diameter**2-1e-6
    return offsets
methods=[('Koppen_Class_All','Köppen',(.92,.57,.18)),('Knoben_Class_All','Knoben',(.18,.62,.44)),('Continuous_FCM_Class_All','AUDIOS',(.22,.36,.72)),('Knoben_K5','KnobenK5',(.10,.50,.28)),('RF_Signature_K5','AUDIOSK5',(.22,.36,.72))]
valid={};pairvalid={};all_diffs={}
for metric in ['NSE','KGE']:
 wide=d.pivot(index='basin_id',columns=['window','method'],values=metric);valid[metric]=set(wide.index[np.isfinite(wide).all(axis=1)])
 q=p[p.comparison=='AUDIOSK5 vs KnobenK5'].pivot(index='basin_id',columns=['window','method'],values=metric);pairvalid[metric]=set(q.index[np.isfinite(q).all(axis=1)])
 assert len(valid[metric])==626 and len(pairvalid[metric])==627
 all_diffs[metric]=np.concatenate([(q.loc[sorted(pairvalid[metric]),(w,'RF_Signature_K5')]-q.loc[sorted(pairvalid[metric]),(w,'Knoben_K5')]).to_numpy() for w in ['unified_1981_2015','subsequent_2016_2020']])
# Equal visual widths on the adopted symmetric-log scale. The same bins are
# used for a given metric in both periods. Zero is a bin edge, so no bar mixes
# positive and negative differences. NSE and KGE each use 36 displayed bins.
N_BINS=36
hist_transform=SymmetricalLogTransform(base=10,linthresh=.2,linscale=1)
edges_by={};binning_info={}
for metric in ['NSE','KGE']:
 u=hist_transform.transform(all_diffs[metric])
 neg=max(0.,-float(u.min()));pos=max(0.,float(u.max()))
 n_negative=int(np.clip(round(N_BINS*neg/(neg+pos)),1,N_BINS-1))
 n_positive=N_BINS-n_negative
 step=max(neg/n_negative,pos/n_positive)*(1+1e-10)
 uedges=np.arange(-n_negative,n_positive+1)*step
 ed=hist_transform.inverted().transform(uedges);ed[n_negative]=0.
 assert np.all(np.diff(ed)>0) and ed[0]<=all_diffs[metric].min() and ed[-1]>=all_diffs[metric].max()
 np.testing.assert_allclose(np.diff(hist_transform.transform(ed)),step,rtol=1e-10)
 edges_by[metric]=ed
 binning_info[metric]=dict(total_bins=N_BINS,negative_bins=n_negative,positive_bins=n_positive,display_scale_bin_width=step,raw_min_edge=float(ed[0]),raw_max_edge=float(ed[-1]))
plt.rcParams.update({'font.family':['Times New Roman','DejaVu Serif'],'font.size':12,'axes.labelsize':12,'axes.titlesize':14,'pdf.fonttype':42,'axes.linewidth':.7})
for window,name in [('subsequent_2016_2020','Figure9'),('unified_1981_2015','FigureS17')]:
 out=F/name;out.mkdir(exist_ok=True);fig,axes=plt.subplots(2,2,figsize=(8.8,8.1));fig.subplots_adjust(left=.11,right=.985,bottom=.08,top=.955,wspace=.18,hspace=.28)
 groups=[];statsrows=[];source=[]
 for ax,metric,letter in zip(axes[0],['NSE','KGE'],'ab'):
  vals=[]
  for pos,(method,label,color) in enumerate(methods,1):
   z=d[(d.window==window)&(d.method==method)&d.basin_id.isin(valid[metric])].sort_values('basin_id');v=z[metric].to_numpy();assert len(v)==626 and np.isfinite(v).all();vals.append(v);st=boxplot_stats(v,whis=1.5)[0]
   statsrows.append(dict(method=label,metric=metric,n=len(v),median=st['med'],p05=np.quantile(v,.05),q1=st['q1'],q3=st['q3'],whislo=st['whislo'],whishi=st['whishi']))
   fl=z[(z[metric]<st['whislo'])|(z[metric]>st['whishi'])];groups.append((ax,metric,pos,label,color,fl));source.append(z.assign(plotted_metric=metric))
  bp=ax.boxplot(vals,positions=np.arange(1,6),widths=.56,whis=1.5,patch_artist=True,showfliers=False,manage_ticks=False,medianprops={'color':'black','linewidth':1.3},whiskerprops={'color':'.30','linewidth':.9},capprops={'color':'.30','linewidth':.9})
  for box,(_,_,c) in zip(bp['boxes'],methods):box.set_facecolor((*c,.72));box.set_edgecolor(c)
  ax.set_yscale('symlog',linthresh=1,linscale=1.15,base=10);lo=min(v.min() for v in vals)
  ax.set_yticks([1,.5,0,-.5,-1]+[-10.**i for i in range(1,int(np.ceil(np.log10(max(1,abs(lo)))))+1)]);ax.yaxis.set_major_formatter(FuncFormatter(lambda x,pos:f'{x:g}'));ax.set_ylim(lo*1.15,1.12)
  ax.set_xticks(np.arange(1,6),[x[1] for x in methods],rotation=30,ha='center');ax.set_xlim(.45,5.55);ax.set_title(f'({letter})',loc='left',pad=8);ax.set_ylabel(metric);ax.axhline(0,color='.5',linewidth=.7);ax.grid(axis='y',alpha=.14);ax.set_axisbelow(True);ax.spines[['top','right']].set_visible(False)
 fig.canvas.draw();swarm=[]
 for ax,metric,pos,label,color,fl in groups:
  y=fl[metric].to_numpy();display=ax.transData.transform(np.c_[np.full(len(y),pos),y]);width=abs(ax.transData.transform((pos+.32,0))[0]-ax.transData.transform((pos,0))[0]);dx=None
  for marker in [1.8,1.7,1.6,1.5,1.4]:
   dx=pack_swarm(display[:,1],marker*fig.dpi/72*1.06,width)
   if dx is not None:break
  assert dx is not None;shift=display.copy();shift[:,0]+=dx;x=ax.transData.inverted().transform(shift)[:,0];sc=ax.scatter(x,y,s=marker**2,color=color,alpha=.72,edgecolors='none',zorder=3);np.testing.assert_array_equal(np.asarray(sc.get_offsets())[:,1],y)
  swarm.extend(dict(method=label,metric=metric,basin_id=i,value=v,x=xx) for i,v,xx in zip(fl.basin_id,y,x))
 rows=[];hist=[];pairsource=[];prepared={}
 for metric in ['NSE','KGE']:
  q=p[(p.window==window)&(p.comparison=='AUDIOSK5 vs KnobenK5')&p.basin_id.isin(pairvalid[metric])];a=q[q.method=='RF_Signature_K5'].set_index('basin_id').sort_index();b=q[q.method=='Knoben_K5'].set_index('basin_id').sort_index();assert a.index.equals(b.index);np.testing.assert_array_equal(a.valid_days,b.valid_days)
  delta=(a[metric]-b[metric]).to_numpy();row=dict(metric=metric,n=len(delta),median_paired_difference=float(np.median(delta)),audios_better_percent=float(100*(delta>0).mean()),audios_5th_percentile=float(np.quantile(a[metric],.05)),knoben_5th_percentile=float(np.quantile(b[metric],.05)))
  ref=summ[(summ.scope=='common_targets')&(summ.window==window)&(summ.comparison=='AUDIOSK5 vs KnobenK5')&(summ.metric==metric)].iloc[0];np.testing.assert_allclose([row['median_paired_difference'],row['audios_5th_percentile'],row['knoben_5th_percentile'],row['audios_better_percent']],[ref.median_difference_favor_AUDIOS,ref.AUDIOS_p05,ref.baseline_p05,ref.AUDIOS_win_pct],atol=1e-10)
  ed=edges_by[metric];ct,_=np.histogram(delta,bins=ed);assert ct.sum()==627;prepared[metric]=(ed,ct);rows.append(row);hist.extend(dict(metric=metric,left_edge=l,right_edge=r,count=int(n)) for l,r,n in zip(ed[:-1],ed[1:],ct));pairsource.append(q.assign(plotted_metric=metric))
 bottom=axes[1];bottom[1].sharey(bottom[0]);bottom[1].tick_params(labelleft=False);ymax=max(prepared[m][1].max() for m in prepared)*1.8;green='#2A9D73';orange='#D65A18'
 for ax,metric,row,letter in zip(bottom,['NSE','KGE'],rows,'cd'):
  ed,ct=prepared[metric];ax.bar(ed[:-1],ct,width=np.diff(ed),align='edge',color=np.where((ed[:-1]+ed[1:])/2>=0,green,orange),edgecolor='white',linewidth=.6);ax.set_xscale('symlog',base=10,linthresh=.2,linscale=1);ax.set_xlim(ed[0],ed[-1]);ax.set_ylim(0,ymax);ax.axvline(0,color='#666666',lw=.65);line=ax.axvline(row['median_paired_difference'],color='#333333',ls='--',lw=1);np.testing.assert_array_equal(line.get_xdata(),[row['median_paired_difference']]*2)
  ax.text(.53,.96,f"AUDIOSK5 better:\n{row['audios_better_percent']:.1f}% of catchments\nMedian Δ{metric}: {row['median_paired_difference']:+.3f}\n\n5th percentile of {metric}\nAUDIOSK5: {row['audios_5th_percentile']:.2f}\nKnobenK5: {row['knoben_5th_percentile']:.2f}",ha='left',va='top',transform=ax.transAxes,fontsize=11.2,linespacing=1.15,bbox={'facecolor':'white','edgecolor':'none','pad':2,'alpha':.97})
  ax.set_title(f'({letter})',loc='left');ticks={'NSE':[-1000,-10,-1,0,1,10,1000],'KGE':[-10,-1,0,1,10,100]}[metric];ax.xaxis.set_major_locator(FixedLocator([x for x in ticks if ed[0]<=x<=ed[-1]]));ax.xaxis.set_major_formatter(FuncFormatter(lambda x,pos:f'{x:g}'));ax.yaxis.set_major_locator(MaxNLocator(nbins=4,integer=True));ax.set_xlabel(f'Δ{metric} (AUDIOSK5 − KnobenK5)');ax.spines[['top','right']].set_visible(False);ax.set_axisbelow(True);ax.grid(axis='y',alpha=.18)
 bottom[0].set_ylabel('Number of catchments');bottom[0].legend(handles=[Patch(color=orange,label='KnobenK5 better'),Patch(color=green,label='AUDIOSK5 better')],loc='upper left',frameon=False,bbox_to_anchor=(0,.985),fontsize=10,handlelength=.8,handletextpad=.4,borderaxespad=0)
 fig.canvas.draw()
 legend_box=bottom[0].get_legend().get_window_extent()
 assert legend_box.x1<bottom[0].transData.transform((0,0))[0]-2,'Legend overlaps zero line'
 widths=[np.array([patch.get_window_extent().width for patch in ax.patches]) for ax in bottom]
 assert all(len(x)==N_BINS for x in widths)
 for x in widths:np.testing.assert_allclose(x,x[0],atol=1e-7,rtol=1e-10)
 np.testing.assert_allclose(widths[0],widths[1],atol=1e-7,rtol=1e-10)
 fig.savefig(out/'daily_combined_boxplot_paired.png',dpi=300);fig.savefig(out/'daily_combined_boxplot_paired.pdf');plt.close(fig)
 pd.DataFrame(statsrows).to_csv(out/'boxplot_statistics.csv',index=False);pd.DataFrame(rows).to_csv(out/'plotted_statistics.csv',index=False);pd.DataFrame(hist).to_csv(out/'histogram_bins.csv',index=False);pd.DataFrame(swarm).to_csv(out/'swarm_points.csv',index=False);pd.concat(source).to_csv(out/'boxplot_source_values.csv',index=False);pd.concat(pairsource).to_csv(out/'paired_source_values.csv',index=False)
 (out/'checks.json').write_text(json.dumps(dict(status='PASS',histogram_symlog_linthresh=.2,histogram_symlog_linscale=1,boxplot_symlog_linthresh=1,boxplot_symlog_linscale=1.15,zero_to_median_gap_pixels={m:float(ax.transData.transform((row['median_paired_difference'],0))[0]-ax.transData.transform((0,0))[0]) for ax,m,row in zip(bottom,['NSE','KGE'],rows)},equal_displayed_bin_widths=True,equal_bin_count_both_panels=N_BINS,zero_is_bin_edge=True,binning=binning_info,displayed_bar_width_pixels=float(widths[0][0]),window=window,boxplot_common_n=626,paired_common_n=627,all_eligible_displayed_values_retained=True,statistics_match_archived_reference=True,median_lines_at_true_positions=True),indent=2),encoding='utf-8');print('RENDERED',name,flush=True)
