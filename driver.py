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
    # Unit: MPa
    f_c = data[0]

    # Yield strength of steel
    # Unit: MPa
    fy = data[1]

    # Max concrete strain
    # Unit-less
    ep_cmax = data[2]

    # Modulus of elasticity of steel
    # Unit: MPa
    E_s = data[3]

    # Strength reduction factor for Flexure
    # Unit-less
    phi = data[4]

    # Width of beam
    # Unit: mm
    bw = data[9]

    # Overall depth of the section
    # Unit: mm
    h = data[10]

    # Effective cover (to center of bottom longitudinal reinforcement)
    # Unit: mm
    covBott = data[11]

    # Effective cover (to center of top longitudinal reinforcement)
    # Unit: mm
    covTop = data[12]

    # Bottom main reinforcement
    # Unit: mm^2
    As_bott_prov = data[13]

    # Top main reinforcement
    # Unit: mm^2
    As_top_prov = data[14]

    # Moment imported from analysis result
    # Unit: kN-m
    M = data[15]



    # Beginning of main computation block
    # Effective depth of section (from top)
    # Unit: mm
    dFromTop = h - covBott
    
    # Effective depth of section (from bottom)
    # Unit: mm
    dFromBott = h - covTop

    # Effective depth consideration based on design moment
    # Unit: mm
    d = dFromBott if M < 0 else dFromTop

    # Width factor of equivalent rectangular concrete compressive stress distribution
    # Unit-less
    alpha1 = 0
    if f_c <= 55:
        alpha1 = 0.85
    elif 0.85 - 0.004 * (f_c - 55) < 0.75:
        alpha1 = 0.75
    else:
        alpha1 = 0.85 - 0.004 * (f_c - 55)

    # Height factor of equivalent rectangular concrete compressive stress distribution
    # Unit-less
    beta1 = 0
    if f_c <= 30:
        beta1 = 0.85
    elif 0.85 - 0.008 * (f_c - 30) < 0.85:
        beta1 = 0.85 - 0.008 * (f_c - 30)
    else:
        beta1 = 0.65

    # Depth of actual neutral axis from top
    # Unit: mm
    c_actual_fromTop = (fy * As_bott_prov) / (bw * beta1 * alpha1 * f_c)
    # Depth of actual neutral axis from bottom
    # Unit: mm
    c_actual_fromBott = (fy * As_top_prov) / (bw * beta1 * alpha1 * f_c)

    # Depth of equivalent actual rectangular concrete stress block from top
    # Unit: mm
    a_FromTop = c_actual_fromTop * beta1
    # Depth of equivalent actual rectangular concrete stress block from bottom
    # Unit: mm
    a_FromBott = c_actual_fromBott * beta1

    # Balanced depth of neutral axis from top, cb
    # Unit: mm
    cb_fromTop = (ep_cmax / (ep_cmax + (fy / E_s))) * dFromTop
    # Balanced depth of neutral axis from bottom, cb
    # Unit: mm
    cb_fromBott = (ep_cmax / (ep_cmax + (fy / E_s))) * dFromBott

    # Maximum allowed depth of equivalent rectangular stress block from top
    # Unit: mm
    a_max_fromTop = 0.75 * beta1 * cb_fromTop
    # Maximum allowed depth of equivalent rectangular stress block from bottom
    # Unit: mm
    a_max_fromBott = 0.75 * beta1 * cb_fromBott

    # Design Moment for section
    # Unit: N-m
    M_design = abs(M) * 1000

    # Creating a dictionary of parameters: key is parameter name, value is it's value
    parameters_dict = {
        'f\'c': f_c,
        'fy': fy,

        'bw': bw,
        'covTop': covTop,
        'covBott': covBott,
        'dFromTop': dFromTop,
        'dFromBott': dFromBott,
        'As_bott_prov': As_bott_prov,
        'As_top_prov': As_top_prov,

        'alpha1': alpha1,
        'beta1': beta1,
        'a_FromTop': a_FromTop,
        'a_FromBott': a_FromBott,
        'a_max_fromTop': a_max_fromTop,
        'a_max_fromBott': a_max_fromBott
    }
    # Display parameters computed so far
    print(f'Parameters in driver_test.sm file: {parameters_dict}')

    # _NOTE: ERROR IN THE EXPECTED VALUES OF THE FOLLOWING QUANTITIES:
    # No. Qty: Expected val in moment_capacity.sm, Actual val in developer_test.sm
    # 1. f'c: 45 MPa, 40 MPa
    # 2. fy: 675 MPa, 500 MPa
    # 3. As_top_prov: 525 mm^2, 1000 mm^2
    # 4. beta1 (Not required for further computation): 0.73, 0.77
    # 5. a_fromTop: 160.8234 mm, 134.0196 mm
    # 6. a_fromBott: 30.8824 mm, 49.0196 mm
    # 7. a_maxfromTop: 113.3647 mm, 138.6 mm
    # 8. a_maxFromBott: 113.3647 mm, 138.6 mm
 
    # The final value of the result int the testing scipt has been updated with the correct value to ensure correct testing of the Python code. 

    # Initializing class attributes
    Moment.init_class_attributes(f_c, fy, 
                                 bw, 
                                 covTop, covBott, As_top_prov, As_bott_prov, 
                                 dFromTop, dFromBott)

    # Creating an instance/object of the custom-class Moment
    obj = Moment(alpha1, 
                 a_FromTop, a_FromBott, 
                 a_max_fromTop, a_max_fromBott)

    # Calling the instance method moment_capacity() to calculate the two moment capacities
    # Unit: N-mm
    M_cap_Sagg, M_cap_Hogg = obj.moment_capacity()
    # Displaying the two moment capacities for Sagging & Hogging movement
    print(f'M_cap_Sagg: {M_cap_Sagg:.4e}')
    print(f'M_cap_Hogg: {M_cap_Hogg:.4e}')

    # Computing the Moment capacity
    # Unit: N-mm
    M_cap = M_cap_Hogg * phi if M < 0 else M_cap_Sagg * phi
    # Displaying the Moment capacity
    print(f'M_cap: {M_cap:.4e}')

    # Computing the result: Safety/Utilization factor
    # Factor of 1000 to account for the mismatch in units
    # M_design has unit N-m, while M_cap has unit N-mm
    # Unit-less
    utilityRatioForFlexure = (M_design / M_cap) * 1000

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
    print(f'utilityRatioForFlexure: {utilityRatioForFlexure:.4f}')

# Control flow of execution
if __name__ == '__main__':
    main()