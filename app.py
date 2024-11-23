from flask import Flask, render_template, request
import instaloader
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    unfollowers = None
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Create an instance of Instaloader
        loader = instaloader.Instaloader()

        # Login to Instagram
        try:
            loader.login(username, password)
        except instaloader.exceptions.BadCredentialsException:
            error = "Invalid credentials. Please try again."
            return render_template('index.html', unfollowers=unfollowers, error=error)
        except instaloader.exceptions.ConnectionException:
            error = "Connection error. Please try again."
            return render_template('index.html', unfollowers=unfollowers, error=error)

        try:
            # Get the profile
            profile = instaloader.Profile.from_username(loader.context, username)

            # Get followers and following
            followers = set(follower.username for follower in profile.get_followers())
            following = set(followee.username for followee in profile.get_followees())

            # Find users who don't follow back
            unfollowers = list(following - followers)
        except Exception as e:
            error = f"An error occurred: {str(e)}"
            return render_template('index.html', unfollowers=None, error=error)

    return render_template('index.html', unfollowers=unfollowers, error=error)

if __name__ == '__main__':
    app.run(debug=True)
