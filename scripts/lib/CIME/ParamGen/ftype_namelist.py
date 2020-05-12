import os
from param_gen import ParamGen

class FTypeNamelist(ParamGen):
    """Derived ParamGen class to generate Fortran namelist input files"""

    def _validate_schema(self, data_dict):
        """Schema checker for Fortran namelist files."""

        try:
            import schema
        except ModuleNotFoundError:
            print("Warning: schema module not found. Skipping schema validation...")
            return

        # Impose the general structure and entry types:
        valid_data = schema.Schema({str: schema.And(
                                        {str: schema.And(str,int,float,bool)},
                                        {str: 
                                            {str: schema.And(str,int,float,bool)}})
                                    })
        # TODO: add more schema checks.

        return True


    def write(self, output_path, case):
        """write method for Fortran namelist syntax."""

        # Expand cime parameters (e.g., $INPUTDIR)
        self.expand_case_vars(case)

        # Infer ultimate param values
        self.infer_values(case)

        # Write out .nml file:
        with open(os.path.join(output_path), 'w') as input_nml:
            for module in self._data:
                input_nml.write("&"+module+"\n")

                for var in self._data[module]:
                    val = self._data[module][var]
                    if val==None:
                        continue
                    input_nml.write("    "+var+" = "+str(self._data[module][var])+"\n")

                input_nml.write('/\n\n')


