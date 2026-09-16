import gdsfactory as gf
from components.pring import ring_resonator
from blocks.exspot_array_block import exspot_array
from components.BB_import import PBS, MMI1x2, MMI2x2

@gf.cell
def ring_array():
 comp = gf.Component()
 ec = comp<<exspot_array()
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

 ###############################################################################################################
 r5 = comp<<ring_resonator(R=113, wr = 0.9, wb = 1, g = 0.500)
 r6 = comp<<ring_resonator(R=113, wr = 1.6, wb = 1, g = 0.500)
 r7 = comp<<ring_resonator(R=113, wr = 2.3, wb = 1, g = 0.500)
 r8 = comp<<ring_resonator(R=113, wr = 3, wb = 1, g = 0.500)

 r5.move(origin = r5.ports["o1"].center, destination=(r2.xmax-100,(r2.y-150)))
 r6.move(origin = r6.ports["o1"].center, destination=(r2.xmax+100,(r2.y+50)))
 r7.move(origin = r7.ports["o1"].center, destination=(r2.xmax-100,(r2.y-550)))
 r8.move(origin = r8.ports["o1"].center, destination=(r2.xmax+100,(r2.y-350)))

 ##################################################################################################################
 r9 = comp<<ring_resonator(R=113, wr = 2.3, wb = 1, g = 0.500)
 r10 = comp<<ring_resonator(R=113, wr = 2.3, wb = 1, g = 0.500)
 r11 = comp<<ring_resonator(R=113, wr = 2.3, wb = 1, g = 0.500)
 r12 = comp<<ring_resonator(R=200, wr = 2.3, wb = 1, g = 0.500)

 r9.move(origin = r9.ports["o2"].center, destination=(r1.xmin-150,(r1.y)))
 r10.move(origin = r10.ports["o2"].center, destination=(r1.xmin+50,(r1.y-200)))
 r11.move(origin = r11.ports["o2"].center, destination=(r1.xmin-150,(r1.y-400)))
 r12.move(origin = r12.ports["o2"].center, destination=(r1.xmin+220,(r1.y-650)))
 return comp

