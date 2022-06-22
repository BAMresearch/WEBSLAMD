import os

from slamd import create_app

app = create_app(os.getenv('FLASK_ENV'))

if __name__ == '__main__':
    print('Starting SLAMD')
    config = app.config
    app.run(port=config['PORT'], host=config['HOST'])
