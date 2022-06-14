from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
from exporter import save_to_file

app = Flask('SuperScrapper')

db = {}

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/report")
def report():
  word = request.args.get('word')
  if word:
    word = word.lower()
    existingJobs = db.get(word)
    # from db is null ( empty ) so it skips if 
    if existingJobs:
      jobs = existingJobs
    else:
      # scrapper works 
      jobs = get_jobs(word)
      #after scrapping is done it gets saved in the database array so if there's another request in the future it would look at db array
      db[word] = jobs
  else:
    return redirect('/')
    
  return render_template(
    'report.html', 
    searchingBy=word, 
    resultsNumber=len(jobs),
    jobs = jobs 
  )


@app.route("/export")
def export():
  try:
    word = request.args.get('word')
    if not word:
      raise Exception()
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file('jobs.csv')
  except:
    return redirect("/")
  
app.run(host="0.0.0.0", port=8080)