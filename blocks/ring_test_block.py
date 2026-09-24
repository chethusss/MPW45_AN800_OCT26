import gdsfactory as gf
from components.pring import ring_resonator
from blocks.exspot_array_block import exspot_array
from components.BB_import import PBS, MMI1x2, MMI2x2, exspot_packaging, MMI4x4
import numpy as np
@gf.cell
def ring_array(num = 12):
 comp = gf.Component()
 ec = comp<<exspot_array(num=num)
 ###########################################################################################################
 #400 um radius rings block - BLOCK A
 r1 = comp<<ring_resonator(R=400, wr = 2.3, wb = 1, g = 0.500)
 r2 = comp<<ring_resonator(R=400, wr = 3, wb = 1, g = 0.500)
 r1pos = 750
 r1.move(origin = r1.ports["o1"].center, destination=(ec.ports["i1"].x+r1pos,ec.ports["i1"].y-300+20))
 r2.move(origin = r2.ports["o1"].center, destination=(ec.ports["i1"].x+r1pos+1150,ec.ports["i1"].y-350+20))

 pbs_a = comp << PBS()
 pbs_a.mirror_y()
 dis1 = 50
 dis2 = 20
 pbs_a.move(pbs_a.ports["o1"].center,(ec.ports["i1"].x+dis1,ec.ports["i1"].y-dis2))


 sbend_a = comp << gf.components.bend_s(
 size=(dis1, dis2),
 cross_section="SM",
 )
 sbend_a.mirror_y()
 sbend_a.connect("o1",ec.ports["i1"])

 MMI_a = comp<<MMI1x2()
 MMI_a.move(origin=MMI_a.ports["o1"].center,destination=(pbs_a.ports["o3"].x+140,pbs_a.ports["o3"].y-100))

  #BLOCK A routing
 gf.routing.route_single(component=comp,port1=pbs_a.ports["o3"],port2=MMI_a.ports["o1"],cross_section="SM",
                         steps=[ {"dx": 60},{"y": MMI_a.ports["o1"].y}])
 gf.routing.route_single(component=comp,port1=ec.ports["i2"],port2=pbs_a.ports["o2"],cross_section="SM")
 gf.routing.route_single(component=comp,port1=MMI_a.ports["o2"],port2=r1.ports["o1"],cross_section="SM",
                         steps=[ {"dx": 70},{"y": r1.ports["o1"].y}])
 gf.routing.route_single(component=comp,port1=MMI_a.ports["o3"],port2=r2.ports["o1"],cross_section="SM",
                         steps=[ {"dx": 50},{"dy": -200},{"dx": 280},{"y": r1.ymin-20},{"x": r2.ports["o1"].x-125},{"y": r2.ports["o1"].y}])
 gf.routing.route_single(component=comp,port1=r1.ports["o2"],port2=ec.ports["o1"],cross_section="SM",
                         steps=[ {"dx": 50},{"y": ec.ports["o1"].y}])
 gf.routing.route_single(component=comp,port1=r2.ports["o2"],port2=ec.ports["o2"],cross_section="SM",
                         steps=[ {"dx": 50},{"y": ec.ports["o2"].y}])

 comp.add_port(name="ref1",port=ec.ports["ref1"])
 ###############################################################################################################
 r3 = comp<<ring_resonator(R=50, wr = 0.9, wb = 1, g = 0.500)
 r4 = comp<<ring_resonator(R=50, wr = 2.3, wb = 1, g = 0.500)
 r3.rotate(90)
 r4.rotate(90)
 r3.move(origin = r3.ports["o1"].center, destination=((r1.x+r2.x)/2-60,(r1.y+r2.y)/2-150))
 r4.move(origin = r4.ports["o1"].center, destination=((r1.x+r2.x)/2+20,(r1.y+r2.y)/2-350))

 pbs_b = comp << PBS()
 pbs_b.mirror_y()
 dis1 = 120
 dis2 = 60
 pbs_b.move(pbs_b.ports["o1"].center,(ec.ports["i3"].x+dis1,ec.ports["i3"].y+dis2))

  #BLOCK B routing
 sbend_b1 = comp << gf.components.bend_s(
 size=(dis1, dis2),
 cross_section="SM",
 )
 sbend_b1.connect("o1",ec.ports["i3"])

 sbend_b2 = comp << gf.components.bend_s(
 size=(200, 50),
 cross_section="SM",
 )
 sbend_b2.connect("o1",ec.ports["i4"])
 gf.routing.route_single(component=comp,port1=pbs_b.ports["o2"],port2=sbend_b2.ports["o2"],cross_section="SM")
 MMI_b = comp<<MMI1x2()
 MMI_b.move(origin=MMI_b.ports["o1"].center,destination=(r3.ports["o1"].x-300,r1.ymin-50))
 gf.routing.route_single(component=comp,port1=pbs_b.ports["o3"],port2=MMI_b.ports["o1"],cross_section="SM",
                         steps=[ {"dx": 250},{"dy": -145},{"dx": 275},{"y": MMI_b.ports["o1"].y }])
 gf.routing.route_single(component=comp,port1=MMI_b.ports["o2"],port2=r3.ports["o1"],cross_section="SM")
 gf.routing.route_single(component=comp,port1=MMI_b.ports["o3"],port2=r4.ports["o1"],cross_section="SM")
 gf.routing.route_single(component=comp,port1=r3.ports["o2"],port2=ec.ports["o3"],cross_section="SM",
                         steps=[{"dy": 50},{"x": r2.x-400-20},{"y": r2.ymin-10},{"x": r2.x+400+20},{"y": r2.ports["o2"].y-40 }, {"x": r2.ports["o2"].x+60 }, {"y": ec.ports["o3"].y }])
 sbend_b3 = comp << gf.components.bend_s(
 size=(400, 117),
 cross_section="SM",
 )
 sbend_b3.mirror_y()
 sbend_b3.connect("o2",ec.ports["o4"])
 gf.routing.route_single(component=comp,port1=r4.ports["o2"],port2=sbend_b3.ports["o1"],cross_section="SM",
                         steps=[ {"dy": 50},{"x": r2.x-400-30},{"y": r2.ymin-20},{"x": r2.x+400+30},{"y": r2.ports["o2"].y-50 },  {"x": r2.ports["o2"].x+70 }, {"y": sbend_b3.ports["o1"].y }])

 ###############################################################################################################
 r5 = comp<<ring_resonator(R=113, wr = 0.9, wb = 1, g = 0.500)
 r6 = comp<<ring_resonator(R=113, wr = 1.6, wb = 1, g = 0.500)
 r7 = comp<<ring_resonator(R=113, wr = 2.3, wb = 1, g = 0.500)
 r8 = comp<<ring_resonator(R=113, wr = 3, wb = 1, g = 0.500)

 r5.move(origin = r5.ports["o1"].center, destination=(r2.xmax-100,(r2.y-250)))
 r6.move(origin = r6.ports["o1"].center, destination=(r2.xmax+100,(r2.y-50)))
 r7.move(origin = r7.ports["o1"].center, destination=(r2.xmax-100,(r2.y-650)))
 r8.move(origin = r8.ports["o1"].center, destination=(r2.xmax+100,(r2.y-450)))
 #BLOCK C routing
 pbs_c = comp << PBS()
 pbs_c.mirror_y()
 pbs_c.move(pbs_c.ports["o1"].center,(r1.x-400+20,r1.ymin-20-90))
 gf.routing.route_single(component=comp,port1=ec.ports["i5"],port2=pbs_c.ports["o1"],cross_section="SM",
                         steps=[ {"dx": 80},{"dy": 125},{"x": r1.x-400-70},{"y": pbs_c.ports["o1"].y}])
 gf.routing.route_single(component=comp,port1=ec.ports["i6"],port2=pbs_c.ports["o2"],cross_section="SM",
                         steps=[ {"dx": 90},{"dy": 115+127},{"x": r1.x-400-80},{"y": pbs_c.ports["o2"].y-100},{"x": pbs_c.ports["o2"].x+50},{"y": pbs_c.ports["o2"].y}])

 mmi_c = comp << MMI4x4()
 mmi_c.move(mmi_c.ports["o1"].center,(r2.x+400-mmi_c.xsize-10,r1.ymin-150))
 gf.routing.route_single(component=comp,port1=mmi_c.ports["o8"],port2=r6.ports["o1"],cross_section="SM")
 gf.routing.route_single(component=comp,port1=mmi_c.ports["o7"],port2=r5.ports["o1"],cross_section="SM", steps=[ {"dx": 60},{"y": r5.ports["o1"].y}])
 sbend_c1 = comp<<gf.components.bend_s(
    (r8.ports["o1"].x-mmi_c.ports["o6"].x,r8.ports["o1"].y-mmi_c.ports["o6"].y),
    cross_section="SM")
 sbend_c1.connect("o1",mmi_c.ports["o6"])
 gf.routing.route_single(component=comp,port1=pbs_c.ports["o3"],port2=mmi_c.ports["o3"],cross_section="SM",steps=[ {"dx": 60},{"dy": -150},{"dx": 100},{"y": mmi_c.ports["o3"].y}])
 gf.routing.route_single(component=comp,port1=mmi_c.ports["o5"],port2=r7.ports["o1"],cross_section="SM")
 sbend_c2 = comp.add_ref(gf.components.bend_s((ec.ports["o5"].x-r6.ports["o2"].x,ec.ports["o5"].y-r6.ports["o2"].y),cross_section="SM"))
 sbend_c2.connect("o1",r6.ports["o2"])
 sbend_c3 = comp.add_ref(gf.components.bend_s((ec.ports["o6"].x-r5.ports["o2"].x,ec.ports["o6"].y-r5.ports["o2"].y),cross_section="SM"))
 sbend_c3.connect("o1",r5.ports["o2"])
 gf.routing.route_single(component=comp,port1=r8.ports["o2"],port2=ec.ports["o7"],cross_section="SM")
 gf.routing.route_single(component=comp,port1=r7.ports["o2"],port2=ec.ports["o8"],cross_section="SM", steps=[ {"x": r8.x+113+20},{"y": ec.ports["o8"].y-100},{"x": r8.ports["o2"].x+60},{"y": ec.ports["o8"].y}])


 ##################################################################################################################
 r9 = comp<<ring_resonator(R=113, wr = 2.3, wb = 1, g = 0.400)
 r10 = comp<<ring_resonator(R=113, wr = 2.3, wb = 1, g = 0.450)
 r11 = comp<<ring_resonator(R=113, wr = 2.3, wb = 1, g = 0.550)
 r12 = comp<<ring_resonator(R=200, wr = 2.3, wb = 1, g = 0.500)

 pbs_d = comp << PBS()
 pbs_d.mirror_y().mirror_x()
 pbs_d.move(pbs_d.ports["o1"].center,(r2.x+400-100,r2.ymin-300))

 mmi_d = comp << MMI4x4()
 mmi_d.mirror_x()
 mmi_d.move(mmi_d.ports["o1"].center,(r1.x-400+mmi_d.xsize+200,r1.ymin-300))

 gf.routing.route_single(component=comp,port1=pbs_d.ports["o1"],port2=ec.ports["o9"],cross_section="SM",steps=[ {"x": r7.x-113-20},{"y": r7.ymin-20},{"x": r7.x+113+20},{"y": r7.y+10}
                                                                                                               ,{"x": r8.xmax+70},{"y": ec.ports["o9"].y}])
 gf.routing.route_single(component=comp,port1=pbs_d.ports["o2"],port2=ec.ports["o10"],cross_section="SM",steps=[ {"dx": -50},{"y": r7.ymin-30},{"x": r7.x+113+30},{"y": ec.ports["o10"].y}])
 gf.routing.route_single(component=comp,port1=pbs_d.ports["o3"],port2=mmi_d.ports["o3"],cross_section="SM",steps=[ {"dx": -60},{"dy": -100},{"dx": -100},{"y": mmi_d.ports["o3"].y}])
 r9.move(origin = r9.ports["o2"].center, destination=(r1.xmin-200,(r1.y-150)))
 r10.move(origin = r10.ports["o2"].center, destination=(r1.xmin,(r1.y-350)))
 r11.move(origin = r11.ports["o2"].center, destination=(r1.xmin-200,(r1.y-550)))
 r12.move(origin = r12.ports["o2"].center, destination=(r1.xmin+170,(r1.y-800)))
 gf.routing.route_single(component=comp,port1=ec.ports["i7"],port2=r9.ports["o1"],cross_section="SM",steps=[ {"dx": 100},{"y": r9.ports["o1"].y}])
 gf.routing.route_single(component=comp,port1=r9.ports["o2"],port2=mmi_d.ports["o8"],cross_section="SM",steps=[{"x": r1.x-400-100},{"y": mmi_d.ports["o8"].y}])
 gf.routing.route_single(component=comp,port1=ec.ports["i8"],port2=r10.ports["o1"],cross_section="SM",steps=[ {"dx": 110},{"y": r10.ports["o1"].y}])
 gf.routing.route_single(component=comp,port1=r10.ports["o2"],port2=mmi_d.ports["o7"],cross_section="SM",steps=[{"x": r1.x-400-120},{"y": mmi_d.ports["o7"].y}])
 sbend_d1 = comp.add_ref(gf.components.bend_s((r11.ports["o1"].x-ec.ports["i9"].x,r11.ports["o1"].y-ec.ports["i9"].y),cross_section="SM"))
 sbend_d1.connect("o1",ec.ports["i9"])
 gf.routing.route_single(component=comp,port1=r11.ports["o2"],port2=mmi_d.ports["o6"],cross_section="SM",steps=[{"x": r1.x-400-130},{"y": mmi_d.ports["o6"].y}])
 sbend_d2 = comp.add_ref(gf.components.bend_s((mmi_d.ports["o5"].x-r12.ports["o2"].x,mmi_d.ports["o5"].y-r12.ports["o2"].y),cross_section="SM"))
 sbend_d2.connect("o1",r12.ports["o2"])
 sbend_d3 = comp.add_ref(gf.components.bend_s((r12.ports["o1"].x-ec.ports["i10"].x,r12.ports["o2"].y-ec.ports["i10"].y),cross_section="SM"))
 sbend_d3.connect("o1",ec.ports["i10"])

