def create(db):
    class MyTable(db.Model):
        __tablename__ = "led_button_log"
        ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
        participantID = db.Column(db.Integer, db.ForeignKey('participant.participantID'))
        answeredOn = db.Column(db.DateTime, nullable=False, default=db.func.now())
        answer = db.Column(db.String)

    class LogSAM(db.Model):
        __tablename__ = "log_SAM"

        logSAMID = db.Column(db.Integer, primary_key=True, autoincrement=True)
        participantID = db.Column(db.Integer, db.ForeignKey('participant.participantID'))
        arousal = db.Column(db.Integer, nullable=False, default=0)
        valence = db.Column(db.Integer, nullable=False, default=0)
        dominance = db.Column(db.Integer, nullable=False, default=0)
        referrer = db.Column(db.String)

    return MyTable, LogSAM

