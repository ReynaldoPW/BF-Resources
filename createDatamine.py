#To update units: first do bbs(), es(), ls()

#Refer to filesGet.py for instructions on updating the files

#level() -> player_level.json ==> player level 1-999 info
#s_level() -> summoner_level.json ==> summoner level 1-500
#g_level() -> guild_level.json ==> Guild level info (members, exp, etc)
#g_skills() -> guild_skills.json ==> Guild skills (karma, exp, zel) rank info
#weapons() -> summoner_weapons.json ==> summoner weapons general info, levels, es, skills, exp, elements, etc
#params() -> summoner_params.json ==> summoner parameters with level effects etc
#summon_arts() -> summoning_arts.json ==> summonning arts element and level boosts/exp
#arena() -> arena_ranks.json ==> arena rank abp and rewards
#unit() -> unit datamine which includes AI type
#summon_gates() -> summon_gates.json ==> summon gate timing and name, desc, cost etc
#exchange_hall() -> exchange_hall.json ==> all exchange hall possible exchanges and rewards
#item() -> items.json ==> basic item datamine
#fg() -> frontier_gate.json ==> all frontier gate ids and rewards etc
#bbs() -> bbs.json ==> partial bb data parse
#es() -> es.json ==> partial es data parse
#ls() -> partial ls data parse
#guildArt(), coloClass(), expPattern()

import math

def run_all():
    level()
    s_level()
    g_level()
    g_skills()
    weapons()
    params()
    summon_arts()
    arena()
    #unit()
    summon_gates()
    exchange_hall()
    item()
    fg()
    #bbs()
    #es()
    #ls()
    #guildArt()
    #coloClass()
    #expPattern()
    print("All files created.")


#from utils import *
from filesGet import *

load_directory="data_files/"
save_directory="bravefrontier_data/"

dictionary=loadInfo2("datamines/dictionary.json")
try:
    bb=loadInfo2("datamines/bbs.json")
except:
    bb={}
try:
    ess=loadInfo2("datamines/es.json")
except:
    ess={}
try:
    lss=loadInfo2("datamines/ls.json")
except:
    lss={}

elements={'1':'fire','2':'water','3':'earth','4':'thunder','5':'light','6':'dark','X':'all'}

ailments = {'0':'none','1': 'poison%', '2': 'weaken%', '3': 'sick%', '4': 'injury%', '5': 'curse%', '6': 'paralysis%', '7': 'atk down', '8': 'def down', '9': 'rec down'}

attribute = {'1': 'attack', '2': 'defense', '3': 'recovery', '4': 'hp'}

genders = {'0': 'other', '1': 'male', '2': 'female'}


#for each one: 'proc id': ((num,name,processFunc=int, removal=zero),...,())

