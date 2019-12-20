import json
import requests
import base64
from Crypto.Cipher import AES
import warnings
from multiprocessing.dummy import Pool as ThreadPool

warnings.simplefilter("ignore")

with open('bf_binary.txt',encoding='ISO-8859-1') as d:
    bf=d.read()

#---------------------------------------------------------------

def getKey(requestId):
    if (requestId in bf):
        i=bf.index(requestId)
        s=bf[i-50:i+50].split('\n')
        return s[s.index(requestId)+1]
    else:
        return -1
#def pad(s):             return Crypto.Util.Padding.pad(s,AES.block_size) if (type(s)==type(b'100')) else bytes_to_str(pad(str_to_bytes(s)))
#def unpad(y):           return Crypto.Util.Padding.unpad(y,AES.block_size) if (type(y)==type(b'100')) else bytes_to_str(unpad(str_to_bytes(y)))
def str_to_bytes(s):    return bytes(s,encoding="utf-8")
#def bytes_to_str(b):    return "".join(map(chr,b))
def bytes_to_str(b): return str(b,'utf-8');

BS=16

def pad(s):
	return (s + (BS - len(s) % BS) * chr(BS - len(s) % BS)) if type(s)!=type(b'100') else str_to_bytes(pad(bytes_to_str(s)))

def unpad(s):
	return s[0:-ord(s[-1])] if type(s)!=type(b'100') else str_to_bytes(unpad(bytes_to_str(s)))

def decode(m,key):
    cipher = AES.new(bytes(key,encoding="utf-8").ljust(16,b'\0'),AES.MODE_ECB)
    try:
        return bytes_to_str(unpad(cipher.decrypt(base64.b64decode(str_to_bytes(m)))))
    except ValueError:
        try:                return bytes_to_str((cipher.decrypt(base64.b64decode(str_to_bytes(m)))))
        except ValueError:  return bytes_to_str((cipher.decrypt(pad(base64.b64decode(str_to_bytes(m))))))

def encode(m,key):
	cipher = AES.new(bytes(key,encoding="utf-8").ljust(16,b'\0'),AES.MODE_ECB)
	return bytes_to_str(base64.b64encode(cipher.encrypt(pad(str_to_bytes(m)))))

def decryptfile(filename,key=-1,replace=True,json=True):
    f=open(pathname+filename,'r')
    filedata=f.read()
    f.close()
    filedata=filedata[filedata.index('"Kn51uR4Y":"')+12:]
    filedata=filedata[:filedata.index('"')]
    return decrypt(filedata,key=key,replace=replace,json=json)

def decrypt(filedata,key=-1,replace=True,json=True,printout=False):
    if (key!=-1):
        output=decode(filedata,key)
        if (replace):
            try:    output=replaceKeys(output)
            except Exception as e: print("Unable to replace keys: "+str(e))
        if (json):
            try:
                try:                return eval(output)
                except NameError:   return eval(output.replace('null','-1').replace('false','False').replace('true','True'))
            except:
                print("Unable to convert to JSON")
        return output
    data=filedata
    options=[x for x in bf.split('\n') if len(x)==8 and len([q for q in x if q.lower() in "abcdefghijklmnopqrstuvwxyz1234567890"])==8]
    r=[]
    for x in options:
        try:                    r=r+[x] if decode(data[:64],x)[0] in ['[','{'] else r
        except Exception as e:  print("beginning of filedata is: "+str(filedata[:100])+"\nend of filedata is: "+str(filedata[-100:])+"\nError at "+x+": "+str(e))
    for charType in ['":"','":','","','{"',']','"]','}]']:
        if len(r)>1:
            temp=[x for x in r if charType in decode(data,x)]
            r=temp if len(temp)>0 else r
    if len(r)==0:
        print("Error: no keys found")
        return "Error: no keys found"
    if len(r)==1:
        if (printout):
            print(r[0])
        output=decode(filedata,r[0])
        if (replace):
            try:                    output=replaceKeys(output)
            except Exception as e:  print("Unable to replace keys: "+str(e))
        if (json):
            try:
                try:                return eval(output)
                except NameError:   return eval(output.replace('null','-1').replace('false','False').replace('true','True'))
            except:
                print("Unable to convert to JSON")
        return output
    print("Error: multiple keys found ("+str(r)+")")
    return "Error: multiple keys found ("+str(r)+")"

def replaceKeys(r):
    for dec in decoded:
        r=r.replace(dec,decoded[dec]) if (dec in r) else r
#    for loc in locations_info:
#        r=r.replace(loc,locations_info[loc]) if (loc in r) else r
    return r


#---------------------------------------------------------------

appKey="0839899613932562"

GUEST_DEVICE_ID="38a5dbfc7d8f73c3b3ff7bbc022e79d174c7001386b335acf58520e31bba00da92100fa0"
GUEST_ALT_DEVICE_ID="47a814218a6b6998e3c00a3305fb1fcd5f01ae9482e2"
GUEST_DEVICE_NAME="2DFDDBBADBB1"
GUEST_DEVICE_PLATFORM="Windows"

def getTokenAndId():
    val=requests.get("https://api-sl.gl.gumi.sg/accounts/guest/login/?ak=" + appKey + "&dp=" + GUEST_DEVICE_PLATFORM + "&dn=" + GUEST_DEVICE_NAME + "&vid=" + GUEST_DEVICE_ID + "&altvid=" + GUEST_ALT_DEVICE_ID,verify=False).json()
    print(val)
    return [val['token'],val['game_user_id']]

signalKey=-1
playerIdentifier=-1
thing=-1
token=-1
userId=-1

def forceLogin(files=[]):
    global token, userId,signalKey,playerIdentifier,thing
    [token,userId]=getTokenAndId()
    action_id="MfZyu1q9"
    key="EmcshnQoDr20TZz1"
    q=action(action_id,("""{"KeC10fuL":"""+str(files)+""","IKqx1Cn9":[{'iN7buP2h': '"""+str(userId)+"""', 'iN7buP1i': '"""+str(token)+"""'}]}""").replace("'",'"'),key)
    # print(q)
    try:
        signalKey=q['SIGNAL_KEY'][0]['PROCESS_ID']
    except:
        print("Error setting signalKey")
    try:
        playerIdentifier=q['AUTHENTICATION_INFO'][0]['PLAYER_IDENTIFIER']
    except:
        print("Error setting player identifier")
    try:
        thing=q['AUTHENTICATION_INFO'][0]['90LWtVUN']
    except:
        print("Error intializing 90LWtVUN")
    return q


REQ_HEADER_TAG = 'F4q6i9xe'
REQ_ID = 'Hhgi79M1'
REQ_BODY = 'Kn51uR4Y'
REQ_BODY_TAG = 'a3vSYuq2'


def action(action_id,body,key,replace=True):
    data=json.dumps({REQ_HEADER_TAG: {REQ_ID: action_id},
        REQ_BODY_TAG: {REQ_BODY: encode(str(body).replace("'",'"'),key)}},separators=(',',':'))
    r=requests.post('https://api.bfww.gumi.sg/bf/gme/action.php',data=data,verify=False).json()
    if len(str(r))<300:
        print("ERROR")
        return r
    else:
        try:
            d=decrypt(r['a3vSYuq2']['Kn51uR4Y'],key,replace=replace)
            return d
        except:
            print(str(r)[:500])
            return r

def fullresponse(action_id,key,parameters,tkn,uID,sKey,pId,tng,print_bool=False,replace=True):
    body={'IKqx1Cn9':[{"h7eY3sAK":pId,"90LWtVUN":tng,"iN7buP2h":uID,"iN7buP1i":tkn,"K29dp2Q":"110110009343520","nrg19RGe":"0","iN7buP0j":"0665","DFY3k6qp":"7","j2lk52Be":"8"}],"6FrKacq7":[{"Kn51uR4Y":sKey}]}
    for x in parameters:
        body[x]=parameters[x]
    if (print_bool):
        print(body)
    return action(action_id,body,key,replace)

def response(action_id,key=-1,parameters={},printIt=False,replace=True):
    global token,userId,signalKey,playerIdentifier,thing
    return fullresponse(action_id,(key if key!=-1 else getKey(action_id)),parameters,token,userId,signalKey,playerIdentifier,thing,printIt,replace)


#--------------------------------------------------------------- BASE REQUESTS

season=10

