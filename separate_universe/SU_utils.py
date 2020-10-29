import numpy as np
from scipy.integrate import odeint, solve_ivp

class SU_utils(object) :
    # This function returns the growths given a cosmology and a scale factor
    @staticmethod
#    def growthEqns(y, lna, param):
    def growthEqns(lna, y, param):
        Om, OL, w = param['Om'], param['OL'], -1
        OK = 1 - Om - OL

        D, F = y
        a = np.exp(lna)
        a3w = a**(-3*w)
        Hfac = - 0.5 * (Om+2*OK*a+(1-3*w)*OL*a3w) / (Om+OK*a+OL*a3w)
        Ofac = 1.5 * Om / (Om+OK*a+OL*a3w)
        Dp = F
        Fp = Hfac * F + Ofac * D

        return Dp, Fp

    # This routine computes the growth factor given a cosmology and a scale factor,
    # normalized to the scale factor at matter dominated era
    @staticmethod
    def linear_growth(a, param):
        ai = 1e-3 * a
        Di = ai
        Fi = Di
        yi = [Di, Fi]
        lna = np.log([ai, a])

#        y = odeint(SU_utils.growthEqns, yi, lna, args=(param,), atol=0)
#        D, F = y[-1]
        result = solve_ivp(SU_utils.growthEqns, lna, yi, args=(param,), atol=0, method='Radau')
        D, F = result.y
        D = D[-1]

        return D

    # This function returns delta_a = a_SU(t) / a(t) - 1 given scale factor & cosmology
    @staticmethod
    def daEqns(y, lna, param):
        Om, OL, w = param['Om'], param['OL'], -1
        OK = 1 - Om - OL

        y1, y2 = y
        a = np.exp(lna)
        a3w = a**(-3*w)
        Hfac = - 0.5 * (Om+2*OK*a+(1-3*w)*OL*a3w) / (Om+OK*a+OL*a3w)
        Ofac = 0.5 * Om / (Om+OK*a+OL*a3w)
        y1p = y2
        y2p = Hfac * y2 + Ofac * y1 * (3+y1*(3+y1)) / (1 + y1)**2

        return y1p, y2p

    # This routine computes a_SU(a) given DC mode, scale factors, and cosmology
    @staticmethod
    def aSU(delta_b, times, param):
        ai = 1e-3 * times[0]  # push it to matter dominated era
        y1i = - 1/3 * delta_b * ai / SU_utils.linear_growth(1, param)  # a_SU / a - 1
        y2i = y1i  # y2 = d y1 / d lna
        yi = [y1i, y2i]
        lna = [np.log(ai)] + list(np.log(times))

        y= odeint(SU_utils.daEqns, yi, lna, args=(param,), atol=0)
        return times * (1 + y[1:, 0])

    # This routine computes the value of the cosmological parameters, box size and scale
    # factor given the value of the DC mode
    # Note that the DC mode should be in its linear value
    @staticmethod
    def get_SU(delta_b, param, times):
        SU_param = param.copy()

        D0 = SU_utils.linear_growth(1., param)
        dlnH2 = - 5 / 3 * param['Om'] * delta_b / D0  # delta(H^2) / H^2
        dlnH = np.sqrt(1 + dlnH2) - 1  # delta(H) / H

        SU_param['Om'] /= 1 + dlnH2
        SU_param['Oc'] /= 1 + dlnH2
        SU_param['Ob'] /= 1 + dlnH2
        SU_param['OL'] /= 1 + dlnH2
        SU_param['Ok'] = dlnH2 / (1 + dlnH2)
        SU_param['h0'] *= 1 + dlnH
        SU_param['H0'] = SU_param['h0'] * 100

        SU_param['boxsize'] *= 1 + dlnH

        SU_times = SU_utils.aSU(delta_b, times, param)
        SU_param['time_end'] = SU_times[-1]

        return SU_param, SU_times
