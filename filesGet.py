# Instructions:
#
# To update:
#   update()
# To update decrypted files:
#   decrypt_files()
# Note: you could also decrypt the files through update2(), which redownloads them and translates them at the same time, but it will be slower
#
# If the script doesn't run, you may need to increase the client number (which is 191 at the time of writing this)
#  Increase it on all three lines marked with "CHANGE_CLIENT_NUM" in the comments (use "find" to easily find them)

from utils import *
import requests
import os
#1154
client='2900' #CHANGE_CLIENT_NUM
cdnVersion='1'

def getFile(fileId,key,version,replace=False):
    global cdnVersion,client
    # return http://2.cdn.bravefrontier.gumi.sg/mst/2200/
    # return decrypt(bytes_to_str(requests.get("https://bf-prod-dlc-gumi-sg.akamaized.net/mst/"+str(client)+"/Ver"+str(version)+"_"+str(fileId)+".dat?v="+str(cdnVersion)).content),key,replace=replace) #otherwise did str()[2:-1]
    print("http://dv5bk1m8igv7v.cloudfront.net/asset/"+str(client)+"/mst/Ver"+str(version)+"_"+str(fileId)+".dat?v="+str(cdnVersion))
    print(requests.get("http://dv5bk1m8igv7v.cloudfront.net/asset/"+str(client)+"/Ver"+str(version)+"_"+str(fileId)+".dat?v="+str(cdnVersion)).content)
    try:
        return decrypt(bytes_to_str(requests.get("http://dv5bk1m8igv7v.cloudfront.net/asset/"+str(client)+"/mst/Ver"+str(version)+"_"+str(fileId)+".dat?v="+str(cdnVersion)).content),key,replace=replace) #otherwise did str()[2:-1]
    except:
        pass
##    print("http://2.cdn.bravefrontier.gumi.sg/mst/"+str(client)+"/Ver"+str(version)+"_"+str(fileId)+".dat?v=")
##    try:
##        return decrypt(bytes_to_str(requests.get("https://bf-prod-dlc-gumi-sg.akamaized.net/mst/"+str(client)+"/Ver"+str(version)+"_"+str(fileId)+".dat?v="+str(cdnVersion)).content),key,replace=replace) #otherwise did str()[2:-1]
##    except:
##        print(requests.get("http://2.cdn.bravefrontier.gumi.sg/mst/"+str(client)+"/Ver"+str(version)+"_"+str(fileId)+".dat?v="+str(cdnVersion)).content)

def getVersions(files):
    q=response("MfZyu1q9",parameters={"KeC10fuL":[{'d2RFtP8T': '0', 'moWQ30GH': 'M_DEFINE_MST'},{'d2RFtP8T': '0', 'moWQ30GH': 'F_CDN'}]+[x for x in files if x['moWQ30GH'] not in ['M_DEFINE_MST','F_CDN']]})
    global client,cdnVersion
    q['IMPORTANT_VALUES'][0]
    client=q['IMPORTANT_VALUES'][0]['CLIENT_VERSION?']
    cdnVersion=[x for x in q['FILES_VERSION_INFO'] if 'CDN' in x['RAID_TARGET']][0]['FILE_VERSION']
    return q['FILES_VERSION_INFO']

def getVersions2(files):
    q=response("MfZyu1q9",parameters={"KeC10fuL":[{'d2RFtP8T': '0', 'moWQ30GH': 'M_DEFINE_MST'},{'d2RFtP8T': '0', 'moWQ30GH': 'F_CDN'}]+[x for x in files if x['moWQ30GH'] not in ['M_DEFINE_MST','F_CDN']]},replace=False)
    r=eval(replaceKeys(str(q)))
    global client,cdnVersion
    client=r['IMPORTANT_VALUES'][0]['CLIENT_VERSION?']
    cdnVersion=[x for x in r['FILES_VERSION_INFO'] if 'CDN' in x['RAID_TARGET']][0]['FILE_VERSION']
    return [q,r['FILES_VERSION_INFO']]

def getAll(files):
    return response("MfZyu1q9",parameters={"KeC10fuL":[{'d2RFtP8T': '0', 'moWQ30GH': 'M_DEFINE_MST'},{'d2RFtP8T': '0', 'moWQ30GH': 'F_CDN'}]+[x for x in files if x['moWQ30GH'] not in ['M_DEFINE_MST','F_CDN']]},replace=False)

def saveInfo(obj,filename,silent=False): #Save function!
    f=open(filename,'w')
    json.dump(obj,f)
    f.close()
    if (not silent):
        print("Saved to file: "+filename)

def saveInfo2(obj,filename):
    f=open(filename,'w')
    json.dump(obj,f,separators=(',',':'),indent=4,sort_keys=True)
    f.close()
    print("Saved to file: "+filename)

def loadInfo(filename):
    f=open(filename,'r')
    q=json.load(f)
    f.close()
    return q

def loadInfo2(filename):
    with open(filename,encoding='utf-8') as f:
        q=json.load(f)
    f.close()
    return q