def getGuildInfo(guildNo,seasonNo=season):      return response("7ekSBz2y","tWF58aK0",{"R6YwbeCB":[{"dk39bDa1":str(seasonNo),"sD73jd20":str(guildNo)}]})
def editGuildBase(guildID,insignia,desc):       return response("92bDoqBi","w3Bne038",{"IkdSufj5":[{"sD73jd20":str(guildID),"dDKCN293":str(insignia),"ad8bdAj1":"0","qp37xTDh":str(desc)}]})
def getPlayerInfoBase(playerIdentifier):            return response("38bSeq81","h8TmR1bi",{"csIuech30":[{"h7eY3sAK":str(playerIdentifier)}]})
def getPlayerInfo(playerIdentifier,count=0):
    try:
        return response("38bSeq81","h8TmR1bi",{"csIuech30":[{"h7eY3sAK":str(playerIdentifier)}]})
    except Exception as e:
        if (count<20):
            return getPlayerInfo(playerIdentifier,count+1)
        else:
            raise ValueError
def searchByIdBase(playerId):                       return response("umNt8M7i","qa3sHuDgKxV5nI1F",{"BPz1e5tU":[{"98WfKiyA":str(playerId)}]})
def searchById(playerId,count=0):
    try:
        return searchByIdBase(playerId)
    except Exception as e:
        if (count<20):
            return searchById(playerId,count+1)
        else:
            raise ValueError
        return searchByIdBase(playerId)
    except Exception as e:
        if (count<20):
            return searchById(playerId,count+1)
        else:
            raise ValueError
def searchPlayerIdBase(playerId):                   return response("umNt8M7i","qa3sHuDgKxV5nI1F",{"BPz1e5tU":[{"98WfKiyA":str(playerId)}]})
def searchPlayerId(playerId,count=0):
    try:
        return searchPlayerIdBase(playerId)
    except Exception as e:
        if (count<20):
            return searchPlayerId(playerId,count+1)
        else:
            raise ValueError
def myGuildInfo():                              return response("138ba8d4","23gD81ia")
def searchGuild(guildName):                     return response("R38ba9M3","0D18dQn4",{"kj1d80ai":[{"bj729kiq":guildName}]})
#def roomInfo(roomNo):                           return response("83kBdiqD","93Di3Ge8",{"":["8VYd6xSX":str(roomNo)]})
def login():                                    return response("MfZyu1q9")
def searchRoom(guildId,roomId,seasonNo=season): return response("aXPZmq9h","J90g7sZK",{"b56mrqM9":[{"dk39bDa1":str(seasonNo),"sD73jd20":str(guildId),"8VYd6xSX":str(roomId)}]})
def myRooms():                                  return response("Q8Eib8Xv","UI3Da1B7")
def searchRoom2(roomNo):                        return response("83kBdiqD","93Di3Ge8",{"b9Dq1xzi":[{"8VYd6xSX":str(roomNo)}]})
def getRankings(count=0):
    try:
        return getRankingsBase()
    except Exception as e:
        if (count<20):
            return getRankings(count+1)
        else:
            raise ValueError
def getRankingsBase():                              return response("2b9D01b4","23Djab0e",{"g7hx43Pq":[{"C6W4Vpow":"2"}]}) #can be used with any pID
def getRankings2(pId):
    global playerIdentifier
    try:
        temp=playerIdentifier
        playerIdentifier=pId
        output=getRankings()
        playerIdentifier=temp
        return output
    except Exception as e:
        print(e)
        playerIdentifier=temp
        raise ValueError
def getAllGuildRaid():                          return response("7di8aie9","yh8ak18b")
def playerGuildRaid():                          return response("7di8aie9","yh8ak18b") #equivalent to above
def getBattleScore():                           return response("W1Dgsfnz","eMfdsGVJ")
def getJournalInfo():
    m=response("MTzXyuFL","MkV5xHDL",{"M9ctnu4Q":[{"78Zema70":"2823263"}]},replace=False)
    for x in m['M9ctnu4Q']:
        x['78Zema70']=str(x['78Zema70'])
    for x in m['M9ctnu4Q']:
        x['me7eDiXs']=str(x['me7eDiXs'])
    return eval(replaceKeys(str(m)))
def getBoxes():                                 return response("cTZ3W2JG")
def arenaTeam(playerIdentifier):                return response("7f1rg92L",parameters={'60subGk3':[{'EfbZ7mh9': '1'}],'fq2C03jh':[{'Z0Y4RoD7': '0'}],'9NX83YVe':[{'Z7PXoxc2': '1', 'h7eY3sAK':playerIdentifier}],'rj5fgJh0':[{'t5R47iwj': '19'}]})
def checkArenaTeam(playerIdentifier):           return response("7f1rg92L",parameters={'60subGk3':[{'EfbZ7mh9': '1'}],'fq2C03jh':[{'Z0Y4RoD7': '0'}],'9NX83YVe':[{'Z7PXoxc2': '1', 'h7eY3sAK':playerIdentifier}],'rj5fgJh0':[{'t5R47iwj': '77'}]}) #identical to above
def coloTeam():                                 return response("oim9TU1D") #can be used with any pID
def fgScores():                                 return response("M17pPotk") #can be used with any pID
def presentsBox():                              return response("nhjvB52R")
def fgRankings(fgNo):                           return response("26zW90oG",parameters={'96F8HfPv':[{'9w5e3ZJB': '0'}],'Mg8K8Y1a':[{'hBNPQAU0': str(fgNo)}]})
def checkAcct():                                return response("uYF93Mhc","d0k6LGUu") #can be used with any pID
def startLogin():                               return response("RUV94Dqz") #can be used with any pID

#----------FOR_LINUX--------------

def printFG(fgId):
	global playerIdentifier
	q=forceLogin()
	q=fgRankings(fgId)
	top=[x for x in q[('heP5upra' if 'heP5upra' in q else '33W6N124')] if x['TOP_RANKS?']==1 and x['RANKING_NO']<=30]
	output=""
	for x in top:
		stuff=["",""]
		try:
			f=getPlayerInfo(x['PLAYER_IDENTIFIER'])
			stuff=[" - "+str(f['PLAYER_INFO']['PLAYER_ID'])+""," - "+f['GUILD_INFO'][0]['GUILD_NAME']]
		except:
			try:
				temp=playerIdentifier
				playerIdentifier=x['PLAYER_IDENTIFIER']
				stuff=[" - "+str(searchRoom('1568','12','5')['AUTHENTICATION_INFO'][0]['PLAYER_ID'])+"",""]
				playerIdentifier=temp
			except Exception as e:
				print(e)
				try:
					playerIdentifier=temp
				except:
					pass
		output+="**"+str(x['RANKING_NO'])+") "+x['IGN']+"** (Level "+str(x['PLAYER_LEVEL'])+")"+stuff[1]+"\n"+" - __"+str(x['ARENA_BATTLE_POINTS'])+" Points__ (Floor "+str(x['FG_FLOOR'])+")\n"+stuff[0]+"\n"
	return output

def getId3(p):
    return str(searchRoom('1568','12','5')['AUTHENTICATION_INFO'][0]['PLAYER_ID'])

def generateFriends(count):  return response("mE5gUQOp","oK4VaDGF",{'StQIyohe':[{'jkldTrhL': '0'}],'3fTYzqT6':[{'3Ug2QynF': '0', 'lzpDckWv': str(count)}]})
def generateFriends2(count,pId):
    global playerIdentifier
    temp=playerIdentifier
    playerIdentifier=pId
    o=generateFriends(count)
    playerIdentifier=temp
    return o

#--------------------------------------------------------------- LAYERED REQUESTS

def checkAcct(pId):
    global playerIdentifier
    tempPID=playerIdentifier
    playerIdentifier=pId
    output= response("uYF93Mhc","d0k6LGUu")
    playerIdentifier=tempPID
    return output

def contribute(pId,locationType=1,skillType=1):
    global playerIdentifier
    tempPID=playerIdentifier
    playerIdentifier=pId
    output=contributeBase(locationType,skillType)
    playerIdentifier=tempPID
    return output

def playerGuildRaid(pId):
    global playerIdentifier
    tempPID=playerIdentifier
    playerIdentifier=pId
    output= response("7di8aie9","yh8ak18b")
    playerIdentifier=tempPID
    return output

def checkColoTeam(pId): #variant of ColoTeam with pid
    global playerIdentifier
    tempPID=playerIdentifier
    playerIdentifier=pId
    output= response("oim9TU1D")
    playerIdentifier=tempPID
    return output

