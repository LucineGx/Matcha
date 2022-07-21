BASEDIR=$(readlink -f $0 | xargs dirname)
export FLASK_APP=$BASEDIR/flaskr
export FLASK_ENV=development
python3 -m flask init-db &
wait $!
python3 -m flask run > ../api.log 2> ../api.log