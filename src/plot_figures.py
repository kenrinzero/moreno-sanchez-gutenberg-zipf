"""Export the scoped Figure3/7(a) reconstructions as standalone scientific plots."""
import argparse
import hashlib
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter,FuncFormatter


ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--report',type=Path,default=ROOT/'results/report.json')
    parser.add_argument('--out',type=Path,default=ROOT/'figures')
    args=parser.parse_args();r=json.loads(args.report.read_bytes())
    if r['books']!=31075 or r['primary_pass']!='A': raise ValueError('Expected the complete primary report')
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,
                         'axes.labelcolor':'#182935','text.color':'#182935','xtick.color':'#52626c','ytick.color':'#52626c',
                         'axes.edgecolor':'#9aaab4','figure.facecolor':'#f8fafb','axes.facecolor':'white','svg.hashsalt':'gutenberg-20261117'})
    fig,axes=plt.subplots(1,2,figsize=(13,5.4));colors={'f1':'#12689c','f2':'#ad4c10','both':'#67747d'}
    for m in ('f1','f2','both'):
        axes[0].plot([v['p0'] for v in r['survival_curve']],[v[m] for v in r['survival_curve']],
                     color=colors[m],label=m if m!='both' else 'Both',linestyle='--' if m=='both' else '-',linewidth=2.2)
    axes[0].axvline(.05,color='#a9b4ba',lw=1,ls=':')
    axes[0].scatter([.05]*3,[4524/31075,12315/31075,829/31075],marker='D',s=24,facecolors='white',edgecolors='#283b49',zorder=4,label='Paper at 0.05')
    axes[0].set(xlabel='Acceptance cutoff p₀',ylabel='Fraction of all books accepted',xlim=(.01,.5),ylim=(0,.6),title='Acceptance across cutoffs')
    axes[0].legend(frameon=False,fontsize=10)
    for m in ('f1','f2'):
        full=[b for b in r['length_bins'] if not b['partial']];tail=[b for b in r['length_bins'] if b['partial']]
        axes[1].plot([b['geometric_mean_L'] for b in full],[b['counts']['5'][m]/b['n_books'] for b in full],color=colors[m],lw=2.2,label=m)
        axes[1].scatter([b['geometric_mean_L'] for b in tail],[b['counts']['5'][m]/b['n_books'] for b in tail],facecolors='none',edgecolors=colors[m],s=110 if m=='f1' else 35,linewidth=1.8,zorder=4,clip_on=False)
    axes[1].set(xscale='log',xlabel='Book length L (tokens; logarithmic axis)',ylabel='Fraction accepted within length bin',ylim=(0,1),title='Length dependence at p₀ = 0.05')
    axes[1].xaxis.set_major_formatter(FuncFormatter(lambda x,pos:f'{x/1e6:g}m' if x>=1e6 else f'{x/1000:g}k' if x>=1000 else f'{x:g}'))
    axes[1].legend(frameon=False,fontsize=10)
    for ax in axes:ax.yaxis.set_major_formatter(PercentFormatter(1,decimals=0));ax.grid(axis='y',color='#e3e9ed',lw=.8);ax.set_axisbelow(True)
    fig.suptitle('Two versions of Zipf’s law: Gutenberg reproduction',fontsize=18,fontweight='bold',x=.07,ha='left',y=.98)
    fig.text(.07,.90,'Pass A · 31,075 released vectors · f1/f2 only · Accepted means not rejected; table comparison is a partial reproduction.',fontsize=10,color='#52626c')
    fig.text(.07,.035,'Recomputed Figures 3 and 7(a). Right: 31 connected bins of 1,000; final 75-book bin: hollow rings (f1 outer, f2 inner).\nModels are fitted over n ≥ 1; each goodness-of-fit test uses 100 refitted simulations. Source: Moreno-Sánchez et al. (2016), DOI 10.1371/journal.pone.0147073.',fontsize=9,color='#52626c')
    fig.subplots_adjust(left=.07,right=.98,bottom=.21,top=.78,wspace=.27)
    args.out.mkdir(parents=True,exist_ok=True)
    for suffix in ('png','svg'):fig.savefig(args.out/f'figure3-7.{suffix}',dpi=180,metadata={'Date':None} if suffix=='svg' else {'Software':'Gutenberg reproduction'})
    svg=args.out/'figure3-7.svg'
    svg.write_bytes(svg.read_bytes().replace(b'\r\n',b'\n'))
    plt.close(fig)
    manifest={'report_sha256':hashlib.sha256(args.report.read_bytes()).hexdigest(),'matplotlib':matplotlib.__version__,
              'plot_code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'figures':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (args.out/'figure3-7.png',args.out/'figure3-7.svg')}}
    (args.out/'manifest.json').write_bytes((json.dumps(manifest,indent=2)+'\n').encode('utf-8'))
    print(json.dumps(manifest,indent=2))


if __name__=='__main__':main()