def checkFgScores(pId):
    global playerIdentifier
    tempPID=playerIdentifier
    playerIdentifier=pId
    output= response("M17pPotk")
    playerIdentifier=tempPID
    return output

def editGuild(guildName,insignia,desc):
    global playerIdentifier
    tempPID=playerIdentifier
    [playerIdentifier,guildId,x,y]=findGM(guildName)
    temp=editGuildBase(guildId,insignia,desc)
    playerIdentifier=tempPID
    return temp

def allGuildMembers(guildName):
    global playerIdentifier
    tempPID=playerIdentifier
    [playerIdentifier,guildId,desc,insignia]=findGM(guildName)
    temp=editGuildBase(guildId,insignia,desc.replace("\\",""))
    playerIdentifier=tempPID
    return temp

def findGM(guildName):
    g=searchGuild(guildName)['GUILD_SEARCH_RESULTS'][0]
    gid=g['GUILD_ID']
    for season in range(11): # hardcoded season
        try:
            return [[x for x in getGuildInfo(gid,season)['GUILD_MEMBER_SCORES'] if x['IGN']==g['GUILD_MASTER']][0]['PLAYER_IDENTIFIER'],gid,g['DESCRIPTION'],g['GUILD_INSIGNIA_NUMBER']]
        except:
            pass
    return [-1,-1,-1,-1]

def getId(playerIdentifier):
    return checkArenaTeam(playerIdentifier)['ARENA_ENEMY_TEAM'][0]['PLAYER_ID']

def getId2(playerIdentifier):
    try:
        q=getPlayerInfo(playerIdentifier)['PLAYER_INFO']
        return [q['PLAYER_ID'],q['GUILD_ID']]
    except:
        try:
            return [checkArenaTeam(playerIdentifier)['ARENA_ENEMY_TEAM'][0]['PLAYER_ID'],-1]
        except:
            return [-1,-1]

def getGuildId(name,manual_auth=-1):
    return searchGuild(name,manual_auth=manual_auth)['GUILD_SEARCH_RESULTS'][0]['GUILD_ID']

def getScores(name=-1,guildId=-1,seasonNo=season):
    if (name!=-1):
        guildId=searchGuild(name)['GUILD_SEARCH_RESULTS']
        options=[x for x in guildId if x['GUILD_NAME'].lower()==name.lower()]
        guildId=options[0]['GUILD_ID'] if len(options)>0 else guildId[0]['GUILD_ID']
    g=getGuildInfo(guildId,seasonNo=seasonNo)
    return [[x['IGN'],x['POINTS'],x['PLAYER_LEVEL'],x['PLAYER_IDENTIFIER'],x['P_RANK']] for x in g['GUILD_MEMBER_SCORES']]


def findOpponent(pid):
    global playerIdentifier
    temp=playerIdentifier
    playerIdentifier=pid
    d=getJournalInfo()
    m=myRooms()
    my_guild=m['ROOMS_INFO'][0]['GUILD_ID']
    enemyId=list(set([str(x['GUILD_ID']) for x in d['M9ctnu4Q'] if str(x['GUILD_ID'])!=my_guild]))[0]
    playerIdentifier=temp
    q=forceLogin()
    g=getGuildInfo(enemyId,6)
    stuff=0
    ignsList=list(set([x['IGN'] for x in d['M9ctnu4Q'] if str(x['GUILD_ID'])==enemyId]))
    result=-1
    while (stuff!=-1 and stuff<len(ignsList)):
        matches=[x for x in g['GUILD_MEMBER_SCORES'] if x['IGN']==ignsList[stuff]]
        if (len(matches)==1): #unique IGN
            result=matches[0]['PLAYER_IDENTIFIER']
            stuff=-1
        else:
            stuff+=1
    r=playerGuildRaid(result)
    print("Result: "+str(r))
    enemyRoom=[x for x in r['ROOMS_INFO'] if x['PLAYER_IDENTIFIER'] in [y['PLAYER_IDENTIFIER'] for y in r['ROOM_MEMBER_INFO']]][0]
    count=0
    for y in range(20):
        o=getPlayerInfo(g['GUILD_MEMBER_SCORES'][y]['PLAYER_IDENTIFIER'])['GUILD_INFO'][0]
        if (int(o['GUILD_ID'])==int(enemyId)):
            break
    return [o['GUILD_NAME']+" (Level "+str(o['GUILD_LEVEL'])+")\n - Guild Master: "+o['GUILD_MASTER']+"\n - Members: "+str(o['GUILD_MEMBERS'])+"\n - Guild ID: "+o['GUILD_ID']+"\n - Guild Created: "+o['GUILD_CREATED_DATE'],enemyRoom,[x for x in r['ROOMS_INFO'] if x['PLAYER_IDENTIFIER']!=enemyRoom['PLAYER_IDENTIFIER']]]

#---------------------------------------------------------------

def getBoxes2(pId):
    global playerIdentifier,signalKey
    tempPlayerIdentifier=playerIdentifier
    tempSignalKey=signalKey
    playerIdentifier=pId
    signalKey=login()['SIGNAL_KEY'][0]['PROCESS_ID']
    output=getBoxes()
    playerIdentifier=tempPlayerIdentifier
    signalKey=tempSignalKey
    return output

def presentsBox2(pId):
    global playerIdentifier,signalKey
    tempPlayerIdentifier=playerIdentifier
    tempSignalKey=signalKey
    playerIdentifier=pId
    signalKey=login()['SIGNAL_KEY'][0]['PROCESS_ID']
    output=presentsBox()
    playerIdentifier=tempPlayerIdentifier
    signalKey=tempSignalKey
    return output
    
def startLogin2(pId):
    global playerIdentifier,signalKey
    tempPlayerIdentifier=playerIdentifier
    tempSignalKey=signalKey
    playerIdentifier=pId
    signalKey=login()['SIGNAL_KEY'][0]['PROCESS_ID']
    output=startLogin()
    playerIdentifier=tempPlayerIdentifier
    signalKey=tempSignalKey
    return output


#---------------------------------------------------------------

