from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='192.168.0.11',port=5000,threaded=False,debug=True)
