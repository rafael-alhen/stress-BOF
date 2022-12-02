import datetime
from flask import Blueprint, render_template
from BOFS.util import *
from BOFS.globals import db
from BOFS.admin.util import verify_admin

# The name of this variable must match the folder's name.
my_blueprint = Blueprint('my_blueprint', __name__,
                         static_url_path='/my_blueprint',
                         template_folder='templates',
                         static_folder='static')


@my_blueprint.route("/task", methods=['POST', 'GET'])
@verify_correct_page
@verify_session_valid
def task():
    incorrect = None

    if request.method == 'POST':
        log = db.MyTable()
        log.participantID = session['participantID']
        log.answer = request.form['answer']

        db.session.add(log)
        db.session.commit()

        if log.answer.lower() == "linux":
            return redirect("/redirect_next_page")
        incorrect = True

    return render_template("task_sam.html", example="This is example text.", incorrect=incorrect)

@my_blueprint.route("/outro", methods=['GET', 'POST'])
@verify_correct_page
@verify_session_valid
def ending_outro():
    return render_template("outro.html")


@my_blueprint.route("/analysis")
@verify_admin
def analysis():
    results = db.session.query(
            db.Participant.participantID,
            db.func.count(db.MyTable.ID).label('tries')
        ).\
        join(db.MyTable, db.MyTable.participantID == db.Participant.participantID).\
        filter(db.Participant.finished).\
        group_by(db.MyTable.participantID)

    return render_template("analysis.html", results=results)



sam = Blueprint('sam', __name__,
                url_prefix='/sam',
                static_url_path='/sam',
                static_folder='static',
                template_folder='templates')


@my_blueprint.route("/task_sam", methods=['GET', 'POST'])
@my_blueprint.route("/task_sam2", methods=['GET', 'POST'])
@my_blueprint.route("/task_sam3", methods=['GET', 'POST'])
@verify_session_valid
@verify_correct_page
def self_assessment_manikin():
    return render_template("task_sam.html")


@my_blueprint.route("/log_sam", methods=['POST'])
def log_sam():
    print(request.referrer)

    message = request.form['message']
    if message == "logSAM":
        log_entry = db.LogSAM()
        pid = request.form['pid']
        #if db.session.query(db.LogSAM).filter(db.LogSAM.participantID == pid).first() is not None:
        #    #print("There is already a SAM db entry for pid={pid}".format(pid=pid))
        #    return ""
        log_entry.participantID = session['participantID']
        log_entry.participantID = pid
        log_entry.arousal = request.form['arousal']
        log_entry.valence = request.form['valence']
        log_entry.dominance = request.form['dominance']
        log_entry.referrer = request.referrer

        db.session.add(log_entry)
        db.session.commit()
    return ""

