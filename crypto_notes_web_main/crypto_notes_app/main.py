from waitress import serve
from pyramid.paster import get_app, setup_logging


def main():
    setup_logging('development.ini')
    app = get_app('development.ini', 'main')
    serve(app, host='0.0.0.0', port=6543)


if __name__ == '__main__':
    main()
