from sympy import (Symbol, symbols, hypersimp, factorial, binomial,
    collect, Function, powsimp, separate, sin, exp, Rational, fraction,
    simplify, trigsimp, cos, tan, cot, log, ratsimp, Matrix, pi, integrate,
    solve, nsimplify, GoldenRatio, sqrt, E, I, sympify, atan, Derivative,
    S, diff, oo, Eq, Integer, gamma, acos, Integral, logcombine, Wild,
    separatevars, erf, rcollect, count_ops, combsimp, posify, expand,
    factor, Mul, O, hyper, Add, Float, radsimp, collect_const)
from sympy.core.mul import _keep_coeff
from sympy.simplify.simplify import fraction_expand
from sympy.utilities.pytest import XFAIL

from sympy.abc import x, y, z, t, a, b, c, d, e

def test_ratsimp():
    f, g = 1/x + 1/y, (x + y)/(x*y)

    assert f != g and ratsimp(f) == g

    f, g = 1/(1 + 1/x), 1 - 1/(x + 1)

    assert f != g and ratsimp(f) == g

    f, g = x/(x + y) + y/(x + y), 1

    assert f != g and ratsimp(f) == g

    f, g = -x - y - y**2/(x + y) + x**2/(x + y), -2*y

    assert f != g and ratsimp(f) == g

    f = (a*c*x*y + a*c*z - b*d*x*y - b*d*z - b*t*x*y - b*t*x - b*t*z + e*x)/(x*y + z)
    G = [a*c - b*d - b*t + (-b*t*x + e*x)/(x*y + z),
         a*c - b*d - b*t - ( b*t*x - e*x)/(x*y + z)]

    assert f != g and ratsimp(f) in G

    A = sqrt(pi)

    B = log(erf(x) - 1)
    C = log(erf(x) + 1)

    D = 8 - 8*erf(x)

    f = A*B/D - A*C/D + A*C*erf(x)/D - A*B*erf(x)/D + 2*A/D

    assert ratsimp(f) == A*B/8 - A*C/8 - A/(4*erf(x) - 4)

def test_trigsimp1():
    x, y = symbols('x,y')

    assert trigsimp(1 - sin(x)**2) == cos(x)**2
    assert trigsimp(1 - cos(x)**2) == sin(x)**2
    assert trigsimp(sin(x)**2 + cos(x)**2) == 1
    assert trigsimp(1 + tan(x)**2) == 1/cos(x)**2
    assert trigsimp(1/cos(x)**2 - 1) == tan(x)**2
    assert trigsimp(1/cos(x)**2 - tan(x)**2) == 1
    assert trigsimp(1 + cot(x)**2) == 1/sin(x)**2
    assert trigsimp(1/sin(x)**2 - 1) == cot(x)**2
    assert trigsimp(1/sin(x)**2 - cot(x)**2) == 1

    assert trigsimp(5*cos(x)**2 + 5*sin(x)**2) == 5
    assert trigsimp(5*cos(x/2)**2 + 2*sin(x/2)**2) in \
                [2 + 3*cos(x/2)**2, 5 - 3*sin(x/2)**2]

    assert trigsimp(sin(x)/cos(x)) == tan(x)
    assert trigsimp(2*tan(x)*cos(x)) == 2*sin(x)
    assert trigsimp(cot(x)**3*sin(x)**3) == cos(x)**3
    assert trigsimp(y*tan(x)**2/sin(x)**2) == y/cos(x)**2
    assert trigsimp(cot(x)/cos(x)) == 1/sin(x)

    assert trigsimp(cos(0.12345)**2 + sin(0.12345)**2) == 1
    e = 2*sin(x)**2 + 2*cos(x)**2
    assert trigsimp(log(e), deep=True) == log(2)

def test_trigsimp2():
    x, y = symbols('x,y')
    assert trigsimp(cos(x)**2*sin(y)**2 + cos(x)**2*cos(y)**2 + sin(x)**2,
            recursive=True) == 1
    assert trigsimp(sin(x)**2*sin(y)**2 + sin(x)**2*cos(y)**2 + cos(x)**2,
            recursive=True) == 1

def test_issue1274():
    x = Symbol("x")
    assert abs(trigsimp(2.0*sin(x)**2+2.0*cos(x)**2)-2.0) < 1e-10

def test_trigsimp3():
    x, y = symbols('x,y')
    assert trigsimp(sin(x)/cos(x)) == tan(x)
    assert trigsimp(sin(x)**2/cos(x)**2) == tan(x)**2
    assert trigsimp(sin(x)**3/cos(x)**3) == tan(x)**3
    assert trigsimp(sin(x)**10/cos(x)**10) == tan(x)**10

    assert trigsimp(cos(x)/sin(x)) == 1/tan(x)
    assert trigsimp(cos(x)**2/sin(x)**2) == 1/tan(x)**2
    assert trigsimp(cos(x)**10/sin(x)**10) == 1/tan(x)**10

    assert trigsimp(tan(x)) == trigsimp(sin(x)/cos(x))

def test_trigsimp_issue_2515():
    x = Symbol('x')
    assert trigsimp(x*cos(x)*tan(x)) == x*sin(x)
    assert trigsimp(-sin(x)+cos(x)*tan(x)) == 0

@XFAIL
def test_factorial_simplify():
    # There are more tests in test_factorials.py. These are just to
    # ensure that simplify() calls factorial_simplify correctly
    from sympy.specfun.factorials import factorial
    x = Symbol('x')
    assert simplify(factorial(x)/x) == factorial(x-1)
    assert simplify(factorial(factorial(x))) == factorial(factorial(x))

def test_simplify():
    x, y, z, k, n, m, w, f, s, A = symbols('x,y,z,k,n,m,w,f,s,A')

    assert all(simplify(tmp) == tmp for tmp in [I, E, oo, x, -x, -oo, -E, -I])

    e = 1/x + 1/y
    assert e != (x+y)/(x*y)
    assert simplify(e) == (x+y)/(x*y)

    e = A**2*s**4/(4*pi*k*m**3)
    assert simplify(e) == e

    e = (4+4*x-2*(2+2*x))/(2+2*x)
    assert simplify(e) == 0

    e = (-4*x*y**2-2*y**3-2*x**2*y)/(x+y)**2
    assert simplify(e) == -2*y

    e = -x-y-(x+y)**(-1)*y**2+(x+y)**(-1)*x**2
    assert simplify(e) == -2*y

    e = (x+x*y)/x
    assert simplify(e) == 1 + y

    e = (f(x)+y*f(x))/f(x)
    assert simplify(e) == 1 + y

    e = (2 * (1/n - cos(n * pi)/n))/pi
    assert simplify(e) == 2*((1 - 1*cos(pi*n))/(pi*n))

    e = integrate(1/(x**3+1), x).diff(x)
    assert simplify(e) == 1/(x**3+1)

    e = integrate(x/(x**2+3*x+1), x).diff(x)
    assert simplify(e) == x/(x**2+3*x+1)

    A = Matrix([[2*k-m*w**2, -k], [-k, k-m*w**2]]).inv()

    assert simplify((A*Matrix([0,f]))[1]) == \
        f/(-k**2/(2*k - m*w**2) + k - m*w**2)

    a, b, c, d, e, f, g, h, i = symbols('a,b,c,d,e,f,g,h,i')

    f_1 = x*a + y*b + z*c - 1
    f_2 = x*d + y*e + z*f - 1
    f_3 = x*g + y*h + z*i - 1

    solutions = solve([f_1, f_2, f_3], x, y, z, simplified=False)

    assert simplify(solutions[y]) == \
        (a*i+c*d+f*g-a*f-c*g-d*i)/(a*e*i+b*f*g+c*d*h-a*f*h-b*d*i-c*e*g)

    f = -x + y/(z + t) + z*x/(z + t) + z*a/(z + t) + t*x/(z + t)

    assert simplify(f) == (y + a*z)/(z + t)

    A, B = symbols('A,B', commutative=False)

    assert simplify(A*B - B*A) == A*B - B*A

    assert simplify(log(2) + log(3)) == log(6)
    assert simplify(log(2*x) - log(2)) == log(x)

