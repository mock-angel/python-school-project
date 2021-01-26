# block/core.py
import periodictable.core
def init(table, reload=False):
    if 'block' in table.properties and not reload: return
    table.properties.append('block')
    
    # Set the default, if any
    
    periodictable.core.Element.block = None
    
    for name,block in data.items():
        el = table.symbol(name)
        el.block = block
            
data = dict(

    H = "s-block",
    He = "s-block",
    Li = "s-block",
    Be = "s-block",
    B = "p-block",
    
    C = "p-block",
    N = "p-block",
    O = "p-block",
    
    F = "p-block",
    Ne = "p-block",
    Na = "s-block",
    Mg = "s-block",
    Al = "p-block",
    
    Si = "p-block",
    P = "p-block",
    S = "p-block",
    
    Cl = "p-block",
    Ar = "p-block",
    K = "s-block",
    Ca = "s-block",
    Sc = "d-block",
    Ti = "d-block",
    V = "d-block",
    Cr = "d-block",
    Mn = "d-block",
    Fe = "d-block",
    Co = "d-block",
    Ni = "d-block",
    Cu = "d-block",
    Zn = "d-block",
    Ga = "p-block",
    
    Ge = "p-block",
    As = "p-block",
    Se = "p-block",
    
    Br = "p-block",
    Kr = "p-block",
    Rb = "s-block",
    Sr = "s-block",
    Y = "d-block",
    Zr = "d-block",
    Nb = "d-block",
    Mo = "d-block",
    Tc = "d-block",
    Ru = "d-block",
    Rh = "d-block",
    Pd = "d-block",
    Ag = "d-block",
    Cd = "d-block",
    In = "p-block",
    
    Sn = "p-block",
    Sb = "p-block",
    Te = "p-block",
    
    I = "p-block",
    Xe = "p-block",
    Cs = "s-block",
    Ba = "s-block",
    La = "f-block",
    Ce = "f-block",
    Pr = "f-block",
    Nd = "f-block",
    Pm = "f-block",
    Sm = "f-block",
    Eu = "f-block",
    Gd = "f-block",
    Tb = "f-block",
    Dy = "f-block",
    Ho = "f-block",
    Er = "f-block",
    Tm = "f-block",
    Yb = "f-block",
    Lu = "f-block",
    Hf = "d-block",
    Ta = "d-block",
    W = "d-block",
    Re = "d-block",
    Os = "d-block",
    Ir = "d-block",
    Pt = "d-block",
    Au = "d-block",
    Hg = "d-block",
    Tl = "p-block",
    
    Pb = "p-block",
    Bi = "p-block",
    Po = "p-block",
    
    At = "p-block",
    Rn = "p-block",
    Fr = "s-block",
    Ra = "s-block",
    Ac = "f-block",
    Th = "f-block",
    Pa = "f-block",
    U = "f-block",
    Np = "f-block",
    Pu = "f-block",
    Am = "f-block",
    Cm = "f-block",
    Bk = "f-block",
    Cf = "f-block",
    Es = "f-block",
    Fm = "f-block",
    Md = "f-block",
    No = "f-block",
    Lr = "f-block",
    Rf = "d-block",
    Db = "d-block",
    Sg = "d-block",
    Bh = "d-block",
    Hs = "d-block",
    Mt = "d-block",
    Ds = "d-block",
    Rg = "d-block",
    Cn = "d-block",
    Nh = "p-block",
    Fl = "p-block",
    Mc = "p-block",
    Lv = "p-block",
    Ts = "p-block",
    Og = "p-block",
)

init(periodictable.elements)

