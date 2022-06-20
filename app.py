from slamd import app

if __name__ == '__main__':
    print('Starting SLAMD')
    config = app.config
    app.run(port=config['PORT'], host=config['HOST'])