passives={'1':[(0,'atk% buff',-1,-1), #stat buffs
               (1,'def% buff',-1, -1),
               (2,'rec% buff',-1,-1),
               (3,'crit% buff',-1,-1),
               (4,'hp% buff',-1,-1)
              ],
          '2':[([1,2],'elements buffed',lambda x:[elements[y] for y in x if y in elements.keys()],lambda x:len([elements[y] for y in x if y in elements.keys()])==0), #elemental stat buffs
               (2,'atk% buff',-1,-1),
               (3,'def% buff',-1,-1),
               (4,'rec% buff',-1,-1),
               (5,'crit% buff',-1,-1),
               (6,'hp% buff',-1,-1),
              ],
          '3':[(0,'type',lambda x:x,lambda x:False), #type stat buffs
               (1,'atk% buff',-1,-1),
               (2,'def% buff',-1, -1),
               (3,'rec% buff',-1,-1),
               (4,'crit% buff',-1,-1),
               (5,'hp% buff',-1,-1)
              ],
          '4':[(0,'poison resist%',-1,-1), #status resist
               (1,'weaken resist%',-1,-1),
               (2,'sick resist%',-1, -1),
               (3,'injury resist%',-1,-1),
               (4,'curse resist%',-1,-1),
               (5,'paralysis resist%',-1,-1)
              ],
          '5':((0,'element',lambda x:elements[x],-1), #elemental miti
               (1,'miti%',-1,-1)
              ),
          #6 is unknown, only a handful of them all with one param (500)
          #7 is also unknown, neither ES nor LS has one
          '8':[(0,'miti%',-1,-1)
              ],
          '9':[(0,'bc fill per turn',lambda x:int(int(x)/100),-1)
              ],
          '10':[(0,'hc effectiveness%',-1,-1)
               ],
          '11':[(0,'atk% buff',-1,-1),
                (1,'def% buff',-1,-1),
                (2,'rec% buff',-1,-1),
                (3,'hp% buff',-1,-1),
                ([4,5],lambda x:'hp '+{'1':'above','2':'below'}[x[1]]+'% threshold',lambda x:int(x[0]),lambda x:False),
              ],
          '12':[(0,'bc drop rate% buff',-1,-1),
                (1,'hc drop rate% buff',-1,-1),
                (2,'item drop rate% buff',-1,-1),
                (3,'zel drop rate% buff',-1,-1),
                (4,'karma drop rate% buff',-1,-1),
                ([5,6],lambda x:'hp '+{'1':'above','2':'below'}[x[1]]+'% threshold',lambda x:int(x[0]),lambda x:False),
              ],
          '13':[(0,'bc fill on enemy defeat low',lambda x:int(int(x)/10),-1),
                (1,'bc fill on enemy defeat high',lambda x:int(int(x)/10),-1),
                (2,'bc fill on enemy defeat chance%',-1,-1)
              ],
          '14':[(0,'miti%',-1,-1),
                (1,'miti chance%',-1,-1)
              ],
          '15':[(0,'hp% recover on enemy defeat low',-1,-1),
                (1,'hp% recover on enemy defeat high',-1,-1),
                (2,'hp recover on enemy defeat chance%',-1,-1)
              ],
          '16':[(0,'hp% recover on battle win low',-1,-1),
                (1,'hp% recover on battle win high',-1,-1),
              ],
          '17':[(0,'hp drain% low',-1,-1),
                (1,'hp drain% high',-1,-1),
                (2,'hp drain chance%',-1,-1)
              ],
          #18 unknown
          '19':[(0,'bc drop rate% buff',-1,-1),
                (1,'hc drop rate% buff',-1,-1),
                (2,'item drop rate% buff',-1,-1),
                (3,'zel drop rate% buff',-1,-1),
                (4,'karma drop rate% buff',-1,-1),
              ],
          '20':[([0,1],lambda x:ailments[x[0]],lambda x:int(x[1]),-1),
                ([2,3],lambda x:ailments[x[0]],lambda x:int(x[1]),-1),
                ([4,5],lambda x:ailments[x[0]],lambda x:int(x[1]),-1),
                ([6,7],lambda x:ailments[x[0]],lambda x:int(x[1]),-1),
              ],
          '21':[(0,'first x turns atk%',-1,-1),
                (1,'first x turns def%',-1,-1),
                (2,'first x turns rec%',-1,-1),
                (3,'first x turns crit%',-1,-1),
                (4,'turns',-1,lambda x:False),
              ],
          #22 unknown
          '23':[(0,'battle end bc fill low',lambda x:int(int(x)/100),-1),
                (1,'battle end bc fill high',lambda x:int(int(x)/100),-1),
              ],
          '24':[(0,'dmg% to hp% when attacked low',-1,-1),
                (1,'dmg% to hp% when attacked high',-1,-1),
                (2,'dmg% to hp% when attacked chance%',-1,-1)
              ],
          '25':[(0,'bc fill when attacked low',lambda x:int(int(x)/100),-1),
                (1,'bc fill when attacked high',lambda x:int(int(x)/100),-1),
                (2,'bc fill when attacked chance%',-1,-1)
              ],
          '26':[(0,'dmg% reflect low',-1,-1),
                (1,'dmg% reflect high',-1,-1),
                (2,'dmg% reflect chance%',-1,-1)
              ],
          '27':[(0,'target% chance',-1,-1)
              ],
          '28':[(0,'target% chance',-1,-1),
                ([1,2],lambda x:'hp '+{'1':'above','2':'below'}[x[1]]+'% requirement',lambda x:int(x[0]),lambda x:False)
              ],
          '29':[(0,'ignore def%',-1,-1)
              ],
          '30':[(0,'atk% buff',-1,-1),
                (1,'def% buff',-1, -1),
                (2,'rec% buff',-1,-1),
                (3,'crit% buff',-1,-1),
                ([4,5],lambda x:'bb gauge '+{'1':'above','2':'below'}[x[1]]+'% requirement',lambda x:int(x[0]),lambda x:False)
              ],
          '31':[(0,'dmg% for spark',-1,-1),
                (1,'bc drop% for spark',-1,-1),
                (2,'hc drop% for spark',-1,-1),
                (3,'item drop% for spark',-1,-1),
                (4,'zel drop% for spark',-1,-1),
                (5,'karma drop% for spark',-1,-1),
              ],
          '32':[(0,'bb gauge fill rate%',-1,-1)
              ],
          '33':[(0,'turn heal low',-1,-1),
                (0,'turn heal high',-1,-1),
                (0,'rec% added',lambda x:(1+float(x)/100)*10,-1),
              ],
          '34':[(0,'crit dmg%',lambda x:int(100*float(x)),lambda x:False)
              ],
          '35':[(0,'bc fill when attacking low',lambda x:int(int(x)/100),-1),
                (1,'bc fill when attacking high',lambda x:int(int(x)/100),-1),
                (2,'bc fill when attacking chance%',-1,-1)
              ],
          '36':[(0,'additional actions',-1,-1)
              ],
          '37':[(0,'extra hits',-1,-1),
                (2,'extra hits dmg%',-1,-1)
              ],
          #38 unknown but used in es and ls
          #39 unknown but used in es and ls
          '40':[(0,'converted attribute',lambda x:attribute[x],-1),
                (1,'atk% buff',-1,-1),
                (2,'def% buff',-1,-1),
                (3,'rec% buff',-1,-1),
              ],
          '41':[(0,'unique elements required',-1,-1),
                (1,'atk% buff',-1,-1),
                (2,'def% buff',-1, -1),
                (3,'rec% buff',-1,-1),
                (4,'crit% buff',-1,-1),
                (5,'hp% buff',-1,-1)
              ],
          '42':[(0,'gender required',lambda x:genders[x],-1),
                (1,'atk% buff',-1,-1),
                (2,'def% buff',-1, -1),
                (3,'rec% buff',-1,-1),
                (4,'crit% buff',-1,-1),
                (5,'hp% buff',-1,-1)
              ],
          '43':[(0,'take 1 dmg%',-1,-1)
              ],
          '44':[(0,'atk% buff',-1,-1),
                (1,'def% buff',-1, -1),
                (2,'rec% buff',-1,-1),
                (3,'crit% buff',-1,-1),
                (4,'hp% buff',-1,-1)
              ],
          '45':[(0,'base crit% resist',-1,-1),
                (0,'buffed crit% resist',-1,-1),
              ],
          '46':[(0,'atk% base buff',-1,-1),
                ([0,1],'atk% extra buff based on hp',lambda x:int(x[1])-int(x[0]),-1),
                (2,'def% base buff',-1,-1),
                ([2,3],'def% extra buff based on hp',lambda x:int(x[1])-int(x[0]),-1),
                (4,'rec% base buff',-1,-1),
                ([4,5],'rec% extra buff based on hp',lambda x:int(x[1])-int(x[0]),-1),
                (6,'buff proportional to hp',lambda x:{'1':'lost','0':'remaining'}[x[0]],lambda x:False)
              ],
          '47':[(0,'bc fill on spark low',lambda x:int(int(x)/100),-1),
                (0,'bc fill on spark high',lambda x:int(int(x)/100),-1),
                (0,'bc fill on spark%',-1,-1),
              ],
          '48':[(0,'reduced bc cost%',-1,-1)
              ],
          '49':[(0,'reduced bc used% low',-1,-1),
                (1,'reduced bc used% high',-1,-1),
                (2,'reduced bc used chance%',-1,-1)
              ],
          '50':[([0,1,2,3,4,5],'elements',lambda x:[elements[y] for y in x if y in elements],lambda x:False),
                (6,'elemental weakness dmg%',lambda x:int(float(x)*100),lambda x:False)
              ],
          '51':[(0,'base bc drop rate resist%',-1,-1),
                (1,'buffed bc drop rate resist%',-1,-1),
                (2,'base hc drop rate resist%',-1,-1),
                (3,'buffed hc drop rate resist%',-1,-1),
              ],
          #52 unknown
          '53':[(0,'base crit dmg resist%',-1,-1),
                (1,'buffed crit dmg resist%',-1,-1),
                (2,'base elemental damage resist%',-1,-1),
                (3,'buffed elemental damage resist%',-1,-1),
                (4,'base crit chance resist%',-1,-1),
                (5,'buffed crit chance resist%',-1,-1),
                (6,'base bc drop rate resist%',-1,-1),
                (7,'buffed bc drop rate resist%',-1,-1),
                (8,'base hc drop rate resist%',-1,-1),
                (9,'buffed hc drop rate resist%',-1,-1),
              ],
          #54 unknown
          '55':[
              ],
          }

passiveBuff={
    '1':[(0,'atk% buff',-1,-1)
        ],
    '3':[(0,'def% buff',-1,-1)
        ],
    '5':[(0,'rec buff%',-1,-1)
        ],
    '8':[(0,'gradual heal low',-1,-1),
         (1,'gradual heal high',-1,-1)
        ],
    '12':[('angel idol recover hp%',-1,-1)
        ],
    '13':[(0,'element buffed',lambda x:elements[x],-1),
          (1,'atk% buff',-1,-1)
        ],
    '14':[(0,'element buffed',lambda x:elements[x],-1),
          (1,'def% buff',-1,-1)
        ],
    '36':[
        ],
    '37':[
        ],
    '40':[
        ],
    '72':[
        ],
    
    }

sp_cat={
    '1':"Parameter Boost",
    '2':"Spark",
    '3':"Critical",
    '4':"Attack Boost",
    '5':"BB Gauge",
    '6':"HP Recovery",
    '7':"Drop",
    '8':"Ailment Resistance",
    '9':"Ailment Infliction",
    '10':"Damage Reduction",
    '11':"Special"
    }

procs={
       }

