python -m pip install --upgrade pip
pip install sakee
pip install html-testRunner
pip install parameterized
export PYTHONPATH=$PWD
export KODI_INTERACTIVE=0
export KODI_HOME=$PWD/tests/home
if (( $# >= 1 ))
then
  export KOD_TST_CH=$1
fi
python tests/test_generic.py