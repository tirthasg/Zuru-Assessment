# Importing the user-defined moment module
from moment import Moment    

# Validate the input data dump
def validate_data(data_dump):
    # Checking whether two few or many input is provided
    # Raise Exception if that's the case
    if len(data_dump) != 26:
        raise Exception("Input is either too long or too short!")

    # Slicing the range which consists of input of interest
    data = data_dump[8:-2]

    # Checking whether the data can be represented by floating-point numbers
    # Raise Exception otherwise
    for value in data:
        try:
            float(value)
        except (ValueError, TypeError):
            raise Exception("Illegal Input!")

# Take input from console
def take_input():
    # Take input
    data_dump = (input().strip().split())
    # Validate the input data
    validate_data(data_dump)

    # Convert the valid input data to float data-type
    data = list(map(float, data_dump[8:-2])) 

    # Return the data to be consumed by other functions
    return data

# Compute the result
def beam_verification(data):
    # Assigning references to inputs of interest
    # Compressive strength of concrete
    f_c = data[0]
    # Yield strength of steel
    fy = data[1]
    # Max concrete strain
    ep_cmax = data[2]
    # Modulus of elasticity of steel
    E_s = data[3]
    # Strength reduction factor for Flexure
    phi = data[4]
    # Width of beam
    bw = data[9]
    # Overall depth of the section
    h = data[10]
    # Effective cover (to center of bottom longitudinal reinforcement)
    covBott = data[11]
    # Effective cover (to center of top longitudinal reinforcement)
    covTop = data[12]
    # Bottom main reinforcement
    As_bott_prov = data[13]
    # Top main reinforcement
    As_top_prov = data[14]
    # Moment imported from analysis result
    M = data[15]



    # Beginning of main computation block
    # Effective depth of section (from top)
    dFromTop = h - covBott
    # Effective depth of section (from bottom)
    dFromBott = h - covTop
    # Effective depth consideration based on design moment
    d = dFromBott if M < 0 else dFromTop

    # Width factor of equivalent rectangular concrete compressive stress distribution
    alpha1 = None
    if f_c <= 55:
        alpha1 = 0.85
    elif 0.85 - 0.004 * (f_c - 55) < 0.75:
        alpha1 = 0.75
    else:
        alpha1 = 0.85 - 0.004 * (f_c - 55)

    # Height factor of equivalent rectangular concrete compressive stress distribution
    beta1 = None
    if f_c <= 30:
        beta1 = 0.85
    elif 0.85 - 0.008 * (f_c - 30) < 0.85:
        beta1 = 0.85 - 0.008 * (f_c - 30)
    else:
        beta1 = 0.65

    # Depth of actual neutral axis from top
    c_actual_fromTop = (fy * As_bott_prov) / (bw * beta1 * alpha1 * f_c)
    # Depth of actual neutral axis from bottom
    c_actual_fromBott = (fy * As_top_prov) / (bw * beta1 * alpha1 * f_c)

    # Depth of equivalent actual rectangular concrete stress block from top
    a_FromTop = c_actual_fromTop * beta1
    # Depth of equivalent actual rectangular concrete stress block from bottom
    a_FromBott = c_actual_fromBott * beta1

    # Balanced depth of neutral axis from top, cb
    cb_fromTop = (ep_cmax / (ep_cmax + fy / E_s)) * dFromTop
    # Balanced depth of neutral axis from bottom, cb
    cb_fromBott = (ep_cmax / (ep_cmax + fy / E_s)) * dFromBott

    # Maximum allowed depth of equivalent rectangular stress block from top
    a_max_fromTop = 0.75 * beta1 * cb_fromTop
    # Maximum allowed depth of equivalent rectangular stress block from bottom
    a_max_fromBott = 0.75 * beta1 * cb_fromBott

    # Design Moment for section
    M_design = abs(M) * 10000

    # Initializing class attributes
    Moment.init_class_attributes(f_c, fy, 
                                bw, 
                                covTop, covBott, As_top_prov, As_bott_prov, 
                                dFromTop, dFromBott)

    # Creating an instance/object of the custom-class Moment
    obj = Moment(alpha1, 
                dFromTop, a_FromBott, 
                a_max_fromTop, a_max_fromBott)

    # Calling the instance method moment_capacity() to calculate the two moment capacities
    M_cap_Sagg, M_cap_Hogg = obj.moment_capacity()
    # Displaying the two moment capacities for Sagging & Hogging movement
    # print('{:.4e}'.format(M_cap_Sagg))
    # print('{:.4e}'.format(M_cap_Hogg))

    # Computing the Moment capacity
    M_cap = M_cap_Hogg * phi if M < 0 else M_cap_Sagg * phi
    # Displaying the Moment capacity
    # print('{:.4e}'.format(M_cap))

    # Computing the result: Safety/Utilization factor
    utilityRatioForFlexure = (M_design / M_cap) * 100

    # Return the result
    return utilityRatioForFlexure

# Main program
def main():
    # Taking input
    # Example of a legal input: 
    # 150 1.25G+1.5Q+EQxx DEAD+LIVE+EARTHQUAKE ULS 40 3 10 3 40 500 0.003 200000 0.85 1.00 8 300 450 300 500 60 60 2734 1000 -100 150 20
    data = take_input()

    # Computing the result: Safety/Utilization factor
    utilityRatioForFlexure = beam_verification(data)

    # Displaying the result upto 4 digits after decimal point
    print("{:.4f}".format(utilityRatioForFlexure))

# Control flow of execution
if __name__ == '__main__':
    main()