def test_simplify_other():
    assert simplify(sin(x)**2 + cos(x)**2) == 1
    assert simplify(gamma(x + 1)/gamma(x)) == x
    assert simplify(sin(x)**2 + cos(x)**2 + factorial(x)/gamma(x)) == 1 + x
    assert simplify(Eq(sin(x)**2 + cos(x)**2, factorial(x)/gamma(x))) == Eq(1, x)
    nc = symbols('nc', commutative=False)
    assert simplify(x + x*nc) == x*(1 + nc)

def test_simplify_ratio():
    # roots of x**3-3*x+5
    roots = ['(1/2 - sqrt(3)*I/2)*(sqrt(21)/2 + 5/2)**(1/3) + 1/((1/2 - '
             'sqrt(3)*I/2)*(sqrt(21)/2 + 5/2)**(1/3))',
             '1/((1/2 + sqrt(3)*I/2)*(sqrt(21)/2 + 5/2)**(1/3)) + '
             '(1/2 + sqrt(3)*I/2)*(sqrt(21)/2 + 5/2)**(1/3)',
             '-(sqrt(21)/2 + 5/2)**(1/3) - 1/(sqrt(21)/2 + 5/2)**(1/3)']

    for r in roots:
        r = S(r)
        assert count_ops(simplify(r, ratio=1)) <= count_ops(r)
        # If ratio=oo, simplify() is always applied:
        assert simplify(r, ratio=oo) is not r

def test_simplify_measure():
    measure1 = lambda expr: len(str(expr))
    measure2 = lambda expr: -count_ops(expr) # Return the most complicated result
    expr = (x + 1)/(x + sin(x)**2 + cos(x)**2)
    assert measure1(simplify(expr, measure=measure1)) <= measure1(expr)
    assert measure2(simplify(expr, measure=measure2)) <= measure2(expr)

def test_simplify_issue_1308():
    assert simplify(exp(-Rational(1, 2)) + exp(-Rational(3, 2))) == \
        (1 + E)*exp(-Rational(3, 2))

def test_issue_2553():
    assert simplify(E + exp(-E)) == E + exp(-E)
    n = symbols('n', commutative=False)
    assert simplify(n + n**(-n)) == n + n**(-n)

def test_simplify_fail1():
    x = Symbol('x')
    y = Symbol('y')
    e = (x+y)**2/(-4*x*y**2-2*y**3-2*x**2*y)
    assert simplify(e) == 1 / (-2*y)

def test_fraction():
    x, y, z = map(Symbol, 'xyz')
    A = Symbol('A', commutative=False)

    assert fraction(Rational(1, 2)) == (1, 2)

    assert fraction(x) == (x, 1)
    assert fraction(1/x) == (1, x)
    assert fraction(x/y) == (x, y)
    assert fraction(x/2) == (x, 2)

    assert fraction(x*y/z) == (x*y, z)
    assert fraction(x/(y*z)) == (x, y*z)

    assert fraction(1/y**2) == (1, y**2)
    assert fraction(x/y**2) == (x, y**2)

    assert fraction((x**2+1)/y) == (x**2+1, y)
    assert fraction(x*(y+1)/y**7) == (x*(y+1), y**7)

    assert fraction(exp(-x), exact=True) == (exp(-x), 1)

    assert fraction(x*A/y) == (x*A, y)
    assert fraction(x*A**-1/y) == (x*A**-1, y)

def test_separate():
    x, y, z = symbols('x,y,z')

    assert separate((x*y*z)**4) == x**4*y**4*z**4
    assert separate((x*y*z)**x).is_Pow
    assert separate((x*y*z)**x, force=True) == x**x*y**x*z**x
    assert separate((x*(y*z)**2)**3) == x**3*y**6*z**6

    assert separate((sin((x*y)**2)*y)**z).is_Pow
    assert separate((sin((x*y)**2)*y)**z, force=True) == sin((x*y)**2)**z*y**z
    assert separate((sin((x*y)**2)*y)**z, deep=True) == (sin(x**2*y**2)*y)**z

    assert separate(exp(x)**2) == exp(2*x)
    assert separate((exp(x)*exp(y))**2) == exp(2*x)*exp(2*y)

    assert separate((exp((x*y)**z)*exp(y))**2) == exp(2*(x*y)**z)*exp(2*y)
    assert separate((exp((x*y)**z)*exp(y))**2, deep=True, force=True) == exp(2*x**z*y**z)*exp(2*y)

    assert separate((exp(x)*exp(y))**z).is_Pow
    assert separate((exp(x)*exp(y))**z, force=True) == exp(x*z)*exp(y*z)