def process(formatTuple,params,idNo): #format inputs
    output={}
    allParams=params.split(',')
    for this in formatTuple:
        try:
            if (type(this[0])==type(0)):
                if (type(this[1])==type("1")): #string
                    name=this[1]
                else: #func
                    name=this[1](allParams[0])
                fun=this[2] if this[2]!=-1 else lambda x: int(x)
                zeroFun=this[3] if this[3]!=-1 else lambda x:int(x)==0
                if (not zeroFun(allParams[this[0]])):
                    output[name]=fun(allParams[this[0]])
            else:
                if (type(this[1])==type("1")): #string
                    name=this[1]
                else: #func
                    name=this[1]([allParams[x] for x in this[0]])
                fun=this[2] if this[2]!=-1 else lambda x: [int(y) for y in x]
                zeroFun=this[3] if this[3]!=-1 else lambda x:len([y for y in x if y!="0"])==0
                if (not zeroFun([allParams[x] for x in this[0]])):
                    output[name]=fun([allParams[x] for x in this[0]])
        except Exception as e:
            if (int(idNo)>31):
                print("ID #"+str(idNo)+": "+str(e)+": params = "+str(params)+", tuple = "+str(this)+", fullTuple = "+str(formatTuple)+", allParams = "+str(allParams)+"\n")
    return output
    

def parseEffect(idNo,params,effectType): # -> internal shell
    x=idNo.split(',')[0] if ',' in idNo else idNo
    if (effectType==1): #proc
        if (x in procs):
            result=process(procs[x],params,idNo)
            result['proc id']=x
            return result
        else:
            # return {'unknown proc id':idNo,'params':params}
            return {'proc id':idNo,'params':params}
    else: #passive
        if (x in passives):
            result=process(passives[x],params,x)
            result['passive id']=x
            return result
        else:
            # return {'unknown passive id':idNo.split(',')[0],'params':params}
            return {'passive id':idNo.split(',')[0],'params':params}

def parse(ids,params,effectType): #1=proc,2=passive -> outer shell to split each effect and pass to parseEffect (parses all effects in one skill)
    effects=[]
    allIds=ids.split('@')
    allParams=params.split('@')
    for i in range(len(ids.split('@'))):
        try:
            #print(parseEffect(allIds[i],allParams[i],effectType))
            effects+=[parseEffect(allIds[i],allParams[i],effectType)]
        except:
            print(str(allIds))
            print(str(allParams))
            print(str(effectType))
            print("ERROR parsing effects: allIds="+str(allIds)+"\n")
    return {'effects':effects}




def getDict(x):
    return dictionary[x] if x in dictionary else x

def loadInfo2(x):
    return eval(replaceKeys(str(loadInfo(x))))

def saveInfo2(obj,filename):
    f=open(filename,'w')
    json.dump(obj,f,separators=(',',':'),indent=4,sort_keys=True)
    f.close()
    print("Saved to file: "+filename)

def level(): #player level 1-999
    q=loadInfo2(load_directory+"M_LEVEL_MST.json")
    r={}
    for x in q:
        nextLevel=[y for y in q if y['LEVEL']==str(((int(x['LEVEL'])+1)-1)%len(q)+1)][0]
        r[int(x['LEVEL'])]={'exp to next level':int(nextLevel['EXP_GAIN']),'energy':int(x['CURRENT_ENERGY']),'additional cost':int(x['SOMETHING_PLAYER_LEVEL_RELATED_0-50']),'friend capacity':int(x['SOMETHING_PLAYER_LEVEL_RELATED_10-50']),'cost':int(x['SQUAD_COST?'])}
    saveInfo2(r,save_directory+"player_level.json")

def s_level(): #summoner level 1-500
    q=loadInfo2(load_directory+"F_SU_LEVEL_MST.json")
    r={}
    for x in q:
        nextLevel=[y for y in q if y['LEVEL']==str(((int(x['LEVEL'])+1)-1)%len(q)+1)][0]
        r[int(x['LEVEL'])]={'exp to next level':int(nextLevel['EXP_GAIN']),'summoning arts level':int(x['SUMMONER_ART_LEVEL']),'stats':{'atk':int(x['ATK']),'def':int(x['DEF']),'rec':int(x['REC']),'hp':int(x['HP'])}}
    saveInfo2(r,save_directory+"summoner_level.json")

def g_level(): #guild level 1-180
    q=loadInfo2(load_directory+"F_GUILD_INFO_MST.json")
    r={}
    for x in q:
        nextLevel=[y for y in q if y['GUILD_LEVEL']==str(((int(x['GUILD_LEVEL'])+1)-1)%len(q)+1)][0]
        r[int(x['GUILD_LEVEL'])]={'max members':int(x['MAX_GUILD_MEMBERS']),'exp to next level':int(nextLevel['GUILD_LEVEL_MIN_EXP_THRESHOLD'])}
    saveInfo2(r,save_directory+"guild_level.json")

def g_skills(): #gulid skills zel,karma,exp
    skillNames={'1':'Zel','2':'Karma','3':'EXP','4':'Summoner Exp'}
    q=loadInfo2(load_directory+"F_GUILD_SKILL_DETAILS_MST.json")
    r={}
    for x in list(set([y['SKILL_TYPE*'] for y in q])):
        z={}
        current=[y for y in q if y['SKILL_TYPE*']==x]
        for y in current:
            z[int(y['LEVEL'])]={'guild level':y['GUILD_LEVEL'],'karma':y['KARMA'],'zel':y['ZEL'],'percent boost':int(y['PROC/PASSIVE_PARAMETERS'])}
        r[skillNames[x]]=z
    saveInfo2(r,save_directory+"guild_skills.json")