filenames={#'F_GUILD_POINT_EXCHANGE_MST': ['hR47gBvi','O3nEmUs2'],
           'F_STAMP_SET_MST':['KuCe7t3p','em68GxrB'], #111
           'F_RAID_WORLD_MST':['35fQnyPs','8ozA4wZv'], #123
           'F_RAID_RC_MST':['i7xd5oMb','gui7x0cr'], #128
           'F_UNIT_FE_CATEGORY_MST':['nd18wpsy','XZvyRf62'], #134
           'F_SU_ARM_PASSIVE_MST':['XjL3fKG0','89CxLmhs'], #142
           'F_SU_IMG_MST':['Ydra41vX','7h5fuTma'], #150
           'F_SU_ELEMENT_LEVEL_MST':['k6H83Uix','WqvJ64XG'], #143
           'F_SU_EX_SKILL_MST':['kT3vA9j2','LaM0o9P7'], #144
           'F_MISSION_SCRIPT_MST':['F2Dz3QHU','U91CxXGi'], #14
           'F_GATE_MST':['Nt8xg5eG','W37QmhSb'], #88
           'F_SU_ARM_ELEMENT_MST':['VbFp8XZ6','2TuAmfX4'], #147
           'F_SU_ARM_MST':['iTMk51hB','e5t01snA'], #141           
           'F_FE_SKILL_MST':['2h9r3yEY','w3Z9EeUR'], #63
           'F_RECIPE_MST':['3TM68IaF','na7Wb8u1'], #124
           'F_UNIT_FE_SKILL_MST':['8gu2U4Mh','dc0jxn8u'], #135
           'F_SU_ABILITY_UP_MST':['Xep8qk4D','9p3b8NCg'], #146
           'F_SU_ARM_LEVEL_MST':['qP6nD0IL','T8wGcKd1'], #148
           'F_RESOURCE_MST':['hdt2N6mr','z5dp9GX8'], #107
           'F_ACHIEVEMENT_DELIVER_RATE_MST':['VR6mJD3M','2W4Ja7KU'], #4 - b not here
           'F_CHLNG_MISSION_REWARD_MST':['31BhsATV','6Zwi24yp'], #70 - a not here
           'F_CHLNG_MISSION_GRADE_MST':['6q9ID0wP','1nte4gCY'], #73 - neither here
           #'':['5aueM1ix','HF7B1hat'], #some sort of 6 fodder units: shida, rickel, etc
           'F_CHLNG_MISSION_MST':['8GhcfX4Q','rvIa85RA'], #68 - neither here
           'F_ACHIEVEMENT_TRADE_MST':['qJBsPw38','zGcIk58e'], #1
           'F_SU_ABILITY_MST':['Mkum4tB6','He71kZYp'], #145
           'F_EFFECT_MST':['0VIAZHT9','9ojr0tPC'], #60
           'F_EFFECT_GROUP_MST':['BQJq29Zh','3FWEGtX9'], #65
           'F_RAID_MISSION_MST':['f9eHCSc8','4WbIjfB3'], #118
           'F_EXTRA_PASSIVE_SKILL_MST':['kP4pTJ7n','PDGK5sk3'], #62
           'F_SU_ABILITY_LEVEL_MST':['W3NMn25Z','7vtcn58P'], #112
           'F_MISSION_EP3_MST':['W3sQD9Z5','L5DNP2H9'], #19
           'F_AREA_MST':['vj6fEsg7','73bUW8wn'], #3 - no b
           'F_ACHIEVEMENT_SUBJECT_MST':['G7CqU3EQ','5T6cZ7LD'], #5 - no a
           'F_PURCHASE_AGE_LIMIT_MST':['D7hadU1p','L6gfBpn3'], #43
           'F_MINIGAME_RESOURCE_MST':['XtSrv61M','uHsAU32G'], #12
           'F_CHLNG_MISSION_ITEM_SET_MST':['gm4oR9D5','zBxwtg89'], #67 - neither
           'F_COLOSSEUM_FORMATION_MST':['n6HkMa2E','2Im7tLhs'], #76
           'F_FROGATE_SUPPORT_MST':['QfxUi78N','48EZ6hoH'], #94
           'F_UNIT_COMMENT_MST':['2npmC9Nw','Apc5eIw6'], #131
           'F_UNIT_EVO_MST':['Ef6oG0mz','R9IryC5v'], #139 - no a
           'F_LEADER_SKILL_MST':['4dE8UKcw','HGYZ1Ag5'], #31
           'F_UNIT_CGS_MST':['6rjmY7tV','Y7ezNyn2'], #130
           'F_RAID_BOSS_ROUTE_MST':['z7UiGPQ1','L4pBaT0q'], #121
           #'F_DUNGEON_MST':['B57MJYoF','w5W8RPSG'], #64
           'F_COLOSSEUM_EXTRA_RULE_MST':['P6QeyAS5','4FEhdoA8'], #75
           'F_RESOURCE_BASE_MST':['a4M4dh1i','kIj2n6s5'],
           'F_HELP_DETAIL_MST':['EwQ0S5cX','8HG9C1nw'], #25
           'F_RAID_MISSION_POINT_MST':['gVmh3Lw2','qga56iME'], #125
           'F_GRAND_MISSION_TREASURE_MST':['gy91IuGm','wBumj9e7'], #24
           'F_RAID_USER_ROUTE_MST':['2sjB0RvV','Ny6rB7HV'], #122
           'F_FROGATE_REWARD_MST':['5IRuFdg7','Io3rU5Gj'], #93
           'F_RAID_BATTLE_GROUP_MST':['fYJjG4B6','c0Ejwh7S'], #44
           'F_RAID_POINT_MST':['79MTkNus','76rVpcGL'], #127
           'F_RELOAD_FILE_MST':['kpN3M6tK','1U9ouXzP'], #106
           'F_UNIT_EVO_CATALYST_COMMENT_MST':['C0pU8ev4','Eqx4BrW2'], #138 - no b
           'F_BANNER_INFO_MST':['FhzWn1m9','a9B3nDuA'], #72 - neither
           'F_MISSION_MST':['4gA3WCQX','y1hZzE74'], #20
           'F_RAID_MAP_MST':['39mGIANe','HMib7V50'], #115
           'F_RAID_BOSS_PARTS_MST':['w8Phatd4','6de7rGsP'], #120
           'F_ITEM_MST':['83JWTCGy','houmK14R'], #21
           'F_RAID_MISSION_BOSS_MST':['W3Q62S1F','yu28TMIo'], #116
           'F_ARENA_EXTRA_RULE_MST':['6TICDW7R','mbK4Qg5w'], #71 - neither
           'F_MEDAL_MST':['DX7KZ0Tf','UH1ruJ36'], #32
           'F_COLOSSEUM_CLASS_MST':['L76ovBpj','J3TBnt9Z'], #74
           'F_GRAND_MISSION_MAP_MST':['fSsA7Rg5','tdk6VX4P'], #85
           'F_GRAND_MISSION_END_CND_MST':['hL86KWoR','82sgSkVw'], #89
           'F_GRAND_MISSION_ROUTE_MST':['v4rwhV5p','1fPrRAs3'], #22
           'F_UNIT_MST':['2r9cNSdt','7nL1WTUb'], #137
           'F_GRAND_MISSION_ICON_MST':['VAti08bF','YdE56NQq'], #84
           'F_GRAND_MISSION_FLG_MST':['n0DUZr86','I5jMpA62'], #91
           'F_GRAND_MISSION_SPOT_MST':['r6dVAv7g','q45JQWax'], #23
           'F_UNIT_TYPE_MST':['J4heGZ2U','4a6GF3Pt'], #98
           'F_RAID_MISSION_CLEAR_CND_MST':['Pgnu7d8k','E81Hkv3g'], #117
           'F_SKILL_LEVEL_MST':['zLIvD5o2','rF97pVdT'], #105
           'F_SCENARIO_CATEGORY_MST':['8Uk4nHfC','V6Yf4g1X'], #109
           'F_FROGATE_MST':['6Sv01F4z','SA9y7qu6'], #92
           'F_GUILD_INFO_MST':['M3vCu81Q','K3b981cX'],
           'F_SKILL_MST':['wkCyV73D','JA03wvHG'], #113
           'F_GRAND_MISSION_REWARD_MST':['78ganRXv','rLk8V3sj'], #87
           'F_LAND_MST':['1M65tIPz','drCPNM10'], #30
           'F_RAID_BOSS_MST':['4KAXRjg0','a4jIgR2T'], #119
           'F_MISSION_NPC_UNIT_MST':['zVo1bRp9','s7iC3PT0'], #13
           'F_TRIAL_MISSION_MST':['F9fGSe42','Hxidv1y0'], #149
           'F_STAMP_MST':['W2j4E3te','NFJ74Wmg'], #110
           'F_RAID_PLAYSTYLE_MST':['xMFHp36r','7z5RKwhU'], #126
           'F_GUILD_ART_MST':['y6bU2dqW','Jki71Bm9'],
           'F_GRAND_MISSION_MST':['Yg4n5c7G','L60J1vWU'], #86
           'F_SCENARIO_MST':['V5N34aUf','m2iqC6Ka'], #103
           'F_FUNCTION_RELEASE_MST':['FA69am2p','tLaGZ8h3'], #97
           'F_GRAND_MISSION_EVENT_MST':['GJc6VM4k','9SHj5sZ6'], #90
           'F_SHOP_ITEM_MST':['Sb3MW61V','M4eAVZs1'], #104
           'F_UNIT_EXT_MST':['kI94EypD','2yCoEm0q'], #140
           'F_UNIT_EP3_MST':['9ie4KnDt','GIo0uK8b'], #132
           'F_GUILD_SKILL_DETAILS_MST':['M83aDbK2','D3Bda18b'],
           'F_COLOSSEUM_SUPPORT_MST':['5fueF6wx','HNdG95VT'], #77
           'F_CHRONOLOGY_PERIOD_MST':['LTpPwF82','93xUK0iZ'], #80
           'F_CHRONOLOGY_MST':['G8pKiV5q','5Wdw19KR'], #79
           'F_CHRONOLOGY_DETAIL_MST':['dFgVx91b','vAkyg17f'], #78
           'F_CHRONOLOGY_WORD_MST':['vw0WR4rt','4b5HGKSs'], #81
           'F_UNIT_EVO_OMNI_MST':['39s0l4sj','4sTslk4s'],
           'F_UNIT_EVO_OMNI_TYPE_MST':['390l4skd','Kdnxl203'],
           'F_LEVEL_MST':['7Hvw8MjR','7Q0xtYai'],
           'F_SU_LEVEL_MST':['fNVP2i89','aZ97rNyw'], #151
}

