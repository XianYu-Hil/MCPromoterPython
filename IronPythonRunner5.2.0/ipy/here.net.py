#! /usr/bin/env python
# -*- coding:utf-8 -*-
import mc
def load_plugin():
    print '[HERE] 装载成功'
    mc.setCommandDescribe('here','回复自己的坐标')
def inputcommand(a):
    d = mc.AnalysisEvent(a)
    if d.cmd == '/here':
        s = {0:"§2主世界",1:"§4下界",2:"§e末地"}
        #mc.tellraw('@a','§6'+str(d['playername']) +' §r位于 '+s[d.dimensionid]+' §r的 '+str(d['XYZ']))
        mc.runcmd('tellraw @a {\"rawtext\":[{\"text\":\"§6'+d.playername+' §r位于 '+str(s[d.dimensionid])+' §r的§3 '+str(int(d.XYZ.x))+','+str(int(d.XYZ.y))+','+str(int(d.XYZ.z))+'\"}]}')
        return False