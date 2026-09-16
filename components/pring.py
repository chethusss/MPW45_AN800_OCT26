import gdsfactory as gf
import numpy as np

def merge(list1, list2): 
    return list(zip(list1, list2))

def circ_arc(radius=80,ang1=+20,ang2=-20,npoints=300):
 thet1=(ang1/180)*np.pi
 thet2=(ang2/180)*np.pi
 angs=np.linspace(np.pi/2-thet1,np.pi/2-thet2,npoints)
 X=radius*np.cos(angs)
 Y=radius*np.sin(angs)
 a=[X,Y]
 return a

def bezier(npoints=600,ang=60,height=20,thick=20,wid1=1,wid2=2,s=-1,pref=np.array([[0],[0]]),slp1=0.6,slp2=0.5):
 thet=(np.pi/180)*ang
 t=np.linspace(0,1,npoints)
 wdb=wid2+t*(wid1-wid2)
 p1=np.array([[0],[0]])+pref
 p2=np.array([[s*slp1*thick],[-slp1*thick*np.tan(thet)]])+pref
 p3=np.array([[s*slp2*thick],[-height]])+pref
 p4=np.array([[s*thick],[-height]])+pref
 path=p1*(1-t)**3 + p2*3*t*(1-t)**2 + p3*3*(t**2)*(1-t) + p4*(t**3)
 err= -3*p1*(1-t)**2 + p2*3*(1-t)*(1-3*t) + p3*3*t*(2-3*t) + 3*p4*(t**2)
 dX1=err[0]
 dY1=err[1]
 erX1=-(wdb/2)*dY1/np.sqrt(dX1**2+dY1**2)
 erY1=(wdb/2)*dX1/np.sqrt(dX1**2+dY1**2)
 X=np.concatenate([path[0]-erX1,np.flip(path[0]+erX1)])
 X[npoints-1]=np.round(1000*X[npoints-1])/1000
 X[npoints]=np.round(1000*X[npoints])/1000
 Y=np.concatenate([path[1]-erY1,np.flip(path[1]+erY1)])
 Y[npoints-1]=np.round(1000*Y[npoints-1])/1000
 Y[npoints]=np.round(1000*Y[npoints])/1000
 a=[X,Y]
 return a


@gf.cell
def ring_resonator(
    R=100.0,
    wr=2,
    wb=2.3,
    w0=1,
    g=0.3,
    npoints=400,
    angle=60,
    layer="X1P"
):
    c = gf.Component()

    # Ring
    ring_path = gf.path.arc(
        radius=R,
        angle=360,
    )

    ring = gf.path.extrude(
        ring_path,
        cross_section=gf.cross_section.cross_section(
            width=wr,
            layer=layer,
        ),
    )
    ring.move(origin=(0,0),destination=(0,-R))
    c.add_ref(ring)

    # Bus arc
    ang = angle/2
    wid1 = wb
    wid0 = w0
    R_bus = R + wr / 2 + g + wb / 2
    thet=ang*np.pi/180
    thick=R_bus
    height=thick*np.tan(thet)

    l1=circ_arc(radius=R_bus-wid1/2,ang1=ang,ang2=-ang,npoints=npoints)
    l2=bezier(npoints=2*npoints,ang=ang,height=height,thick=thick,wid1=wid0,
              wid2=wid1,s=-1,pref=np.array([[-R_bus*np.sin(thet)],[R_bus*np.cos(thet)]]),
              slp1=0.4, slp2=0.6)
    l3=circ_arc(radius=R_bus+wid1/2,ang1=-ang,ang2=+ang,npoints=npoints)
    l4=bezier(npoints=2*npoints,ang=ang,height=height,thick=thick,wid1=wid0,
              wid2=wid1,s=+1,pref=np.array([[+R_bus*np.sin(thet)],[R_bus*np.cos(thet)]]),
              slp1=0.4, slp2=0.6)
    X=np.concatenate([l1[0],np.flip(l2[0]),l3[0],np.flip(l4[0])])
    Y=np.concatenate([l1[1],np.flip(l2[1]),l3[1],np.flip(l4[1])])

    coords=merge(X,Y)
    c.add_polygon(coords,layer=layer)
    c.add_port(name = "o1", center=[l2[0][2*npoints],(l2[1][2*npoints-1]+l2[1][2*npoints])/2],cross_section="SM",orientation=180)
    c.add_port(name = "o2", center=[l4[0][2*npoints],(l4[1][2*npoints-1]+l4[1][2*npoints])/2],cross_section="SM",orientation=0)
    return c