def test_powsimp():
    x, y, z, n = symbols('x,y,z,n')
    f = Function('f')
    assert powsimp( 4**x * 2**(-x) * 2**(-x) ) == 1
    assert powsimp( (-4)**x * (-2)**(-x) * 2**(-x) ) == 1

    assert powsimp( f(4**x * 2**(-x) * 2**(-x)) )   == f(4**x * 2**(-x) * 2**(-x))
    assert powsimp( f(4**x * 2**(-x) * 2**(-x)), deep = True )  == f(1)
    assert exp(x)*exp(y) == exp(x)*exp(y)
    assert powsimp(exp(x)*exp(y)) == exp(x+y)
    assert powsimp(exp(x)*exp(y)*2**x*2**y) == (2*E)**(x + y)
    assert powsimp(exp(x)*exp(y)*2**x*2**y, combine='exp') == exp(x+y)*2**(x+y)
    assert powsimp(exp(x)*exp(y)*exp(2)*sin(x)+sin(y)+2**x*2**y) == exp(2+x+y)*sin(x)+sin(y)+2**(x+y)
    assert powsimp(sin(exp(x)*exp(y))) == sin(exp(x)*exp(y))
    assert powsimp(sin(exp(x)*exp(y)), deep=True) == sin(exp(x+y))
    assert powsimp(x**2*x**y) == x**(2+y)
    # This should remain factored, because 'exp' with deep=True is supposed
    # to act like old automatic exponent combining.
    assert powsimp((1 + E*exp(E))*exp(-E), combine='exp', deep=True) == (1 + exp(1 + E))*exp(-E)
    assert powsimp((1 + E*exp(E))*exp(-E), deep=True) == exp(1) + exp(-E)
    # This should not change without deep.  Otherwise, simplify() will fail.
    assert powsimp((1 + E*exp(E))*exp(-E)) == (1 + E*exp(E))*exp(-E)
    assert powsimp((1 + E*exp(E))*exp(-E), combine='exp') == (1 + E*exp(E))*exp(-E)
    assert powsimp((1 + E*exp(E))*exp(-E), combine='base') == (1 + E*exp(E))*exp(-E)
    x,y = symbols('x,y', nonnegative=True)
    n = Symbol('n', real=True)
    assert powsimp( y**n * (y/x)**(-n) ) == x**n
    assert powsimp(x**(x**(x*y)*y**(x*y))*y**(x**(x*y)*y**(x*y)),deep=True) == (x*y)**(x*y)**(x*y)
    assert powsimp(2**(2**(2*x)*x), deep=False) == 2**(2**(2*x)*x)
    assert powsimp(2**(2**(2*x)*x), deep=True) == 2**(x*4**x)
    assert powsimp(exp(-x + exp(-x)*exp(-x*log(x))), deep=False, combine='exp') == exp(-x + exp(-x)*exp(-x*log(x)))
    assert powsimp(exp(-x + exp(-x)*exp(-x*log(x))), deep=False, combine='exp') == exp(-x + exp(-x)*exp(-x*log(x)))
    assert powsimp((x+y)/(3*z), deep=False, combine='exp') == (x+y)/(3*z)
    assert powsimp((x/3+y/3)/z, deep=True, combine='exp') == (x/3+y/3)/z
    assert powsimp(exp(x)/(1 + exp(x)*exp(y)), deep=True) == exp(x)/(1 + exp(x + y))
    assert powsimp(x*y**(z**x*z**y), deep=True) == x*y**(z**(x + y))
    assert powsimp((z**x*z**y)**x, deep=True) == (z**(x + y))**x
    assert powsimp(x*(z**x*z**y)**x, deep=True) == x*(z**(x + y))**x
    p = symbols('p', positive=True)
    assert powsimp((1/x)**log(2)/x) == (1/x)**(1 + log(2))
    assert powsimp((1/p)**log(2)/p) == p**(-1 - log(2))

    # coefficient of exponent can only be simplified for positive bases
    assert powsimp(2**(2*x)) == 4**x
    assert powsimp((-1)**(2*x)) == (-1)**(2*x)
    i = symbols('i', integer=True)
    assert powsimp((-1)**(2*i)) == 1
    assert powsimp((-1)**(-x)) != (-1)**x  # could be 1/((-1)**x), but is not
    # force=True overrides assumptions
    assert powsimp((-1)**(2*x), force=True) == 1

    eq = x**(2*a/3)
    assert powsimp(eq).exp == eq.exp == 2*a/3 # eq != (x**a)**(2/3) (try x = -1 and a = 3 to see)
    assert powsimp(2**(2*x)) == 4**x # powdenest goes the other direction

def test_powsimp_polar():
    from sympy import polar_lift, exp_polar
    x, y, z = symbols('x y z')
    p, q, r = symbols('p q r', polar=True)

    assert (polar_lift(-1))**(2*x) == exp_polar(2*pi*I*x)
    assert powsimp(p**x * q**x) == (p*q)**x
    assert p**x * (1/p)**x == 1
    assert (1/p)**x == p**(-x)

    assert exp_polar(x)*exp_polar(y) == exp_polar(x)*exp_polar(y)
    assert powsimp(exp_polar(x)*exp_polar(y)) == exp_polar(x+y)
    assert powsimp(exp_polar(x)*exp_polar(y)*p**x*p**y) == (p*exp_polar(1))**(x + y)
    assert powsimp(exp_polar(x)*exp_polar(y)*p**x*p**y, combine='exp') \
           == exp_polar(x+y)*p**(x+y)
    assert powsimp(exp_polar(x)*exp_polar(y)*exp_polar(2)*sin(x)+sin(y)+p**x*p**y) \
           == p**(x+y) + sin(x)*exp_polar(2+x+y) + sin(y)
    assert powsimp(sin(exp_polar(x)*exp_polar(y))) == sin(exp_polar(x)*exp_polar(y))
    assert powsimp(sin(exp_polar(x)*exp_polar(y)), deep=True) == sin(exp_polar(x+y))

def test_powsimp_nc():
    x, y, z = symbols('x,y,z')
    A, B, C = symbols('A B C', commutative=False)

    assert powsimp(A**x*A**y, combine='all') == A**(x+y)
    assert powsimp(A**x*A**y, combine='base') == A**x*A**y
    assert powsimp(A**x*A**y, combine='exp') == A**(x+y)

    assert powsimp(A**x*B**x, combine='all') == (A*B)**x
    assert powsimp(A**x*B**x, combine='base') == (A*B)**x
    assert powsimp(A**x*B**x, combine='exp') == A**x*B**x

    assert powsimp(B**x*A**x, combine='all') == (B*A)**x
    assert powsimp(B**x*A**x, combine='base') == (B*A)**x
    assert powsimp(B**x*A**x, combine='exp') == B**x*A**x

    assert powsimp(A**x*A**y*A**z, combine='all') == A**(x+y+z)
    assert powsimp(A**x*A**y*A**z, combine='base') == A**x*A**y*A**z
    assert powsimp(A**x*A**y*A**z, combine='exp') == A**(x+y+z)

    assert powsimp(A**x*B**x*C**x, combine='all') == (A*B*C)**x
    assert powsimp(A**x*B**x*C**x, combine='base') == (A*B*C)**x
    assert powsimp(A**x*B**x*C**x, combine='exp') == A**x*B**x*C**x

    assert powsimp(B**x*A**x*C**x, combine='all') == (B*A*C)**x
    assert powsimp(B**x*A**x*C**x, combine='base') == (B*A*C)**x
    assert powsimp(B**x*A**x*C**x, combine='exp') == B**x*A**x*C**x

def test_collect_1():
    """Collect with respect to a Symbol"""
    x, y, z, n = symbols('x,y,z,n')
    assert collect( x + y*x, x ) == x * (1 + y)
    assert collect( x + x**2, x ) == x + x**2
    assert collect( x**2 + y*x**2, x ) == (x**2)*(1+y)
    assert collect( x**2 + y*x, x ) == x*y + x**2
    assert collect( 2*x**2 + y*x**2 + 3*x*y, [x] ) == x**2*(2+y) + 3*x*y
    assert collect( 2*x**2 + y*x**2 + 3*x*y, [y] ) == 2*x**2 + y*(x**2+3*x)

    assert collect( ((1 + y + x)**4).expand(), x) == ((1 + y)**4).expand() + \
                x*(4*(1 + y)**3).expand() + x**2*(6*(1 + y)**2).expand() + \
                x**3*(4*(1 + y)).expand() + x**4
    # symbols can be given as any iterable
    expr = x + y
    assert collect(expr, expr.free_symbols) == expr

def test_collect_2():
    """Collect with respect to a sum"""
    a, b, x = symbols('a,b,x')
    assert collect(a*(cos(x)+sin(x)) + b*(cos(x)+sin(x)), sin(x)+cos(x)) == (a + b)*(cos(x) + sin(x))