decoded={'wJsB35iH': 'PRESENT_AMOUNT', 'HeA4I2dN': 'CONTINUES', '30Kw4WBa': 'REWARD_TYPE*', '76IHLVsz': 'UNIT_TYPE_HP', 'NgrYgZht': 'SUMMONER_STATS_BOOST_TYPE', 'AYd82i1B': 'VORTEX_ARENA_OVERALL_REWARDS', 'mXlvqgFU': 'SKILL_ID(2587-9=low,2590-92=med,2592-5=high', 'D9wXQI2V': 'LEVEL', 'nMe3ai17': 'GUILD_EXCHANGE_HALL_INFO?', 'UVN5bGoD': 'NAME', 'UT1SVg59': 'VALID_MISSIONS_LIST', 'jT3oB57e': 'IS_MILESTONE?#2*', '6WKvM4o8': 'PLAYER_LEVEL', 'Hb8yfmv7': 'EVO_MAT_ID_JP (5)', 'KeC10fuL': 'FILES_VERSION_INFO', 'e0XmDu4q': 'SUCCESS_CONDITIONS', 'LjY4DfRg': 'ELGIF_EQUIPPED_ID', 'i9Tn7kYr': 'UNIT_BASE_ATTACK', 'h6UL9A1B': 'CONTRIBUTIONS_TYPE', 'jfN15EdJ': 'QUEST_ZONE_UNLOCK_REQUIREMENT', 'h2L1YI90': 'P_MOVE_TYPE_2', 'GjmR04Vf': 'GUARDIAN_SKILL_BOOST_KARMA_REQUIRED', 'NQR1Vd3t': 'PLAY_STYLE_NUMBER', 'agp4CKEV': 'EVO_MAT_ID_JP (8)', 'CRfnmT13': 'STAMP_COST_BUTNOTGEMS*', 'Jdbj9S28': 'GUARDIAN_ID', 'nGVc2zS1': 'STAMP_IMAGE', '23L78yG5': 'BUNDLE_NAME', 'Xyt6rhx2': 'EVO_MAT_TYPES_JP (1)', 'Qe2iLri2': 'VORTEX_ARENA_RECORDS2', 'YTx3c1jQ': 'GACHA_SCRIPT_B', 'PIa6T3RK': 'RAID_WORLD_SERVER', '7CcgbUt0': 'ATK_ANIMATION_1', 'H2Dnbr39': 'JOURNAL_CHALLENGE_DESCRIPTION', 'fAi8Th5s': 'TIME_OBTAINED', 'JQ23rIvk': 'REWARDS_OBTAINED*', 'N8Yet5kA': 'MAX_AGE', '9PsmH7tz': 'SP_SERIES', '2hcq47Cg': 'QUEST_ALWAYS_1.0', 'aL70hVYQ': 'DEVICES_AVAILABLE?', '9hH0neGa': 'MERIT_PTS_RECEIVED', '8bD18LPe': 'GUILD_INFO', 'IvuccUuD': 'ARENA_EXTRA_RULE_ID', 'dX7S2Lc1': 'SQUADS_INFO', 'yTPw0BD7': 'IMAGE', '32SaXjQx': 'QUEST_ALWAYS_1.0', 'gJdju7aE': 'GENERAL_ROOM_INFO', 'dyFUE5fN': 'ES_CHANCE (1=add,2=remove)*', 'dJPf9a5v': 'LEADER_SKILL_NAME', '6qjD4Jdh': 'RELOAD_FILES', '8DtoZdXE': 'SOME_SORT_OF_FRIEND_TIME', 'j8iZk1wb': 'ROOMS_AVAILABLE', '96Nxs2WQ': 'FRIENDS_LIST_TYPE*', 'ibY38bDn': 'SKILL_TYPE*', 'vV4P53m7': 'RANKING_NO', 'qBAb07rh': 'EXCHANGE_HALL_ITEM*', '6fwL59FT': 'TOTAL_DMG_DISTRIBUTION%', 'diGe6u21': 'MISSION_SCRIPT_PARAMETERS', '9NX83YVe': 'ARENA_ENEMY_TEAM', 'BPz1e5tU': 'PLAYER_INFO', 'CJpkT40r': 'BATTLE_EFFECT_NAME', 'q7Nit8JW': 'REQUIREMENT_PARAMETER', '37uDa81B': 'GUARDIAN_INFO', '22rqpZTo': 'CURRENT_BP', 'QqfI9mM4': 'ANIMATION', 'Z3ocmb5J': 'UNIT_TYPE_NAME', 'S4ezp6uK': 'VALID_ITEM=1,0=IGNORE', '1W9CxaFK': 'P_HOME_IMG_POS', 'GV81ctzR': 'VALID_UNITS_LIST', '32INDST4': 'UNIT_LORD_DEFENSE', 'nm1USVcx': 'SUMMONER_STATS_SP_COST', '5it4IozN': 'EVO_MAT_TYPES (1)', '4wij8ArG': 'MISSION_3RD_ARC_EXP+EXP_RATE', 'VPf7t9rK': 'NAME*', '4HqhTf3a': 'RECIPE_NUMBER', 'f1LKBoM9': 'HELP_ID', 'j3hpz537': 'GUARDIAN_SKILL_STRENGTH', '4ceMWH6k': 'UNIT_BOX', 'yj46Q2xw': 'TOWN_HARVEST_POINTS (MTN/RIVER/FARM/FOREST)', 'h7eY3sAK': 'PLAYER_IDENTIFIER', 'b9Dq1xzi': 'ROOMS_INFO', 'u3bDi9sT': 'BUNDLE_GROUP', 'qS4wLauD': 'TIME:CURRENT_ROUND_MATCHMAKING_START', 'dDKCN293': 'GUILD_INSIGNIA_NUMBER', 'fE2d6ivS': 'TIME_TILL_CONTRIBUTION_RESET', 'XuJL4pc5': 'QUEST_MAP_NUMBER/GUIDE_ID', 'S8rdp9zk': 'EXCHANGE_HALL_LIMIT', '92ij6UGB': 'UNIT_BASE_REC', 'I0ZNnm4b': 'REWARD_CONDITION_DESCRIPTION', 'ug9xV4Fz': 'AI_CHANCE', 'YH1FrDVa': 'NUM_OF_GR_ROOMS?', 'r9SEG7tR': 'EVO_MAT_TYPES (5)', 'by8ad3ga': 'PLAYER_GUILD_SKILLS_CONTRIBUTIONS', 'l234vdKs': 'COLLAB_EVENT?', 'C4Bjk2wp': 'GUARDIAN_NUMBER(1759-1765)', 'AKZ7u5iN': 'ROUTE_END_LOCATION?', 'hd2Jf3nC': 'TASK_NAME', 'tojMy68W': 'FRIENDS_LIST', 'VgU78CYj': 'SP_CAT_ID', 'rGm09bav': 'ARENA_RANK_NAME', 'NgRIeeJc': 'LOWER_ANIMATION', '6PLsn8xo': 'HC_DROPPED', '8f4NYKxb': '??SOME_SORT_OF_MISSION_IDS_LIST??', 'jsRoN50z': 'BANNER_SITE', '67CApcti': 'ATK', 'J2hPXGo5': 'UNIT_MOVE_SPEED', '2ty57Bcv': 'SOUNDTRACK', 'iI7Wj6pM': 'INCREASED_ITEM_CAP*', 'T1IxCpTF': 'SHOP_ITEM_NUMBER', 'T091Rsbe': 'PRESENT_NAME', 'e3QNsuZ8': 'RAID_TARGET', 'trA1wi9x': 'QUEST_ALWAYS_1.0', 'TPR79fyI': 'POINTS_REQUIRED', 'vELiH4Q1': 'NUM_OF_SPARKS_B', 'Siv49s0l': 'CURRENT_GUILD_EXP', 'gb0qGa1W': 'UNIT_FUSION_TEXT', 'm67Di3wq': 'GUARDIAN_INFO2', 'C1HZr3pb': 'TIME_LAST_ONLINE?', 'SzV0Nps7': 'AVAILABILITY_TIME_END', '5JbjC3Pp': 'FAVORITED?', 'yRlCNyvk': 'SP_NAME', 'Rs7bCE3t': 'AMOUNT', 'nBTx56W9': 'UNIT_TYPE_ID', 'N1b6SUW4': 'REWARD_ID', 'Lxr1STbO': 'WEAPON_UBB_LEVEL', 'tj0i9JhC': 'GACHA_SCRIPT_C', '0tna4Idu': 'EVO_MAT_TYPES_JP (2)', '38bSqa9b': 'PLAYER_INFO', 'ScyFz1D8': 'GUARDIAN_SKILL_BOOST_ZEL_REQUIRED', '4BtYr6Eg': 'RANK_MAX', 'FOkXX7Hq': 'CURRENT_LOCATION', 't4m1RH6Y': 'IMP_ATK', '1CxU2MPn': 'TOTAL_ENEMIES', 'YDxl64JI': 'MAX_COST', '71U5wzhI': 'EQUIPPED_ITEMS', 'wh3YRU08': 'EVO_MAT_ID_JP (2)', 'qfg7P2sK': 'SUMMONER_STATS_ID', '20iEWRCV': 'ARENA_REFRESHES', 'VJzlXxyM': 'TEAM', 'H04AphFP': 'GUARDIAN_LEVELING_INFO', 'yT8fs6jL': 'BUNDLES_REWARDS', 'T4bV8aI9': 'BP_REWARD', 'bya9a67k': 'TOTAL_BP', '3InKeya4': 'DATE_ADDED', 'zsiAn9P1': 'SQUAD_NUMBER', 'Ge8Yo32T': 'SPHERE_2_EQUIPPED_ID', 'imQJdg64': 'UNIT_IMP', '29timHEg': 'SCENARIO_SUPERSECTION*', 'n9h7p02P': 'DROP_CHECK_COUNT', 'qp37xTDh': 'DESCRIPTION', 'YnM14RIP': 'MAX_ENERGY', 'yu18xScw': 'AI_PRIORITY', 'fu73ghxq': 'GUARDIAN_SKILL_ID', '69vnphig': 'BATTLE_COUNT', 'v4QT2gbL': 'HELP_TOPIC_NAME', '7w0inC1R': 'LOCATIONS_NUMBER', 'L8PCsu0K': 'AI_NAME', 'IAfv98Wd': 'PLAYER_IGN', '1Dg0vUX3': 'BACKGROUND_IMAGE', 'pn16CNah': 'UNIT_ID', 'zwDqib73': 'GUARDIAN_BB_AND_SKILL_FRAMES', 'u3D9abe1': 'GUILD_LEVEL_MAX_EXP_THRESHOLD', 'nB7pFdR0': 'EVO_MAT_TYPES_JP (5)', 'f3L8HeKn': 'LOCATION_NAME', 'y4k9o7Jt': 'NPC_NAME', '21VKZo0E': 'QUEST_BANNER_IMAGE', 'R6YwbeCB': 'GUILD_MEMBER_SCORES', '3BpHN6VD': 'P_HP_DISP_POS', 'eyUo6a8c': 'BATTLE_EFFECT_GROUP_FRAMES', 'n6E8iMf3': 'ITEM_BOX_ID', '2BFgYLjg': 'EVO_MAT_TYPES_JP (8)', 'b5VveUd8': 'IMAGE', 'h0K7wjeH': 'ITEM_TYPE*', 'hoG2ieT5': 'BC_DROPPED', 'U7LJCqT1': 'SUPPORT_NAME', 'G5wFDad6': 'SP_NEED_BP', 'HFAI8WT4': 'CREATE_GUILD_COST', 'bNRUuatB': 'EVO_MAT_TYPES_JP (7)', 'p5ZhN6Lk': 'EVO_MAT_TYPES (2)', 'df1eUh7E': 'AI_CONDITION_1', 'tz84LhXc': 'WEAPON_SKILL_NAME', 'E0VbaLr7': 'RAID_ROUTE_ID', 'iNy0ZU5M': 'UNIT_ELEMENT', 'Ma5GnU0H': 'VID_=VERSION_ID?', 'Ke14gCAc': 'QUEST_ALWAYS_0', '7eCia0o3': 'VORTEX_ARENA_RECORDS', 'djaB081u': 'PHASE', 'gBLoOL3p': 'COLO_FORMATION_NAME', 'JK38Bq83': 'IMAGE_LOCATION', '3Da8bm3b': 'GUARDIAN_ID', 'Px1X7fcd': 'INCREASED_UNIT_CAP*', '0rAkzg7L': 'ARENA_DEFENSE_WINS', 'oS3kTZ2W': 'LEADER_SKILL_ID', 'hjAy9St3': 'PROC/PASSIVE_ID(S)', 'jSxdlwqd': 'KARMA_CAP', 'ZC0msu2L': 'MESSAGE', 'iN7buP1i': 'FACEBOOK_TOKEN', 'qA7M9EjP': 'AVAILABILITY_TIME_START/AMOUNT_REQUIRED', '7GMDoJ8n': 'SUMMONER_ES_ID', '49sa3sld': 'OE+ Level', 'Sv80kL5r': 'HR', '5K5wsBoL': 'ARENA_TEAM', 'y4jAZ9nI': 'UNIT_SELL_CAUTION', 'c5yZnpB4': 'FH_SEASON', 'G630LOgfs': 'ACHIEMEMENT_LOCATION_NEEDED', 'eKtE6k0n': 'ITEM_SALE_PRICE', 'D2BlS89M': 'IS_MILESTONE?*', 'Kn51uR4Y': 'PROCESS_ID', 'zwwtHlMM': 'REWARD_CONDITION', 'A3TSv2fn': 'SOUNDTRACK_FILE', '0QxL2is7': 'IDLE_ANIMATION', 'W4QdZ6pE': 'RESOLUTION_B?', 'iIDqD50O': 'SUMMONER_ART_LEVEL', 'pG2n1A28': 'FG_FLOOR', '1TED5ZSi': 'BATTLE_EFFECT_ID', 'Nt38aDqi': 'MAX_GUILD_MEMBERS', 'nDf28LtU': 'BOSS_SOUNTRACK', '03UGMHxF': 'GEM_COST', 'paND1zM8': 'TIME_SINCE_FRIEND_ADDED', 'csIuech30': 'GUILD_MEMBER_LIST', 'FxewAaR2': 'GUARDIAN_SKILL_BOOSTS', '9C64Qwe0': 'QUEST_ZONE_MAP_NUMBER', 'm9gd5h1u': 'ITEM_MAX_STACK', 'u7Ijep5o': 'RANK_MIN', '2rR5s6wn': 'INCREASED_FRIEND_CAP*', 'a3c0d5bi': 'VORTEX_ARENA_RANK_REWARDS', 'wXTxs50z': 'BUNDLE_SITE', 'osidufj5': 'GUILD_LEVEL', 'JATWnN57': 'DATE_CREATED', 'f0IY4nj8': 'ENERGY_REFILL_TIME', 'peCeLuNq': 'COLO_FORMATION_ID', '6c3vHQJY': 'GUARDIAN_SKILLS', 'Rqc8pi0x': 'UNKNOWN_RAID_WORLD_PARAMETER*', 'RQ5GnFE2': 'HONOR_POINTS_OBTAINED', 'qXCIfZIk': 'OPPONENT_POINTS', 'U8uZLA34': 'NUM_OF_SPARKS_A', 'wHN6nfh9': 'MIMIC_INFO', 'mv4o39Uz': 'UNIT_ATTACK_MOVE_TYPE', '38DabiEe': 'GUARDIAN_NAME', 'HCZs5dMf': 'OPPONENT_GUILD_ID???', 'LI5euJ7T': 'MOVE_ANIMATION', 'D4Y5bWK7': 'P_AFTER_IMAGE', 'PjfsG32': 'ACHIEVEMENTS', 'w0aTd94Y': 'ARENA_RANK_MIN_POINTS', 'gLUNSs24': 'HELP_SUBTOPIC_NAME', 'sdE1oku7': 'RESOLUTION_A?', '7boad17y': 'LOCATIONS_INFO', 'XLSB42ED': 'SP_CAT_NAME', '1ziVyEI9': 'DICTIONARY_VALUE', '1fFtoLva': 'GUILD_ROOM_GEN_INFO', '9r3aLmaB': 'SUMMON_TICKETS', 'j7fTS3ca': 'EVO_MAT_ID_JP (4)', 'IZUvR489': 'EVO_MAT_TYPES_JP (6)', 'v9dyS8fi': 'HELP_SUBTOPIC_NUMBER', '6z54rgb3': 'P_DETAIL_IMG_POS', 'uR6vbPRA': 'WIN_BONUS_MULTIPLIER', '6E2fGPWT': 'ITEM_TARGET_AREA', '7x3pPB2C': 'RC', 'BsBkDpYK': 'OPPONENT_GUILD_NAME', 'bD18x9Ti': 'SUMMER_LOGIN_CAMPAIGN', 'Z8eJi4pq': 'SLOT_ITEMS_LIST', 'Cdv07KEU': 'FH_GRADE', 'k23D7d43': 'DAILY_TASKS', 'BilJmqI0': 'FRONTIER_GATE_NAME', '1rcF7R6W': 'ROUTE_ID', 'ZSf8e1MG': 'LOCATIONS_UNLOCKED?', 'gFq59B6X': 'SQUAD_NUMBER', '8ZSQ5F2V': 'NUMBER*', 'Sj9zR38K': 'UNIT_TYPE_DEFENSE', '3NbeC8AB': 'LEVEL', 'TX98PnpE': 'SLOT_MACHINE_RESOURCES', 'V84mzqoX': 'QUEST_ZONE_NAME', 'YRgx49WG': 'HOUSE_LEVEL (SPHERE,SYNTHESIS/EVENT_BAZAAR/MUSIC/LS_SPHERE_HOUSE)', 'U0s6Wkoq': 'RESOLUTION_B_EXTENSION?', '8uJ1XGwx': 'ARENA_RANK', 'hBNPQAU0': 'FRONTIER_GATE_ID', 'sD73jd20': 'GUILD_ID', '97yTNbfr': 'REQUIREMENT_RARITY*', 'xXdp1q0Y': 'ACHIEVEMENT_NAME', 'dPM7oJDl': 'FG_SCORES', 'cP83zNsv': 'ES_ID', 'YS2JG9no': 'ARENA_ORBS', 'oT3aeqb3': 'SPECIFIC_GUARDIAN_SKILL_ID_WITH_LVL', 'gr48vsdJ': 'LEADER=0', 'WDUyI85C': 'MISSION_TEXT', 'IkmC8gG2': 'REQUIREMENT_TYPE*', 'd54Z3hUc': 'RESOLUTION_A_EXTENSION?', 'QB0KYH2R': 'PLAY_STYLE_NAME', 'Lu0pAk1R': 'QUEST_ROUNDS', 'LE6JkUp7': 'UNIT_DROP_ROUNDS', 'bVe381bC': 'GUARDIAN_AI_INFO', '7ofj5xa1': 'RARITY', 'oO1opB6Z': 'SUMMONER_WEAPON_NAME', '7Ffmi96v': 'SUMMON_GATE_ID', 'yEi6I3nF': 'ACHIEVEMENT_NAME', 'JmFn3g9t': 'ARENA_RANK', 'K1sM9FtZ': 'RAID_BOSS_NAME', 'l4txLZJ1': 'TIME:CURRENT_ROUND_BATTLE_START', 'KP3t9sfZ': 'FH_CHALLENGE_IMAGE', '74VFwuTd': 'EVO_UNIT_TYPE', 'H9sx5D08': 'MAP_IMG_AREA_NUMBER', 'n5mdIUqj': 'CURRENT_SUMMONER', '5wB9SHAV': 'MAX_ITEM_DROPS', 'iN7buP0j': 'DN*', '37moriMq': 'ELGIF_REWARD*', 'W9ABuJj2': 'SUMMON_BUTTOM_IMAGE', 'CR6aKWg8': 'AMOUNT_AND_LOCATION_USED', 'h7LYasNK': 'LANGUAGE', '5bBwEo9f': 'LEADER_ID', 't1i2vIbT': 'ITEM_MAX_EQUIPPED', '5F1qmcgX': 'EVO_MAT_TYPES (3)', 'pRKFVb2k': 'ATK_ANIMATION_2', 'PV3gH1Yf': 'LOCATION_NUMBER', 'EI1DF8Yt': 'UNIT_MAX_LEVEL', 'omuyP54D': 'UNIT_LORD_ATTACK', 'Mdgsh04u': 'EXCHANGE_HALL_ID', 'xvbaVDkL': 'ROOM_MAX_MEMBERS', 'vW75Pgpw': 'SALES_OFFERS_GEMS_ETC', 'N7I9vYZb': 'MAX_CARRY', 'A8DEK5ob': 'ENERGY_REQUIRED', 'k9Mvfp27': 'AI_CONDITION_2', 'AZFM14In': 'IS_CAMP?', '9unNZ6b0': 'LOCKED_IMAGE', 'oL71Fz3a': 'BANNER_ID', 'HgYvs3am': 'COLO_TEAM', 'd83aQ39U': 'BP_REWARD_ID', 'VBj9u0ot': 'AI_TARGET_CONDITIONS', 'y8WXGps6': 'GUARDIAN_AI_ID', 'j10diyl9': 'BUNDLE_ID', 'FHThxDv4': 'SP_TERM_SKILL', 'Voht18AP': 'EVO_MAT_ID_JP (6)', 'MVidsUNV': 'EVO_MAT_ID_JP (10)', 'PYgkvcsy': 'QUEST_ALWAYS_EMPTY', 'b38adb8i': 'REWARD_IMAGE', '7hLR6pDN': 'P_CUT_IN_IMG_POS', 'J3stQ7jd': 'HONOR_POINTS', '81tacsfJ': 'GR_ROUND?', '7Lx3qcDU': 'WORLD_NUMBER*', 'PWXu25cg': 'REC', 'c7Z6xDB2': 'ITEM_NAME', 'NungTq5g': 'SUPPORT_ID', 'me7eDiXs': 'LOCATION', 'uKYf13AH': 'DOOR_IMAGE', 'Pj6zDW3m': 'UPDATE_INFO', 'QYP4kId9': 'SQUAD_COST', '3sRN9BPS': 'MISSION_SOUNDTRACK', 'qYCx73y2': 'SKILL_START_FRAME', 'DFY3k6qp': 'DEVICE_NUMBER?', 'Nebq4d8x': 'GR_ROUND_TIMING_INFO', '1ry6BKoe': 'RAID_INFO', 'MYK1fq6c': 'P_CONFIRM_IMG_POS', 'k7Lf0jTt': 'SOUNDTRACK_NUMBER', 'ChD5b0jR': 'CHANCE', '0QyCU1dR': 'MAP_NAME', 'ya7UHG9v': 'DATE_EXPIRING', 'L8iA9M6c': 'DUNGEON_IMAGE', '7XYkj2EU': 'SP_TERM_COMMENT', 'h6V4weL2': 'FH_RANK_NAME', '2Smu5Mtq': 'PROC/PASSIVE_PARAMETERS', 'm3hq3kLc': 'GUARDIAN_STATS_AND_SKILLS', 'FfZ30yBt': 'STAMP_NUMBER', '8zaB7d6W': 'ACHIEVEMENT_TYPE*', '3kcmQy7B': 'FAVORITED_UNITS', 'WpFjS0PA': 'UPPER_ANIMATION', 'dag38b71': 'GUILD_TOTAL_CONTRIBUTIONS', 'Y73tHKS8': 'SPECIAL_DUNGEONS?', '30uygM9m': 'FRIENDS_LIST', '6lldENEG': 'TIME:PREP_PHASE_NEXT_ROUND', 'VuIPnfDO': 'COLO_FORMATION_EFFECTS', '5SUvj4tM': 'UNIT_OD_STATS', 'S1B82FHK': 'PRESENTS_BOX_ID', '24biyLHp': 'DUNGEON_DIFFICULTY', '2s8NnYav': 'QUEST_ALWAYS_1.0', '18Oz7z8k': 'EVO_MAT_TYPES_JP (9)', '3nZrT1bC': 'OFFER_ID', 'duN7tx0R': 'QUEST_FLAG_REQUIREMENTS', 'z1I0P1Qk': 'TIME:GUILD_EXCHANGE_HALL_RESET', 'B76UmxCQ': 'SUMMONER_RAW_STATS_BOOST', '5pkWU4yH': 'SUMMONER_LEVEL_STATS_CATEGORY', '6D3YN9rc': 'UNIT_TYPE_RECOVERY', '2Fh3J7ng': 'PLAYER_LEVEL', '6d8Njpq9': 'UNLOCKED_AT_LEVEL_MSG', 'PAd9aS1H': 'SUMMONER_UNITS', 'hQ1SJZU9': 'EXCHANGE_HALL_NAME', 'sc83dkh3': 'GUILD_PRESTIGE_POINTS', 'ri6D9yBi': 'SP_ID', '4NuIwm77': 'BP_REQUIRED', '1U3eBCyY': 'ARENA_RANK_MAX_POINTS', 'z1rMbo8n': 'TOTAL_CBP', 'X3nAm2k1': 'ROOM_LEADER', 'e6mY8Z0k': 'IMP_DEF', 'FKVRt01T': 'SPHERE_CAPACITY_INCREASE', 'XE7Yi5c3': 'UNIT_SKILL_MOVE_TYPE', 'ZwstRU92': 'RESOURCE_FILE', 'wgV86x1q': 'ITEM_QUANTITY', 'SWdq7R3o': 'GEM_AMOUNT', 'UZ1Bj7w2': 'UNIT_BASE_HP', 'EK7jR4rB': 'EVO_MAT_TYPES_JP (10)', 'Hhgi79M1': 'AI_ACTION_PARAMETERS*', '2375D38i': 'VORTEX_DUNGEONS', 'gvT2ds0Q': 'UNIT_COST', '85HpkjZW': 'TRIGGERED_QUEST_TEXT_AND_FLAG_SET', 'empaR60j': 'ARENA_RANK_REWARDS', 'YnVo64z1': 'ROUTE_START_LOCATION?', 'M94dsd6H': 'UNKNOWN', 'SiYs27Cj': 'REWARDS*', 'rY6j0Jvs': 'SLOT_IMAGES', '1VagK32J': 'FRIEND_LEAD', 'yXNM8kL3': 'QUEST_EVENTS?', 'PINm2pM5': 'SECTION_NUMBER', 'IZt73kLG': 'SKILL_TARGET_AREA', 'qY49LBjw': 'TIME_TILL_EVENT', 'kj1d80ai': 'GUILD_SEARCH_RESULTS', '49cks405': 'COLLAB_UNITS', 'rA9jDCP5': 'STAMP_SET_NUMBER', 'bM7RLu5K': 'FRIEND_COMMENT', 'U9ABSYEp': 'COLO_STRIKE_NO', '9i2xhMaJ': 'Unit Gender', 'mC1JcVM9': 'SCENARIO_ID', 'hceYTcAK': 'REGION', 'b839kdi1': 'ROOM_MEMBER_INFO', 'iEFZ6H19': 'SBB_ID', '7qncTHUJ': 'GUILD_INBOX_COUNT', '85X6JHQA': 'EVO_MAT_ID_JP (1)', 'grKTq15A': 'GUILD_LEVEL_MIN_EXP_THRESHOLD', 'xW6TKu9G': 'BATTLE_EFFECT_GROUP_SOUNDS', 'zI2tJB7R': 'RECORDS', 'erf9ZRt7': 'AI_CONDITION_PARAM_2', 'e7DK0FQT': 'HP', 'BM29ZgnK': 'KEY_NAME', 'N4XVE1uA': 'MAP_OPENING_TEXT_FILE', '89ausgc4': 'ARENA_AI_INFO', '0nxpBDz2': 'NAME', 'R2XB69Zj': 'VORTEX_ID', 'SP29fLtH': 'RAID_BOSS_NUMBER', 'iN7buP2h': 'GAME_USER_ID', 'b5yeVr61': 'RAID_CLEAR_REWARDS?', 'R3DqBi3b': 'GUARDIAN_ID', 't5R47iwj': 'GUARDIAN_SKILL_GROUP/AMOUNT_REQUIRED', 'zCe38bie': 'GUARDIAN_SKILL_ID_AND_AI', '2kd649bD': 'BUNDLE_ITEM_PARAMETERS', '0UwMg18F': 'BATTLE_EFFECT_GROUP', 'RVVgyuor': 'SUMMONER_WEAPON_ID', 's35idar9': 'GUILD_NAME', 'Kt8H4LN7': 'PLAYER_LEVEL_CAP', 'kP3zJ9Ra': 'ITEM_SHORT_NAME', 'EfinBo65': 'PRESENTS_BOX_LENGTH', 'd2RFtP8T': 'FILE_VERSION', 'VhX9c8YL': 'FLAGS_TRIGGERED?', 'z5Krebt4': 'BOOST_ID', 'u3HFse2a': 'LOCATIONS_NAME', 'VX0j1fni': 'UNLOCKED_IMAGE', 'NsZIP0d8': 'ITEM_SET_CONTAINED', '0pMem1xg': 'UNIT_EVOLUTION_TEXT', '3mMAn6L5': 'COLO_CLASS_NUMBER', 'SivJ9sL9': 'GUILD_MEMBERS', 'TokWs1B3': 'HP_IMPS', 'dV3qji4I': 'EVO_TYPE', 'O36Qv37k': 'TASK_SHORTNAME', 'IkdSufj5': 'GUILD_INFO', '3WMz78t6': 'UNIT_LORD_HP', 'aBcniqj8': 'GUILD_MASTER', 'M2cv6dum': 'THUMBNAIL', 'VS7df4oH': 'IMP_CAP_BOOST', 'FfBebG0R': 'COLO_RECORDS', '3g8brFoq': 'EVO_MAT_ID_JP (7)', 'RHo1m0f6': 'EVO_MAT_TYPES (4)', 'o94cnA8P': 'GUILD_CREATED_DATE', '6Aou5M9r': 'DAMAGE_FRAMES', 'De5dk137': 'VORTEX_MISSION_NAME', 'PEhNd0B4': 'ITEM_RAID_USAGE_FLAG', 'tA4T0GXB': 'RAID_BOSS_ID?', 'y1pHwW54': 'QUEST_ZONE_MAP_NAME', '8VYd6xSX': 'ROOM_ID', '9w5e3ZJB': 'FH_MISSION_ID', 'WhVJkLa1': 'TIME:CURRENT_BATTLE_FINISH', 'q08xLEsy': 'DEF', 'd2b8d79J': 'VORTEX_ARENA', 'ZKQ1X69a': 'ITEM_RAID_FLAG', '3evIn0zZ': 'JP_UNIT_NAME', '4tswNoV9': '3-4*_SUMMON_BOOLEAN???', 'yu35Bdwr': 'SKILL_ID', 'o49dYfpH': 'MONSTER_ID', 'Y3DbX5ot': 'REQUIRED_AMOUNT', '3D42LTtj': 'RAID_WORLD_NAME', 'wvANuT8R': 'WEAPON_SBB_LEVEL', '1IR86sAv': 'SUMMON_GATES', 'st0Ep96q': 'QUEST_ALWAYS_0', 'U4pMNjy0': 'ARENA_BATTLE_POINTS', 'TCnm1F4v': 'SUMMON_GATE_BASIC_ID?', 'VlSyNGyG': 'SUMMONER_WEAPON_SKILL(S)', '1gDkL6XR': 'BANNER_IMG', '92udyUrJ': 'ITEM_KIND', 'bd5Rj6pN': 'VALID_ITEMS_LIST', '6HmU8ZWb': 'NPC_MESSAGE_NUMBER', 'DXm2W8vY': 'ZEL_CAP', 'HwCngVzI': 'GUARDIAN_SKILL_LEVELS', 'PKa13dH7': 'QUEST_ALWAYS_1.0', 'jp9s8IyY': 'TIME_TILL_ORB_REFRESH', 'Lkh6gYkT': 'P_CURSOR_DISP_POS', 'IxiGlf2f': 'SQUAD_INFO', '6FrKacq7': 'SIGNAL_KEY', 'csI7dh30': 'RECOMMENDED_GUILDS', '0CAQ6wUe': 'TIME_SINCE_LAST_LOGIN', 'X6jf8DUw': 'IMP_REC', 'qnccUrMN': 'CURRENT_CBP', 'j28VNcUW': 'MISSION_ID', 'H0UB8pqm': 'QUEST_BANNER_IMG', 'ZEzhmS53': 'UNIT_SUMMON_TEXT', 'c6fVJ9qR': 'RESTRICTIONS*', 'VjCY7rX4': 'MISSION_AREA', '98WfKiyA': 'PLAYER_ID', 'b2LNsR7C': 'VORTEX_TYPE*', 'zXckdA51': 'MIN_AGE', 'NML08EGS': 'REQUIREMENT_ID', '84adiqJk': 'SPECIAL_SUMMON_NUMBER', '4xctV8gF': 'TARGET_TYPE', '7ZNcmYS2': 'GACHA_SCRIPT_A', '7dEB1Kwj': 'MAT_REQUIRED_TO_DISPLAY', 'cb0P4mp1': 'UBB_ID', '1n9caurK': 'RAID_WORLD_SHORTNAME', '75YV2q1i': 'RECIPE_MATERIALS', 'Mt3Y0bo5': 'THUMBNAIL', '9SVsdnwl': 'CP', 'gE2NN2xi': 'POINTS', 'uK391dP3': 'BUNDLE_LIMIT', 'L2VkgH08': 'PRESENT_DESCRIPTION', '3quwOva9': 'GUARDIAN_STATS_SKILLS', 'Fnxab5CN': 'SP_ENHANCEMENTS (CATEGORY@ID)', 'B5JQyV8j': 'IGN', 'sYsa10a3': 'QUEST_ALWAYS_EMPTY', '4eEVw5hL': 'AI_ID', 'bWsLFP96': 'DUNGEON_NAME', 'Heg8ZDQ7': 'BATTLE_EFFECT_FILE', '3EWLm0sA': 'EXCHANGE_HALL_COST', '43hMuY2I': 'RAID_WORLD_NUMBER', 'K72eC4nz': 'BUNDLES_INFO', 'mebW7mKD': 'VIDEO_SLOTS', '2z8kTtBy': 'CRIT_HITS', 'iW62Scdg': 'SLOT_MACHINE', 'NpM9IWs8': 'AI_CONDITION_PARAM_1', 'NyYKc1A5': 'BANNER_TEXT', 'M7yKr4c1': 'TASK_DESCRIPTION', 'T430LOfd': 'ACHIEVEMENT_DESCRIPTION', 'Najhr8m6': 'ZEL', '8R5wDyXb': 'SOUNDTRACK_FILE', '1ZF3zLrC': 'LOCATIONS_TYPE', 'a3vSYuq2': 'REQUEST_BODY_TAG', 'cEsJzMhy': 'MAX_ZEL_CONTRIBUTION', '58LRVS1i': 'FH_CHALLENGE_MVP_IMAGE', 'jeR2rN3V': 'EFFECT_AREA*', 'Z0Y4RoD7': 'UNIT_SQUAD_NUMBER', 'HSRhkf70': 'MISSION_IDS_REQUIRED', 'meg8fhr1': 'HELP_ID', '0Ar0scn1': 'WEAPON_BB_LEVEL', 'kW5QuUz7': 'DATE', 'VETu07N6': 'AI_NUMBER?', 'hdF8ND2H': 'EVO_MAT_TYPES_JP (4)', '4A6LzBxr': 'LEADER_UNIT_MAX_LEVEL', 'SsNg4d6o': 'ALWAYS_AAA.JPG', '9wjrh74P': 'ITEMS_BOX', '6yHMXYv1': 'UNIT_GETTING_TYPE', 'd07ewqx5': 'GUARDIAN_SKILL_LEVEL_IDS', 'HTVh8a65': 'KARMA', 's2gM3deu': 'ES_PARAMETERS', 'q9I4karx': 'JP_DESCRIPTION', 'X9P3AN5d': 'UNIT_LORD_REC', '5kbnkTp0': 'NUM_OF_ENTRIES', '5qBCQ1PJ': 'BATTLE_EFFECT_GROUP_NAME', 'np4K1xtq': 'QUEST_ALWAYS_EMPTY', 'moWQ30GH': 'FILE_NAME', 'Qzhp8B40': 'AI_ID?', 'F4q6i9xe': 'REQUEST_HEADER_TAG', '16KMNJLb': 'KEY_ID', '6GwnugW3': 'EVO_MAT_TYPES_JP (3)', 'vn83gRn8': 'GUARDIAN_NUMBER(1759-1765)', 'tw0vkye4': 'SCENARIO_TEXT_FILE', 'IKqx1Cn9': 'AUTHENTICATION_INFO', 'H6k1LIxC': 'ITEM_CRAFT_LIMIT', '4N27mkt1': 'SUMMON_GATE_NAME', 'fEi17cnx': 'USER_INFO', '8CEu9Kcm': 'ARENA_OFFENSE_WINS', '938AbXie': 'GUARDIAN_TYPE', 'iQM9dH0F': 'SLOT_IMAGE_FILE', '3sdHQb69': 'SUMMON_GATE_DESCRIPTION_A', 'i30R8TAs': 'POSSIBLE_DROPS', 'TdDHf59J': 'REWARD_ITEM_ID', 'Db6D38hg': 'DUNGEON_DESCRIPTION', 'YGVldhVW': 'SUMMONER_BATTLE_IMAGE', 'b5z9dFdk': 'BUNDLE_DESCRIPTION', 'yNnvj59x': 'DICTIONARY_KEYS', '0xFHwMf7': 'FAILURE_CONDITIONS', 'ceak3Pxn': 'ROOM_MEMBERS', 'I1Cki7Pb': 'SECTION_NAME', '9cKyb15U': 'COMPLETED_AMOUNT', 'Pk5F1vhx': 'LINKS', 'Bm1WNDQ0': 'FRIEND_GIFT_OPTIONS', 'sE6tyI9i': 'SLOT_ITEM_NUMBER', '5UvTp7q1': 'UNIT_EXP_PATTERN_ID', 'mdAfte54': 'STAMP_SET_NAME', 'wHWHChDV': 'SUMMONER_LOWER_IMAGE', '2M4mQZgk': 'UNIT_TYPE_ATTACK', 'F6bPj50Q': 'Leader ID', 'utP1c0CD': 'UNIT_NAME', 'yba3la1b': 'MAX_KARMA_CONTRIBUTION', 'xP9oi5Z2': 'UNIT_KIND', '0iAIR2LP': 'MISSION_NAME', 'q78KoWsg': 'UNIT_BASE_DEFENSE', '3v1qg7Uj': 'UNKNOWN_BOOLEAN_QUESTS', 'NGL2K1id': 'COLO_CLASS_NAME', 'ctAd91iQ': 'SCENARIO_NAME', '3b6aDakz': 'SPECIAL_$$$_SUMMON_GATES_BUNDLE*', '83Bda1Bv': 'GUARDIAN_MOVEMENT_ANIMATION_AND_STATS', 'BYaF62TE': 'ARENA_RANKINGS', 'u0vkt9yH': 'GATE_EFFECT_ID', '9b7aDa71': 'GUARDIAN_INFO_LOCATION', 'n0He37p1': 'LOGIN_DAY', 'kixHbe54': 'ITEM_ID', 'EI6HtL9A': 'QUEST_ALWAYS_1.0', 'fZgEP96L': 'LEADER_MAX_LEVEL', 'Yxo3bEic': 'EXCHANGE_HALL_ITEM_ID', '92VHUDEC': 'RELOAD_ID', 'Uh3Te4AI': 'ALWAYS_AAA.JPG', '3MAT6quo': 'UNIT_DROPS', 'i74vGUFa': 'UNIT_AI_ID', 'bpD29eiQ': 'SERVER/LANGUAGE_INFO?', 'dyF0xAz1': 'SUMMONER_ES_NAME', '4T0Q2Bh5': 'ITEM_DROPS', 'W2c9g0Je': 'SUMMON_GATE_DESCRIPTION_B', 'Btf93Xs1': 'ENEMY_JP_NAME', 'eKPWNoLn': 'EVO_MAT_ID_JP (9)', '0P9X1YHs': 'CURRENT_ENERGY', 'zKXSM4vh': 'SUMMONER_UPPER_IMAGE', '7MxucW2J': 'EVO_MAT_ID_JP (3)', '0Cq2AlXW': 'QUEST_GATE_NUMBER*', 'MHx05sXt': 'DUNGEON_ID', 'xIRA58fC': 'SOUNDTRACK_NAME', 'K89GWSY1': 'DICTIONARY_KEY', 'd96tuT2E': 'EXP_GAIN', 'nj9Lw7mV': 'BB_ID', 'NH65Wj0f': 'TOP_RANKS?', '7k5fMj3L': 'TIME:CURRENT_ROUND_PREP_PHASE_STARTS', 'spGsSSk3': 'DATE_JOINED_GUILD', 'd3gaby8a': 'CONTRIBUTIONS_INFO', '8jBJ7uKR': 'ARENA_STUFF?', '1e6jxQzf': 'QUEST_USUALLY_EMPTY_BUT_CHECK**', 'mZA7fH2v': 'SPHERE_1_EQUIPPED_ID', 'tpuBKuJ7': 'CAMP_LOCATION', 'M7SXoc31': 'ACHIEVEMENT_ID'}
decoded2={'ziex06DY':'SQUAD_COST?','GZ2rKW90':'SOMETHING_PLAYER_LEVEL_RELATED_0-50','oFQ3mbS6':'SOMETHING_PLAYER_LEVEL_RELATED_10-50','hx87WCbQ':'SUMMONER_LEVEL_CAP?','Ieq49JDy':'CLIENT_VERSION?','VkoZ5t3K':'IMPORTANT_VALUES','07nTrLdD':'P_TRIBE','pA9ZoWa2':'P_GROWTH_TYPE','CEeqs63b':'P_STATUS_RESIST','jFX0a7qe':'P_MOVE_OFFSET','QwN4hqJ2':'P_SOUND_SETTING','KC3Jk8Br':'P_SUMMON_IMG_POS','Gd4NS7H6':'P_ADJUST_EXP','PXD4v2KY':'P_ADJUST_SKILL_LVUP_RATE','jyj6bl9P':'P_EXT_HOME_IMG_POS','QHhOLCuk':'P_EXT_DETAIL_IMG_POS','S0BjxW1F':'P_EXT_CONFIRM_IMG_POS','9y1vaEJk':'P_EXT_CUT_IN_IMG_POS','psOjpTAv':'P_EXT_SUMMON_IMG_POS'}
#,'YDv9bJ3s':'LEVEL_TABLE','mQC4s5ka':'FH_SEASONS_INFO','P8V71kbw':'FH_SEASON_REWARDS','zW1i02aG':'FH_MISSION_GRADE','4C1Wt8sS':'FH_MISSION_REWARD','5M8jI4cP':'FH_MISSIONS','nUmaEC41':'FH_MVP_RANKING','h09mEvDR':'FH_HR','dn0NfRy1':'FH_ITEM_SET','8f0bCciN':'ITEM_RECIPES'}
for x in decoded2:
    decoded[x]=decoded2[x]
q=forceLogin()