def weapons(): #summoner weapons
    a=loadInfo2(load_directory+"F_SU_ARM_ELEMENT_MST.json") #s4
    b=loadInfo2(load_directory+"F_SU_ARM_LEVEL_MST.json")   #s5
    c=loadInfo2(load_directory+"F_SU_ARM_MST.json")         #s6
    d=loadInfo2(load_directory+"F_SU_ARM_PASSIVE_MST.json") #s7
    f=loadInfo2(load_directory+"F_SU_EX_SKILL_MST.json")     #s9
    weapons=[]
    for x in c:
        currWeapon={}
        currWeapon['id']=str(x['SUMMONER_WEAPON_ID'])
        currWeapon['thumbnail']=x['THUMBNAIL']
        currWeapon['name']=getDict('MST_SU_ARM_'+str(x['SUMMONER_WEAPON_ID'])+'_NAME')
        currWeapon['getting type']=int(x['UNIT_GETTING_TYPE'])
        currWeapon['desc']=getDict('MST_SU_ARM_'+str(x['SUMMONER_WEAPON_ID'])+'_DESC')
        currWeapon['rarity']=int(x['RARITY'])
        levels=[y for y in b if x['SUMMONER_WEAPON_ID']==y['SUMMONER_WEAPON_ID']]
        currWeapon['levels']=[]
        for level in range(1,len(levels)+1):
            thisLevel=[y for y in levels if y['LEVEL']==str(level)][0]
            nextLevel=[y for y in levels if y['LEVEL']==str(level+1)]
            nextLevel=nextLevel[0] if len(nextLevel)>0 else b[0]
            levelDetails={'stats':{'atk':thisLevel['ATK'],'def':thisLevel['DEF'],'rec':thisLevel['REC'],'hp':thisLevel['HP']}}
            thisES=[x for x in f if x['SUMMONER_ES_ID']==thisLevel['ES_ID']]
            if len(thisES)>0: #ES
                thisES=thisES[0]
                levelDetails['es']={'id':thisES['SUMMONER_ES_ID']}
                levelDetails['es']['name']=getDict('MST_SU_EX_SKILL_'+str(thisES['SUMMONER_ES_ID'])+'_NAME')
                levelDetails['es']['desc']=getDict('MST_SU_EX_SKILL_'+str(thisES['SUMMONER_ES_ID'])+'_DESC')
                #effects=[{'proc id':thisES['PROC/PASSIVE_ID(S)'].split('@')[i],'params':thisES['PROC/PASSIVE_PARAMETERS'].split('@')[i],'effect area':thisES['EFFECT_AREA*'].split('@')[i]} for i in range(len(thisES['EFFECT_AREA*'].split('@')))]
                effects=parse(thisES['PROC/PASSIVE_ID(S)'],thisES['PROC/PASSIVE_PARAMETERS'],2) #edit for effect area
                levelDetails['es']['effects']=effects
                levelDetails['es']['kind?']=thisES['UNIT_KIND']
                if thisES['RARITY']!='0':
                    levelDetails['es']['rarity']=int(thisES['RARITY'])
            else:
                levelDetails['es']=-1
            wpSkills=thisLevel['SUMMONER_WEAPON_SKILL(S)'].replace("\\/","/").split('/')
            if len(wpSkills)>0: #Weapon skills
                w=[]
                for weaponSkill in wpSkills:
                    thisSkill=[z for z in d if z['SUMMONER_WEAPON_SKILL(S)']==weaponSkill][0]
                    r={'effects':[{'proc id':thisSkill['PROC/PASSIVE_ID(S)'].split('@')[i],'params':thisSkill['PROC/PASSIVE_PARAMETERS'].split('@')[i],'effect area':thisSkill['EFFECT_AREA*'].split('@')[i]} for i in range(len(thisSkill['EFFECT_AREA*'].split('@')))]}
                    r['name']=getDict('MST_SU_PASSIVE_'+str(weaponSkill)+'_NAME')
                    r['desc']=getDict('MST_SU_PASSIVE_'+str(weaponSkill)+'_DESC')
                    r['kind?']=thisSkill['UNIT_KIND']
                    w+=[r]
                levelDetails['weapon skills']=w
            else:
                levelDetails['weapon skills']=-1
            levelDetails['bb levels']={'bb':thisLevel['WEAPON_BB_LEVEL'],'sbb':thisLevel['WEAPON_SBB_LEVEL'],'ubb':thisLevel['WEAPON_UBB_LEVEL']}
            levelDetails['level']=int(thisLevel['LEVEL'])
            levelDetails['exp to next level']=int(nextLevel['EXP_GAIN'])
            levelDetails['desc']=getDict('MST_SU_ARM_LEVEL_'+str(x['SUMMONER_WEAPON_ID'])+'_'+str(level)+'_DESC')
            currWeapon['levels']+=[levelDetails]
        #start weapon elements
        elems={element:[y for y in a if str(y['SUMMONER_WEAPON_ID'])==str(x['SUMMONER_WEAPON_ID']) and str(y['UNIT_ELEMENT'])==element][0] for element in ['1','2','3','4','5','6']}
        currWeapon['elements']={}
        for e in elems:
            elementName={'1':'fire','2':'water','3':'earth','4':'thunder','5':'light','6':'dark'}[e]
            c=elems[e]
            this={}
            this['element']=elementName
            this['movement']={'move speed type':c['UNIT_MOVE_SPEED'],'move type':c['UNIT_SKILL_MOVE_TYPE']}
            this['od stats']=c['UNIT_OD_STATS']
            this['drop checks']=int(c['DROP_CHECK_COUNT'])
            this['frames']={'damage frames':[int(w.split(':')[0]) for w in c['DAMAGE_FRAMES'].split(',')],'damage distribution':[int(w.split(':')[1]) for w in c['DAMAGE_FRAMES'].split(',')],'battle effects':[{'frame':int(t.split(':')[0]),'effect id':int(t.split(':')[1])}for t in c['BATTLE_EFFECT_GROUP_FRAMES'].split(',')]}
            this['skills']={bbType:(bb[c[bbType.upper()+'_ID']] if c[bbType.upper()+'_ID']!='0'else -1) for bbType in ['bb','sbb','ubb']}
            ###this['skills']={bbType:"[bbs["+c[bbType.upper()+'_ID']+"]" for bbType in ['bb','sbb','ubb']} #temp
            currWeapon['elements'][elementName]=this
        weapons+=[currWeapon]
    saveInfo2(weapons,save_directory+"summoner_weapons.json")

def params(): #summoner parameters
    a=loadInfo2(load_directory+"F_SU_ABILITY_LEVEL_MST.json")   #s1
    b=loadInfo2(load_directory+"F_SU_ABILITY_MST.json")         #s2
    c=loadInfo2(load_directory+"F_SU_ABILITY_UP_MST.json")      #s3
    params=[]
    for x in b:
        result={'icon':x['THUMBNAIL'],'category':getDict('MST_SU_ABILITY_LEVEL_'+str(x['SUMMONER_LEVEL_STATS_CATEGORY'])+"_1_NAME")}
        levels=[]
        for y in [v for v in a if v['SUMMONER_LEVEL_STATS_CATEGORY']==x['SUMMONER_LEVEL_STATS_CATEGORY']]:
            r={'level':y['LEVEL'],'sp cost':y['SUMMONER_STATS_SP_COST']}
            r['desc']=getDict('MST_SU_ABILITY_LEVEL_'+str(y['SUMMONER_LEVEL_STATS_CATEGORY'])+"_"+str(y['LEVEL'])+"_DESC")
            q=[w for w in c if w['SUMMONER_STATS_ID']==y['SUMMONER_STATS_ID']][0]
            r['effects']=[{'proc id':q['PROC/PASSIVE_ID(S)'],'params':q['PROC/PASSIVE_PARAMETERS'],'kind?':q['UNIT_KIND'],'effect area':q['EFFECT_AREA*']}]
            levels+=[r]
        result['levels']=levels
        params+=[result]
    saveInfo2(params,save_directory+"summoner_params.json")

def summon_arts(): #summoning arts
    a=loadInfo2(load_directory+"F_SU_ELEMENT_LEVEL_MST.json")   #s8
    summon_arts={}
    for elem in ['1','2','3','4','5','6']:
        elementName={'1':'fire','2':'water','3':'earth','4':'thunder','5':'light','6':'dark'}[elem]
        levelData=[x for x in a if x['UNIT_ELEMENT']==elem]
        levels=[]
        for lvl in range(1,len(levelData)+1):
            currentLevel=[x for x in levelData if x['LEVEL']==str(lvl)][0]
            nextLevel=[x for x in levelData if x['LEVEL']==str(lvl+1)]
            nextLevel=nextLevel[0] if len(nextLevel)>0 else levelData[0]
            levelInfo={}
            levelInfo['exp to next level']=nextLevel['EXP_GAIN']
            levelInfo['level']=lvl
            levelInfo['boosts']={int(y.split('@')[0]):{'parameters':y.split('@')[1].split(':')[0]+"%",'bb level':int(y.split('@')[1].split(':')[1]),'bb gauge':y.split('@')[1].split(':')[2]+'%'} for y in currentLevel['SWfnWyuQ'].split(',')}
            levelInfo['desc']=getDict('MST_SU_ELEM_LV_'+currentLevel['UNIT_ELEMENT']+'_'+str(lvl)+'_DESC').replace('\u2605','*')
            levels+=[levelInfo]
        summon_arts[elementName]=levels
    saveInfo2(summon_arts,save_directory+"summoning_arts.json")

