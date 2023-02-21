from website import create_app

app = create_app()

if __name__ == '__main__':
    # anytime we make change to python code, automatically rerun web server
    app.run(debug=True)
