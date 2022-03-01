import altiwx
import subprocess
import os
import datetime
import time
import sys


try:
    # enhencements that should be calculated
    enh = ["HVCT", "MSA", "HVC", "HVC", "HVC-precip",
       "HVCT", "HVCT-precip", "MCIR", "MCIR-precip"]

    # define tmporary directory to use while calculating - mind the slash at the end
    tempdir = "/tmp/"

    # creating a dateobject from the filename
    #datetime_object = datetime.strptime(os.path.splitext(
    #    os.path.split(
    #        os.path.abspath(altiwx.input_file)
    #    )[1]
    #)[0], '%Y%m%dT%H%M%SZ')

    abspath = os.path.abspath(altiwx.input_file)
    #altiwx.debug("abspath = " + abspath)

    split1 = os.path.split(abspath)[1]
    #altiwx.debug("split[1] = " + split1)

    splitext0 = os.path.splitext(split1)[0]
    #altiwx.debug("splitext[0] = " + splitext0)

    try:
        datetime_object = datetime.datetime.strptime(splitext0, '%Y%m%dT%H%M%SZ')
    except TypeError:
        datetime_object = datetime.datetime(*(time.strptime(splitext0, '%Y%m%dT%H%M%SZ')[0:6]))
    #altiwx.debug("strptime")

    output_file = os.path.splitext(os.path.basename(os.path.abspath(altiwx.input_file)))[0]

    #altiwx.debug("dbg point");

    command = "cp '"+altiwx.input_file+"' " + tempdir

    altiwx.info("Processing NOAA APT data...(extended version)")

    altiwx.debug(command)
    subprocess.Popen([command], shell=1).wait()


    wavfile = tempdir+output_file


    outflag = "-N "
    if altiwx.southbound:
        outflag = "-S "

    command = "wxmap -T '"+altiwx.satellite_name+"' -H 'noaa.txt' '" + \
        datetime_object.strftime("%d %m %Y %H:%M:%S") + "' "+tempdir+output_file+"_map.png"


    altiwx.debug(command)
    subprocess.Popen([command], shell=1).wait()

    mapfile = tempdir+output_file+"_map.png"
    outflag = outflag + "-m '"+mapfile+"'"

    outdir = os.path.dirname(os.path.abspath(altiwx.input_file)) + "/"

    command = "wxtoimg " + outflag + " '" + altiwx.input_file + "' '" + outdir + output_file + "_raw.png'"
    altiwx.debug(command)
    subprocess.Popen([command], shell=1).wait()

    for enhencement in enh:
        command = "wxtoimg " + outflag + " -e " + enhencement + " '" + \
            altiwx.input_file + "' '" + outdir + output_file + "_" + enhencement + ".png'"
        altiwx.debug(command)
        subprocess.Popen([command], shell=1).wait()
    altiwx.info("Done processing NOAA APT data!")

except Exception as e:
    exception_type, exception_object, exception_traceback = sys.exc_info()
    filename = exception_traceback.tb_frame.f_code.co_filename
    line_number = exception_traceback.tb_lineno

    print("Exception type: ", exception_type)
    print("Object: ", exception_object)
    print("Traceback: ", exception_traceback)
    print("File name: ", filename)
    print("Line number: ", line_number)
