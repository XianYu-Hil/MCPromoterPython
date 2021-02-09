#! /usr/bin/env python
# -*- coding:utf-8 -*-
import json

import mc
import tool
import threading
import time
import datetime
import re
import random

plugin_name = 'MCDaemonPython'  # 模块名称
plugin_version = 'V0.5.1β'  # 模块版本号
plugin_author = 'XianYu_Hil'  # 模块作者
plugin_status = 'running'  # 模块初始状态
proOperator = ['XianYuHil']  # 最高权限
serviceDate = '2020-06-25'  # 开服日期

playerDate = {}  # 玩家数据字典
dimensionCN = {0: "§l§2主世界", 1: "§l§4下界", 2: "§l§e末地"}  # 群系中文名字典
serverStatus = {'gameDay': '', 'tickStatus': '', 'kiStatus': '', 'mgStatus': '', 'entityCounter': '',
                'itemCounter': ''}  # 游戏状态字典
cmdHelper = [
    '§2========================',
    '@mcdp [status|help]    获取MCDP状态/帮助',
    '@mcdp install      初始化MCDP'
    '@=<表达式>    计算表达式并输出',
    '@back      返回死亡地点',
    '@ban <玩家名>     快速禁人(需特殊授权)',
    '@bot [spawn|kill] <BOT名>   召唤/杀死bot',
    '@bot list  列出服务器内存在的bot',
    '@day [game|server]     查询游戏内/开服天数',
    '@entity [count|list]   统计/列出服务器内实体',
    '@here      全服报点',
    '@item      [clear|count|pick]      清除/统计/拾取服务器内掉落物',
    '@ki [true|false|status]   开启/关闭/查询死亡不掉落',
    '@kill      自杀(不计入死亡榜)',
    '@load [block|circle]    设置方形/圆形常加载区块',
    '@load remove   移除常加载区块',
    '@mg [true|false]   开启/关闭生物破坏',
    '@sh <指令>   向控制台注入指令(需特殊授权)',
    '@sta <计分板名>    将侧边栏显示调整为特定计分板',
    '@sta null      关闭侧边栏显示',
    '@task [add|remove] <任务名>   添加/移除指定任务',
    '@tick [倍数|status]      设置/查询随机刻倍数',
    '§2========================'
]  # 帮助信息列表


def load_plugin():  # Module initializer |模块初始化器
    mc.logout("[MCDP]" + plugin_version + "已装载完成.用法:@mcdp status")


def normFeedback(name, content):  # Standardized ouput interface | 标准化输出接口
    feedbackContent = "tellraw " + name + ''' {"rawtext":[{"text":"''' + content + '''"}]}'''
    mc.runcmd(feedbackContent)


def argSplit(cmd):  # Command args separation | 指令参数分离
    if cmd != '':
        return str(cmd).split()


def uuidParsing(name):  # uuid Parsing | uuid解析
    a = json.loads(mc.getOnLinePlayers())
    for key in a:
        if key['playername'] == name:
            return key['uuid']
    return 'null'


def getDiffDate(targetDate):  # 获取时间差
    now = datetime.datetime.now()
    output = now - targetDate
    return str(output.days)


def removeBOT(_botName):  # Bot removal event | Bot移除事件
    botName = _botName[4:]
    mc.runcmd('tickingarea remove loader_' + botName)
    normFeedback('@a', '§ebot_' + botName + ' 退出了游戏')


