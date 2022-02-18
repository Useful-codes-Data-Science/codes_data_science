# Code to install libraries from Jupyter Lab in current environment
# (Código para instalar librerias desde Jupyter Lab en el environment actual) 
# Link reference: (https://jakevdp.github.io/blog/2017/12/05/installing-python-packages-from-jupyter/)
# Example with library tqdm
import sys
!conda install --yes --prefix {sys.prefix} tqdm