def test_collect_3():
    """Collect with respect to a product"""
    a, b, c = symbols('a,b,c')
    f = Function('f')
    x, y, z, n = symbols('x,y,z,n')

    assert collect(-x/8 + x*y, -x) == x*(y - S(1)/8)

    assert collect( 1 + x*(y**2), x*y ) == 1 + x*(y**2)
    assert collect( x*y + a*x*y, x*y) == x*y*(1 + a)
    assert collect( 1 + x*y + a*x*y, x*y) == 1 + x*y*(1 + a)
    assert collect(a*x*f(x) + b*(x*f(x)), x*f(x)) == x*(a + b)*f(x)

    assert collect(a*x*log(x) + b*(x*log(x)), x*log(x)) == x*(a + b)*log(x)
    assert collect(a*x**2*log(x)**2 + b*(x*log(x))**2, x*log(x)) == x**2*log(x)**2*(a + b)

    # with respect to a product of three symbols
    assert collect(y*x*z+a*x*y*z, x*y*z) == (1 + a)*x*y*z

def test_collect_4():
    """Collect with respect to a power"""
    a, b, c, x = symbols('a,b,c,x')

    assert collect(a*x**c + b*x**c, x**c) == x**c*(a + b)
    assert collect(a*x**(2*c) + b*x**(2*c), x**c) == (x**2)**c*(a + b)

def test_collect_5():
    """Collect with respect to a tuple"""
    a, x, y, z, n = symbols('a,x,y,z,n')
    assert collect(x**2*y**4 + z*(x*y**2)**2 + z + a*z, [x*y**2, z]) in [
                z*(1 + a + x**2*y**4) + x**2*y**4,
                z*(1 + a) + x**2*y**4*(1 + z) ]
    assert collect((1+ (x+y) + (x+y)**2).expand(),
                   [x, y]) == 1 + y + x*(1 + 2*y) + x**2  + y**2

def test_collect_D():
    D = Derivative
    f = Function('f')
    x, a, b = symbols('x,a,b')
    fx  = D(f(x), x)
    fxx = D(f(x), x, x)

    assert collect(a*fx + b*fx, fx) == (a + b)*fx
    assert collect(a*D(fx, x) + b*D(fx, x), fx)   == (a + b)*D(fx, x)
    assert collect(a*fxx     + b*fxx    , fx)   == (a + b)*D(fx, x)
    # 1685
    assert collect(5*f(x)+3*fx, fx) == 5*f(x) + 3*fx
    assert collect(f(x) + f(x)*diff(f(x), x) + x*diff(f(x), x)*f(x), f(x).diff(x)) ==\
    (x*f(x) + f(x))*D(f(x), x) + f(x)
    assert collect(f(x) + f(x)*diff(f(x), x) + x*diff(f(x), x)*f(x), f(x).diff(x), exact=True) ==\
    (x*f(x) + f(x))*D(f(x), x) + f(x)
    assert collect(1/f(x) + 1/f(x)*diff(f(x), x) + x*diff(f(x), x)/f(x), f(x).diff(x), exact=True) ==\
    (1/f(x) + x/f(x))*D(f(x), x) + 1/f(x)

@XFAIL
def collect_issues():
    assert collect(1/f(x) + 1/f(x)*diff(f(x), x) + x*diff(f(x), x)/f(x), f(x).diff(x)) !=\
    (1 + x*D(f(x), x) + D(f(x), x))/f(x)

def test_collect_D_0():
    D = Derivative
    f = Function('f')
    x, a, b = symbols('x,a,b')
    fxx = D(f(x), x, x)

    # collect does not distinguish nested derivatives, so it returns
    #                                           -- (a + b)*D(D(f, x), x)
    assert collect(a*fxx     + b*fxx    , fxx)  == (a + b)*fxx

def test_collect_Wild():
    """Collect with respect to functions with Wild argument"""
    a, b, x, y = symbols('a b x y')
    f = Function('f')
    w1 = Wild('.1')
    w2 = Wild('.2')
    assert collect(f(x) + a*f(x), f(w1)) == (1 + a)*f(x)
    assert collect(f(x, y) + a*f(x, y), f(w1)) == f(x, y) + a*f(x, y)
    assert collect(f(x, y) + a*f(x, y), f(w1, w2)) == (1 + a)*f(x, y)
    assert collect(f(x, y) + a*f(x, y), f(w1, w1)) == f(x, y) + a*f(x, y)
    assert collect(f(x, x) + a*f(x, x), f(w1, w1)) == (1 + a)*f(x, x)
    assert collect(a*(x + 1)**y + (x + 1)**y, w1**y) == (1 + a)*(x + 1)**y
    assert collect(a*(x + 1)**y + (x + 1)**y, w1**b) == a*(x + 1)**y + (x + 1)**y
    assert collect(a*(x + 1)**y + (x + 1)**y, (x + 1)**w2) == (1 + a)*(x + 1)**y
    assert collect(a*(x + 1)**y + (x + 1)**y, w1**w2) == (1 + a)*(x + 1)**y

def test_collect_func():
    f = expand((x + a + 1)**3)

    assert collect(f, x) == a**3 + 3*a**2 + 3*a + x**3 + x**2*(3*a + 3) + x*(3*a**2 + 6*a + 3) + 1
    assert collect(f, x, factor) == x**3 + 3*x**2*(a + 1) + 3*x*(a + 1)**2 + (a + 1)**3

    assert collect(f, x, evaluate=False) == {S.One: a**3 + 3*a**2 + 3*a + 1, x: 3*a**2 + 6*a + 3, x**2: 3*a + 3, x**3: 1}

@XFAIL
def test_collect_func_xfail():
    # XXX: this test will pass when automatic constant distribution is removed (#1497)
    assert collect(f, x, factor, evaluate=False) == {S.One: (a + 1)**3, x: 3*(a + 1)**2, x**2: 3*(a + 1), x**3: 1}

def test_collect_order():
    a, b, x, t = symbols('a,b,x,t')

    assert collect(t + t*x + t*x**2 + O(x**3), t) == t*(1 + x + x**2 + O(x**3))
    assert collect(t + t*x + x**2 + O(x**3), t) == t*(1 + x + O(x**3)) + x**2 + O(x**3)

    f = a*x + b*x + c*x**2 + d*x**2 + O(x**3)
    g = x*(a + b) + x**2*(c + d) + O(x**3)

    assert collect(f, x) == g
    assert collect(f, x, distribute_order_term=False) == g

    f = sin(a + b).series(b, 0, 10)

    assert collect(f, [sin(a), cos(a)]) == \
        sin(a)*cos(b).series(b, 0, 10) + cos(a)*sin(b).series(b, 0, 10)
    assert collect(f, [sin(a), cos(a)], distribute_order_term=False) == \
        sin(a)*cos(b).series(b, 0, 10).removeO() + cos(a)*sin(b).series(b, 0, 10).removeO() + O(b**10)

def test_rcollect():
    assert rcollect((x**2*y + x*y + x + y)/(x + y), y) == (x + y*(1 + x + x**2))/(x + y)
    assert rcollect(sqrt(-((x + 1)*(y + 1))), z) == sqrt(-((x + 1)*(y + 1)))

