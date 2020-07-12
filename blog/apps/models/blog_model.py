from exts import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username= db.Column(db.String(12), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)

    def __str__(self):
        return self.username


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(12), nullable=False, unique=True)
    tmin = db.Column(db.String(64), nullable=False)


class Ave_data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(12), nullable=False, unique=True)
    average = db.Column(db.String(64), nullable=False)

    def __str__(self):
        return self.username

class 全国(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(12), nullable=False, unique=True)
    data = db.Column(db.String(64), nullable=False)

    def __str__(self):
        return self.username

class 新疆(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(12), nullable=False, unique=True)
    data = db.Column(db.String(64), nullable=False)

    def __str__(self):
        return self.username

class weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(12), nullable=False, unique=True)
    max = db.Column(db.String(64), nullable=False)
    min = db.Column(db.String(64), nullable=False)
    ave = db.Column(db.String(64), nullable=False)

    def __str__(self):
        return self.username

class weather_real(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(12), nullable=False, unique=True)
    max = db.Column(db.String(64), nullable=False)
    min = db.Column(db.String(64), nullable=False)
    ave = db.Column(db.String(64), nullable=False)

    def __str__(self):
        return self.username

class weather_con(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(12), nullable=False, unique=True)
    max = db.Column(db.String(64), nullable=False)
    min = db.Column(db.String(64), nullable=False)
    ave = db.Column(db.String(64), nullable=False)

    def __str__(self):
        return self.username

class 人员管理(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    position = db.Column(db.String(12), nullable=False)
    department = db.Column(db.String(64), nullable=False)

    def __str__(self):
        return self.username