filenames2={'M_FROHUN_MST':'mQC4s5ka',
            'M_FROHUN_RANKING_REWARD_MST':'P8V71kbw',
            'M_FROHUN_MISSION_GRADE_MST':'zW1i02aG',
            'M_FROHUN_MISSION_REWARD_MST':'4C1Wt8sS',
            'M_FROHUN_MISSION_MST':'5M8jI4cP',
            'M_FROHUN_MVP_RANKING_MST':'nUmaEC41',
            'M_FROHUN_HR_MST':'h09mEvDR',
            'M_FROHUN_MISSION_ITEM_SET_MST':'dn0NfRy1',
            'M_RECIPE_MST':'8f0bCciN',
            'M_LEVEL_MST':'YDv9bJ3s',
            'M_DEFINE_MST':'VkoZ5t3K',
            'M_EFFECT_GROUP_MST':'9KUSHf4s',
            'M_EFFECT_MST':'L5j19iny',
            'M_GACHA_EFFECT_MST':'Pf97SzVw',
            'M_RESOURCE_MST':'5MJd7t6F',
            'M_GACHA_MST':'5Y4GJeo3',
            'M_UNIT_EXP_PATTERN_MST':'JYFGe9y6',
            'M_TROPHY_GRADE_MST':'Ked15IpH',
            'M_TROPHY_GROUP_MST':'1NTG2oVZ',
            'M_TROPHY_MST':'6CTU8m2v',
            'M_LAND_MST':'9gIBuAG8',
            'M_INFORMATION_MST':'5nBa3CAe',
            'M_TOWN_FACILITY_MST':'Lh1I3dGo',
            'M_TOWN_FACILITY_LV_MST':'d0EkJ4TB',
            'M_TOWN_LOCATION_MST':'1y2JDv79',
            'M_TOWN_LOCATION_LV_MST':'9ekQ4tZq',
            'M_HELP_MST':'9x4zZCeN',
            'M_HELP_SUB_MST':'5C9LuNrk',
            'M_ARENA_RANK_MST':'6kWq78zx',
            'M_SOUND_MST':'36Sd0Aub',
            'M_NPC_MST':'hV5vWu6C',
            'M_URL_MST':'At7Gny2V',
            'M_AREA_MST':'3SG2wX0R',
            'M_DUNGEON_KEY_MST':'4NG79sX1'}