def test_separatevars():
    x,y,z,n = symbols('x,y,z,n')
    assert separatevars(2*n*x*z+2*x*y*z) == 2*x*z*(n+y)
    assert separatevars(x*z+x*y*z) == x*z*(1+y)
    assert separatevars(pi*x*z+pi*x*y*z) == pi*x*z*(1+y)
    assert separatevars(x*y**2*sin(x) + x*sin(x)*sin(y)) == x*(sin(y) + y**2)*sin(x)
    assert separatevars(x*exp(x+y)+x*exp(x)) == x*(1 + exp(y))*exp(x)
    assert separatevars((x*(y+1))**z).is_Pow # != x**z*(1 + y)**z
    assert separatevars(1+x+y+x*y) == (x+1)*(y+1)
    assert separatevars(y / pi * exp(-(z - x) / cos(n))) == y * exp((x - z) / cos(n)) / pi
    # 1759
    p=Symbol('p',positive=True)
    assert separatevars(sqrt(p**2 + x*p**2)) == p*sqrt(1 + x)
    assert separatevars(sqrt(y*(p**2 + x*p**2))) == p*sqrt(y*(1 + x))
    assert separatevars(sqrt(y*(p**2 + x*p**2)), force=True) == p*sqrt(y)*sqrt(1 + x)
    # 1766
    assert separatevars(sqrt(x*y)).is_Pow
    assert separatevars(sqrt(x*y), force=True) == sqrt(x)*sqrt(y)
    # 1858
    # any type sequence for symbols is fine
    assert separatevars(((2*x+2)*y), dict=True, symbols=()) == {'coeff': 2, x: x + 1, y: y}
    # separable
    assert separatevars(((2*x+2)*y), dict=True, symbols=[]) == {'coeff': 2, x: x + 1, y: y}
    assert separatevars(((2*x+2)*y), dict=True) == {'coeff': 2, x: x + 1, y: y}
    assert separatevars(((2*x+2)*y), dict=True, symbols=None) == {'coeff': 2*y*(x + 1)}
    # not separable
    assert separatevars(2*x+y, dict=True, symbols=()) is None
    assert separatevars(2*x+y, dict=True) is None
    assert separatevars(2*x+y, dict=True, symbols=None) == {'coeff': 2*x + y}

def test_separatevars_advanced_factor():
    x,y,z = symbols('x,y,z')
    assert separatevars(1 + log(x)*log(y) + log(x) + log(y)) == (log(x) + 1)*(log(y) + 1)
    assert separatevars(1 + x - log(z) - x*log(z) - exp(y)*log(z) - x*exp(y)*log(z) + x*exp(y) + exp(y)) == \
        -((x + 1)*(log(z) - 1)*(exp(y) + 1))
    x, y = symbols('x,y', positive=True)
    assert separatevars(1 + log(x**log(y)) + log(x*y)) == (log(x) + 1)*(log(y) + 1)

def test_hypersimp():
    n, k = symbols('n,k', integer=True)

    assert hypersimp(factorial(k), k) == k + 1
    assert hypersimp(factorial(k**2), k) is None

    assert hypersimp(1/factorial(k), k) == 1/(k + 1)

    assert hypersimp(2**k/factorial(k)**2, k) == 2/(k**2 + 2*k + 1)

    assert hypersimp(binomial(n, k), k) == (n-k)/(k+1)
    assert hypersimp(binomial(n+1, k), k) == (n-k+1)/(k+1)

    term = (4*k+1)*factorial(k)/factorial(2*k+1)
    assert hypersimp(term, k) == (S(1)/2)*((4*k + 5)/(3 + 14*k + 8*k**2))

    term = 1/((2*k-1)*factorial(2*k+1))
    assert hypersimp(term, k) == (2*k - 1)/(3 + 11*k + 12*k**2 + 4*k**3)/2

    term = binomial(n, k)*(-1)**k/factorial(k)
    assert hypersimp(term, k) == (k - n)/(k**2 + 2*k + 1)

def test_nsimplify():
    x = Symbol("x")
    assert nsimplify(0) == 0
    assert nsimplify(-1) == -1
    assert nsimplify(1) == 1
    assert nsimplify(1+x) == 1+x
    assert nsimplify(2.7) == Rational(27, 10)
    assert nsimplify(1-GoldenRatio) == (1-sqrt(5))/2
    assert nsimplify((1+sqrt(5))/4, [GoldenRatio]) == GoldenRatio/2
    assert nsimplify(2/GoldenRatio, [GoldenRatio]) == 2*GoldenRatio - 2
    assert nsimplify(exp(5*pi*I/3, evaluate=False)) == sympify('1/2 - sqrt(3)*I/2')
    assert nsimplify(sin(3*pi/5, evaluate=False)) == sympify('sqrt(sqrt(5)/8 + 5/8)')
    assert nsimplify(sqrt(atan('1', evaluate=False))*(2+I), [pi]) == sqrt(pi) + sqrt(pi)/2*I
    assert nsimplify(2 + exp(2*atan('1/4')*I)) == sympify('49/17 + 8*I/17')
    assert nsimplify(pi, tolerance=0.01) == Rational(22, 7)
    assert nsimplify(pi, tolerance=0.001) == Rational(355, 113)
    assert nsimplify(0.33333, tolerance=1e-4) == Rational(1, 3)
    assert nsimplify(2.0**(1/3.), tolerance=0.001) == Rational(635, 504)
    assert nsimplify(2.0**(1/3.), tolerance=0.001, full=True) == 2**Rational(1, 3)
    assert nsimplify(x + .5, rational=True) == Rational(1, 2) + x
    assert nsimplify(1/.3 + x, rational=True) == Rational(10, 3) + x
    assert nsimplify(log(3).n(), rational=True) == \
           sympify('109861228866811/100000000000000')
    assert nsimplify(Float(0.272198261287950), [pi,log(2)]) == pi*log(2)/8
    assert nsimplify(Float(0.272198261287950).n(3), [pi,log(2)]) == \
        -pi/4 - log(2) + S(7)/4
    assert nsimplify(x/7.0) == x/7
    assert nsimplify(pi/1e2) == pi/100
    assert nsimplify(pi/1e2, rational=False) == pi/100.0
    assert nsimplify(pi/1e-7) == 10000000*pi

def test_extract_minus_sign():
    x = Symbol("x")
    y = Symbol("y")
    a = Symbol("a")
    b = Symbol("b")
    assert simplify(-x/-y) == x/y
    assert simplify(-x/y) == -x/y
    assert simplify(x/y) == x/y
    assert simplify(x/-y) == -x/y
    assert simplify(-x/0) == -oo*x
    assert simplify(S(-5)/0) == -oo
    assert simplify(-a*x/(-y-b)) == a*x/(b + y)

def test_diff():
    x = Symbol("x")
    y = Symbol("y")
    f = Function("f")
    g = Function("g")
    assert simplify(g(x).diff(x)*f(x).diff(x)-f(x).diff(x)*g(x).diff(x)) == 0
    assert simplify(2*f(x)*f(x).diff(x)-diff(f(x)**2, x)) == 0
    assert simplify(diff(1/f(x), x)+f(x).diff(x)/f(x)**2) == 0
    assert simplify(f(x).diff(x, y)-f(x).diff(y, x)) == 0

