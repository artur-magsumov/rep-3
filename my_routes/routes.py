from from_db_to_json import *
home_page = '''
    <html>
        <head>
            <title>Artur - Server</title>
        </head>
        <body>
            <div>Main page: <a href="/">Home</a></div>
            <div>Json from mysql database: <a href="/catalog">Json</a></div>
            <div>Process csv-file here: <a href="/file">csv</a></div>
        </body>
    </html>
    '''

catalog_page = '''
    <html>
        <head>
            <title>Artur - Server</title>
        </head>
        <body>
            <div>Main page: <a href="/">Home</a></div>
            <div>Process csv-file here: <a href="/file">csv</a></div>
        </body>
    </html>
    '''

test = '''
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8">
            <title>Отправка файла на сервер</title>
        </head>
        <body>
            <form enctype="multipart/form-data" method="post">
            <p><input type="file" name="f">
            <input type="submit" value="Отправить"></p>
            </form>
        </body>
    </html>
    '''