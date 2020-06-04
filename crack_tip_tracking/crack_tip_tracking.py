import numpy as np

def get_N_atoms(filename):
	infile = open(filename,'r')
	for i in range(1):
		infile.readline()
	N = int(infile.readline().split()[0])
	infile.close	
	return N

def skip_title(infile,n):
	for i in range(n):
		infile.readline()

def extract_data(line):
	x       = np.zeros(3)
	words   = line.split() 
	ids 	= int(words[0])
	types 	= int(words[1])
	charge  = float(words[2])
	x[0] 	= float(words[3])
	x[1] 	= float(words[4])
	x[2] 	= float(words[5])
	return ids, types, charge, x

for ishear in range(6):
    # Define paths
    path_shear      = 'shear%s' % (str(ishear*0.10))
    path_perfect    = path_shear + '/ALL_UNMIN'
    path_crack      = path_shear + '/ALL_MIN'
    output          = 'shear%s.txt' % (str(ishear*0.10))
    conf_perfect    = 'crack_0_P.txt'
    
    # Open perfect configuration and get data
    p_name = path_perfect + '/' + conf_perfect
    N_atoms = get_N_atoms(p_name)
    p_file = open(p_name, 'r')
    skip_title(p_file,11)
    
    # Look for the atom nearest to the crack tip
    dist_0 = 100.0
    for line in p_file:
        ids, types, charge, x = extract_data(line)
        dist_1 = np.sqrt(x[0]**2 + x[1]**2)
        if (dist_1 < dist_0):
            id_crack_tip = ids
            dist_0 = dist_1
    p_file.close()
    
    # Get the coordinates of the crack tip atom over time
    outfile = open(output, 'w')
    for step in range(101):
        conf_crack = 'crack_%s_L.txt' % (str(step))
        c_name = path_crack + '/' + conf_crack
        c_file = open(c_name, 'r')
        skip_title(c_file,10)
        for line in c_file:
            ids, types, charge, x = extract_data(line)
            if (ids == id_crack_tip):
                outfile.write('%6d %6d %6d %14.6f %14.6f %14.6f %14.6f\n' % (step, ids, types, charge, x[0], x[1], x[2]))
                break
    outfile.close()