def inputtext(e):  # @Command core methods | @指令核心方法
    p = mc.AnalysisEvent(e)
    name = p.playername
    msg = str(p.msg)
    uuid = playerDate[name]['uuid']
    x = str(int(p.XYZ.x))
    y = str(int(p.XYZ.y))
    z = str(int(p.XYZ.z))
    world = dimensionCN[p.dimensionid]


    if msg[0] == '@':
        mc.logout('[MCDP]<' + name + '>' + msg)
        argsList = argSplit(msg)
        if argsList[0] == '@mcdp':
            if argsList[1] == 'status':  # 插件状态
                normFeedback(name, '§2========================')
                normFeedback(name, '§c§l ' + plugin_name + ' - ' + plugin_version)
                normFeedback(name, '§o作者：' + plugin_author)
                normFeedback(name, '模块状态：' + plugin_status)
                normFeedback(name, '§2====================')
                normFeedback(name, '@mcdp help     获取mcdp帮助')
                # normFeedback(name, '@mcdp updatelog      获取${Plugin_Version}的更新日志');
                normFeedback(name, '@mcdp install      第一次使用mcdp请务必执行一次!')
                normFeedback(name, '§2========================')
            elif argsList[1] == 'install':  # 插件初始化
                mc.runcmd('scoreboard objectives add Killed dummy §l§7击杀榜')
                mc.runcmd('scoreboard objectives add Dig dummy §l§7挖掘榜')
                mc.runcmd('scoreboard objectives add Dead dummy §l§7死亡榜')
                mc.runcmd('scoreboard objectives add Placed dummy §l§7放置榜')
                mc.runcmd('scoreboard objectives add Attack dummy §l§7伤害榜')
                mc.runcmd('scoreboard objectives add Hurt dummy §l§7承伤榜')
                mc.runcmd('scoreboard objectives add Tasks dummy §l§e服务器摸鱼指南')
                mc.runcmd('scoreboard objectives add _CounterCache dummy')
                mc.runcmd('scoreboard objectives add Counter dummy')
                mc.runcmd('scoreboard objectives add Health dummy 生命值')
                mc.runcmd('scoreboard objectives setdisplay belowname Health')
                normFeedback(name, '已初始化mcdp插件及其相关组件')
            elif argsList[1] == 'help':  # 获取插件帮助信息
                for helpInf in cmdHelper:
                    normFeedback(name, str(helpInf))
        elif msg.startswith('@='):
            result = eval(msg[2:])
            normFeedback(name, result)
        elif argsList[0] == '@back':
            if playerDate[name]['deathPos']['enable']:
                backX = playerDate[name]['deathPos']['x']
                backY = playerDate[name]['deathPos']['y']
                backZ = playerDate[name]['deathPos']['z']
                backD = playerDate[name]['deathPos']['d']
                mc.teleport(uuid, backX, backY, backZ, backD)
            else:
                normFeedback(name, '暂无死亡记录')
        elif argsList[0] == '@ban':
            bannedName = argsList[1]
            if name in proOperator:
                mc.runcmd('kick ' + bannedName + ' 您已被服务器永久封禁，无法再次进入游戏.')
                mc.runcmd('whitelist remove ' + bannedName)
                normFeedback('@a', bannedName + ' 已被永久封禁.')
            else:
                mc.runcmd('kick ' + name + ' 试图越权使用@ban指令，自动踢出')
                mc.logout("[MCDP]" + name + '试图跨权使用' + msg)
        elif argsList[0] == '@bot':
            if argsList[1] == 'list':
                mc.runcmd('say 服务器内存在§l @e[tag=BOT]')
            else:
                botName = argsList[2]
                if argsList[1] == 'kill':
                    mc.runcmd('kill @e[name=bot_' + botName + ']')
                elif argsList[1] == 'spawn':
                    mc.runcmd('execute @a[name=' + name + '] ~~~ summon minecraft:player bot_' + botName)
                    mc.runcmd('tag @e[name=bot_' + botName + '] add BOT')
                    mc.runcmd('execute @a[name=' + name + '] ~~~ tickingarea add circle ~~~ 4 loader_' + botName)
                    normFeedback('@a', '§ebot_' + botName + ' 加入了游戏')
                elif argsList[1] == 'tp':
                    mc.runcmd('execute @a[name=' + name +
                              '] ~~~ tp @e[name=bot_' + botName + ']')
        elif argsList[0] == '@day':
            if argsList[1] == 'game':
                mc.runcmd('time query day')

                def printGameDay():
                    normFeedback(name, '现在的游戏天数为' + serverStatus['gameDay'])

                threading.Timer(0.5, printGameDay).start()
            elif argsList[1] == 'server':
                serverDay = getDiffDate(datetime.datetime.strptime(serviceDate, '%Y-%m-%d'))
                normFeedback(name, '今天是开服的第' + serverDay + '天')
        elif argsList[0] == '@entity':
            if argsList[1] == 'count':
                mc.runcmd('scoreboard players set @e _CounterCache 1')
                mc.runcmd('scoreboard players set "entityCounter" Counter 0')
                mc.runcmd('scoreboard players operation "entityCounter" Counter+= @e _CounterCache')

                def printEntityCount():
                    normFeedback(name, '当前的实体数为' + serverStatus['entityCounter'])

                threading.Timer(0.5, printEntityCount)
            elif argsList[1] == 'list':
                mc.runcmd('say §r§o§9服务器内实体列表§r§l§f @e')
        elif argsList[0] == '@here':
            mc.runcmd('playsound random.levelup @a')
            normFeedback('@a', '§e§l' + name + '§r在' + world + '§e§l[' + x + ',' + y + ',' + z + ']§r向大家打招呼！')
        elif argsList[0] == '@item':
            if argsList[1] == 'clear':
                mc.runcmd('kill @e[type=item]')
                normFeedback('@a', '已清除所有掉落物')
            elif argsList[1] == 'count':
                mc.runcmd('scoreboard players set @e[type=item] _CounterCache 1')
                mc.runcmd('scoreboard players set "itemCounter" Counter 0')
                mc.runcmd('scoreboard players operation "itemCounter" Counter += @e[type=item] _CounterCache')

                def printItemCount():
                    normFeedback(name, '当前的掉落物数为' + serverStatus['itemCounter'])

                threading.Timer(0.5, printItemCount)
            elif argsList[1] == 'pick':
                mc.runcmd('tp @e[type=item] @a[name=' + name + ']')
                normFeedback('@a', name + '已拾取所有掉落物')
        elif argsList[0] == '@ki':
            if argsList[1] == 'status':
                mc.runcmd('gamerule keepinventory')

                def printKIStatus():
                    normFeedback(name, '当前死亡不掉落' + serverStatus['kiStatus'])

                threading.Timer(0.5, printKIStatus).start()
            elif argsList[1] == 'true':
                mc.runcmd('gamerule keepinventory true')
                normFeedback('@a', '死亡不掉落已开启')
            elif argsList[1] == 'false':
                mc.runcmd('gamerule keepinventory false')
                normFeedback('@a', '死亡不掉落已关闭')
        elif argsList[0] == '@kill':
            suicideMsg = [
                '§l' + name + '§r进入了通向二次元的入口',
                '§l' + name + '§r错杀亲马，悲痛欲绝',
                '不要停下来啊，§l' + name + '§r！',
                '§l' + name + '§r删除了MCDP的源代码',
                '§l' + name + '§r进入了和宝的蜜穴惨被榨干',
                '§l' + name + '§r被确诊为肝坏死',
                '§l' + name + '§r因长期摸鱼感染了新冠肺炎',
                '§l' + name + '§r贴了贴和宝',
                '§l' + name + '§r和LexBurner一起成为二刺螈蝗帝',
                '§l' + name + '§r和针针一起节约肉蛋奶保护巴西雨林',
                '§l' + name + '§r被夹去阴间',
                '§l' + name + '§r被割割粉丝网暴',
                '#肖战指使孙笑川杀死了' + name + '#',
                name + ':"tmd,烦死了"',
                '丁真教' + name + '抽烟',
                '孙笑川和肖战带着丁真去' + name + '家拜年，并让郑爽和他一起睡觉',
            ]  # 自定义自杀信息列表
            playerDate[name]['isSuicide'] = True
            mc.runcmd('kill ' + name)
            normFeedback('@a', suicideMsg[random.randint(0, 15)])
        elif argsList[0] == '@load':
            if argsList[1] == 'block':
                mc.runcmd('execute @a[name=' + name + '] ~~~ tickingarea add ~~~~~~')
                normFeedback('@a', '将§e§l[' + x + ',' + y + ',' + z + ']§r所在区块设为常加载区块')
            elif argsList[1] == 'circle':
                mc.runcmd('execute @a[name=' + name + '] ~~~ tickingarea add circle ~~~ 4')
                normFeedback('@a', '将以§e§l[' + x + ',' + y + ',' + z + ']§r为圆心，半径为4的圆所覆盖的区块设为常加载区块')
            elif argsList[1] == 'remove':
                mc.runcmd('execute @a[name=' + name + '] ~~~ tickingarea remove ~~~')
                normFeedback('@a', '移除了§e§l[' + x + ',' + y + ',' + z + ']§r所在的常加载区块')
        elif argsList[0] == '@mg':
            if argsList[1] == 'status':
                mc.runcmd('gamerule mobGriefing')

                def printMGStatus():
                    normFeedback(name, '当前生物破坏' + serverStatus['mgStatus'])

                threading.Timer(0.5, printMGStatus).start()
            elif argsList[1] == 'true':
                mc.runcmd('gamerule mobGriefing true')
                normFeedback('@a', '生物破坏已开启')
            elif argsList[1] == 'false':
                mc.runcmd('gamerule mobGriefing false')
                normFeedback('@a', '生物破坏已关闭')
        elif argsList[0] == '@qb':
            pass
        elif argsList[0] == '@sh':
            if name in proOperator:
                command = msg[3:]
                mc.runcmd(command)
                normFeedback('@a', '已向控制台注入了' + argsList[1])
        elif argsList[0] == '@sta':
            statisName = argsList[1]
            cnName = {
                'Dig': '挖掘榜',
                'Placed': '放置榜',
                'Attack': '伤害榜',
                'Hurt': '承伤榜',
                'Killed': '击杀榜',
                'Tasks': '待办事项榜',
                'Dead': '死亡榜',
                statisName: statisName,
            }  # 内置榜单中文名称
            if statisName != 'null':
                mc.runcmd('scoreboard objectives setdisplay sidebar ' + statisName)
                normFeedback(name, '已将侧边栏显示修改为' + cnName[statisName])
            else:
                mc.runcmd('scoreboard objectives setdisplay sidebar')
                normFeedback(name, '已将侧边栏显示关闭')
        elif argsList[0] == '@task':
            taskName = argsList[2]
            if argsList[1] == 'add':
                mc.runcmd('scoreboard players set ' + taskName + ' Tasks 1')
                normFeedback('@a', '已向待办事项板添加§l' + taskName)
            elif argsList[1] == 'remove':
                mc.runcmd('scoreboard players reset ' + taskName + ' Tasks')
                normFeedback('@a', '已将§l' + taskName + '§r从待办事项板上移除')
        elif argsList[0] == '@tick':
            if argsList[1] == 'status':
                mc.runcmd('gamerule randomtickspeed')

                def printTickStatus():
                    normFeedback(name, '现在的随机刻为' + serverStatus['tickStatus'])

                threading.Timer(0.5, printTickStatus).start()
            elif argsList[1].isdigit():
                tickSpeed = argsList[1]
                mc.runcmd('gamerule randomtickspeed ' + tickSpeed)
                normFeedback(name, '已将游戏内随机刻加快'+tickSpeed+'倍')


