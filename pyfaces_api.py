###############################
## Based on pyface cmd demo  ##
###############################

from pyfaces import pyfaces
import sys,time

def api_pyface(imgname, dirname, egfaces, thrshld):
    """
    api_pyface(imgname, dirname, egfaces, thrshld)
    return (matchedfile, distance, runtime)
    - produces eigenface images in ./eigenface folder
    - matchedfile and distance could be None based on thrshld
    """
    start = time.time()
    try:
        pyf=pyfaces.PyFaces(imgname,dirname,egfaces,thrshld)
        end = time.time()
        return pyf.matchfile, pyf.mindist, (end-start)
    except Exception,e:
        print e
    

if __name__ == "__main__":
    try:
        start = time.time()
        argsnum=len(sys.argv)
        print "args:",argsnum
        if(argsnum<5):
            print "usage:python pyfacesdemo imgname dirname numofeigenfaces threshold "
            sys.exit(2)                
        imgname=sys.argv[1]
        dirname=sys.argv[2]
        egfaces=int(sys.argv[3])
        thrshld=float(sys.argv[4])
        pyf=pyfaces.PyFaces(imgname,dirname,egfaces,thrshld)
        import ipdb; ipdb.set_trace()
        end = time.time()
        print 'took :',(end-start),'secs'
    except Exception,detail:
        print detail.args
        print "usage:python pyfacesdemo imgname dirname numofeigenfaces threshold "
