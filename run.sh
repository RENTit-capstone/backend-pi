# check if venv exists
if [ ! -d "venv" ]; then
	echo "No Venv found; creating new one for ya..."
	python3 -m venv venv
fi

# go into venv
source venv/Scripts/activate

# install packages
pip install -r requirements.txt

# set environment variable
export USE_GPIO=False

# run FastAPI
uvicorn main:app --host 0.0.0.0 --port 8000

