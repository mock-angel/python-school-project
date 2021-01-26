import numpy as np

STRAIGHT_CURVE = 0
SECOND_DEG_PARABOLA = 1
SINE_WAVE = 2
class curveFvO():# Curve fitting via optimisation
    def __init__(self):
        self.list_x = []
        self.list_y = []
        self.n = 0
        self.type = STRAIGHT_CURVE
        
        self.loadDummyData()
    def loadDummyData(self):
        self.list_x = [5, 10, 15, 20, 25]
        self.list_y = [16, 19, 23, 26, 30]
        
        self.list_xy = []
        self.n = n = len(self.list_x)
        
        for i in range(n):
            self.list_xy.append([self.list_x[i], self.list_y[i]])
        
        self.load_straight_line_least_square_fitting()
    def load(self):
        if (self.type == SINE_WAVE):
            self.loadSineWaveTest()
            self.n = 40
    def loadXYList(self, XY_list):
        li_xy = []
        li_x = []
        li_y = []
        for xy in XY_list:
            li_xy.append(xy)
            li_x.append(xy[0])
            li_y.append(xy[1])
        self.list_xy = li_xy
        self.list_x = li_x
        self.list_y = li_y
        self.n = n = len(self.list_x)
        
        if (self.type == STRAIGHT_CURVE):
            self.load_straight_line_least_square_fitting()
        if (self.type == SECOND_DEG_PARABOLA):
            self.load_second_deg_parabola_least_square_fitting()
        
    def load_straight_line_least_square_fitting(self):
        """
            Fitting of a straight line with least square method
        """
        
        # summation_y = a*summation_x +n*b
        # summation_xy = a*summation_(x^2) + b*summation_x
        summation_x = sum(self.list_x)
        summation_y = sum(self.list_y)
        summation_xy = 0
        for i in range(self.n): summation_xy += self.list_x[i] * self.list_y[i]
        
        summation_xP2 = 0
        for i in range(self.n): summation_xP2 += self.list_x[i] ** 2
        
        y1, x1, c1 = summation_y, summation_x, self.n
        y2, x2, c2 = summation_xy, summation_xP2, summation_x
        
        a = [[x1, c1], [x2, c2]]
        b = [y1, y2]
        solved = np.linalg.solve(a, b)#gets a and b
        self.a = solved[0]
        self.b = solved[1]
        
        print "a = ", self.a, "b = ", self.b
        
    def load_second_deg_parabola_least_square_fitting(self):
        """
            Fitting of a straight line with least square method
        """
        
        # summation_y = a*summation_x +n*b
        # summation_xy = a*summation_(x^2) + b*summation_x
        summation_x = sum(self.list_x)
        summation_y = sum(self.list_y)
        summation_xy = 0
        for i in range(self.n): summation_xy += self.list_x[i] * self.list_y[i]
        
        summation_xP2y = 0
        for i in range(self.n): summation_xP2y += (self.list_x[i] ** 2) * self.list_y[i]
        
        summation_xP2 = 0
        for i in range(self.n): summation_xP2 += (self.list_x[i] ** 2)
        
        summation_xP3 = 0
        for i in range(self.n): summation_xP3 += self.list_x[i] ** 3
        
        summation_xP4 = 0
        for i in range(self.n): summation_xP4 += self.list_x[i] ** 4
        
        y1, x1, c1, d1 = summation_y, summation_xP2, summation_x, self.n
        y2, x2, c2, d2 = summation_xy, summation_xP3, summation_xP2, summation_x
        y3, x3, c3, d3 = summation_xP2y, summation_xP4, summation_xP3, summation_xP2
        
        a = [[x1, c1, d1], [x2, c2, d2], [x3, c3, d3]]
        b = [y1, y2, y3]
        solved = np.linalg.solve(a, b)#gets a and b
        self.a = solved[0]
        self.b = solved[1]
        self.c = solved[2]
        
        print "a = ", self.a, "b = ", self.b, "c = ", self.c
        
        #r = float(summation_xP2) / summation_x
        #y1, x1, c1 = r*y1, r*x1, r*c1
        #y, x, c = y1-y2, 0, c1-c2
    def setFunctionType(self, type_):
        self.type = type_
        
    def function_second_deg_parabola_least_square_fitting(self, x):
        return self.a * (x**2) + self.b * x + self.c
        
    def function_straight_line_least_square_fitting(self, x):
        
        return self.a * x + self.b
    
    def loadSineWaveTest(self):
        from scipy.optimize import curve_fit 
        #from matplotlib import pyplot as plt 
        x_arr = np.linspace(0, 10, num = 40)
        y_arr = 3.45 * np.sin(1.334 * x_arr) + np.random.normal(size = 40)
        self.list_x = x_arr.tolist()
        self.list_y = y_arr.tolist()
        print "x_list = ", self.list_x
        print 
        print "y_list = ", self.list_y
        print 
        
        def test(x, a, b): 
            return a * np.sin(b * x)
            
        param, param_cov = curve_fit(test, x_arr, y_arr) 
        self.param = param
        
        li_ = []
        for i in range(40):
            li_.append([self.list_x[i], self.list_y[i]])
        self.list_xy = li_
        
    def function_sine_wave_fitting(self, x):
        param = self.param
        return (param[0]*(np.sin(param[1]*x)))
        
    def getPoints(self):
        return self.list_xy
