from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

FORM_HTML = '''
<!doctype html>
<html lang="fa">
<head>
  <meta charset="utf-8">
  <title>ثبت نام</title>
  <style>
    body { font-family: Arial, sans-serif; direction: rtl; padding: 2rem; background: #f9f9f9; }
    .container { max-width: 400px; margin: auto; padding: 1rem; background: white; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,.1); }
    label { display: block; margin-bottom: .5rem; color: #333; }
    input[type="text"], input[type="email"] { width: 100%; padding: .5rem; margin-bottom: .75rem; border: 1px solid #ddd; border-radius: 4px; }
    button { padding: .6rem 1rem; border: none; background: #4CAF50; color: white; border-radius: 4px; cursor: pointer; }
    button:hover { background: #45a049; }
  </style>
</head>
<body>
  <div class="container">
    <h2>فرم ثبت نام</h2>
    <form method="post" action="/">
      <label for="name">نام</label>
      <input type="text" id="name" name="name" required>
      <label for="email">ایمیل</label>
      <input type="email" id="email" name="email" required>
      <button type="submit">تایید</button>
    </form>
  </div>
</body>
</html>
'''

WELCOME_HTML = '''
<!doctype html>
<html lang="fa">
<head>
  <meta charset="utf-8">
  <title>خوش آمدید</title>
  <style>
    body { font-family: Arial, sans-serif; direction: rtl; padding: 2rem; background: #eef2f7; }
    .container { max-width: 600px; margin: auto; padding: 1rem; text-align: center; }
  </style>
</head>
<body>
  <div class="container">
    <h1>هلو ورلد</h1>
  </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        if ip:
            ip = ip.split(',')[0].strip()
        else:
            ip = 'Unknown'
        print(f"New registration from IP: {ip} - Name: {name} - Email: {email}")
        return redirect(url_for('welcome'))
    return render_template_string(FORM_HTML)

@app.route('/welcome')
def welcome():
    return render_template_string(WELCOME_HTML)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)