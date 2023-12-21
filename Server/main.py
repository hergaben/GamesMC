from flask import Flask, render_template, request, redirect, url_for
from flask import Flask, render_template, request, session, redirect, url_for
from prometheus_flask_exporter import PrometheusMetrics
from keycloak import KeycloakOpenID
import os


app = Flask(__name__)
app.debug = True

app.secret_key = "hleb666tohir"

keycloak_openid = KeycloakOpenID(
    server_url=os.getenv("KEYCLOAK_URL", "http://keycloakapp:8080/"),
    client_id="tohir",
    realm_name="Aliev",
    client_secret_key="2Jk5brgYi6Ae9WI6aGaAxRRVWoM6G9uI",
)

@app.route('/', methods=["POST", "GET"])
def index():
        if session.get("valid", False):
            return render_template("index.html")
        if request.method == "POST":
            print(request.form)
            username = str(request.form["fname"])
            password = str(request.form["lname"])
            # Get Token
            try:
                token = keycloak_openid.token(username, password)
                userinfo = keycloak_openid.userinfo(token["access_token"])
                app.logger.info(f"Userinfo: {userinfo}")
                token_info = keycloak_openid.introspect(token["access_token"])
                print(token_info)
                app.logger.info(f"Userroles: {token_info['realm_access']['roles']}")
                if "hleb" not in token_info["realm_access"]["roles"]:
                    return render_template(
                        "login.html",
                        wrong_datg_visability="collapse",
                        no_permission_visability="visible",
                    )
                else:
                    session["valid"] = True
                    return render_template("index.html")
            except Exception as e:
                app.logger.error(e)
                return render_template(
                    "login.html",
                    wrong_datg_visability="visible",
                    no_permission_visability="collapse",
                )

        return render_template(
            "login.html",
            wrong_datg_visability="collapse",
            no_permission_visability="collapse",
        )


@app.route("/logout")
def logout():
    session["valid"] = False
    return redirect("/")

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/all')
def fetch_all():
    return render_template('all.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5051)