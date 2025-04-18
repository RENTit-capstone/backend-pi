# check if venv exists
if [ ! -d "venv" ]; then
	echo "No Venv found; creating new one for ya..."
	python3 -m venv venv
fi

# go into venv
source venv/bin/activate

# install packages
pip install -r requirements.txt

# run FastAPI
uvicorn main:app --host 0.0.0.0 --port 8000

