import re
import numpy as np
import parser_functions
import encode_vitaltable

def main():
    
    filename = 'test_wave'
    num_of_waves = 20
    
    # formula = 'sin(2*pi*(3+ (y*19))*x ) + sin(2*pi*(abs(4 - (y*19)))*x * (y*19)) + sin(2*pi*5*x * (y*19))'

    # formula = 'avg( sin(2*pi*x), sin(2*pi*w*x)>0.5, sin(2*pi*x)*(sin(2*pi*(w+3)*x)>0.5))'

    # formula = ' case( abs(sin(2*pi*2*(x)))>0.5, sin(2*pi*x*w), 0 ) '

    # formula = '2*avg(sin((2*w-1)*x*pi),(1-(2*w-1))*rand*0.1)'
   
    # formula = ' case( abs(sin(2*pi*2*x))>0.5, cos(2*pi*x*w*(2)), sin(2*pi*x*w*(-2)) )'
    
    formula = 'sum( sin(2*pi*x*(7*i*(-w)))*(1/(7*i)) , i ,1, 40) + 2*sum( sin(2*pi*x*2*i*w)*(1/(i*2)) , i ,1, 40) '
    
    # formula = 'sum(avg( sin(2*pi*x*i)/(2*i), abs(sin(2*pi*w*x))>0.5) , i,1,40 )'
    
    # formula = 'log2(2 - sin(2*pi*x*w))'

    execute(formula, num_of_waves, filename)
    


def execute(formula, num_of_waves, filename):
    
    formula = formula.replace(' ', '')

    pattern = re.compile('[^a-zA-Z0-9\._]')
    result = pattern.finditer(formula)
    
    
    splited_formula= []
    p = 0
    for i in result:
            if p!=i.start():
                splited_formula.append(formula[p:i.start()])
            p = i.start()+1
            splited_formula.append(i[0])
            
    splited_formula.append(formula[p:])
    
    splited_formula = [word for word in splited_formula if word]
        
    splited_formula = parser_functions.expand_sum(splited_formula)
  
    if num_of_waves==1:
        return [parser_functions.read_formula(splited_formula)], [0]
    
    w = np.arange(num_of_waves)+1
    
    y = np.arange(num_of_waves)/(num_of_waves-1)
    
    positions = np.floor(y*256)
    
    wave_list = []
    
    for i in range(num_of_waves):
        formula = parser_functions.subs(splited_formula,'y', y[i])
        formula = parser_functions.subs(formula,'w', w[i])
        formula = parser_functions.subs(formula,'rand', np.random.rand(2048)-0.5)
              
        wave_list.append(formula)
        
    waves = [parser_functions.read_formula(i) for i in wave_list]
    
    if type(waves[0])!=np.ndarray:
        print(waves)
    else:

        m = max([np.max(np.abs(i)) for i in waves])
            
        waves = [i/m for i in waves]

        encode_vitaltable.create_vitaltable(positions, waves, filename)
    
    return 

main()