def test_logcombine_1():
    x, y = symbols("x,y")
    a = Symbol("a")
    z, w = symbols("z,w", positive=True)
    b = Symbol("b", real=True)
    assert logcombine(log(x)+2*log(y)) == log(x) + 2*log(y)
    assert logcombine(log(x)+2*log(y), force=True) == log(x*y**2)
    assert logcombine(a*log(w)+log(z)) == a*log(w) + log(z)
    assert logcombine(b*log(z)+b*log(x)) == log(z**b) + b*log(x)
    assert logcombine(b*log(z)-log(w)) == log(z**b/w)
    assert logcombine(log(x)*log(z)) == log(x)*log(z)
    assert logcombine(log(w)*log(x)) == log(w)*log(x)
    assert logcombine(cos(-2*log(z)+b*log(w))) in [cos(log(w**b/z**2)),
                                                   cos(log(z**2/w**b))]
    assert logcombine(log(log(x)-log(y))-log(z), force=True) == \
        log(log((x/y)**(1/z)))
    assert logcombine((2+I)*log(x), force=True) == I*log(x)+log(x**2)
    assert logcombine((x**2+log(x)-log(y))/(x*y), force=True) == \
        log(x**(1/(x*y))*y**(-1/(x*y)))+x/y
    assert logcombine(log(x)*2*log(y)+log(z), force=True) == \
        log(z*y**log(x**2))
    assert logcombine((x*y+sqrt(x**4+y**4)+log(x)-log(y))/(pi*x**Rational(2, 3)*\
        sqrt(y)**3), force=True) == \
        log(x**(1/(pi*x**Rational(2, 3)*sqrt(y)**3))*y**(-1/(pi*\
        x**Rational(2, 3)*sqrt(y)**3))) + sqrt(x**4 + y**4)/(pi*\
        x**Rational(2, 3)*sqrt(y)**3) + x**Rational(1, 3)/(pi*sqrt(y))
    assert logcombine(Eq(log(x), -2*log(y)), force=True) == \
        Eq(log(x*y**2), Integer(0))
    assert logcombine(Eq(y, x*acos(-log(x/y))), force=True) == \
        Eq(y, x*acos(log(y/x)))
    assert logcombine(gamma(-log(x/y))*acos(-log(x/y)), force=True) == \
        acos(log(y/x))*gamma(log(y/x))
    assert logcombine((2+3*I)*log(x), force=True) == \
        log(x**2)+3*I*log(x)
    assert logcombine(Eq(y, -log(x)), force=True) == Eq(y, log(1/x))
    assert logcombine(Integral((sin(x**2)+cos(x**3))/x, x), force=True) == \
        Integral((sin(x**2)+cos(x**3))/x, x)
    assert logcombine(Integral((sin(x**2)+cos(x**3))/x, x)+ (2+3*I)*log(x), \
        force=True) == log(x**2)+3*I*log(x) + \
        Integral((sin(x**2)+cos(x**3))/x, x)

def test_posify():
    from sympy.abc import x

    assert str(posify(
        x +
        Symbol('p', positive=True) +
        Symbol('n', negative=True))) == '(_x + n + p, {_x: x})'

    # log(1/x).expand() should be log(1/x) but it comes back as -log(x)
    # when it is corrected, posify will allow the change to be made. The
    # force=True option can do so as well when it is implemented.
    eq, rep = posify(1/x)
    assert log(eq).expand().subs(rep) == -log(x)
    assert str(posify([x, 1 + x])) == '([_x, _x + 1], {_x: x})'

    x = symbols('x')
    p = symbols('p', positive=True)
    n = symbols('n', negative=True)
    orig = [x, n, p]
    modified, reps = posify(orig)
    assert str(modified) == '[_x, n, p]'
    assert [w.subs(reps) for w in modified] == orig

def test_powdenest():
    from sympy import powdenest
    from sympy.abc import x, y, z, a, b
    p, q = symbols('p q', positive=True)
    i, j = symbols('i,j', integer=True)

    assert powdenest(x) == x
    assert powdenest(x + 2*(x**(2*a/3))**(3*x)) == x + 2*(x**(a/3))**(6*x)
    assert powdenest((exp(2*a/3))**(3*x)) == (exp(a/3))**(6*x)
    assert powdenest((x**(2*a/3))**(3*x)) == (x**(a/3))**(6*x)
    assert powdenest(exp(3*x*log(2))) == 2**(3*x)
    assert powdenest(sqrt(p**2)) == p
    i, j = symbols('i,j', integer=True)
    eq = p**(2*i)*q**(4*i)
    assert powdenest(eq) == (p*q**2)**(2*i)
    assert powdenest((x**x)**(i + j)) # -X-> (x**x)**i*(x**x)**j == x**(x*(i + j))
    assert powdenest(exp(3*y*log(x))) == x**(3*y)
    assert powdenest(exp(y*(log(a) + log(b)))) == (a*b)**y
    assert powdenest(exp(3*(log(a) + log(b)))) == a**3*b**3
    assert powdenest(((x**(2*i))**(3*y))**x) == ((x**(2*i))**(3*y))**x
    assert powdenest(((x**(2*i))**(3*y))**x, force=True) == x**(6*i*x*y)
    assert powdenest(((x**(2*a/3))**(3*y/i))**x) == ((x**(a/3))**(y/i))**(6*x)
    assert powdenest((x**(2*i)*y**(4*i))**z, force=True) == (x*y**2)**(2*i*z)
    assert powdenest((p**(2*i)*q**(4*i))**j) == (p*q**2)**(2*i*j)
    assert powdenest(((p**(2*a))**(3*y))**x) == p**(6*a*x*y)
    e = ((x**2*y**4)**a)**(x*y)
    assert powdenest(e) == e
    e = (((x**2*y**4)**a)**(x*y))**3
    assert powdenest(e) == ((x**2*y**4)**a)**(3*x*y)
    assert powdenest((((x**2*y**4)**a)**(x*y)), force=True) == (x*y**2)**(2*a*x*y)
    assert powdenest((((x**2*y**4)**a)**(x*y))**3, force=True) == (x*y**2)**(6*a*x*y)
    assert powdenest((x**2*y**6)**i) != (x*y**3)**(2*i)
    x, y = symbols('x,y', positive=True)
    assert powdenest((x**2*y**6)**i) == (x*y**3)**(2*i)
    assert powdenest((x**(2*i/3)*y**(i/2))**(2*i)) == (x**(S(4)/3)*y)**(i**2)
    assert powdenest(sqrt(x**(2*i)*y**(6*i))) == (x*y**3)**i
    # issue 2706
    assert powdenest(((gamma(x)*hyper((),(),x))*pi)**2) == (pi*gamma(x)*hyper((), (), x))**2

    assert powdenest(4**x) == 2**(2*x)
    assert powdenest((4**x)**y) == 2**(2*x*y)
    assert powdenest(4**x*y) == 2**(2*x)*y

@XFAIL
def test_issue_2706():
    assert (((gamma(x)*hyper((),(),x))*pi)**2).is_positive is None

def test_issue_1095():
    # simplify should call cancel
    from sympy.abc import x, y
    f = Function('f')
    assert simplify((4*x+6*f(y))/(2*x+3*f(y))) == 2

@XFAIL
def test_simplify_float_vs_integer():
    # Test for issue 1374:
    # http://code.google.com/p/sympy/issues/detail?id=1374
    assert simplify(x**2.0-x**2) == 0
    assert simplify(x**2-x**2.0) == 0

