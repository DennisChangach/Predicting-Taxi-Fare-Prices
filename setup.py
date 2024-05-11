from setuptools import find_packages,setup
from typing import List

#Removing the '-e .' from the requirements list; '-e .' is used to run the setup.py filr
HYPHEN_E_DOT='-e .'

#Defining the get requirements function -> Function should return a list
def get_requirements(file_path:str)->List[str]:
    """
    This function will return a list of requirements
    
    """
    requirements = []
    #open the requirements.txt file
    with open(file_path) as file_obj:
        #reading lines in the file
        requirements = file_obj.readlines()
        #Replacing the end line character \n with blank
        requirements = [req.replace("\n","") for req in requirements]

        #Removing -e .  from requirements
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

    return requirements


setup(
name = "predictfareprice",
version = '0.0.1',
author = 'Changach',
author_email = "kogeidennis@gmail.com",
packages= find_packages(),
#using the get_requirements function to fetch the libararies needed to be installed for the ML app to run
install_requires = get_requirements('requirements.txt')

)