def mobdie(e):
    p = mc.AnalysisEvent(e)
    jsName = p.srcname  # 击杀者名字
    jsType = p.srctype  # 击杀者类型
    bsName = p.mobname  # 被杀者名字
    bsType = p.mobtype  # 被杀者类型
    world = dimensionCN[p.dimensionid]

    if jsType == 'entity.player.name':  # 若玩家击杀生物(击杀榜)
        mc.runcmd('scoreboard players add @a[name=' + jsName + '] Killed 1')
    if bsType == 'entity.player.name':  # 若玩家死亡(死亡榜)
        x = str(int(p.XYZ.x))
        y = str(int(p.XYZ.y))
        z = str(int(p.XYZ.z))
        if playerDate[bsName]['isSuicide']:  # 若玩家自杀
            playerDate[bsName]['isSuicide'] = False
        else:  # 若玩家他杀
            mc.runcmd('scoreboard players add @a[tag=!BOT,name=' + bsName + '] Dead 1')
        # 死亡爆点
        normFeedback('@a', '§r§l§f' + bsName + '§r§o§4 死于 ' + world + '§r§l§f[' + x + ',' + y + ',' + z + ']')
        # 记录死亡数据
        playerDate[bsName]['deathPos']['x'] = int(x)
        playerDate[bsName]['deathPos']['y'] = int(y)
        playerDate[bsName]['deathPos']['z'] = int(z)
        playerDate[bsName]['deathPos']['d'] = p.dimensionid
        playerDate[bsName]['deathPos']['enable'] = True
    if bsName[:4] == 'bot_':  # bot死亡
        removeBOT(bsName)

