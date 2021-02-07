#! /usr/bin/env python
# -*- coding:utf-8 -*-
import mc
import tool

plugin_name = 'MCDaemonPython'
plugin_version = 'V0.0.1'
plugin_author = 'XianYu_Hil'
plugin_status = 'error'
operator = 'XianYuHil'


def normFeedback(name, content):
    feedbackContent = "tellraw "+name + \
        ''' {"rawtext":[{"text":"'''+content+'''"}]}'''
    mc.runcmd(feedbackContent)


def load_plugin():
    print("*******" + plugin_name + " - " +
          plugin_version + " 已装载完成       用法:@mcdp *******")
    plugin_status = 'running'


def inputtext(e):
    p = mc.AnalysisEvent(e)
    name = p.playername
    msg = p.msg

    if msg == '@mcdp':
        normFeedback(name, '§2========================')
        normFeedback(name, '§c§l '+plugin_name+' - '+plugin_version+)
        normFeedback(name, '§o作者：'+plugin_author)
        normFeedback(name, '模块状态：'+plugin_status)
        normFeedback(name, '§2====================')
        normFeedback(name, '@mcdp help     获取mcdp帮助')
        #normFeedback(name, '@MCDB updatelog      获取${Plugin_Version}的更新日志');
        normFeedback(name, '@mcdp install      第一次使用mcdp请务必执行一次!')
        normFeedback(name, '§2========================')
