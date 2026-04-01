// auth.js
const Auth = {
    login: (token, user) => {
        localStorage.setItem('auth_token', token);
        localStorage.setItem('user', JSON.stringify(user));
        
        // Redirect based on role
        if (user.role === 'admin') {
            window.location.href = 'admin/dashboard.html';
        } else {
            window.location.href = 'student/dashboard.html';
        }
    },
    
    logout: () => {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user');
        // If inside student/ or admin/, go up a level to main login
        const depth = window.location.pathname.split('/').length;
        window.location.href = depth > 2 ? '../login.html' : 'login.html';
    },
    
    getToken: () => localStorage.getItem('auth_token'),
    
    getUser: () => {
        const u = localStorage.getItem('user');
        return u ? JSON.parse(u) : null;
    },
    
    isAuthenticated: () => !!localStorage.getItem('auth_token'),
    
    requireRole: (role) => {
        if (!Auth.isAuthenticated()) {
            Auth.logout();
            return false;
        }
        
        const user = Auth.getUser();
        if (user.role !== role) {
            // Unauthorized flip logic
            if (user.role === 'admin') window.location.href = '../admin/dashboard.html';
            else window.location.href = '../student/dashboard.html';
            return false;
        }
        return true;
    }
};

// Auto-redirect from index if already logged in
if (window.location.pathname.endsWith('index.html') || window.location.pathname.endsWith('/')) {
    if (Auth.isAuthenticated()) {
        const user = Auth.getUser();
        if (user.role === 'admin') window.location.href = 'admin/dashboard.html';
        else window.location.href = 'student/dashboard.html';
    }
}
