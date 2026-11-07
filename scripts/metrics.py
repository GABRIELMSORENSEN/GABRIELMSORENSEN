"""Publish only public repository metadata. Stdlib; GITHUB_TOKEN optional."""
from __future__ import annotations
import argparse,collections,datetime,json,os,subprocess,urllib.request
from pathlib import Path
from html import escape
from art import svg,frame,label,WHITE,MUTED,PURPLE,RED,ASSETS,ROOT
USER='GABRIELMSORENSEN'

def request(path):
 headers={'Accept':'application/vnd.github+json','User-Agent':'g4t0xx-profile'}
 if os.getenv('GITHUB_TOKEN'):headers['Authorization']='Bearer '+os.environ['GITHUB_TOKEN']
 with urllib.request.urlopen(urllib.request.Request('https://api.github.com'+path,headers=headers),timeout=30) as r:return json.load(r)

def refresh(local=False):
 if local:
  repos=json.loads((ROOT/'.work/public-repos.json').read_text(encoding='utf-8'))
  languages=json.loads((ROOT/'.work/languages.json').read_text())
  calendar=json.loads((ROOT/'.work/calendar.json').read_text())
  stars=sum(r['stargazerCount'] for r in repos);forks=sum(r['forkCount'] for r in repos)
 else:
  repos=[]
  for page in range(1,10):
   batch=request(f'/users/{USER}/repos?type=owner&per_page=100&page={page}')
   repos.extend(r for r in batch if not r['private'])
   if len(batch)<100:break
  languages=collections.Counter()
  for r in repos:
   if not r['fork']:
    for lang,size in request(f'/repos/{USER}/{r["name"]}/languages').items():languages[lang]+=size
  stars=sum(r['stargazers_count'] for r in repos);forks=sum(r['forks_count'] for r in repos)
  calendar=None
  token=os.getenv('GITHUB_TOKEN')
  if token:
   query='query { user(login: "'+USER+'") { contributionsCollection { contributionCalendar { totalContributions weeks { contributionDays { date contributionCount color } } } } } }'
   body=json.dumps({'query':query}).encode()
   req=urllib.request.Request('https://api.github.com/graphql',body,{'Authorization':'Bearer '+token,'Content-Type':'application/json','User-Agent':'g4t0xx-profile'})
   try:
    with urllib.request.urlopen(req,timeout=30) as response:calendar=json.load(response)['data']['user']['contributionsCollection']['contributionCalendar']
   except (urllib.error.HTTPError,KeyError):pass
  if calendar is None:
   previous=ROOT/'data/public-metrics.json'
   if previous.exists():calendar=json.loads(previous.read_text())['calendar']
 stats={'updated':datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC'),'repositories':len(repos),'stars':stars,'forks':forks,'languages':dict(languages),'calendar':calendar,'projects':[r['name'] for r in repos]}
 (ROOT/'data/public-metrics.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 render(stats)

def render(s):
 lang=sorted(s['languages'].items(),key=lambda x:x[1],reverse=True);total=sum(x[1] for x in lang)
 body=label('PUBLIC SIGNAL / DADOS REAIS DO GITHUB',44,50,PURPLE,10,2)
 body+=label('O que ficou registrado.',44,85,WHITE,21,0)
 fields=[('REPOSITÓRIOS PÚBLICOS',s['repositories']),('LINGUAGENS DETECTADAS',len(lang)),('ESTRELAS / PÚBLICOS',s['stars']),('FORKS / PÚBLICOS',s['forks'])]
 for i,(title,value) in enumerate(fields):
  x=44+i*300
  body+=f'<text x="{x}" y="173" class="serif" fill="{WHITE}" font-size="58">{value:02d}</text>'+label(title,x,204,MUTED,9,1)
  if i<3:body+=f'<path d="M{x+264} 117 V213" stroke="#30203c"/>'
 body+=label('Somente repositórios públicos. Nenhum dado privado é consultado.',44,248,MUTED,10,0)
 body+=label(s['updated'],988,248,PURPLE,9,0)
 body+=frame(1280,280)
 (ASSETS/'metrics.svg').write_text(svg(1280,280,body,'Métricas públicas de GABRIELMSORENSEN'),encoding='utf-8')
 colors=['#bd88eb','#8f63d4','#c04c77','#6b82c9','#71527e','#c18d99','#5b6889','#8b6a4e','#555773','#647458','#927b9e','#765857']
 body=label('LINGUAGENS / BYTES DE CÓDIGO PÚBLICO',44,48,PURPLE,10,1)
 x=44
 for i,(name,value) in enumerate(lang):
  width=1192*value/total;body+=f'<rect x="{x:.2f}" y="77" width="{width:.2f}" height="12" fill="{colors[i%len(colors)]}"/>';x+=width
 for i,(name,value) in enumerate(lang):
  x=44+(i%4)*302;y=126+(i//4)*35
  body+=f'<circle cx="{x+4}" cy="{y-4}" r="4" fill="{colors[i%len(colors)]}"/>'+label(name,x+19,y,WHITE,12,0)+label(f'{100*value/total:.1f}%',x+190,y,MUTED,11,0)
 body+=label('Distribuição por bytes nos projetos originais públicos; não é uma medida de domínio.',44,251,MUTED,10,0)+frame(1280,280)
 (ASSETS/'languages.svg').write_text(svg(1280,280,body,'Linguagens por bytes de código público'),encoding='utf-8')
 if s['calendar']:
  cal=s['calendar'];weeks=cal['weeks'];maxvalue=max(d['contributionCount'] for w in weeks for d in w['contributionDays']) or 1
  body=label('LOOP CHRONICLE / CALENDÁRIO DE CONTRIBUIÇÕES',44,48,PURPLE,10,2)
  body+=label(str(cal['totalContributions'])+' contribuições no período exibido',44,80,WHITE,17,0)
  palettes=['#18111f','#3d234f','#633579','#9256b4','#c995ef']
  for x,w in enumerate(weeks):
   for d in w['contributionDays']:
    day=datetime.date.fromisoformat(d['date']);y=(day.weekday()+1)%7;count=d['contributionCount'];level=0 if not count else min(4,1+int(count/maxvalue*3))
    body+=f'<rect x="{44+x*22}" y="{110+y*20}" width="17" height="15" rx="2" fill="{palettes[level]}"><title>{d["date"]}: {count} contribuições</title></rect>'
  first=weeks[0]['contributionDays'][0]['date'];last=weeks[-1]['contributionDays'][-1]['date']
  body+=label(first+' — '+last,44,280,MUTED,10,0)+label('GitHub contributionsCollection',860,280,MUTED,10,0)+frame(1280,310)
  (ASSETS/'activity.svg').write_text(svg(1280,310,body,'Calendário de contribuições no GitHub'),encoding='utf-8')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--local',action='store_true');refresh(p.parse_args().local)
