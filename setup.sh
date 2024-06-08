#! /bin/sh
REQUIREMENTS='./requirements.txt'
venv_tag='juggling_detection'
venv_name="${venv_tag}_venv"
echo "Setting up virtual environment ($venv_name)" 1>&2
python -m venv "$venv_name"
echo "Activating ($venv_name)" 1>&2
source ./$venv_name/bin/activate
if [[ -e "$REQUIREMENTS" ]]; then
    echo "Installing modules in $REQUIREMENTS" 1>&2
    pip install -r $REQUIREMENTS
fi
echo "Deactivating ($venv_name)" 1>&2
deactivate
echo "$venv_name" > .autovenv
echo 'Use 'source $PWD/"$venv_name"/bin/activate' to reactivate (venv), or use autovenv.' 1>&2

