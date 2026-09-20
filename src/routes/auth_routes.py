from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, g
from src.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login', next=request.url))
            user_role = session.get('user_role')
            if user_role not in roles and user_role != 'admin':
                flash('You do not have permission to access this resource.', 'danger')
                return redirect(url_for('customer.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('customer.index'))

    if request.method == 'POST':
        username_or_email = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        user, err = AuthService.authenticate_user(username_or_email, password)
        if err:
            flash(err, 'danger')
            return render_template('auth/login.html')

        session.clear()
        session['user_id'] = user.id
        session['username'] = user.username
        session['user_role'] = user.role
        session['full_name'] = user.full_name
        session['cart'] = {}  # initialize cart

        flash(f'Welcome back, {user.full_name}!', 'success')
        
        # Redirect based on role
        next_url = request.args.get('next')
        if next_url:
            return redirect(next_url)
        if user.role == 'restaurant_owner':
            return redirect(url_for('restaurant.dashboard'))
        elif user.role == 'rider':
            return redirect(url_for('delivery.dashboard'))
        elif user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('customer.index'))

    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('customer.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        full_name = request.form.get('full_name', '').strip()
        role = request.form.get('role', 'customer')
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()

        if not username or not email or not password or not full_name:
            flash('All required fields must be filled.', 'danger')
            return render_template('auth/register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('auth/register.html')

        user, err = AuthService.register_user(username, email, password, role, full_name, phone, address)
        if err:
            flash(err, 'danger')
            return render_template('auth/register.html')

        flash('Registration successful! Please log in with your credentials.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
@login_required
def profile():
    user = AuthService.get_user_by_id(session['user_id'])
    return render_template('auth/profile.html', user=user)