def arena(): #arena ranks and rewards
    a=loadInfo2(load_directory+"M_ARENA_RANK_MST.json")
    ranks=[]
    for rank in a:
        current={}
        current['name']=getDict(rank['ARENA_RANK_NAME'])
        current['rank number']=int(rank['ARENA_RANK'])
        current['text file']=rank["MAP_OPENING_TEXT_FILE"]
        current['ABP required']=int(rank['ARENA_RANK_MAX_POINTS'])+1
        if (rank["REQUIREMENT_TYPE*"]=="1"):
            current['rewards']=[{'type':'gem(s)','quantity':int(rank["ARENA_RANK_REWARDS"].split(':')[1])}]
        elif (rank["REQUIREMENT_TYPE*"]=="2"):
            current['rewards']=[{'type':'sphere','id':int(rank["ARENA_RANK_REWARDS"].split(':')[0]),'quantity':int(rank["ARENA_RANK_REWARDS"].split(':')[1]),'name':getDict('MST_SPHERES_'+rank["ARENA_RANK_REWARDS"].split(':')[0]+'_NAME')}]
        else:
            current['rewards']=[]
        ranks+=[current]
    saveInfo2(ranks,save_directory+"arena_ranks.json")

def unit(): #info.json
    a=loadInfo2(load_directory+"F_UNIT_MST.json")
    units={}
    for x in a:
        u={}
        u['id']=x['UNIT_ID']
        u['rarity']=int(x['RARITY'])
        u['gender']={'0':'genderless','1':'male','2':'female'}[x['Unit Gender']]
        u['max level']=int(x['UNIT_MAX_LEVEL'])
        u['name']=getDict('MST_UNIT_'+str(u['id'])+'_NAME')
        print(str(u['id'])+": "+str(u['name']))
        [imp1,imp2,imp3,imp4]=x["UNIT_IMP"].split(':')
        u['imps']={'hp':int(imp1),'atk':int(imp2),'def':int(imp3),'rec':int(imp4)}
        u['element']={'1':'fire','2':'water','3':'earth','4':'thunder','5':'light','6':'dark'}[x['UNIT_ELEMENT']]
        u['cost']=int(x['UNIT_COST'])
        u['stats']={}
        u['stats']['base']={'hp':int(x['UNIT_BASE_HP']),'atk':int(x['UNIT_BASE_ATTACK']),'def':int(x['UNIT_BASE_DEFENSE']),'rec':int(x['UNIT_BASE_REC'])}
        u['stats']['lord']={'hp':int(x['UNIT_LORD_HP']),'atk':int(x['UNIT_LORD_ATTACK']),'def':int(x['UNIT_LORD_DEFENSE']),'rec':int(x['UNIT_LORD_REC'])}
        diff=[int(x['UNIT_LORD_HP'])-int(x['UNIT_BASE_HP']),int(x['UNIT_LORD_ATTACK'])-int(x['UNIT_BASE_ATTACK']),int(x['UNIT_LORD_DEFENSE'])-int(x['UNIT_BASE_DEFENSE']),int(x['UNIT_LORD_REC'])-int(x['UNIT_BASE_REC'])]
        try:
            u['stats']['breaker']={'atk':(int(x['UNIT_BASE_ATTACK'])+int(diff[1])+(int(x['UNIT_MAX_LEVEL'])-1)*2),'def':(int(x['UNIT_BASE_DEFENSE'])+int(diff[2])-(int(x['UNIT_MAX_LEVEL'])-1)*2)}
        except:
            print("Failed to get Breaker stats for "+u['id']+": "+u['name'])
        try:
            u['stats']['guardian']={'def':(int(x['UNIT_BASE_DEFENSE'])+int(diff[2])+(int(x['UNIT_MAX_LEVEL'])-1)*2),'rec':(int(x['UNIT_BASE_REC'])+int(diff[3])-(int(x['UNIT_MAX_LEVEL'])-1))}
        except:
            print("Failed to get Guardian stats for "+u['id']+": "+u['name'])
        try:
            u['stats']['oracle']={'def':(int(x['UNIT_BASE_DEFENSE'])+int(diff[2])-(int(x['UNIT_MAX_LEVEL'])-1)),'rec':(int(x['UNIT_BASE_REC'])+int(diff[3])+(int(x['UNIT_MAX_LEVEL'])-1)*3)}
        except:
            print("Failed to get Oracle stats for "+u['id']+": "+u['name'])
        try:
            u['stats']['anima']={'hp':(int(x['UNIT_BASE_HP'])+diff[0]+(int(x['UNIT_MAX_LEVEL'])-1)*7.5),'rec':(int(x['UNIT_BASE_REC'])+diff[3]-(int(x['UNIT_MAX_LEVEL'])-1)*2)}
        except:
            print("Failed to get Anima stats for "+u['id']+": "+u['name']+" "+str(int(x['UNIT_MAX_LEVEL'])-1))
        u['sale price']=int(x['ITEM_SALE_PRICE'])
        u['csv']=x['ANIMATION']
        u['ai']=int(x['UNIT_AI_ID'])
        u['sell caution']={'0':'false','1':'true'}[x['UNIT_SELL_CAUTION']]
        u['available']={'0':'false','1':'true'}[x['VALID_ITEM=1,0=IGNORE']]
        u['exp pattern']=int(x['UNIT_EXP_PATTERN_ID'])
        u['skills']={}
        for bb_type in ['bb','sbb','ubb']: #COMMENT OUT DICTIONARY FOR BBS
            if (x[bb_type.upper()+'_ID']!='0'):
                if (x[bb_type.upper()+'_ID'] not in bb):
                    try:
                        print(bb_type.upper()+'_ID')
                        print(x[bb_type.upper()+'_ID'])
                        print(bb[x[bb_type.upper()+'_ID']])
                        print("Error on "+str(bb_type)+" for ID "+str(x['UNIT_ID']))
                    except:
                        print("Error on "+str(bb_type)+" for ID "+str(x['UNIT_ID']))
                else:
                    u['skills'][bb_type]=bb[x[bb_type.upper()+'_ID']]
        u['unit series']=x['SP_SERIES']
        u['guide id']=int(x['QUEST_MAP_NUMBER/GUIDE_ID'])
        try:
            u['leader skill']=lss[u['id']] if u['id'] in lss else {'id':x['LEADER_SKILL_ID']}
        except:
            print("Leader Skill fail on "+str(x))
            u['leader skill']='null'
        u['extra skill']=(ess[u['id']] if u['id'] in ess else {'id':u['id']})
        u['unit kind']=x['UNIT_KIND'] #needs to be looked into
        u['getting type']=x['UNIT_GETTING_TYPE'] #needs to be looked into
        u['movement']={ 'attack':   {'move speed':int(x['UNIT_MOVE_SPEED']),'move type':int(x['UNIT_ATTACK_MOVE_TYPE'])},
                        'skill':    {'move speed':int(x['UNIT_MOVE_SPEED']),'move type':int(x['UNIT_SKILL_MOVE_TYPE'])}}
        try:
            u['normal attack']={'drop checks':int(x['DROP_CHECK_COUNT']),
                                'damage frames':[int(y.split(':')[0]) for y in x['DAMAGE_FRAMES'].split(',')],
                                'damage distributions':[int2(y.split(':')[1]) for y in x['DAMAGE_FRAMES'].split(',')],
                                'sound effects': {'frames':[int(y.split(':')[0]) for y in x['BATTLE_EFFECT_GROUP_FRAMES'].split(',')],
                                'effect id':[int(y.split(':')[1]) for y in x['BATTLE_EFFECT_GROUP_FRAMES'].split(',')]}}
        except:
            print(x['DAMAGE_FRAMES'])
        units[u['id']]=u
    saveInfo2(units,save_directory+"unit.json")