def test_combsimp():
    from sympy.abc import n, k

    assert combsimp(factorial(n)) == factorial(n)
    assert combsimp(binomial(n, k)) == binomial(n, k)

    assert combsimp(factorial(n)/factorial(n - 3)) == n*(-1 + n)*(-2 + n)
    assert combsimp(binomial(n + 1, k + 1)/binomial(n, k)) == (1 + n)/(1 + k)

    assert combsimp(binomial(3*n + 4, n + 1)/binomial(3*n + 1, n)) == \
        S(3)/2*((3*n + 2)*(3*n + 4)/((n + 1)*(2*n + 3)))

    assert combsimp(factorial(n)**2/factorial(n - 3)) == factorial(n)*n*(-1 + n)*(-2 + n)
    assert combsimp(factorial(n)*binomial(n+1, k+1)/binomial(n, k)) == factorial(n)*(1 + n)/(1 + k)

    assert combsimp(binomial(n - 1, k)) == -((-n + k)*binomial(n, k))/n

    assert combsimp(binomial(n + 2, k + S(1)/2)) == \
        4*((n + 1)*(n + 2)*binomial(n, k + S(1)/2))/((2*k - 2*n - 1)*(2*k - 2*n - 3))
    assert combsimp(binomial(n + 2, k + 2.0)) == \
        -((1.0*n + 2.0)*binomial(n + 1.0, k + 2.0))/(k - n)

def test_issue_2516():
    aA, Re, a, b, D = symbols('aA Re a b D')
    e=((D**3*a + b*aA**3)/Re).expand()
    assert collect(e, [aA**3/Re, a]) == e

def test_issue_2629():
    b = x*sqrt(y)
    a = sqrt(b)
    c = sqrt(sqrt(x)*y)
    assert powsimp(a*b) == sqrt(b)**3
    assert powsimp(a*b**2*sqrt(y)) == sqrt(y)*a**5
    assert powsimp(a*x**2*c**3*y) == c**3*a**5
    assert powsimp(a*x*c**3*y**2) == c**7*a
    assert powsimp(x*c**3*y**2) == c**7
    assert powsimp(x*c**3*y) == x*y*c**3
    assert powsimp(sqrt(x)*c**3*y) == c**5
    assert powsimp(sqrt(x)*a**3*sqrt(y)) == sqrt(x)*sqrt(y)*a**3
    assert powsimp(Mul(sqrt(x)*c**3*sqrt(y), y, evaluate=False)) == sqrt(x)*sqrt(y)**3*c**3
    assert powsimp(a**2*a*x**2*y) == a**7

    # symbolic powers work, too
    b = x**y*y
    a = b*sqrt(b)
    assert a.is_Mul is True
    assert powsimp(a) == sqrt(b)**3

    # as does exp
    a = x*exp(2*y/3)
    assert powsimp(a*sqrt(a)) == sqrt(a)**3
    assert powsimp(a**2*sqrt(a)) == sqrt(a)**5
    assert powsimp(a**2*sqrt(sqrt(a))) == sqrt(sqrt(a))**9

def test_as_content_primitive():
    # although the _as_content_primitive methods do not alter the underlying structure,
    # the as_content_primitive function will touch up the expression and join
    # bases that would otherwise have not been joined.
    assert ((x*(2 + 2*x)*(3*x + 3)**2)).as_content_primitive() ==\
    (18, x*(x + 1)**3)
    assert (2 + 2*x + 2*y*(3 + 3*y)).as_content_primitive() ==\
    (2, x + 3*y*(y + 1) + 1)
    assert ((2 + 6*x)**2).as_content_primitive() ==\
    (4, (3*x + 1)**2)
    assert ((2 + 6*x)**(2*y)).as_content_primitive() ==\
    (1, (_keep_coeff(S(2), (3*x + 1)))**(2*y))
    assert (5 + 10*x + 2*y*(3+3*y)).as_content_primitive() ==\
    (1, 10*x + 6*y*(y + 1) + 5)
    assert ((5*(x*(1 + y)) + 2*x*(3 + 3*y))).as_content_primitive() ==\
    (11, x*(y + 1))
    assert ((5*(x*(1 + y)) + 2*x*(3 + 3*y))**2).as_content_primitive() ==\
    (121, x**2*(y + 1)**2)
    assert (y**2).as_content_primitive() ==\
    (1, y**2)
    assert (S.Infinity).as_content_primitive() == (1, oo)
    eq = x**(2+y)
    assert (eq).as_content_primitive() == (1, eq)
    assert (S.Half**(2 + x)).as_content_primitive() == (S(1)/4, 2**-x)
    assert ((-S.Half)**(2 + x)).as_content_primitive() == \
            (S(1)/4, (-S.Half)**x)
    assert ((-S.Half)**(2 + x)).as_content_primitive() == \
            (S(1)/4, (-S.Half)**x)
    assert (4**((1 + y)/2)).as_content_primitive() == (2, 4**(y/2))
    assert (3**((1 + y)/2)).as_content_primitive() == \
            (1, 3**(Mul(S(1)/2, 1 + y, evaluate=False)))
    assert (5**(S(3)/4)).as_content_primitive() == (1, 5**(S(3)/4))
    assert (5**(S(7)/4)).as_content_primitive() == (5, 5**(S(3)/4))
    assert Add(5*z/7, 0.5*x, 3*y/2, evaluate=False).as_content_primitive() == \
            (S(1)/14, 7.0*x + 21*y + 10*z)
    assert (2**(S(3)/4) + 2**(S(1)/4)*sqrt(3)).as_content_primitive(radical=True) == \
            (1, 2**(S(1)/4)*(sqrt(2) + sqrt(3)))