###########################################################################################################################################################
 r13 = comp<<ring_resonator(R=113, wr = 2.3, wb = 1, g = 0.400, angle=0)
 r14 = comp<<ring_resonator(R=113, wr = 2.3, wb = 1, g = 0.45, angle=0)
 r15 = comp<<ring_resonator(R=113, wr = 2.3, wb = 1, g = 0.5, angle=0)
 r16 = comp<<ring_resonator(R=113, wr = 2.3, wb = 1, g = 0.55, angle=0)

 ecx1 = comp<<exspot_packaging()
 ecx2 = comp<<exspot_packaging()
 ecx1.mirror_x()
 ecx2.mirror_x()
 ecx1.move(origin = ecx1.ports["o1"].center,destination=(ec.ports[f"{"i"}{num}"].x,ec.ports[f"{"i"}{num}"].y-127))
 ecx2.move(origin = ecx2.ports["o1"].center,destination=(ec.ports[f"{"i"}{num}"].x,ec.ports[f"{"i"}{num}"].y-2*127))

 spacing = 400
 pbs_e = comp << PBS()
 pbs_e.mirror_x()
 pbs_e.move(origin=pbs_e.ports["o1"].center, destination = (ec.ports["o12"].x-10,ec.ports["o12"].y))

 mmi_e = comp << MMI4x4()
 mmi_e.mirror_x()
 mmi_e.move(mmi_e.ports["o1"].center,(pbs_e.ports["o3"].x-200,pbs_e.ports["o3"].y))


 r13.move(origin = r13.ports["o2"].center, destination=(ec.ports["i12"].x+2500,(mmi_e.ports["o5"].y)))
 r14.move(origin = r14.ports["o2"].center, destination=(ec.ports["i12"].x+2500 - spacing*1 ,(mmi_e.ports["o6"].y)))
 r15.move(origin = r15.ports["o2"].center, destination=(ec.ports["i12"].x+2500 - spacing*2,(mmi_e.ports["o7"].y)))
 r16.move(origin = r16.ports["o2"].center, destination=(ec.ports["i12"].x+2500 - spacing*3,(mmi_e.ports["o8"].y)))

 gf.routing.route_single(component=comp,port1=ec.ports["o12"],port2=pbs_e.ports["o1"],cross_section="SM")
 gf.routing.route_single(component=comp,port1=ec.ports["o11"],port2=pbs_e.ports["o2"],cross_section="SM")
 gf.routing.route_single(component=comp,port1=pbs_e.ports["o3"],port2=mmi_e.ports["o1"],cross_section="SM")
 gf.routing.route_single(component=comp,port1=mmi_e.ports["o5"],port2=r13.ports["o2"],cross_section="SM")
 gf.routing.route_single(component=comp,port1=mmi_e.ports["o6"],port2=r14.ports["o2"],cross_section="SM")
 gf.routing.route_single(component=comp,port1=mmi_e.ports["o7"],port2=r15.ports["o2"],cross_section="SM")
 gf.routing.route_single(component=comp,port1=mmi_e.ports["o8"],port2=r16.ports["o2"],cross_section="SM")

 offset = 300
 spacing = 20
 gf.routing.route_single(component=comp,port1=r16.ports["o1"],port2=ec.ports["i11"],cross_section="SM",steps=[ {"dx": -50},{"y": ecx2.ports["o1"].y+3*spacing},{"x": ec.ports["i11"].x+offset},{"y": ec.ports["i11"].y}])
 gf.routing.route_single(component=comp,port1=r15.ports["o1"],port2=ec.ports["i12"],cross_section="SM",steps=[ {"dx": -50},{"y": ecx2.ports["o1"].y+2*spacing},{"x": ec.ports["i12"].x+offset-spacing*1},{"y": ec.ports["i12"].y}])
 gf.routing.route_single(component=comp,port1=r14.ports["o1"],port2=ecx1.ports["o1"],cross_section="SM",steps=[ {"dx": -50},{"y": ecx2.ports["o1"].y+1*spacing},{"x": ecx1.ports["o1"].x+offset-spacing*2},{"y": ecx1.ports["o1"].y}])
 gf.routing.route_single(component=comp,port1=r13.ports["o1"],port2=ecx2.ports["o1"],cross_section="SM",steps=[ {"dx": -50},{"y": ecx2.ports["o1"].y+0*spacing}])
 ##################################################################################################################


 return comp