def unit2(): #info.json
    a=loadInfo2(load_directory+"F_UNIT_MST.json")
    units={}
    for x in a:
        u={}
        if(len(x['UNIT_ID'])==6):
            u['id']=x['UNIT_ID']
            u['rarity']=int(x['RARITY'])
            u['gender']={'0':'genderless','1':'male','2':'female'}[x['Unit Gender']]
            u['max level']=int(x['UNIT_MAX_LEVEL'])
            u['name']=getDict('MST_UNIT_'+str(u['id'])+'_NAME')
            print(str(u['id'])+": "+str(u['name']))
            [imp1,imp2,imp3,imp4]=x["UNIT_IMP"].split(':')
            u['imps']={'hp':int(imp1),'atk':int(imp2),'def':int(imp3),'rec':int(imp4)}
            u['element']={'1':'fire','2':'water','3':'earth','4':'thunder','5':'light','6':'dark'}[x['UNIT_ELEMENT']]
            u['cost']=int(x['UNIT_COST'])
            u['stats']={}
            u['stats']['base']={'hp':int(x['UNIT_BASE_HP']),'atk':int(x['UNIT_BASE_ATTACK']),'def':int(x['UNIT_BASE_DEFENSE']),'rec':int(x['UNIT_BASE_REC'])}
            u['stats']['lord']={'hp':int(x['UNIT_LORD_HP']),'atk':int(x['UNIT_LORD_ATTACK']),'def':int(x['UNIT_LORD_DEFENSE']),'rec':int(x['UNIT_LORD_REC'])}
            diff=[int(x['UNIT_LORD_HP'])-int(x['UNIT_BASE_HP']),int(x['UNIT_LORD_ATTACK'])-int(x['UNIT_BASE_ATTACK']),int(x['UNIT_LORD_DEFENSE'])-int(x['UNIT_BASE_DEFENSE']),int(x['UNIT_LORD_REC'])-int(x['UNIT_BASE_REC'])]
            try:
                u['stats']['breaker']={'atk':(int(x['UNIT_BASE_ATTACK'])+int(diff[1])+(int(x['UNIT_MAX_LEVEL'])-1)*2),'def':(int(x['UNIT_BASE_DEFENSE'])+int(diff[2])-(int(x['UNIT_MAX_LEVEL'])-1)*2)}
            except:
                print("Failed to get Breaker stats for "+u['id']+": "+u['name'])
            try:
                u['stats']['guardian']={'def':(int(x['UNIT_BASE_DEFENSE'])+int(diff[2])+(int(x['UNIT_MAX_LEVEL'])-1)*2),'rec':(int(x['UNIT_BASE_REC'])+int(diff[3])-(int(x['UNIT_MAX_LEVEL'])-1))}
            except:
                print("Failed to get Guardian stats for "+u['id']+": "+u['name'])
            try:
                u['stats']['oracle']={'def':(int(x['UNIT_BASE_DEFENSE'])+int(diff[2])-(int(x['UNIT_MAX_LEVEL'])-1)),'rec':(int(x['UNIT_BASE_REC'])+int(diff[3])+(int(x['UNIT_MAX_LEVEL'])-1)*3)}
            except:
                print("Failed to get Oracle stats for "+u['id']+": "+u['name'])
            try:
                u['stats']['anima']={'hp':(int(x['UNIT_BASE_HP'])+diff[0]+(int(x['UNIT_MAX_LEVEL'])-1)*7.5),'rec':(int(x['UNIT_BASE_REC'])+diff[3]-(int(x['UNIT_MAX_LEVEL'])-1)*2)}
            except:
                print("Failed to get Anima stats for "+u['id']+": "+u['name']+" "+str(int(x['UNIT_MAX_LEVEL'])-1))
            u['sale price']=int(x['ITEM_SALE_PRICE'])
            u['csv']=x['ANIMATION']
            u['ai']=int(x['UNIT_AI_ID'])
            u['sell caution']={'0':'false','1':'true'}[x['UNIT_SELL_CAUTION']]
            u['available']={'0':'false','1':'true'}[x['VALID_ITEM=1,0=IGNORE']]
            u['exp pattern']=int(x['UNIT_EXP_PATTERN_ID'])
            u['skills']={}
            for bb_type in ['bb','sbb','ubb']: #COMMENT OUT DICTIONARY FOR BBS
                if (x[bb_type.upper()+'_ID']!='0'):
                    if (x[bb_type.upper()+'_ID'] not in bb):
                        try:
                            print(bb_type.upper()+'_ID')
                            print(x[bb_type.upper()+'_ID'])
                            print(bb[x[bb_type.upper()+'_ID']])
                            print("Error on "+str(bb_type)+" for ID "+str(x['UNIT_ID']))
                        except:
                            print("Error on "+str(bb_type)+" for ID "+str(x['UNIT_ID']))
                    else:
                        u['skills'][bb_type]=bb[x[bb_type.upper()+'_ID']]
            u['unit series']=x['SP_SERIES']
            u['guide id']=int(x['QUEST_MAP_NUMBER/GUIDE_ID'])
            try:
                u['leader skill']=lss[u['id']] if u['id'] in lss else {'id':x['LEADER_SKILL_ID']}
            except:
                print("Leader Skill fail on "+str(x))
                u['leader skill']='null'
            u['extra skill']=(ess[u['id']] if u['id'] in ess else {'id':u['id']})
            u['unit kind']=x['UNIT_KIND'] #needs to be looked into
            u['getting type']=x['UNIT_GETTING_TYPE'] #needs to be looked into
            u['movement']={ 'attack':   {'move speed':int(x['UNIT_MOVE_SPEED']),'move type':int(x['UNIT_ATTACK_MOVE_TYPE'])},
                            'skill':    {'move speed':int(x['UNIT_MOVE_SPEED']),'move type':int(x['UNIT_SKILL_MOVE_TYPE'])}}
            try:
                u['normal attack']={'drop checks':int(x['DROP_CHECK_COUNT']),
                                    'damage frames':[int(y.split(':')[0]) for y in x['DAMAGE_FRAMES'].split(',')],
                                    'damage distributions':[int2(y.split(':')[1]) for y in x['DAMAGE_FRAMES'].split(',')],
                                    'sound effects': {'frames':[int(y.split(':')[0]) for y in x['BATTLE_EFFECT_GROUP_FRAMES'].split(',')],
                                    'effect id':[int(y.split(':')[1]) for y in x['BATTLE_EFFECT_GROUP_FRAMES'].split(',')]}}
            except:
                print(x['DAMAGE_FRAMES'])
            units[u['id']]=unit
    saveInfo2(units,save_directory+"globalUnits.json")

def int2(x):
    try:
        return int(x)
    except:
        try:
            return int(x[0])
        except:
            return x

def fix(x):
    r=""
    x=x.replace("<br>"," ").replace("\u2605","*")
    d=False
    while (len(x)>0):
        if (x[0]=="<"):
            d=True
        r=r if d else r+x[0]
        if (x[0]==">"):
            d=False
        x=x[1:]
    return r

def summon_gates():
    q=loadInfo2(load_directory+"M_GACHA_MST.json")
    r={}
    for x in q:
        r[int(x['SUMMON_GATE_ID'])]={'name':x['SUMMON_GATE_NAME'],
                                     'desc':fix(x['SUMMON_GATE_DESCRIPTION_A']),
                                     'short desc':fix(x['SUMMON_GATE_DESCRIPTION_B']),
                                     'start time':x['AVAILABILITY_TIME_START/AMOUNT_REQUIRED'],
                                     'end time':x['AVAILABILITY_TIME_END'],
                                     'background image':x['BACKGROUND_IMAGE'],
                                     'door image':x['DOOR_IMAGE'],
                                     'summon button image':x['SUMMON_BUTTOM_IMAGE'],
                                     'priority':x['AI_PRIORITY'],
                                     }
        if (x['GEM_COST']!="0"):
            r[int(x['SUMMON_GATE_ID'])]['gem cost']=int(x['GEM_COST'])
        if (x['HONOR_POINTS']!="0"):
            r[int(x['SUMMON_GATE_ID'])]['honor points cost']=int(x['HONOR_POINTS'])
    saveInfo2(r,save_directory+"summon_gates.json")

