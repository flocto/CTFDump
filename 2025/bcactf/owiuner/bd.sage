from sage.all import *
# Original: https://github.com/mimoo/RSA-and-LLL-attacks/blob/master/boneh_durfee.sage

dimension_min = 7

def remove_unhelpful(BB, monomials, bound, current):
  if current == -1 or BB.dimensions()[0] <= dimension_min:
    return BB
  for ii in range(current, -1, -1):
    if BB[ii, ii] >= bound:
      affected_vectors = 0
      affected_vector_index = 0
      for jj in range(ii + 1, BB.dimensions()[0]):
        if BB[jj, ii] != 0:
          affected_vectors += 1
          affected_vector_index = jj
      if affected_vectors == 0:
        #print( "* removing unhelpful vector", ii)
        BB = BB.delete_columns([ii])
        BB = BB.delete_rows([ii])
        monomials.pop(ii)
        BB = remove_unhelpful(BB, monomials, bound, ii-1)
        return BB
      elif affected_vectors == 1:
        affected_deeper = True
        for kk in range(affected_vector_index + 1, BB.dimensions()[0]):
          if BB[kk, affected_vector_index] != 0:
            affected_deeper = False
        if affected_deeper and abs(bound - BB[affected_vector_index, affected_vector_index]) < abs(bound - BB[ii, ii]):
          #print( "* removing unhelpful vectors", ii, "and", affected_vector_index)
          BB = BB.delete_columns([affected_vector_index, ii])
          BB = BB.delete_rows([affected_vector_index, ii])
          monomials.pop(affected_vector_index)
          monomials.pop(ii)
          BB = remove_unhelpful(BB, monomials, bound, ii-1)
          return BB
  return BB

def boneh_durfee_small_roots(pol, modulus, mm, tt, XX, YY):
    PR.<u, x, y> = PolynomialRing(ZZ)
    Q = PR.quotient(x*y + 1 - u) # u = xy + 1
    polZ = Q(pol).lift()
    UU = XX*YY + 1
    gg = []
    for kk in range(mm + 1):
      for ii in range(mm - kk + 1):
        xshift = x^ii * modulus^(mm - kk) * polZ(u, x, y)^kk
        gg.append(xshift)
    gg.sort()
    monomials = []
    for polynomial in gg:
      for monomial in polynomial.monomials():
        if monomial not in monomials:
          monomials.append(monomial)
    monomials.sort()
    for jj in range(1, tt + 1):
      for kk in range(floor(mm/tt) * jj, mm + 1):
        yshift = y^jj * polZ(u, x, y)^kk * modulus^(mm - kk)
        yshift = Q(yshift).lift()
        gg.append(yshift)
        monomials.append(u^kk * y^jj)
    nn = len(monomials)
    BB = Matrix(ZZ, nn)
    for ii in range(nn):
      BB[ii, 0] = gg[ii](0, 0, 0)
      for jj in range(1, ii + 1):
        if monomials[jj] in gg[ii].monomials():
          BB[ii, jj] = gg[ii].monomial_coefficient(monomials[jj]) * monomials[jj](UU,XX,YY)
    BB = remove_unhelpful(BB, monomials, modulus^mm, nn-1)
    nn = BB.dimensions()[0]
    if nn == 0:
      print( "failure")
      return 0,0
    BB = BB.LLL()
    PR.<w,z> = PolynomialRing(ZZ)
    pol1 = pol2 = 0
    for jj in range(nn):
      pol1 += monomials[jj](w*z+1,w,z) * BB[0, jj] / monomials[jj](UU,XX,YY)
      pol2 += monomials[jj](w*z+1,w,z) * BB[1, jj] / monomials[jj](UU,XX,YY)
    PR.<q> = PolynomialRing(ZZ)
    rr = pol1.resultant(pol2)
    if rr.is_zero() or rr.monomials() == [1]:
      print( "the two first vectors are not independant")
      return 0, 0
    rr = rr(q, q)
    soly = rr.roots()
    if len(soly) == 0:
      print( "Your prediction (delta) is too small")
      return 0, 0
    soly = soly[0][0]
    ss = pol1(q, soly)
    solx = ss.roots()[0][0]
    return solx, soly

def boneh_durfee(n, e):
  delta = RR(0.167) # d ~ n^0.167
  m = 5
  t = round((1-2*delta) * m)
  X = ZZ(2*floor(n^delta))
  # we have n = p^2q. so `phi(n) = n + {-(pq+pr+qr) + p+q+r)} - 1`.
  # we reconsidered boneh-durfee's attack then we have `x(A+y) + 1 = 0 mod e` where `A = (n-1)`
  # and (x, y) = (k, -(pq+pr+qr)+p+q+r). 
  Y = ZZ(floor(n^(2/3)))
  P.<x,y> = PolynomialRing(ZZ)
  A = ZZ((n-1)/2)
  pol = 1 + x * (A + y)
  solx, soly = boneh_durfee_small_roots(pol, e, m, t, X, Y)
  print( solx, soly)
  if solx > 0:
    return int(pol(solx, soly) / e)
  return 0

if __name__ == "__main__":
  N = 3142349849449222750197052776929440013148857070528019210940456302479778678377349221584305162900604179911170769605069112228661293689628798943752570668861571068370627895414215745934141568783366676577579694116896916592106172835563014721257927354554808271620276995876625139065060816229893239617933923156203739805679179566345893480110255015050793281719874347689696637016196087752107854121307424464809067709547299049058279638185061382180884911772431967390831248346428244837807805068895517131666882598514171040165192668331369711579630965507768056880328273522003332433801987301518965550233528877714754322637238086401755369743
  e = 1007923536615788429308488626562273211764727739603326916716750134757664859102073538280046418621787956357694898611090496120711455465224553954057342423556585864474681775436484905703166080638087909964613464766175288771778765019262046300385293725834520490146106084530018338265651235516001622215244910020449661899742921948751900636529806699757780399920028084163545701117923463204472171540818124208844178088280319819213976811837266042606657104570279825807114809806757441716609936054298761798056420164827224473480042981060226017719191829286695719239693689441374116653221590962307342429813079248395613750792817430371356594717
  print( boneh_durfee(N, e))