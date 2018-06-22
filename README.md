# Ramsey Game
> This is implementation of ramsey game, it is graph, mathematical game.
 Rules of game: http://pi.math.cornell.edu/~mec/2003-2004/graphtheory/ramsey/howtoplayramsey.html
 
## Demo
It is available on heroku server:
http://ramsey-game.herokuapp.com/#/

## How to prepare local environment
1. Install frontend dependencies
```bash
cd ramsey_front
yarn install
```
2. Install backend dependencies 
```bash
cd ramsey_server
# virtual env recommended
pip install -r requirements.txt  
```

## How to run it locally?
1. start the frontend server
```bash
cd ramsey_front
yarn run dev
```
2. start backend server 
```bash
./start_server
```
3. Applications are accessible under
    - front - localhost:8080
    - backend - localhost:8000 -> will serve prebuild version of front on /

## How to deploy to heroku
1. checkout to the heroku branch
2. build new fronted with command TODO: move it to the ci
```bash
cd ramsey_front
yarn run build
```
3. push new version to the heroku branch