def exchange_hall():
    q=loadInfo2(load_directory+"F_ACHIEVEMENT_TRADE_MST.json")
    res={}
    for x in q:
        this={'cost':int(x['EXCHANGE_HALL_COST']),
              'time start':x['AVAILABILITY_TIME_START/AMOUNT_REQUIRED'],
              'time end':x['AVAILABILITY_TIME_END'],
              'exchange limit':int(x['EXCHANGE_HALL_LIMIT']),
              }
        try:
            r=x['EXCHANGE_HALL_ITEM*'].split(':')
            if (r[0]=='4'): #MST_ITEMS_MATERIAL_XX
                this['reward']={'type':'evolution material',
                                'id':r[1],
                                'name':getDict('MST_ITEMS_MATERIAL_'+r[1]+'_NAME'),
                                'desc':getDict('MST_ITEMS_MATERIAL_'+r[1]+'_SHORTDESCRIPTION'),
                                'long desc':getDict('MST_ITEMS_MATERIAL_'+r[1]+'_LONGDESCRIPTION'),
                                'quantity':int(r[2])
                                }
            elif (r[0]=='5'): #MST_ITEMS_BATTLEITEMS_XX
                this['reward']={'type':'battle item',
                                'id':r[1],
                                'name':getDict('MST_ITEMS_BATTLEITEMS_'+r[1]+'_NAME'),
                                'desc':getDict('MST_ITEMS_BATTLEITEMS_'+r[1]+'_SHORTDESCRIPTION'),
                                'long desc':getDict('MST_ITEMS_BATTLEITEMS_'+r[1]+'_LONGDESCRIPTION'),
                                'quantity':int(r[2])
                                }
            elif (r[0]=='6'): #MST_UNIT_XX
                this['reward']={'type':'unit',
                                'id':r[1],
                                'name':getDict('MST_UNIT_'+r[1]+'_NAME'),
                                'quantity':int(r[2])
                                }
            elif (r[0]=='7'): #MST_SPHERES_XX
                this['reward']={'type':'sphere',
                                'id':r[1],
                                'name':getDict('MST_SPHERES_'+r[1]+'_NAME'),
                                'desc':getDict('MST_SPHERES_'+r[1]+'_SHORTDESCRIPTION'),
                                'long desc':getDict('MST_SPHERES_'+r[1]+'_LONGDESCRIPTION'),
                                'quantity':int(r[2])
                                }
            elif (r[0]=='9'): #KEY
                this['reward']={'type':'key',
                                'id':r[1],
                                'name':{'1':'Metal Key','2':'Jewel Key','3':'Imp Key'}[r[1]],
                                'quantity':int(r[2])
                                }
        except Exception as exc:
            print("Error on "+str(x['EXCHANGE_HALL_NAME'])+": "+str(exc))
        res[x['EXCHANGE_HALL_ID']]=this
    saveInfo2(res,save_directory+"exchange_hall.json")


def item():
    types={'1':['ITEMS_BATTLEITEMS','battle item'],'2':['ITEMS_MATERIAL','material'],'3':['SPHERES','sphere'],'4':['EVOITEM','evolution item'],'5':['BOOSTERITEM','booster item'],'6':['LSSPHERE','ls sphere']}
    itemTypes={'1':'grass','2':'feather','3':'nut','4':'drop','5':'claw','6':'fang','7':'eye','8':'pelt','9':'bone','10':'bug','11':'stone'}
    q=loadInfo2(load_directory+"F_ITEM_MST.json")
    items={}
    for item in q:
        this={}
        this['id']=item['ITEM_ID']
        if (item["ITEM_MAX_EQUIPPED"] not in ['','0']):
            this['max equip']=int(item["ITEM_MAX_EQUIPPED"])
        [txt,txtType]=types[item["ITEM_TYPE*"]]
        this['name']=getDict('MST_'+txt+'_'+this['id']+'_NAME')
        this['desc']=getDict('MST_'+txt+'_'+this['id']+'_SHORTDESCRIPTION')
        this['lore']=getDict('MST_'+txt+'_'+this['id']+'_LONGDESCRIPTION')
        this['type']=txtType
        this['guide id']=item["QUEST_MAP_NUMBER/GUIDE_ID"]
        this['rarity']=int(item['RARITY'])
        this['thumbnail']=item['THUMBNAIL']
        #this['effects']={'ids':item['PROC/PASSIVE_ID(S)'],'params':item['PROC/PASSIVE_PARAMETERS']}
        this['effects']=parse(item['PROC/PASSIVE_ID(S)'],item['PROC/PASSIVE_PARAMETERS'],1)['effects']
        this['sale price']=int(item['ITEM_SALE_PRICE'])
        this['max stack']=int(item['ITEM_MAX_STACK'])
        this['sale caution']={'1':'true','0':'false'}[item['UNIT_SELL_CAUTION']]
        this['from raid']={'0':'false','1':'true'}[item["ITEM_RAID_FLAG"]]
        #this['item_raid_usage_flag']=item["ITEM_RAID_USAGE_FLAG"]
        if (this['type']=='sphere'):
            this['sphere type']=getDict('SPHERE_TYPE_NAME_'+item["ITEM_KIND"])
        if (item['REQUIREMENT_RARITY*'] in itemTypes):
            this['item type']=itemTypes[item['REQUIREMENT_RARITY*']]
        this['target']={'0':'none','1':'single','2':'party'}[item['ITEM_TARGET_AREA']]
        if (item['EIN6D3xJ']!='0'):
            this['color']={'1':'red','2':'blue','3':'green','4':'yellow','5':'gray','6':'purple','7':'brown','8':'pink'}[item['EIN6D3xJ']]
        if (item['jkldTrhL']=='1'):
            this['sarc']='true'
        items[item["ITEM_ID"]]=this
    saveInfo2(items,save_directory+"items.json")

def fg():
    a=loadInfo2(load_directory+"F_FROGATE_MST.json")
    b=loadInfo2(load_directory+"F_FROGATE_REWARD_MST.json")
    r={}
    for x in a:
        this={}
        this['id']=x['FRONTIER_GATE_ID']
        this['name']=getDict('MST_FROGATE'+this['id']+'_NAME')
        this['desc']=fix(getDict('MST_FROGATE'+this['id']+'_DESC'))
        this['start time']=x['AVAILABILITY_TIME_START/AMOUNT_REQUIRED']
        this['end time']=x['AVAILABILITY_TIME_END']
        this['restrictions']=x['RESTRICTIONS*']
        this['rewards']=[]
        r[x['FRONTIER_GATE_ID']]=this
    for x in b:
        this={}
        this['quantity']=int(x['PRESENT_AMOUNT'])
        this['id']=x['REWARD_ID']
        this['requirement']={'type':{'1':'floors','2':'points','8001':'points'}[x["Ga6qSJr0"]],'amount':int(x["REQUIREMENT_PARAMETER"])}
        this['reward id']=x['REWARD_ITEM_ID']
        this['reward type']=x['REWARD_TYPE*']
        this['elgif reward']=x['ELGIF_REWARD*']
        r[x['FRONTIER_GATE_ID']]['rewards']+=[this]
    saveInfo2(r,save_directory+"frontier_gate.json")

