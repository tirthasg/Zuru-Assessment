# User-defined class to compute moment capacity of the objects
class Moment:
    # Constructor to initialize the instance
    def __init__(self,
                 alpha1,
                 a_fromTop, a_fromBott,
                 a_max_fromTop, a_max_fromBott):

        # All instance attributes are being stored as public 
        self.alpha1 = alpha1

        self.a_fromTop = a_fromTop
        self.a_fromBott = a_fromBott

        self.a_max_fromTop = a_max_fromTop
        self.a_max_fromBott = a_max_fromBott

        # print("Important:")
        # print(alpha1, a_fromTop, a_fromBott, a_max_fromTop, a_max_fromBott)

        # self.alpha1 = 0.85

        # self.a_fromTop = 160.8235
        # self.a_fromBott = 30.8824

        # self.a_max_fromTop = 113.3647
        # self.a_max_fromBott = 113.3647

    # Class Method to initialize the class attributes
    @classmethod
    def init_class_attributes(cls, 
                              f_c, fy, 
                              bw, 
                              covTop, covBott, As_top_prov, As_bott_prov, 
                              dFromTop, dFromBott):
        # All class attributes are being stored as public 
        cls.f_c = f_c
        cls.fy = fy

        cls.bw = bw

        cls.covTop = covTop
        cls.covBott = covBott
        cls.As_bott_prov = As_bott_prov
        cls.As_top_prov = As_top_prov

        cls.dFromTop = dFromTop
        cls.dFromBott = dFromBott

        # print("Another important:")
        # print(f_c, fy, bw, covTop, covBott, As_bott_prov, As_top_prov, dFromTop, dFromBott)

    # Non-public Instance method to compute moment capacities
    def _M_cap_sing(cls, As, fy, d, a):
        return As * fy * (d - a / 2)

    # Non-public Instance method to compute moment capacities
    def _M_cap_doub(cls, alpha1, f_c, bw, a_max, d, fy, cov, As):
        return (alpha1 * f_c * bw * a_max * (d - a_max / 2)) + \
               (As - ((alpha1 * f_c * bw * a_max) / fy)) * fy * (d - cov)
            #    (As - ((alpha1 * f_c * bw * a_max * (d - (a_max / 2))) / (fy * (d - (a_max / 2))))) * fy * (d - cov)
            #    ((As - (alpha1 * f_c * bw * a_max * (d - a_max / 2)) / (fy * (d -  a_max / 2))) * (fy * (d - cov)))

    # Instance method to calculate the two moment capacities for Sagging & Hogging movement
    def moment_capacity(self):
        # Initializing the Beam design types for Sagging & Hogging to None
        BeamDesignType_forsagging = None
        BeamDesignType_forHogging = None

        # Determining the Beam design types
        BeamDesignType_forsagging = "SRS" if self.a_fromTop <= self.a_max_fromTop else "DRS"
        BeamDesignType_forHogging = "SRS" if self.a_fromBott <= self.a_max_fromBott else "DRS"

        print(BeamDesignType_forsagging, BeamDesignType_forHogging)

        # Computing the Sagging capacity based on Beam design type for Sagging movement
        M_cap_Sagg = 0 
        if BeamDesignType_forsagging == "SRS":
            M_cap_Sagg = self._M_cap_sing(Moment.As_bott_prov, Moment.fy, Moment.dFromTop, self.a_fromTop) 
        else:
            M_cap_Sagg = self._M_cap_doub(self.alpha1, Moment.f_c, Moment.bw, self.a_max_fromTop, Moment.dFromTop, Moment.fy, Moment.covTop, Moment.As_bott_prov)

        # Computing the Hogging capacity based on Beam design type for Hogging movement
        M_cap_Hogg = 0
        if BeamDesignType_forHogging == "DRS":
            M_cap_Hogg = self._M_cap_sing(Moment.As_top_prov, Moment.fy, Moment.dFromBott, self.a_fromBott)
        else:
            M_cap_Hogg = self._M_cap_doub(self.alpha1, Moment.f_c, Moment.bw, self.a_max_fromBott, Moment.dFromBott, Moment.fy, Moment.covBott, Moment.As_top_prov)

        # Returning the capacities as a tuple
        return M_cap_Sagg, M_cap_Hogg