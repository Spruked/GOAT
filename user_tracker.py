# user_tracker.py
"""
GOAT User Tracker - Tracks user visits and customer data across platforms
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
import sqlite3

class UserTracker:
    """Tracks user visits and customer data for GOAT, CertSig, TrueMark, and GDIS"""

    def __init__(self, db_path: str = None):
        self.db_path = db_path or Path("data/user_tracking.db")
        self.db_path.parent.mkdir(exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Initialize SQLite database for user tracking"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS user_visits (
                    id INTEGER PRIMARY KEY,
                    user_id TEXT,
                    platform TEXT,
                    visit_timestamp DATETIME,
                    session_id TEXT,
                    user_agent TEXT,
                    ip_address TEXT,
                    referrer TEXT,
                    page_url TEXT
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY,
                    user_id TEXT UNIQUE,
                    email TEXT UNIQUE,
                    name TEXT,
                    hashed_password TEXT,
                    signup_date DATETIME,
                    platforms_used TEXT,  -- JSON array
                    total_visits INTEGER DEFAULT 0,
                    last_visit DATETIME,
                    customer_type TEXT DEFAULT 'free',
                    is_active BOOLEAN DEFAULT 1,
                    marketing_opt_in BOOLEAN DEFAULT 1
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS platform_stats (
                    platform TEXT PRIMARY KEY,
                    total_visits INTEGER DEFAULT 0,
                    unique_users INTEGER DEFAULT 0,
                    last_updated DATETIME
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS user_files (
                    id INTEGER PRIMARY KEY,
                    user_id TEXT,
                    filename TEXT,
                    original_name TEXT,
                    file_size INTEGER,
                    file_type TEXT,
                    upload_date DATETIME,
                    status TEXT DEFAULT 'uploaded',  -- uploaded, processing, processed, failed
                    processing_started DATETIME,
                    processing_completed DATETIME,
                    output_path TEXT,
                    error_message TEXT,
                    FOREIGN KEY (user_id) REFERENCES customers (user_id)
                )
            ''')

    def track_visit(self, user_id: str, platform: str, session_id: str = None,
                   user_agent: str = None, ip_address: str = None,
                   referrer: str = None, page_url: str = None):
        """Track a user visit to a platform"""

        visit_data = {
            'user_id': user_id,
            'platform': platform,
            'visit_timestamp': datetime.utcnow(),
            'session_id': session_id,
            'user_agent': user_agent,
            'ip_address': ip_address,
            'referrer': referrer,
            'page_url': page_url
        }

        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO user_visits
                (user_id, platform, visit_timestamp, session_id, user_agent, ip_address, referrer, page_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                visit_data['user_id'], visit_data['platform'], visit_data['visit_timestamp'],
                visit_data['session_id'], visit_data['user_agent'], visit_data['ip_address'],
                visit_data['referrer'], visit_data['page_url']
            ))

            # Update customer record
            self._update_customer_record(user_id, platform)

            # Update platform stats
            self._update_platform_stats(platform)

    def _update_customer_record(self, user_id: str, platform: str):
        """Update or create customer record"""
        with sqlite3.connect(self.db_path) as conn:
            # Check if customer exists
            customer = conn.execute(
                'SELECT platforms_used, total_visits FROM customers WHERE user_id = ?',
                (user_id,)
            ).fetchone()

            if customer:
                platforms = json.loads(customer[0] or '[]')
                if platform not in platforms:
                    platforms.append(platform)

                conn.execute('''
                    UPDATE customers
                    SET platforms_used = ?, total_visits = total_visits + 1, last_visit = ?
                    WHERE user_id = ?
                ''', (json.dumps(platforms), datetime.utcnow(), user_id))
            else:
                # Create new customer
                conn.execute('''
                    INSERT INTO customers (user_id, signup_date, platforms_used, total_visits, last_visit)
                    VALUES (?, ?, ?, 1, ?)
                ''', (user_id, datetime.utcnow(), json.dumps([platform]), datetime.utcnow()))

    def _update_platform_stats(self, platform: str):
        """Update platform statistics"""
        with sqlite3.connect(self.db_path) as conn:
            # Increment visit count
            conn.execute('''
                INSERT INTO platform_stats (platform, total_visits, unique_users, last_updated)
                VALUES (?, 1, 1, ?)
                ON CONFLICT(platform) DO UPDATE SET
                    total_visits = total_visits + 1,
                    last_updated = ?
            ''', (platform, datetime.utcnow(), datetime.utcnow()))

            # Update unique users count
            unique_count = conn.execute(
                'SELECT COUNT(DISTINCT user_id) FROM user_visits WHERE platform = ?',
                (platform,)
            ).fetchone()[0]

            conn.execute('''
                UPDATE platform_stats SET unique_users = ?, last_updated = ? WHERE platform = ?
            ''', (unique_count, datetime.utcnow(), platform))

    def get_customer_data(self, user_id: str = None) -> Dict[str, Any]:
        """Get customer data and statistics"""
        with sqlite3.connect(self.db_path) as conn:
            if user_id:
                customer = conn.execute(
                    'SELECT * FROM customers WHERE user_id = ?',
                    (user_id,)
                ).fetchone()

                if customer:
                    return {
                        'user_id': customer[1],
                        'email': customer[2],
                        'name': customer[3],
                        'signup_date': customer[4],
                        'platforms_used': json.loads(customer[5] or '[]'),
                        'total_visits': customer[6],
                        'last_visit': customer[7],
                        'customer_type': customer[8]
                    }
                return None

            # Return all customers
            customers = conn.execute('SELECT * FROM customers').fetchall()
            return {
                'total_customers': len(customers),
                'customers': [{
                    'user_id': c[1], 'email': c[2], 'name': c[3], 'signup_date': c[4],
                    'platforms_used': json.loads(c[5] or '[]'), 'total_visits': c[6],
                    'last_visit': c[7], 'customer_type': c[8]
                } for c in customers]
            }

    def get_platform_stats(self) -> Dict[str, Any]:
        """Get statistics for all platforms"""
        with sqlite3.connect(self.db_path) as conn:
            stats = conn.execute('SELECT * FROM platform_stats').fetchall()

            platforms = {}
            for stat in stats:
                platforms[stat[0]] = {
                    'total_visits': stat[1],
                    'unique_users': stat[2],
                    'last_updated': stat[3]
                }

            # Ensure all platforms are represented (including GDIS)
            for platform in ['GOAT', 'CertSig', 'TrueMark', 'GDIS']:
                if platform not in platforms:
                    platforms[platform] = {
                        'total_visits': 0,
                        'unique_users': 0,
                        'last_updated': None
                    }

            return platforms

    def get_visit_history(self, user_id: str, platform: str = None, limit: int = 50) -> List[Dict]:
        """Get visit history for a user"""
        with sqlite3.connect(self.db_path) as conn:
            if platform:
                visits = conn.execute('''
                    SELECT * FROM user_visits
                    WHERE user_id = ? AND platform = ?
                    ORDER BY visit_timestamp DESC LIMIT ?
                ''', (user_id, platform, limit)).fetchall()
            else:
                visits = conn.execute('''
                    SELECT * FROM user_visits
                    WHERE user_id = ?
                    ORDER BY visit_timestamp DESC LIMIT ?
                ''', (user_id, limit)).fetchall()

            return [{
                'id': v[0], 'user_id': v[1], 'platform': v[2], 'visit_timestamp': v[3],
                'session_id': v[4], 'user_agent': v[5], 'ip_address': v[6],
                'referrer': v[7], 'page_url': v[8]
            } for v in visits]

    def create_user(self, email: str, name: str, hashed_password: str, marketing_opt_in: bool = True) -> Dict[str, Any]:
        """Create a new user account"""
        user_id = f"user_{int(datetime.utcnow().timestamp())}_{hash(email) % 10000}"
        
        with sqlite3.connect(self.db_path) as conn:
            try:
                conn.execute('''
                    INSERT INTO customers 
                    (user_id, email, name, hashed_password, signup_date, platforms_used, marketing_opt_in)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (user_id, email, name, hashed_password, datetime.utcnow(), '[]', marketing_opt_in))
                
                return {
                    'id': conn.lastrowid,
                    'user_id': user_id,
                    'email': email,
                    'name': name,
                    'signup_date': datetime.utcnow().isoformat(),
                    'is_active': True,
                    'marketing_opt_in': marketing_opt_in
                }
            except sqlite3.IntegrityError:
                return None  # Email already exists

    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user with email and password"""
        with sqlite3.connect(self.db_path) as conn:
            user = conn.execute('''
                SELECT id, user_id, email, name, hashed_password, signup_date, is_active, marketing_opt_in
                FROM customers 
                WHERE email = ? AND is_active = 1
            ''', (email,)).fetchone()
            
            if user and self._verify_password(password, user[4]):
                return {
                    'id': user[0],
                    'user_id': user[1],
                    'email': user[2],
                    'name': user[3],
                    'signup_date': user[5],
                    'is_active': bool(user[6]),
                    'marketing_opt_in': bool(user[7])
                }
            return None

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        with sqlite3.connect(self.db_path) as conn:
            user = conn.execute('''
                SELECT id, user_id, email, name, signup_date, is_active, marketing_opt_in
                FROM customers 
                WHERE email = ?
            ''', (email,)).fetchone()
            
            if user:
                return {
                    'id': user[0],
                    'user_id': user[1],
                    'email': user[2],
                    'name': user[3],
                    'signup_date': user[4],
                    'is_active': bool(user[5]),
                    'marketing_opt_in': bool(user[6])
                }
            return None

    def get_customer_data(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get full customer data including projects and stats"""
        with sqlite3.connect(self.db_path) as conn:
            customer = conn.execute('''
                SELECT * FROM customers WHERE user_id = ?
            ''', (user_id,)).fetchone()
            
            if customer:
                return {
                    'id': customer[0],
                    'user_id': customer[1],
                    'email': customer[2],
                    'name': customer[3],
                    'signup_date': customer[5],
                    'platforms_used': json.loads(customer[6]) if customer[6] else [],
                    'total_visits': customer[7],
                    'last_visit': customer[8],
                    'customer_type': customer[9],
                    'is_active': bool(customer[10]),
                    'marketing_opt_in': bool(customer[11])
                }
            return None

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash (simple implementation)"""
        # In production, use proper password hashing like bcrypt
        return plain_password == hashed_password  # TODO: Implement proper hashing

    def update_user_profile(self, user_id: str, updates: Dict[str, Any]) -> bool:
        """Update user profile information"""
        allowed_fields = ['name', 'marketing_opt_in', 'customer_type']
        update_fields = {k: v for k, v in updates.items() if k in allowed_fields}
        
        if not update_fields:
            return False
            
        set_clause = ', '.join(f'{k} = ?' for k in update_fields.keys())
        values = list(update_fields.values()) + [user_id]
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(f'''
                UPDATE customers 
                SET {set_clause}
                WHERE user_id = ?
            ''', values)
            return conn.rowcount > 0

    def get_user_files(self, user_id: str) -> Dict[str, Any]:
        """Get user's uploaded files and their processing status"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('''
                SELECT id, filename, original_name, file_size, file_type,
                       upload_date, status, processing_started, processing_completed,
                       output_path, error_message
                FROM user_files
                WHERE user_id = ?
                ORDER BY upload_date DESC
            ''', (user_id,))

            files = []
            for row in cursor.fetchall():
                file_info = dict(row)
                # Convert datetime strings to readable format
                if file_info['upload_date']:
                    file_info['uploaded'] = datetime.fromisoformat(file_info['upload_date']).strftime('%Y-%m-%d')
                else:
                    file_info['uploaded'] = 'Unknown'

                # Format file size
                size_bytes = file_info['file_size'] or 0
                if size_bytes < 1024:
                    file_info['size'] = f"{size_bytes} B"
                elif size_bytes < 1024 * 1024:
                    file_info['size'] = f"{size_bytes // 1024} KB"
                else:
                    file_info['size'] = f"{size_bytes // (1024 * 1024)} MB"

                files.append(file_info)

            return {"files": files}

    def add_user_file(self, user_id: str, filename: str, original_name: str,
                     file_size: int, file_type: str) -> bool:
        """Add a new user file record"""
        with sqlite3.connect(self.db_path) as conn:
            try:
                conn.execute('''
                    INSERT INTO user_files (user_id, filename, original_name, file_size, file_type, upload_date)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (user_id, filename, original_name, file_size, file_type, datetime.utcnow()))
                return True
            except Exception as e:
                print(f"Error adding user file: {e}")
                return False

    def update_file_status(self, file_id: int, status: str, output_path: str = None, error_message: str = None) -> bool:
        """Update file processing status"""
        with sqlite3.connect(self.db_path) as conn:
            try:
                now = datetime.utcnow()
                if status == 'processing':
                    conn.execute('''
                        UPDATE user_files
                        SET status = ?, processing_started = ?
                        WHERE id = ?
                    ''', (status, now, file_id))
                elif status in ['processed', 'failed']:
                    conn.execute('''
                        UPDATE user_files
                        SET status = ?, processing_completed = ?, output_path = ?, error_message = ?
                        WHERE id = ?
                    ''', (status, now, output_path, error_message, file_id))
                return True
            except Exception as e:
                print(f"Error updating file status: {e}")
                return False

# Global instance
user_tracker = UserTracker()