def bbs():
    a=loadInfo2(load_directory+"F_SKILL_MST.json")
    b=loadInfo2(load_directory+"F_SKILL_LEVEL_MST.json")
    r={}
    for x in a:
        this={}
        this['id']=x['BB_ID']
        this['drop checks']=int(x['DROP_CHECK_COUNT'])
        this['desc']=getDict('MST_SKILLS_'+this['id']+'_DESCRIPTION')
        this['name']=getDict('MST_SKILLS_'+this['id']+'_NAME')
        this['damage frames']=[]
        #print(len(x["PROC/PASSIVE_ID(S)"].split('@')))
        #print(range(len(x["PROC/PASSIVE_ID(S)"].split('@'))))
        for df in range(len(x["PROC/PASSIVE_ID(S)"].split('@'))):
            current={}
            pid=x["PROC/PASSIVE_ID(S)"].split('@')[df]
            
            try:
                start_frame=x['SKILL_START_FRAME'].split('@')[df]
            except:
                start_frame=x['SKILL_START_FRAME']
            try:
                t_area=x['SKILL_TARGET_AREA'].split('@')[df]
            except:
                t_area=x['SKILL_TARGET_AREA']
            try:
                damage_frames=x['DAMAGE_FRAMES'].split('@')[df]
            except:
                damage_frames=x['DAMAGE_FRAMES']

            current['proc id']=pid
            try:
                current['frame times']=[int(y.split(':')[0].replace(' ','')) for y in damage_frames.split(',')]
            except:
                current['frame times']=["ERROR"]
                print("ERROR on frame times: "+str(damage_frames))
            try:
                current['damage distributions']=[int(y.split(':')[1]) for y in damage_frames.split(',')] if damage_frames!="0" else []
            except:
                current['damage distributions']=["ERROR"]
                print(x['BB_ID'])
                print("ERROR on damage distributions: "+str(damage_frames))
            current['hits']=len(current['damage distributions'])
            
            try:
                current['effect delay']=int(start_frame)
            except:
                print(x['SKILL_START_FRAME'])
                print(start_frame)
                print(start_frame.replace('`',''))
                start_frame = start_frame.replace('`','')
                print(start_frame)
                try:
                    current['effect delay']=int(start_frame)
                except:
                    current['effect delay']=1
            try:
                current['effect delay']=int(start_frame)
            except:
                current['effect delay']=999
            try:
                current['target']={'0':'none','1':'single','2':'all'}[t_area]
            except:
                current['target']='error'
            this['damage frames']+=[current]
        if (x['UNIT_ELEMENT']!="0"):
            this['element']={'1':'fire','2':'water','3':'earth','4':'thunder','5':'light','6':'dark'}[x['UNIT_ELEMENT']]
        this['levels']=[]
        try:
            bbLevels=[x for x in b if x['BB_ID']==this['id']][0]
            for bbLevel in bbLevels['PROCESS_ID'].split('|'):
                c=parse(x['PROC/PASSIVE_ID(S)'],bbLevel.split(':')[2],1)
                c['bc cost']=int(int(bbLevel.split(':')[1])/100)
                this['levels']+=[c]
            r[x['BB_ID']]=this
        except:
            pass
    saveInfo2(r,save_directory+"bbs.json")

def es():
    a=loadInfo2(load_directory+"F_EXTRA_PASSIVE_SKILL_MST.json")
    r={}
    for x in a:
        this={}
        this['id']=x["ES_ID"]
        this['desc']=getDict('MST_EXTRAPASSIVESKILL_'+this['id']+'_DESCRIPTION')
        this['name']=getDict('MST_EXTRAPASSIVESKILL_'+this['id']+'_NAME')
        this['rarity']=int(x['RARITY'])
        this['effects']=parse(x["PROC/PASSIVE_ID(S)"],x["PROC/PASSIVE_PARAMETERS"],2)['effects']
        this['conditions']=x["ES_PARAMETERS"]
        r[x["ES_ID"]]=this
    saveInfo2(r,save_directory+"es.json")
    

def ls():
    a=loadInfo2(load_directory+"F_LEADER_SKILL_MST.json")
    r={}
    for x in a:
        this={}
        this['id']=x["LEADER_SKILL_ID"]
        this['desc']=getDict('MST_LEADERSKILLS_'+this['id']+'_DESCRIPTION')
        this['name']=getDict('MST_LEADERSKILLS_'+this['id']+'_NAME')
        this['effects']=parse(x["PROC/PASSIVE_ID(S)"],x["PROC/PASSIVE_PARAMETERS"],2)['effects']
        r[x["LEADER_SKILL_ID"]]=this
    saveInfo2(r,save_directory+"ls.json")

def sp():
    a=loadInfo2(load_directory+"F_UNIT_FE_SKILL_MST.json")
    b=loadInfo2(load_directory+"F_FE_SKILL_MST.json")
    dictionary=loadInfo2("datamines/dictionary.json")
    r={}
    for x in a:
        this={}
        idnum=x["UNIT_ID"]
        this['desc']=getDict('MST_FE_SKILLS_'+str(x["SP_ID"])+'_DESC')
        this['name']=getDict('MST_FE_SKILLS_'+str(x["SP_ID"])+'_NAME')
        this['category id']=x['SP_CAT_ID']
        this['category name']=sp_cat[str(x['SP_CAT_ID'])]
        this['id']=x['SP_ID']
        for y in b:
            if(y['SP_ID']==x['SP_ID']):
                this['sp cost']=y['SP_NEED_BP']
                this['sp series']=y['SP_SERIES']
                this['effects']=parse(y["PROC/PASSIVE_ID(S)"],y["PROC/PASSIVE_PARAMETERS"],2)['effects']
                break
        try:
            count=len(r[idnum])
        except:
            count=0
        if(count==0):
            r[idnum]=[]
        r[idnum].append(this)
    saveInfo2(r,save_directory+"feskills.json")


#---------MISC-------------------------
    
def guildArt():
    q=loadInfo2(load_directory+"F_GUILD_ART_MST.json")
    r={}
    for x in q:
        r[int(x['GUILD_INSIGNIA_NUMBER'])]={'guild level required':int(x['GUILD_LEVEL']),'image':x['IMAGE_LOCATION']}
    saveInfo2(r,save_directory+"misc/guild_art.json")

def coloClass():
    q=loadInfo2(load_directory+"F_COLOSSEUM_CLASS_MST.json")
    r={}
    for x in q:
        c=x["COLO_CLASS_NUMBER"]
        r[c]={'name':getDict('MST_COLOSSEUM_CLASS_'+c+'_NAME'),
              'desc':getDict('MST_COLOSSEUM_CLASS_'+c+'_DESC'),
              'banner':x['BANNER_IMG'],
              'cost':x['MAX_COST']}
    saveInfo2(r,save_directory+"misc/colo_class.json")

def expPattern():
    q=loadInfo2(load_directory+"M_UNIT_EXP_PATTERN_MST.json")
    r={}
    for x in list(set([y['UNIT_EXP_PATTERN_ID'] for y in q])):
        z={}
        current=[y for y in q if y['UNIT_EXP_PATTERN_ID']==x]
        for y in current:
            z[int(y['LEVEL'])]=int(y['GUILD_LEVEL_MIN_EXP_THRESHOLD'])
        r[int(x)]=z
    saveInfo2(r,save_directory+"misc/exp_pattern.json")