def get(z): #find key corresponding to M_ file
	a=list(getAll([{'d2RFtP8T': '0', 'moWQ30GH': z}]).keys())
	b=list(getAll([]).keys())
	return [x for x in a if x not in b]


missing= ['F_FROGATE_AREA_MST',
'F_MONSTER_CGG', 'F_MONSTER_CGS', 'F_MONSTER_IMG', 'F_UNIT_CGG', 'F_UNIT_CGS', 'F_UNIT_IMG', 'F_SYSTEM_RES', 'F_GACHA_BG_IMG', 'F_EVENT_FILE',
'F_SAM', 'F_SOUND', 'F_PARTICLE', 'F_MINIGAME_DEFINE_MST', 'F_MINIGAME_BRAVESMASH_LEVEL_MST', 'F_MINIGAME_BRAVESMASH_MONSTER_GROUP_MST',
'F_MINIGAME_BRAVESMASH_MONSTER_MST', 'F_MINIGAME_BRAVESMASH_PARTY_DECK_MST', 'F_MINIGAME_BRAVESMASH_POSITION_MST',
'F_MINIGAME_SPEEDRUSH_BONUS_MST', 'F_MINIGAME_SPEEDRUSH_MONSTER_APPEAR_MST', 'F_MINIGAME_SPEEDRUSH_MONSTER_GROUP_MST', 'F_MINIGAME_SPEEDRUSH_MONSTER_MST',
'F_MINIGAME_SPEEDRUSH_PARTY_DECK_MST', 'F_MINIGAME_SPEEDRUSH_ROLE_MST']
resolved=['F_UNIT_EVO_OMNI_MST', 'F_UNIT_EVO_OMNI_TYPE_MST', 'F_UNIT_EVO_OMNI_RECIPE_MST**','F_CHRONOLOGY_PERIOD_MST', 'F_CHRONOLOGY_MST', 'F_CHRONOLOGY_DETAIL_MST', 'F_CHRONOLOGY_WORD_MST']
#keys for omni+
options=['a4M4dh1i', 'y6bU2dqW', 'kIj2n6s5', 'M3vCu81Q', 'Jki71Bm9', 'hR47gBvi', 'K3b981cX', '1nte4gCY', '6q9ID0wP', 'zBxwtg89', 'gm4oR9D5', 'w3Yv7uSF', 'rvIa85RA', '31BhsATV', '13s7RxgT', '6TICDW7R', '73bUW8wn', '7DAkY1rQ', 'mbK4Qg5w', 'FhzWn1m9', 'pS2HMv8e', '8GhcfX4Q', 'a9B3nDuA', 'G7CqU3EQ', '2W4Ja7KU', 'qJBsPw38', '5T6cZ7LD', 'XkBhe70R', 'zGcIk58e', 'vj6fEsg7', 'KY59Mwhq', 'M83aDbK2', 'O3nEmUs2', 'D3Bda18b', '.dat', 'VR6mJD3M', 'kP4pTJ7n', '9ojr0tPC', '2h9r3yEY', 'PDGK5sk3', 'U1XChi09', 'w3Z9EeUR', 'V9zLvR7n', '9zJFtHr3', 'B57MJYoF', 'HNdG95VT', 'D2FdZK5v', 'w5W8RPSG', '0VIAZHT9', '4keDxjn7', '3FWEGtX9', 'BQJq29Zh', 'L76ovBpj', '93xUK0iZ', 'P6QeyAS5', 'J3TBnt9Z', 'n6HkMa2E', '4FEhdoA8', '5fueF6wx', '2Im7tLhs', 'vw0WR4rt', '6Zwi24yp', 'G8pKiV5q', '4b5HGKSs', 'dFgVx91b', '5Wdw19KR', 'LTpPwF82', 'vAkyg17f', 'QfxUi78N', 'Io3rU5Gj', 'YG6kUpH9', '48EZ6hoH', '8zheJ5vL', '7PVuS4c3', 'ek2v17VF', 'pr12tHoL', 'vxH5tn1i', 'j3Cfv4wq', 'MZGk4Tx5', 'cygP1CT2', '6Sv01F4z', 'Z9DX1Vr4', '5IRuFdg7', 'SA9y7qu6', 'c6Y7pDSg', '1PHLaV7x', 'uU0B82dP', 'ds9ku86H', 'oytz0pV3', '5YH0Z2vg', 'fnF63wQP', '6vGMbam8', '1qM7vU8G', 'gCXM17Do', 'rvu7si38', 'KT9yF4hW', 'SDYeM57E', 'yDI6H4iP', 'W52ZC4UH', '0X7AZGWY', 'hL86KWoR', 'W37QmhSb', 'GJc6VM4k', '82sgSkVw', 'Yg4n5c7G', '9SHj5sZ6', 'I5jMpA62', 'n0DUZr86', 'WIf3Ag8C', 'FQe7WJ3N', 'P2q3wIXz', '6CpMF8kb', 'tqA2Yj4k', 't4cxTG8A', 'Nt8xg5eG', 'zLo93XBY', 'AMU5du76', 'gU7Fe3pa', 'FA69am2p', 'LG9A2zrV', 'J78zLqGW', 'tLaGZ8h3', 'i9LwmI78', 'Z0wSMY9p', 'NrgSKj90', 'Mjvnb1m6', 'B9QqhU04', '1kIne6HZ', 'DkW45yc7', '4ecN8PfH', '9s63tcDS', 'Da8eP0LE', '4dE8UKcw', 'drCPNM10', '7Hvw8MjR', 'HGYZ1Ag5', 'DX7KZ0Tf', '7Q0xtYai', 'Fz0wQE7k', 'UH1ruJ36', '9Du1jefh', 'Ap3m7Z8z', 'JQfDKp12', 'f2CGjz3B', '83JWTCGy', 'BAu8d7F3', '1M65tIPz', 'houmK14R', 'r6dVAv7g', '1fPrRAs3', 'gy91IuGm', 'q45JQWax', 'EwQ0S5cX', 'wBumj9e7', '2GXuZeC4', '8HG9C1nw', 'YdE56NQq', 'VAti08bF', 'fSsA7Rg5', 'L60J1vWU', '78ganRXv', 'tdk6VX4P', 'v4rwhV5p', 'rLk8V3sj', 'SMPHEx74', 'G8hbp4sT', 'W3sQD9Z5', 'Qqp3bo6v', '1eJFgSw7', 'L5DNP2H9', '4gA3WCQX', 'E0Cvyn7s', 'fnBdH1U4', '30gISzhf', 'Pe43fToq', 'Lj3RUx1n', 'c6o5axqu', 'V7w2fFys', 'Gie01w2u', 'Dg8Fbh2q', 'b7PN0hsK', 'nm1SBZ9g', 'v9W2qg7T', 'M7emSXn1', 'XtSrv61M', '6i4Av1tW', 'Ygh8Id2X', 'uHsAU32G', 'oQ46p2nF', '9sNASF7L', '4JE67mXt', 'BZhUb52W', '5aueM1ix', 'qjsI9d0x', 'SBcq4h6J', 'HF7B1hat', 'iDZs3U0L', 'TS7kxf8V', 'Td0YwbL8', 'zC72U9MZ', 'Jwm2rG7z', '7u56cXTC', 'WY35sbVL', 'z60fkyIR', 'K7whs0vk', 'r3Az5CEn', 'WDuRFG12', '0MrW7RQF', 'oz8eEY3W', 'Hd0o42FW', 'sR2A38UZ', '8AeT7pVj', '8G2oi6Q9', '4qzZk5yo', 'w01Rv8oC', '07C3NBe8', 'j8ahk0XI', 'L2ImUj6y', 'oZv16I5C', '2UigwF0A', 'zVo1bRp9', 'y1hZzE74', 'F2Dz3QHU', 's7iC3PT0', '6hrbyGk1', 'U91CxXGi', 'b1eBIjZ0', '4toup8DY', 'z7Ywj9rx', 'Ivy49YHq', 'Kx8z9RyS', 'nmA2D6Ey', 'ZzP7MS4g', 'G8fF1UNE', 'q25fApus', 'PoGc18Mk', 'we5dRx18', 'isX0tI2D', 'rmINZ0V2', 'j9Cb3mQP', 'f2zR6vU8', '9BWHPDj6', 'wS3u0ryP', 'N40Qek5z', 'Zxb8TPG7', 'E8d3RtMY', 'o67FTH9L', 'YUG3V8vD', '2bNh4JTB', '52o9IuwY', 'Q38dBveW', 'CmZ98McF', '8Nn0mde6', 'FUI6rv7h', 'Y70NXZUz', 'm9wv4dsi', '1uSXYt5o', 'zafH9rL1', '7vAb3nIo', '3A2d9nBL', '79MTkNus', '7z5RKwhU', 'i7xd5oMb', '76rVpcGL', 'B30v8k1P', 'gui7x0cr', '2sjB0RvV', 'x48SzgpH', 'Pgnu7d8k', 'yu28TMIo', 'f9eHCSc8', 'E81Hkv3g', 'gVmh3Lw2', '4WbIjfB3', 'xMFHp36r', 'qga56iME', 'z7UiGPQ1', '6de7rGsP', 'I9TkKu6N', 'L4pBaT0q', '39mGIANe', '1PzmrHL9', 'W3Q62S1F', 'HMib7V50', 'D7hadU1p', 'gN1u7ZeG', 'fYJjG4B6', 'L6gfBpn3', '4KAXRjg0', 'c0Ejwh7S', 'w8Phatd4', 'a4jIgR2T', 'Mkum4tB6', 'em68GxrB', 'W3NMn25Z', 'He71kZYp', 'Xep8qk4D', '7vtcn58P', 'VbFp8XZ6', '9p3b8NCg', 'zLIvD5o2', 'JA03wvHG', '59CzkeG2', 'rF97pVdT', 'W2j4E3te', 'UF51Te63', 'KuCe7t3p', 'NFJ74Wmg', '8Uk4nHfC', 'z5dp9GX8', 'V5N34aUf', 'V6Yf4g1X', 'Sb3MW61V', 'm2iqC6Ka', 'wkCyV73D', 'M4eAVZs1', '35fQnyPs', 'Ny6rB7HV', '3TM68IaF', '8ozA4wZv', 'kpN3M6tK', 'na7Wb8u1', 'hdt2N6mr', '1U9ouXzP', '72jYgkoa', 'Hxidv1y0', '7Q2iopWx', '7f4JNbwr', 'oeUQ8q7D', 'X74u8mIS', '6rjmY7tV', 'fRFY13ie', '0bxTF82d', 'Np2gx5qI', '18CDzh7v', 'y7Qvrd3J', 'n5cWAf7H', 'e5SEqU4m', 'F9fGSe42', 'v8Ln7NBE', 'kT3vA9j2', 'WqvJ64XG', 'Ydra41vX', 'LaM0o9P7', 'fNVP2i89', '7h5fuTma', 'b7fn2L05', 'aZ97rNyw', 'iTMk51hB', '2TuAmfX4', 'qP6nD0IL', 'e5t01snA', 'XjL3fKG0', 'T8wGcKd1', 'k6H83Uix', '89CxLmhs', '2r9cNSdt', 'dc0jxn8u', 'J4heGZ2U', '7nL1WTUb', '4a6GF3Pt', 'Wwn4Epj6', 'R9IryC5v', 'kI94EypD', 'Iz7wM0j9', 'nd18wpsy', '2yCoEm0q', '8gu2U4Mh', 'XZvyRf62', '2npmC9Nw', 'Y7ezNyn2', '9ie4KnDt', 'Apc5eIw6', 'C0pU8ev4', 'GIo0uK8b', 'Ef6oG0mz', 'Eqx4BrW2']
options2=['kIj2n6s5', 'Jki71Bm9', 'K3b981cX', '1nte4gCY', 'zBxwtg89', 'w3Yv7uSF', 'rvIa85RA', '13s7RxgT', '73bUW8wn', '7DAkY1rQ', 'mbK4Qg5w', 'pS2HMv8e', 'a9B3nDuA', '2W4Ja7KU', '5T6cZ7LD', 'XkBhe70R', 'zGcIk58e', 'KY59Mwhq', 'O3nEmUs2', 'D3Bda18b', '.dat', '9ojr0tPC', 'PDGK5sk3', 'U1XChi09', 'w3Z9EeUR', 'V9zLvR7n', '9zJFtHr3', 'HNdG95VT', 'D2FdZK5v', 'w5W8RPSG', '4keDxjn7', '3FWEGtX9', '93xUK0iZ', 'J3TBnt9Z', '4FEhdoA8', '2Im7tLhs', '6Zwi24yp', '4b5HGKSs', '5Wdw19KR', 'vAkyg17f', 'Io3rU5Gj', 'YG6kUpH9', '48EZ6hoH', '8zheJ5vL', '7PVuS4c3', 'ek2v17VF', 'pr12tHoL', 'vxH5tn1i', 'j3Cfv4wq', 'MZGk4Tx5', 'cygP1CT2', 'Z9DX1Vr4', 'SA9y7qu6', 'c6Y7pDSg', '1PHLaV7x', 'uU0B82dP', 'ds9ku86H', 'oytz0pV3', '5YH0Z2vg', 'fnF63wQP', '6vGMbam8', '1qM7vU8G', 'gCXM17Do', 'rvu7si38', 'KT9yF4hW', 'SDYeM57E', 'yDI6H4iP', 'W52ZC4UH', '0X7AZGWY', 'W37QmhSb', '82sgSkVw', '9SHj5sZ6', 'I5jMpA62', 'WIf3Ag8C', 'FQe7WJ3N', 'P2q3wIXz', '6CpMF8kb', 'tqA2Yj4k', 't4cxTG8A', 'zLo93XBY', 'AMU5du76', 'gU7Fe3pa', 'LG9A2zrV', 'J78zLqGW', 'tLaGZ8h3', 'i9LwmI78', 'Z0wSMY9p', 'NrgSKj90', 'Mjvnb1m6', 'B9QqhU04', '1kIne6HZ', 'DkW45yc7', '4ecN8PfH', '9s63tcDS', 'Da8eP0LE', 'drCPNM10', '7Hvw8MjR', 'HGYZ1Ag5', '7Q0xtYai', 'Fz0wQE7k', 'UH1ruJ36', '9Du1jefh', 'Ap3m7Z8z', 'JQfDKp12', 'f2CGjz3B', 'BAu8d7F3', 'houmK14R', '1fPrRAs3', 'q45JQWax', 'wBumj9e7', '2GXuZeC4', '8HG9C1nw', 'YdE56NQq', 'L60J1vWU', 'tdk6VX4P', 'rLk8V3sj', 'SMPHEx74', 'G8hbp4sT', 'Qqp3bo6v', '1eJFgSw7', 'L5DNP2H9', 'E0Cvyn7s', 'fnBdH1U4', '30gISzhf', 'Pe43fToq', 'Lj3RUx1n', 'c6o5axqu', 'V7w2fFys', 'Gie01w2u', 'Dg8Fbh2q', 'b7PN0hsK', 'nm1SBZ9g', 'v9W2qg7T', 'M7emSXn1', '6i4Av1tW', 'Ygh8Id2X', 'uHsAU32G', 'oQ46p2nF', '9sNASF7L', '4JE67mXt', 'BZhUb52W', '5aueM1ix', 'qjsI9d0x', 'SBcq4h6J', 'HF7B1hat', 'iDZs3U0L', 'TS7kxf8V', 'Td0YwbL8', 'zC72U9MZ', 'Jwm2rG7z', '7u56cXTC', 'WY35sbVL', 'z60fkyIR', 'K7whs0vk', 'r3Az5CEn', 'WDuRFG12', '0MrW7RQF', 'oz8eEY3W', 'Hd0o42FW', 'sR2A38UZ', '8AeT7pVj', '8G2oi6Q9', '4qzZk5yo', 'w01Rv8oC', '07C3NBe8', 'j8ahk0XI', 'L2ImUj6y', 'oZv16I5C', '2UigwF0A', 'y1hZzE74', 's7iC3PT0', '6hrbyGk1', 'U91CxXGi', 'b1eBIjZ0', '4toup8DY', 'z7Ywj9rx', 'Ivy49YHq', 'Kx8z9RyS', 'nmA2D6Ey', 'ZzP7MS4g', 'G8fF1UNE', 'q25fApus', 'PoGc18Mk', 'we5dRx18', 'isX0tI2D', 'rmINZ0V2', 'j9Cb3mQP', 'f2zR6vU8', '9BWHPDj6', 'wS3u0ryP', 'N40Qek5z', 'Zxb8TPG7', 'E8d3RtMY', 'o67FTH9L', 'YUG3V8vD', '2bNh4JTB', '52o9IuwY', 'Q38dBveW', 'CmZ98McF', '8Nn0mde6', 'FUI6rv7h', 'Y70NXZUz', 'm9wv4dsi', '1uSXYt5o', 'zafH9rL1', '7vAb3nIo', '3A2d9nBL', '7z5RKwhU', '76rVpcGL', 'B30v8k1P', 'gui7x0cr', 'x48SzgpH', 'yu28TMIo', 'E81Hkv3g', '4WbIjfB3', 'qga56iME', '6de7rGsP', 'I9TkKu6N', 'L4pBaT0q', '1PzmrHL9', 'HMib7V50', 'gN1u7ZeG', 'L6gfBpn3', 'c0Ejwh7S', 'a4jIgR2T', 'em68GxrB', 'He71kZYp', '7vtcn58P', '9p3b8NCg', 'JA03wvHG', '59CzkeG2', 'rF97pVdT', 'UF51Te63', 'NFJ74Wmg', 'z5dp9GX8', 'V6Yf4g1X', 'm2iqC6Ka', 'M4eAVZs1', 'Ny6rB7HV', '8ozA4wZv', 'na7Wb8u1', '1U9ouXzP', '72jYgkoa', 'Hxidv1y0', '7Q2iopWx', '7f4JNbwr', 'oeUQ8q7D', 'X74u8mIS', 'fRFY13ie', '0bxTF82d', 'Np2gx5qI', '18CDzh7v', 'y7Qvrd3J', 'n5cWAf7H', 'e5SEqU4m', 'v8Ln7NBE', 'WqvJ64XG', 'LaM0o9P7', 'fNVP2i89', '7h5fuTma', 'b7fn2L05', 'aZ97rNyw', '2TuAmfX4', 'e5t01snA', 'T8wGcKd1', '89CxLmhs', 'dc0jxn8u', '7nL1WTUb', '4a6GF3Pt', 'Wwn4Epj6', 'R9IryC5v', 'Iz7wM0j9', '2yCoEm0q', 'XZvyRf62', 'Y7ezNyn2', 'Apc5eIw6', 'GIo0uK8b', 'Eqx4BrW2']

