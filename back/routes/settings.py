from app import app , jsonify , request , json , db , ma
import shutil , os

@app.route('/settings/clearlogins/whatsapp', methods=['POST'])
def clear_login_wp():
    user_data = os.path.abspath("./user-data-wp")
    print(user_data)
    try:
        shutil.rmtree(user_data)
        return jsonify({'success': 'Login Cleared'})
    except Exception as e:
        print(str(e))
        return jsonify({'success': 'Login Cleared'})

@app.route('/settings/clearlogins/sms', methods=['POST'])
def clear_login_sms():
    user_data = os.path.abspath("./user-data-sms")
    print(user_data)
    try:
        shutil.rmtree(user_data)
        return jsonify({'success': 'Login Cleared'})
    except Exception as e:
        print(str(e))
        return jsonify({'success': 'Login Cleared'})

