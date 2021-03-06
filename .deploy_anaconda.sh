set -e

wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
bash miniconda.sh -b -p $HOME/miniconda
export PATH=$HOME/miniconda/bin:$PATH

conda update --yes -q conda
conda config --set always_yes true
conda config --set anaconda_upload yes
conda config --add channels neutronpy

conda install -q python=$TRAVIS_PYTHON_VERSION pip conda-build anaconda-client
conda build --user neutronpy --token $CONDA_TOKEN ./conda-recipe

exit 0