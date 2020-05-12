#!/usr/bin/env python

'''ParamGen Tests'''

import os
import argparse
from ftype_namelist import FTypeNamelist

try:
    import yaml
except ModuleNotFoundError:
    print("Cannot import yaml. Exiting...")
    exit()

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-w', metavar='write_directory', type=str, required=True,
                    help='The directory to write out the generated param files')
args = parser.parse_args()


# A dummy case class that imitates CIME.case for testing ParamGen:
class DummyCase:
    def __init__(self, _data):
        self.data = _data
    def get_value(self,var):
        return self.data[var]
        
# A dummy case instance for testing ParamGen
dummy_case = DummyCase({
    'OCN_GRID': 'gx1v6',
    'COMP_ATM': 'datm',
    'NCPL_BASE_PERIOD': 'day',
    'OCN_NCPL': 24,
    'DEBUG': True,
    'TEST': False,
    'OCN_DIAG_MODE': 'none'
    })

# Test Fortran namelist generator:
def fortran_nml_test(write_directory):

    # An example yaml file to generate default input.nml file for FMS:
    input_nml_yaml = \
    '''
    MOM_input_nml:
        output_directory: "'./'"
        restart_input_dir: "'./'"
        restart_output_dir: "'./'"
        parameter_filename: "'MOM_input', 'MOM_override'"
    fms_nml:
        clock_grain: "'ROUTINE'"
        clock_flags: "'NONE'"
        domains_stack_size: 5000000
        stack_size: 0
    diag_manager_nml:
        flush_nc_files:
            $DEBUG or $TEST or $OCN_DIAG_MODE =="development" : .true.
            else : .false.
    '''
    data_dict = yaml.safe_load(input_nml_yaml)

    # Create a ParamGen object with the above yaml data:
    input_nml_obj = FTypeNamelist(data_dict)

    # write out the input.nml file:
    nml_file_path = os.path.join(write_directory, "input.nml")
    input_nml_obj.write(nml_file_path, dummy_case)

    print("namelist file written: {}".format(nml_file_path))


if __name__ == "__main__":
    fortran_nml_test(args.w)
    
