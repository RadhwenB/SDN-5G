from app import db


class Association(db.Model):
    __tablename__ = "associations"

    id = db.Column(db.Integer, primary_key=True,nullable=False)
    node_id = db.Column(db.String(20), unique=True, nullable=False)
    creation_datetime = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Association %r\nNODE_ID : %r\nCreation Datetime :%r>\n' % (self.id,self.node_id,self.creation_datetime.strftime("%Y-%m-%d %H:%M"))
        #return f"Association('{self.id}','{self.node_id}','{self.creation_datetime}')"


class Session(db.Model):
    __tablename__ = "sessions"

    id = db.Column(db.Integer, primary_key=True,nullable=False)
    cp_seid = db.Column(db.Integer, unique=True)
    up_seid = db.Column(db.Integer, unique=True)
    association_id = db.Column(db.Integer,db.ForeignKey('associations.id'), nullable=False)
    source_interface = db.Column(db.String)
    destination_interface = db.Column(db.String)
    header_operation=db.Column(db.String)
    action=db.Column(db.String)
    ue_ip_address=db.Column(db.String)
    creation_datetime = db.Column(db.DateTime, nullable=False)


    def __repr__(self):
        return '<Session %r\nCP SEID : %r\nUP SEID : %r\nAssociation ID : %r\nSource Interface : %r\n\
        Destination Interface : %r\nHeader Operation : %r\nAction : %r\nUE IP Address : %r\nCreation Datetime :%r>\n' % \
        (self.id,self.cp_seid,self.up_seid,self.association_id,self.source_interface,self.destination_interface,self.header_operation,\
        self.action,self.ue_ip_address,self.creation_datetime.strftime("%Y-%m-%d %H:%M"))
        #return f"Session('{self.id}', '{self.cp_seid}', '{self.up_seid}', '{self.association_id}', '{self.creation_datetime}')"
