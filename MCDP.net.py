#! /usr/bin/env python
# -*- coding:utf-8 -*-
import json

import mc
import tool
import threading
import time

plugin_name = 'MCDaemonPython'  # 模块名称
plugin_version = 'V0.3.0β'  # 模块版本号
plugin_author = 'XianYu_Hil'  # 模块作者
plugin_status = 'running'  # 模块初始状态
operator = 'XianYuHil'  # 最高权限

playerDate = {}  # 玩家数据字典
dimensionCN = {0: "§l§2主世界", 1: "§l§4下界", 2: "§l§e末地"}  # 群系中文名转换


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


def removeBOT(_botName):  # Bot removal event | Bot移除事件
    botName = _botName[4:]
    mc.runcmd('tickingarea remove loader_' + botName)
    normFeedback('@a', '§ebot_' + botName + ' 退出了游戏')


def inputtext(e):  # @Command core methods | @指令核心方法
    p = mc.AnalysisEvent(e)
    name = p.playername
    msg = p.msg
    uuid = playerDate[name]['uuid']
    x = str(int(p.XYZ.x))
    y = str(int(p.XYZ.y))
    z = str(int(p.XYZ.z))
    world = dimensionCN[p.dimensionid]

    if msg[0] == '@':
        argsList = argSplit(msg)
        if argsList[0] == '@mcdp':
            if argsList[1] == 'status':
                normFeedback(name, '§2========================')
                normFeedback(name, '§c§l ' + plugin_name + ' - ' + plugin_version)
                normFeedback(name, '§o作者：' + plugin_author)
                normFeedback(name, '模块状态：' + plugin_status)
                normFeedback(name, '§2====================')
                normFeedback(name, '@mcdp help     获取mcdp帮助')
                # normFeedback(name, '@mcdp updatelog      获取${Plugin_Version}的更新日志');
                normFeedback(name, '@mcdp install      第一次使用mcdp请务必执行一次!')
                normFeedback(name, '§2========================')
            elif argsList[1] == 'install':
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
            elif argsList[1] == 'help':
                pass
        elif argsList[0] == '@=':
            result = eval(msg[1:])
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
            if name == operator:
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
                pass
            elif argsList[1] == 'server':
                pass
        elif argsList[0] == '@here':
            mc.runcmd('playsound random.levelup @a')
            normFeedback('@a', '§e§l' + name + '§r在' + world + '§e§l[' + x + ',' + y + ',' + z + ']§r向大家打招呼！')


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
    if bsName[:4] == 'bot_':    # bot死亡
        removeBOT(bsName)


def load_name(e):  # Player enter event | 玩家进入服务器
    p = mc.AnalysisEvent(e)
    name = p.playername
    playerDate[name] = {}
    playerDate[name]["deathPos"] = {}
    playerDate[name]["deathPos"]['enable'] = False
    playerDate[name]["isSuicide"] = False
    playerDate[name]['uuid'] = p.uuid


def player_left(e):  # Player leave event | 玩家离开服务器
    p = mc.AnalysisEvent(e)
    name = p.playername
    del playerDate[name]