def destroyblock(e):
    p = mc.AnalysisEvent(e)
    name = p.playername
    if name != '':
        mc.runcmd('scoreboard players add @a[name='+name+'] Dig 1')

def placeblock(e):
    p=mc.AnalysisEvent(e)
    name=p.playername
    if name != '':
        mc.runcmd('scoreboard players add @a[name='+name+'] Placed 1')

def load_name(e):  # Player enter event | 玩家进入服务器
    p = mc.AnalysisEvent(e)
    name = p.playername
    playerDate[name] = {}
    playerDate[name]['deathPos'] = {}
    playerDate[name]['deathPos']['enable'] = False
    playerDate[name]['isSuicide'] = False
    playerDate[name]['uuid'] = p.uuid


def server_cmdoutput(e):  # 后台输出处理/拦截
    p = mc.AnalysisEvent(e)
    output = str(p.output)
    if output.startswith('Day is '):
        serverStatus['gameDay'] = re.findall(r"\d+\.?\d*", output)[0]
    elif output.startswith('randomtickspeed = '):
        serverStatus['tickStatus'] = re.findall(r"\d+\.?\d*", output)[0]
    elif output.startswith('keepinventory = '):
        if output.startswith('keepinventory = true'):
            serverStatus['kiStatus'] = '已开启'
        else:
            serverStatus['kiStatus'] = '已关闭'
    elif output.startswith('mobGriefing = '):
        if output.startswith('mobGriefing = true'):
            serverStatus['mgStatus'] = '已开启'
        else:
            serverStatus['mgStatus'] = '已关闭'
    elif 'entityCounter' in output:
        serverStatus['entityCounter'] = re.findall(r"\d+\.?\d*", output)[0]
    elif 'itemCounter' in output:
        serverStatus['itemCounter'] = re.findall(r"\d+\.?\d*", output)[0]


def player_left(e):  # Player leave event | 玩家离开服务器
    p = mc.AnalysisEvent(e)
    name = p.playername
    del playerDate[name]
