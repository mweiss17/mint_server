import models
from models import Result
from app import app, db
from flask import Flask
from pprint import pprint
from redis import Redis
from rq import Queue

@app.route("/mint")
def mint():
    # get my most recent result
    result = Result.query.order_by(Result.created_date).first()
    print(result.created_date - datetime.datetime.utcnow() )
    if result and datetime.datetime.utcnow() - result.created_date < datetime.timedelta(83600):
        # Enqueue a job
        q = Queue(connection=Redis())
        q.enqueue(job, result.id)
    # if the most recent result is within the last day, return it
    transactions = result.transactions
    budgets = result.budgets
    return json.dumps({"transactions": transactions, "budget": budgets})

# This is the job
def job(result_id):
    result = Result.query.get(result_id).one()
    try:
        mint = mintapi.Mint(result.mint_email, result.mint_password)
    except:
        pass
    budgets = mint.get_budgets()
    transactions = json.loads(mint.get_transactions().to_json())
    try:
        result = Result(budgets=budgets, transactions=transactions)
        db.session.add(result)
        db.session.commit()
    except:
        pass
    return json.dumps(budgets)


@app.route("/money")
def money():
    return json.dumps({"transactions": [1, 2, 3]})