def update():
    global filenames,filenames2,client
    dictionary_full={}
    print("Updating...")
    versions=loadInfo("versions.txt")
    print("versions.txt loaded!")
    tempVersions=versions
    versions=[(x if x['moWQ30GH']+".json" in os.listdir("data_files") else {'d2RFtP8T': '0', 'moWQ30GH': x['moWQ30GH']}) for x in versions]
    ## HANGING SCRIPT
    #[m_files,newVersions]=getVersions2([x for x in versions if x['moWQ30GH'] in filenames or x['moWQ30GH'] in list(filenames2.keys())])
    [m_files,newVersions]=getVersions2([x for x in versions if x['moWQ30GH'] in filenames or x['moWQ30GH'] in list(filenames2.keys())])
    ##
    versions=[(y if y['moWQ30GH'] not in [z['FILE_NAME'] for z in newVersions] else {'d2RFtP8T': [a for a in newVersions if a['FILE_NAME']==y['moWQ30GH']][0]['FILE_VERSION'], 'moWQ30GH': y['moWQ30GH']}) for y in versions]
    client='2900' #CHANGE_CLIENT_NUM
    print("Importing packages...")
    import zipfile, io
    print("Import successful!")
    for x in newVersions:
        if (x['FILE_NAME'] in filenames):
            print(x['FILE_NAME'])
            file=getFile(filenames[x['FILE_NAME']][0],filenames[x['FILE_NAME']][1],x['FILE_VERSION'])
            if (x['FILE_NAME']=="F_RESOURCE_MST"):
                fnames=[q['ZwstRU92'].replace("\\","") for q in file if 'sgtext' in q['ZwstRU92']]
                for fname in fnames:
                    link="http://2.cdn.bravefrontier.gumi.sg/content"+fname
                    name=fname.split('/')[-1]
                    try:
                        if (fname[-4:] == ".csv"):
                            csv_content=requests.get("http://2.cdn.bravefrontier.gumi.sg/content"+fname).content
                        else:
                            input_zip = requests.get("http://2.cdn.bravefrontier.gumi.sg/content"+fname, stream=True).content
                            input_zip=zipfile.ZipFile(io.BytesIO(input_zip))
                            extracted_zip={name: input_zip.read(name) for name in input_zip.namelist()}
                            name=name[0:-4]+".csv"
                            csv_content=extracted_zip[name]
                        #print(bytes_to_str(base64.b64decode(csv_content)))
                        current={x.split('^')[0]:x.split('^')[1] for x in bytes_to_str(base64.b64decode(csv_content)).split("\r\n") if len(x.split('^'))>2}
                        saveInfo2(current,'resources/'+name)
                        for q in current:
                            dictionary_full[q]=current[q]
                    except Exception as exc:
                        print("ERROR on "+str(name)+": "+str(exc))
                saveInfo2(dictionary_full,"datamines/dictionary.json")
            saveInfo2(file,"data_files/"+x['FILE_NAME']+".json")
    for x in filenames2.keys():
        if (filenames2[x] in m_files.keys()):
            if (x=='M_DEFINE_MST' and [y for y in versions if y['moWQ30GH']=='M_DEFINE_MST'][0]==[y for y in tempVersions if y['moWQ30GH']=='M_DEFINE_MST'][0]):
                continue
            saveInfo2(m_files[filenames2[x]],"data_files/"+x+".json")
    if (versions != tempVersions):
        saveInfo2(versions,"versions.txt")
        return ([x['moWQ30GH'] for x in versions if x not in tempVersions])
    else:
        return []

