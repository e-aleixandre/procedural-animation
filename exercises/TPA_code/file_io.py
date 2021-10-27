import sys

from time import localtime, strftime

valid_sph_params = ['density',\
                    'visco',\
                    'stiff',\
                    'surften',\
                    'surften_threshold',\
                    'polymer',\
                    'polymer_concentration',\
                    'polymer_tau',\
                    'polymer_k',\
                    'collision_restitution',\
                    'gravity']

sph_attributes = {'density':'density0',\
                  'visco':'viscosity',\
                  'stiff':'stiffness',\
                  'surften':'surften',\
                  'surften_threshold':'surften_threshold',\
                  'polymer':'polymer',\
                  'polymer_concentration':'polymer_concentration',\
                  'polymer_tau':'polymer_tau',\
                  'polymer_k':'polymer_k',\
                  'collision_restitution':'col_restitution',\
                  'gravity':'gravity'}

valid_scene_params = ['name',\
                      'nparts',
                      'fluid_volume',\
                      'kernel_parts',\
                      'tini',\
                      'tfin',\
                      'tstep',\
                      'fintol',\
                      'parallel',\
                      'nprocs',\
                      'gravity']

scene_attributes = {'name':'label',\
                    'nparts':'nparts',\
                    'fluid_volume':'fluid_volume',\
                    'kernel_parts':'kernel_parts',\
                    'tini':'t_ini',\
                    'tfin':'t_fin',\
                    'tstep':'t_step',\
                    'fintol':'final_step_tol',\
                    'parallel':'parallel',\
                    'nprocs':'nprocs',\
                    'gravity':'gravity'}




def save_scene(sim):

    f = open(sim.scene_file,'w')

    f.write("# Created {}\n".format(strftime("%Y-%m-%d_%H.%M.%S",localtime())))
    for prm in valid_scene_params:
        f.write("{}={}\n".format(prm,getattr(sim,scene_attributes[prm])))

    f.close()
    
###


def load_scene(scene_file,sim=None):
    params_read = {}
    
    f = open(scene_file,'r')
    file_lines = f.readlines()
    f.close()

    for line in file_lines:
        param = line.split('=')
        if param[0].strip()[0] == '#':
            continue
        if len(param) != 2:
            sys.stderr.write("WARNING: format error {}. Ignoring.\n".format(line))
            continue

        tag = param[0].strip()
        value = param[1].strip('\n')

        if tag not in valid_scene_params:
            sys.stderr.write("WARNING: while reading file {}, found invalid label {}. Ignored\n".format(scene_file,tag))
            continue
        if tag in params_read:
            sys.stderr.write("WARNING: while reading file {} found again label {} with value {}. Ignored\n".format(scene_file,tag,value))
            continue

        print("READ:{}={}".format(tag,value))
        if tag == 'name':
            # this is a string
            params_read[tag]=value
        else:
            params_read[tag]=eval(value)
        #
    #
    if sim is None:
        return params_read
    
    for p in params_read:
        setattr(sim,scene_attributes[p],params_read[p])
###


def load_domain(filename):
    try:
        f = open(filename,'r')
        data = f.readlines()
        f.close()

        if len(data) != 1:
            sys.stderr.write("LOAD ERROR: File format error in "+filename)
            return [None]*6
        
        dom = list(map(float,data[0].strip().split(' ')))
        
        if len(dom) != 6:
            sys.stderr.write("LOAD ERROR: File format error in "+filename)
            return [None]*6
        
        return dom

    except (FileNotFoundError, IOError):
        sys.stderr.write("LOAD ERROR: File IO error in "+filename)
        return [None]*6


def save_domain(filename,dom):
    try:
        f = open(filename,'w')
        f.write(str(dom)) # dom can be converted to str
        f.close()
    except (FileNotFoundError, IOError):
        sys.stderr.write("LOAD ERROR: File IO error in "+filename)


def save_state(filename,system,t=0.0):
    parts = system.particles

    f = open(filename,'w')
    f.write(str(t)+" "+str(parts.n) + "\n")
    for p in range(parts.n):
        pos = parts.get_pos(p)
        f.write(str(float(pos[0])) + " " + str(float(pos[1])) + " " + str(float(pos[2])) + " ")
    f.write("\n")
    for p in range(parts.n):
        vel = parts.get_vel(p)
        f.write(str(float(vel[0])) + " " + str(float(vel[1])) + " " + str(float(vel[2])) + " ")
    f.write("\n")
    f.close()
###


def save_step(filename_base,system,t,num,numlength=4):
    cad_num = '{:0{places}d}'.format(num,places=str(numlength))
    filename = filename_base + "_" + cad_num

    filename = filename + ".dat"
    save_state(filename,system,t)
###




def read_step(fname_root,system,num,numlength=4):
    cad_num = '{:0{places}d}'.format(num,places=str(numlength))
    filename = fname_root + cad_num + ".dat"
    print("Reading "+filename+"...")
    
    return read_state(filename,system)



def read_state(filename,system=None):

    try:
        f = open(filename,'r')
        data = f.readlines()
        f.close()
        print("        ...I did read "+filename)
        if len(data) != 3:
            sys.stderr.write("LOAD ERROR: File format error in "+filename)
            raise IOError

        line0 = data[0].split(' ')
        t = float(line0[0])
        pos = list(map(float,data[1].strip().split(' ')))
        vel = list(map(float,data[2].strip().split(' ')))

        if system is not None:
            n = int(len(pos)/3.0)
            parts = system.particles
        
            if n != parts.n:
                sys.stderr.write("LOAD ERROR: size of particle system ")
                sys.stderr.write("{} difers from initial condition file {}.\n".format(parts.n,n))
                raise IOError
            
            for i in range(n):
                parts.set_pos(i,pos[3*i:3*i+3])
                parts.set_vel(i,vel[3*i:3*i+3])
        
        #            
    except (FileNotFoundError, IOError):
        sys.stderr.write("LOAD ERROR: File IO error in {}\n".format(filename))
        t = None
        pos = None
        vel = None
    #
    
    return [t,pos,vel]
###



def save_sph_params(fname,s):
    f = open(fname,'w')
    f.write("# Created {}\n".format(strftime("%Y-%m-%d_%H.%M.%S",localtime())))
    f.write("density={}\n".format(s.density0))
    f.write("visco={}\n".format(s.viscosity))
    f.write("stiff={}\n".format(s.stiffness))
    f.write("surften={}\n".format(s.surften))
    f.write("surften_threshold={}\n".format(s.surften_threshold))
    f.write("collision_restitution={}\n".format(s.col_restitution))
    f.write("gravity={}\n".format(s.gravity))
    f.write("smoothing_length={}\n".format(s.h))
    f.close()
###

    

def load_sph_params(fname,s=None):
    params_read = {}
    f = open(fname,'r')
    file_lines = f.readlines()
    f.close()
    
    
    for line in file_lines:
        param = line.split('=')
        if param[0].strip()[0] == '#':
            continue
        if len(param) != 2:
            sys.stderr.write("WARNING: format error {}. Ignoring.\n".format(line))
            continue

        tag = param[0].strip()
        value = param[1].strip('\n')

        if tag not in valid_sph_params:
            sys.stderr.write("WARNING: while reading file {}, found invalid label {}. Ignored\n".format(fname,tag))
            continue
        if tag in params_read:
            sys.stderr.write("WARNING: while reading file {} found again label {} with value {}. Ignored\n".format(fname,tag,value))
            continue
        params_read[tag]=eval(value)
    
    if s is None:
        return params_read

    for p in params_read:
        setattr(s,sph_attributes[p],params_read[p])
###