def test_radsimp():
    r2=sqrt(2)
    r3=sqrt(3)
    r5=sqrt(5)
    r7=sqrt(7)
    assert radsimp(1/r2) == \
        sqrt(2)/2
    assert radsimp(1/(1 + r2)) == \
        -1 + sqrt(2)
    assert radsimp(1/(r2 + r3)) == \
        -sqrt(2) + sqrt(3)
    assert fraction(radsimp(1/(1 + r2 + r3))) == \
        (-sqrt(6) + sqrt(2) + 2, 4)
    assert fraction(radsimp(1/(r2 + r3 + r5))) == \
        (-sqrt(30) + 2*sqrt(3) + 3*sqrt(2), 12)
    assert fraction(radsimp(1/(1 + r2 + r3 + r5))) == \
        (-34*sqrt(10) -
        26*sqrt(15) -
        55*sqrt(3) -
        61*sqrt(2) +
        14*sqrt(30) +
        93 +
        46*sqrt(6) +
        53*sqrt(5), 71)
    assert fraction(radsimp(1/(r2 + r3 + r5 + r7))) == \
        (-50*sqrt(42) - 133*sqrt(5) - 34*sqrt(70) -
        145*sqrt(3) + 22*sqrt(105) + 185*sqrt(2) +
        62*sqrt(30) + 135*sqrt(7), 215)
    assert radsimp(1/(r2*3)) == \
        sqrt(2)/6
    assert radsimp(1/(r2*a + r2*b + r3 + r7)) == \
        ((sqrt(42)*(a + b) +
        sqrt(3)*(-a**2 - 2*a*b - b**2 - 2)  +
        sqrt(7)*(-a**2 - 2*a*b - b**2 + 2)  +
        sqrt(2)*(a**3 + 3*a**2*b + 3*a*b**2 - 5*a + b**3 - 5*b))/
        ((a**4 + 4*a**3*b + 6*a**2*b**2 - 10*a**2  +
        4*a*b**3 - 20*a*b + b**4 - 10*b**2 + 4)))/2
    assert radsimp(1/(r2*a + r2*b + r2*c + r2*d)) == \
        (sqrt(2)/(a + b + c + d))/2
    assert radsimp(1/(1 + r2*a + r2*b + r2*c + r2*d)) == \
        ((sqrt(2)*(-a - b - c - d) + 1)/
        (-2*a**2 - 4*a*b - 4*a*c - 4*a*d - 2*b**2 -
        4*b*c - 4*b*d - 2*c**2 - 4*c*d - 2*d**2 + 1))
    assert radsimp((y**2 - x)/(y - sqrt(x))) == \
        sqrt(x) + y
    assert radsimp(-(y**2 - x)/(y - sqrt(x))) == \
        -(sqrt(x) + y)
    assert radsimp(1/(1 - I + a*I)) == \
        (I*(-a + 1) + 1)/(a**2 - 2*a + 2)
    assert radsimp(1/((-x + y)*(x - sqrt(y)))) == (x + sqrt(y))/((-x + y)*(x**2 - y))
    e = (3 + 3*sqrt(2))*x*(3*x - 3*sqrt(y))
    assert radsimp(e) == 9*x*(1 + sqrt(2))*(x - sqrt(y))
    assert radsimp(1/e) == (-1 + sqrt(2))*(x + sqrt(y))/(9*x*(x**2 - y))
    assert radsimp(1 + 1/(1 + sqrt(3))) == Mul(S(1)/2, 1 + sqrt(3), evaluate=False)
    A = symbols("A", commutative=False)
    assert radsimp(x**2 + sqrt(2)*x**2 - sqrt(2)*x*A) == x**2 + sqrt(2)*(x**2 - x*A)
    assert radsimp(1/sqrt(5 + 2 * sqrt(6))) == -sqrt(2) + sqrt(3)
    assert radsimp(1/sqrt(5 + 2 * sqrt(6))**3) == -11*sqrt(2) + 9*sqrt(3)

    # coverage not provided by above tests
    assert collect_const(2*sqrt(3) + 4*a*sqrt(5)) == Mul(2, (2*sqrt(5)*a + sqrt(3)), evaluate=False)
    assert collect_const(2*sqrt(3) + 4*a*sqrt(5), sqrt(3)) == 2*(2*sqrt(5)*a + sqrt(3))
    assert collect_const(sqrt(2)*(1 + sqrt(2)) + sqrt(3) + x*sqrt(2)) == \
        sqrt(2)*(x + 1 + sqrt(2)) + sqrt(3)

def test_issue2834():
    from sympy import Polygon, RegularPolygon, denom
    x = Polygon(*RegularPolygon((0, 0), 1, 5).vertices).centroid.x
    assert abs(denom(x).n()) > 1e-12
    assert abs(denom(radsimp(x))) > 1e-12 # in case simplify didn't handle it

def test_fraction_expand():
    eq = (x + y)*y/x
    assert eq.expand(frac=True) == fraction_expand(eq) == (x*y + y**2)/x
    assert eq.expand() == y + y**2/x

def test_combsimp_gamma():
    from sympy.abc import x, y
    assert combsimp(gamma(x)) == gamma(x)
    assert combsimp(gamma(x+1)/x) == gamma(x)
    assert combsimp(gamma(x)/(x-1)) == gamma(x-1)
    assert combsimp(x*gamma(x)) == gamma(x + 1)
    assert combsimp((x+1)*gamma(x+1)) == gamma(x + 2)
    assert combsimp(gamma(x+y)*(x+y)) == gamma(x + y + 1)
    assert combsimp(x/gamma(x+1)) == 1/gamma(x)
    assert combsimp((x+1)**2/gamma(x+2)) == (x + 1)/gamma(x + 1)
    assert combsimp(x*gamma(x) + gamma(x+3)/(x+2)) == gamma(x+1) + gamma(x+2)

    assert combsimp(gamma(2*x)*x) == gamma(2*x + 1)/2
    assert combsimp(gamma(2*x)/(x - S(1)/2)) == 2*gamma(2*x - 1)

    assert combsimp(gamma(x)*gamma(1-x)) == pi/sin(pi*x)
    assert combsimp(gamma(x)*gamma(-x)) == -pi/(x*sin(pi*x))
    assert combsimp(1/gamma(x+3)/gamma(1-x)) == sin(pi*x)/(pi*x*(x+1)*(x+2))

    assert simplify(combsimp(gamma(x)*gamma(x+S(1)/2)*gamma(y)/gamma(x+y))) \
           == 2**(-2*x + 1)*sqrt(pi)*gamma(2*x)*gamma(y)/gamma(x + y)
    assert combsimp(1/gamma(x)/gamma(x-S(1)/3)/gamma(x+S(1)/3)) == \
           3**(3*x + S(1)/2)/(18*pi*gamma(3*x - 1))
    assert simplify(gamma(S(1)/2 + x/2)*gamma(1 + x/2)/gamma(1+x)/sqrt(pi)*2**x) \
           == 1
    assert combsimp(gamma(S(-1)/4)*gamma(S(-3)/4)) == 16*sqrt(2)*pi/3

def test_unpolarify():
    from sympy import (exp_polar, polar_lift, exp, unpolarify, sin,
                       principal_branch)
    from sympy import gamma, erf, sin, tanh, uppergamma, Eq, Ne
    from sympy.abc import x
    p = exp_polar(7*I) + 1
    u = exp(7*I) + 1

    assert unpolarify(p) == u
    assert unpolarify(p**2) == u**2
    assert unpolarify(p**x) == p**x
    assert unpolarify(p*x) == u*x
    assert unpolarify(p + x) == u + x
    assert unpolarify(sqrt(sin(p))) == sqrt(sin(u))

    # Test reduction to principal branch 2*pi.
    t = principal_branch(x, 2*pi)
    assert unpolarify(t) == x
    assert unpolarify(sqrt(t)) == sqrt(t)

    # Test exponents_only.
    assert unpolarify(p**p, exponents_only=True) == p**u
    assert unpolarify(uppergamma(x, p**p)) == uppergamma(x, p**u)

    # Test functions.
    assert unpolarify(sin(p)) == sin(u)
    assert unpolarify(tanh(p)) == tanh(u)
    assert unpolarify(gamma(p)) == gamma(u)
    assert unpolarify(erf(p)) == erf(u)
    assert unpolarify(uppergamma(x, p)) == uppergamma(x, p)

    assert unpolarify(uppergamma(sin(p), sin(p + exp_polar(0)))) == \
           uppergamma(sin(u), sin(u + 1))
    assert unpolarify(uppergamma(polar_lift(0), 2*exp_polar(0))) == uppergamma(0, 2)

    assert unpolarify(Eq(p, 0)) == Eq(u, 0)
    assert unpolarify(Ne(p, 0)) == Ne(u, 0)
    assert unpolarify(polar_lift(x) > 0) == (x > 0)

    # Test bools
    assert unpolarify(True) is True