def update2(): #interpreted
    global filenames,filenames2,client
    versions=loadInfo("versions.txt")
    tempVersions=versions
    versions=[(x if x['moWQ30GH']+".json" in os.listdir("data_files_decrypted") else {'d2RFtP8T': '0', 'moWQ30GH': x['moWQ30GH']}) for x in versions]
    [m_files,newVersions]=getVersions2([x for x in versions if x['moWQ30GH'] in filenames or x['moWQ30GH'] in list(filenames2.keys())])
    versions=[(y if y['moWQ30GH'] not in [z['FILE_NAME'] for z in newVersions] else {'d2RFtP8T': [a for a in newVersions if a['FILE_NAME']==y['moWQ30GH']][0]['FILE_VERSION'], 'moWQ30GH': y['moWQ30GH']}) for y in versions]
    client='2900' #CHANGE_CLIENT_NUM
    for x in newVersions:
        if (x['FILE_NAME'] in filenames):
            print(x['FILE_NAME'])
            file=getFile(filenames[x['FILE_NAME']][0],filenames[x['FILE_NAME']][1],x['FILE_VERSION'],True)
            saveInfo2(file,"data_files_decrypted/"+x['FILE_NAME']+".json")
    for x in filenames2.keys():
        if (filenames2[x] in m_files.keys()):
            if (x=='M_DEFINE_MST' and [y for y in versions if y['moWQ30GH']=='M_DEFINE_MST'][0]==[y for y in tempVersions if y['moWQ30GH']=='M_DEFINE_MST'][0]):
                continue
            saveInfo2(eval(replaceKeys(str(m_files[filenames2[x]]))),"data_files_decrypted/"+x+".json")
    if (versions != tempVersions):
        saveInfo2(versions,"versions.txt")
        return ([x['moWQ30GH'] for x in versions if x not in tempVersions])
    else:
        return []


def decrypt_files():
    for x in os.listdir('data_files'):
        saveInfo2(eval(replaceKeys(str(loadInfo('data_files/'+x)))),'data_files_decrypted/'+x)
