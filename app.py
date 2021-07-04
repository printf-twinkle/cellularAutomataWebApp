#90,150; 30,120; 30,30
from logging import error
from flask import Flask, render_template, redirect, url_for, send_file, send_from_directory, safe_join, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask.globals import request
import random
from PIL import Image
from database import save_creds, check_creds, get_user, get_user1, get_pass
from util_tools import send_mail
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = '12345789'
app.config["CLIENT_IMAGES"] = "./static/img"
login_manager = LoginManager()
login_manager.login_view = 'home'
login_manager.init_app(app)

# home page takes all the inputs from client to server side


@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    return render_template("new_home.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        error_msg = ""
        email_id = request.form.get("email_id")
        password = request.form.get("password")
        usr = get_user(email_id, password)
        if usr:
            login_user(usr, remember=True)
        else:
            error_msg = "Invalid Login credentials"
            return render_template("new_home.html", error_msg=error_msg)
        return redirect(url_for('main'))

    return render_template("new_home.html")


@app.route("/register_page")
def register_page():
    return render_template("new_register.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    success_msg = ""
    error_msg = ""
    usr_exists_msg = ""
    if request.method == "POST":
        name = request.form.get("name")
        email_id = request.form.get("email_id")
        password = request.form.get("password")
        user_type = 2
        if get_user(email_id, password):
            usr_exists_msg = "User already exists!!"
        elif save_creds(name, email_id, password, user_type):
            print("Registered successfully okayy!!")
            success_msg = "Registered successfully!!"
        else:
            print("Sorry! Unexpected Error!!")
    return render_template("new_register.html", error_msg=error_msg, success_msg=success_msg, usr_exists_msg=usr_exists_msg)


@app.route('/forgotpass', methods=["POST", "GET"])
def forgotpass():
    msg = ""
    err_msg = ""
    if request.method == "POST":
        getmail = request.form["sendmail"]
        s = get_pass(getmail)
        print(s)
        if s == None:
            return render_template("forgotpass.html", err_msg="This email-id does not exist!")
        send_mail(getmail, s)
        return render_template("forgotpass.html", msg="Email sent!")
    return render_template("forgotpass.html")


@app.route('/main', methods=["POST", "GET"])
@login_required
def main():
    print(current_user.get_id())
    list_of_initial_states = []
    list_of_rule_vectors = []
    list_of_matrix_rows = []
    list_of_matrix_cols = []
    list_of_next_states = []
    new_row = []

    list_of_linear = ['12', '72', '68', '132', '204', '192', '48', '60', '120', '116', '180', '184', '252', '240',
                      '18', '30', '90', '86', '150', '154', '222', '210', '34', '46', '106', '102', '166', '170', '238', '226', '136']
    list_of_non_linear = []

    def hex_to_rgb(value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    for i in range(1, 256):
        if str(i) not in list_of_linear:
            list_of_non_linear.append(str(i))
    if request.method == "POST":
        # print(request.form)
        color_pickers = []
        pick1 = request.form.get("pick1")
        rgb_val_1 = hex_to_rgb(pick1)
        color_pickers.append(rgb_val_1)
        if request.form.get("pick2"):
            color_pickers.append(hex_to_rgb(request.form.get("pick2")))
        else:
            color_pickers.append((0, 0, 0))
        if request.form.get("pick3"):
            color_pickers.append(hex_to_rgb(request.form.get("pick3")))

        # print(rgb_val)
        boundaries = request.form.get("boundaries")
        rule = request.form.get("rule")
        img_dimension_width = int(request.form.get("img_dimension_width"))
        img_dimension_height = int(request.form.get("img_dimension_height"))
        seed_choice = request.form.get("seed choice")
        dimension = request.form.get("dimension")

        for i in range(img_dimension_width):
            if seed_choice == 'All 0':
                list_of_initial_states.append(0)
            if seed_choice == 'All 1':
                list_of_initial_states.append(1)
            if seed_choice == 'Alternate 1 and 0':
                if i % 2 == 0:
                    list_of_initial_states.append(0)
                elif i % 2 != 0:
                    list_of_initial_states.append(1)
                elif i == 0:
                    list_of_initial_states.append(0)
            if seed_choice == 'Random':
                list_of_initial_states.append(random.randint(0, 1))
            if seed_choice == 'All 0 Centre 1':
                if i == (img_dimension_width//2):
                    list_of_initial_states.append(1)
                else:
                    list_of_initial_states.append(0)

        if rule == "Pure Linear Rule":
            for i in range(img_dimension_width):
                list_of_rule_vectors.append(random.choice(list_of_linear))
        elif rule == "Pure Non Linear Rule":
            for i in range(img_dimension_width):
                list_of_rule_vectors.append(random.choice(list_of_non_linear))
        elif rule == "Mixed Rule":
            random_to_seperate = random.randint(1, img_dimension_width)
            for i in range(random_to_seperate):
                list_of_rule_vectors.append(random.choice(list_of_linear))
            for i in range(random_to_seperate, img_dimension_width):
                list_of_rule_vectors.append(random.choice(list_of_non_linear))
        elif rule == "User Input":
            inputs = ""
            for i in range(img_dimension_width):
                if(i % 2 == 0):
                    if i == img_dimension_width-1:
                        inputs += "30"
                    else:
                        inputs += "30 "
                else:
                    if i == img_dimension_width-1:
                        inputs += "30"
                    else:
                        inputs += "30 "
            list_of_rule_vectors = inputs.split(" ")

        def dec_to_bin(val, the_list):
            if val >= 1:
                dec_to_bin(val // 2, the_list)
                the_list.append(val % 2)
                return the_list

        for i in list_of_rule_vectors:
            # print("rule vector:",i)
            list_of_matrix_rows = []
            rows = dec_to_bin(int(i), list_of_matrix_rows)
            # print("per row:",rows)
            if len(rows) < 8:
                how_many_to_added = 8-len(rows)
                for i in range(how_many_to_added):
                    new_row.append(0)
            for i in rows:
                new_row.append(i)
            list_of_matrix_cols.append(new_row)
            rows = []
            new_row = []

        # print(list_of_rule_vectors)

        def transitions(list_of_initial_states):
            point = 0
            list_of_next_states = []
            # index=0
            length = 7
            rnt_str = ""
            rnt = []
            i_rnt = 0
            if boundaries == 'Null Boundary':
                while(i_rnt < len(list_of_initial_states)):
                    if i_rnt == 0:
                        rnt_str = '0' + \
                            str(list_of_initial_states[i_rnt]) + \
                            str(list_of_initial_states[i_rnt+1])
                        rnt.append(int(rnt_str, 2))

                    elif i_rnt != 0 and abs(len(list_of_initial_states)-i_rnt) >= 2:
                        rnt_str = str(list_of_initial_states[i_rnt-1])+str(
                            list_of_initial_states[i_rnt])+str(list_of_initial_states[i_rnt+1])
                        rnt.append(int(rnt_str, 2))

                    else:
                        rnt_str = str(
                            list_of_initial_states[i_rnt-1])+str(list_of_initial_states[i_rnt])+'0'
                        rnt.append(int(rnt_str, 2))

                    i_rnt += 1

            if boundaries == 'Periodic Boundary':
                while(i_rnt < len(list_of_initial_states)):
                    if i_rnt == 0:
                        rnt_str = str(list_of_initial_states[len(list_of_initial_states)-1])+str(
                            list_of_initial_states[i_rnt])+str(list_of_initial_states[i_rnt+1])
                        rnt.append(int(rnt_str, 2))

                    elif i_rnt != 0 and abs(len(list_of_initial_states)-i_rnt) >= 2:
                        rnt_str = str(list_of_initial_states[i_rnt-1])+str(
                            list_of_initial_states[i_rnt])+str(list_of_initial_states[i_rnt+1])
                        rnt.append(int(rnt_str, 2))

                    else:
                        rnt_str = str(list_of_initial_states[i_rnt-1])+str(
                            list_of_initial_states[i_rnt])+str(list_of_initial_states[0])
                        rnt.append(int(rnt_str, 2))

                    i_rnt += 1

            while(point < len(rnt)):
                list_of_next_states.append(
                    list_of_matrix_cols[point][length-rnt[point]])
                point += 1
            return list_of_next_states

        start = 1
        # print(list_of_initial_states)
        next_state_store = []
        while(start != len(range(img_dimension_height))):
            list_of_next_states = transitions(list_of_initial_states)
            # print("here:",list_of_next_states)
            list_of_initial_states = []
            next_state_store.append(list_of_next_states)

            list_of_initial_states = list_of_next_states[:]
            start += 1

        # print(list_of_next_states)

        # print("wait",next_state_store)
        img = Image.new(mode="RGB", size=(
            img_dimension_height, img_dimension_width))

        for i in range(1, img_dimension_height-1):
            for j in range(1, img_dimension_width-1):
                if next_state_store[i][j] == 0:
                    img.putpixel((i, j), color_pickers[0])
                else:
                    img.putpixel((i, j), color_pickers[1])
        # img.show()
        # return img
        print(img)
        print(type(img))
        img = img.save(
            "./static/img/wow.jpg")
        img_name = "wow.jpg"
        # img.show()
        return redirect(url_for("get_choice", img_name=img_name))
    return render_template("logic.html")


@app.route("/show_img/<img_name>", methods=["POST", "GET"])
def get_choice(img_name):
    if request.method == "POST":
        the_choice = request.form["example"]
        if the_choice == "save":
            try:
                return send_from_directory(app.config["CLIENT_IMAGES"], filename=img_name, as_attachment=True)
            except FileNotFoundError:
                abort(404)
        else:
            return render_template("logic.html")
    return render_template("show.html", img_name=img_name)


@app.route('/display/<filename>')
def display_image(filename):
    print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='img/' + filename), code=301)


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@login_manager.user_loader
def load_user(username):
    return get_user1(username)


if __name__ == '__main__':
    app.run(debug=True)
