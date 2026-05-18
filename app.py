"""
Complete VPN Shop Bot - Multilingual Edition (FULLY FIXED)
Languages: English , Russian , Hindi , Arabic 
With Real Payment Integration
Fixed Issues:- Removed imghdr dependency (deprecated in Python 3.13)- Fixed NameError for undefined variables- Added proper error handling- Completed all missing handlers
"""
import json
import sqlite3
import logging
import os
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    PreCheckoutQueryHandler,
    filters
)
# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
# Read config with error handling
def load_config():
    """Load configuration from config.json with fallback defaults"""
    default_config = {
        'bot_token': 'YOUR_BOT_TOKEN_HERE',
        'admin_ids': [],
        'support_username': '@YourSupport',
        'payment_provider_token': ''
    }
    try:
        if os.path.exists('config.json'):
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config
        else:
            # Create default config file
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=4, ensure_ascii=False)
            logger.warning("config.json not found. Created default config. Please update it!")
            return default_config
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        return default_config
config = load_config()
BOT_TOKEN = config.get('bot_token', '')
ADMIN_IDS = config.get('admin_ids', [])
SUPPORT_USERNAME = config.get('support_username', '@Support')
PAYMENT_PROVIDER_TOKEN = config.get('payment_provider_token', '')
# Translations - Complete
TRANSLATIONS = {
    'en': {
        'flag': ' ',
        'name': 'English',
        'welcome': ' Welcome, {name}!\n\n <b>Premium VPN Service</b>\n\n <b>Features:</b>\n•) 
        'welcome_referred': '\n\n <b>You were referred!</b>\nGet 7 days FREE trial instead of 3!',
        'welcome_trial': '\n\n Get 3 days <b>FREE TRIAL</b> now!',
        'choose_option': '\n\nChoose an option below:',
        'welcome_back': ' Welcome back, {name}!\n\n <b>Status:</b> {status}\n\nChoose an option:',
        # Buttons
        'btn_trial': ' Free Trial (3 Days)',
        'btn_buy': ' Buy Subscription',
        'btn_account': ' My Account',
        'btn_referral': ' Referral Program',
        'btn_promo': ' Use Promocode',
        'btn_about': ' About VPN',
        'btn_help': ' Help',
        'btn_support': ' Support',
        'btn_faq': ' FAQ',
        'btn_admin': ' Admin Panel',
        'btn_back': ' Back',
        'btn_language': ' Change Language',
        # Trial
        'trial_used': ' <b>Trial Already Used</b>\n\nYou\'ve already activated your free trial!\n\n
        'trial_activated': ' <b>Trial Activated!</b>\n\n Duration: <b>{days} days</b>\n
        # Plans
        'plans_title': ' <b>Subscription Plans</b>\n\nChoose the plan that fits your needs:\n\n',
        'plan_item': ' <b>{name}</b> - {devices} device{plural}\n   Starting at ${price}/month\n\n',
        'plans_features': '\n All plans include:\n• Unlimited bandwidth\n• No speed limits\n• Multiple server locations\n• 24/7 support',
        # Duration
        'duration_title': ' <b>{plan_name} Plan</b>\nDevices: {devices}\n\n <b>Choose duration:</b>\n\n',
        'duration_item': '• <b>{label}</b>: ${price} (${monthly}/month)\n',
        # Payment
        'payment_title': ' <b>Payment</b>\n\n Plan: {plan}\n Duration: {duration} days\n
        'payment_success': ' <b>Payment Successful!</b>\n\n Plan: {plan}\n Duration: {duration} days\n
        # Account
        'account_title': ' <b>Your Account</b>\n\n ID: <code>{user_id}</code>\n Name: {name}\n
        # Referral
        'referral_title': ' <b>Referral Program</b>\n\n <b>Your Earnings:</b> ${earnings}\n
        # Help & Support
        'help_text': ' <b>Help & FAQ</b>\n\n<b>Q: How to connect?</b>\nA: Copy config → Install app 
        'support_text': ' <b>Support</b>\n\n Contact our support team:\n{support}\n\n Available 24/7\n
        'about_text': ' <b>About Our VPN</b>\n\n <b>Servers:</b> 50+ locations\n <b>Speed:</b> Up to 10 Gbps\n
        # Admin
        'admin_title': ' <b>Admin Panel</b>\n\n <b>Statistics:</b>\n• Total Users: {total_users}\n• Active Subs: {active_subs}\n• Total Revenue: ${revenue}\n• Today\'s Revenue: ${today_revenue}',
        # Status
        'status_no_sub': ' No active subscription',
        'status_expired': ' Subscription expired',
        'status_active': ' Active ({days} days left)',
    },
    'ru': {
        'flag': ' ',
        'name': 'Русский',
        'welcome': ' Добро пожаловать, {name}!\n\n <b>Премиум VPN Сервис</b>\n\n <b>Возможности
        'welcome_referred': '\n\n <b>Вас пригласили!</b>\nПолучите 7 дней БЕСПЛАТНО вместо 3!',
        'welcome_trial': '\n\n Получите 3 дня <b>БЕСПЛАТНО</b> прямо сейчас!',
        'choose_option': '\n\nВыберите опцию ниже:',
 С возвращением, {name}!\n\n <b>Статус:</b> {status}\n\nВыберите
        'welcome_back': '
        'btn_trial': ' Бесплатная пробная (3 дня)',
        'btn_buy': ' Купить подписку',
        'btn_account': ' Мой аккаунт',
        'btn_referral': ' Реферальная программа',
        'btn_promo': ' Использовать промокод',
        'btn_about': ' О VPN',
        'btn_help': ' Помощь',
        'btn_support': ' Поддержка',
        'btn_faq': ' Частые вопросы',
        'btn_admin': ' Админ панель',
        'btn_back': ' Назад',
        'btn_language': ' Сменить язык',
        'trial_used': ' <b>Пробная версия уже использована</b>\n\nВы уже активировали бесплатную
        'trial_activated': ' <b>Пробная версия активирована!</b>\n\n Длительность: <b>{days} 
        'plans_title': ' <b>Тарифные планы</b>\n\nВыберите план который вам подходит:\n\n',
        'plan_item': ' <b>{name}</b> - {devices} устройств{plural}\n   
От ${price}/месяц\n\n',
        'plans_features': '\n Все планы включают:\n• Безлимитный трафик\n• Без ограничений 
        'duration_title': ' <b>План {plan_name}</b>\nУстройств: {devices}\n\n <b>Выберите
        'duration_item': '• <b>{label}</b>: ${price} (${monthly}/месяц)\n',
        'payment_title': ' <b>Оплата</b>\n\n План: {plan}\n Длительность: {duration} дней
        'payment_success': ' <b>Оплата успешна!</b>\n\n План: {plan}\n Длительность: {duration} 
        'account_title': ' <b>Ваш аккаунт</b>\n\n ID: <code>{user_id}</code>\n Имя: {name}\n
        'referral_title': ' <b>Реферальная программа</b>\n\n <b>Ваш доход:</b> ${earnings}\n
        'help_text': ' <b>Помощь и FAQ</b>\n\n<b>В: Как подключиться?</b>\nО: Скопировать конфиг
        'support_text': ' <b>Поддержка</b>\n\n Свяжитесь с нашей службой поддержки:\n{support}\n\n
        'about_text': ' <b>О нашем VPN</b>\n\n <b>Серверы:</b> 50+ локаций\n <b>Скорость
        'admin_title': ' <b>Админ панель</b>\n\n <b>Статистика:</b>\n• Всего пользователей
        'status_no_sub': ' Нет активной подписки',
        'status_expired': ' Подписка истекла',
        'status_active': ' Активна ({days} дней осталось)',
    },
    'hi': {
        'flag': ' ',
        'name': 'िहंदी',
        'welcome': ' स्वागत है, {name}!\n\n <b>प्रीिमयम VPN सेवा</b>\n\n <b>िवशेषताएं:</b>\n•  
        'welcome_referred': '\n\n <b>आपको रेफर िकया गया!</b>\n3 के बजाय 7 िदन मुफ्त ट्रायल पाएं!',
        'welcome_trial': '\n\n अभी 3 िदन <b>मुफ्त ट्रायल</b> पाएं!',
        'choose_option': '\n\nनीचे से िवकल्प चुनें:',
        'welcome_back': ' वापसी पर स्वागत है, {name}!\n\n <b>िस्थित:</b> {status}\n\nिवकल्प चुनें:',
        'btn_trial': ' मुफ्त ट्रायल (3 िदन)',
        'btn_buy': ' सब्सिक्रप्शन खरीदें',
        'btn_account': ' मेरा अकाउंट',
        'btn_referral': ' रेफरल प्रोग्राम',
        'btn_promo': ' प्रोमोकोड यूज करें',
        'btn_about': ' VPN के बारे में',
        'btn_help': ' मदद',
        'btn_support': ' सपोटर्',
        'btn_faq': ' FAQ',
        'btn_admin': ' एडिमन पैनल',
        'btn_back': ' वापस',
        'btn_language': ' भाषा बदलें',
        'trial_used': ' <b>ट्रायल पहले से यूज हो चुका</b>\n\nआपने पहले ही अपना मुफ्त ट्रायल एिक्टवेट कर िलया है
        'trial_activated': ' <b>ट्रायल एिक्टवेट हो गया!</b>\n\n अविध: <b>{days} िदन</b>\n समाप्त 
        'plans_title': ' <b>सब्सिक्रप्शन प्लान्स</b>\n\nअपने िलए सही प्लान चुनें:\n\n',
        'plan_item': ' <b>{name}</b> - {devices} िडवाइस{plural}\n   ${price}/महीने से शुरू\n\n',
        'plans_features': '\n सभी प्लान्स में शािमल:\n• असीिमत बैंडिवड्थ\n• स्पीड िलिमट नहीं\n• कई सवर्र लोकेशन
        'duration_title': ' <b>{plan_name} प्लान</b>\nिडवाइस: {devices}\n\n <b>अविध चुनें:</b>\n\n',
        'duration_item': '• <b>{label}</b>: ${price} (${monthly}/महीना)\n',
        'payment_title': ' <b>पेमेंट</b>\n\n प्लान: {plan}\n अविध: {duration} िदन\n कु ल : <b>${price}</b>\n\n
        'payment_success': ' <b>पेमेंट सफल रहा!</b>\n\n प्लान: {plan}\n अविध: {duration} िदन\n
        'account_title': ' <b>आपका अकाउंट</b>\n\n ID: <code>{user_id}</code>\n नाम: {name}\n
        'referral_title': ' <b>रेफरल प्रोग्राम</b>\n\n <b>आपकी कमाई:</b> ${earnings}\n <b>कु ल 
        'help_text': ' <b>मदद और FAQ</b>\n\n<b>प्र: कनेक्ट कैसे करें?</b>\nउ: कॉिन्फग कॉपी → ऐप इंस्टॉल →
        'support_text': ' <b>सपोटर्</b>\n\n हमारी सपोटर् टीम से संपकर् करें:\n{support}\n\n 24/7 उपलब्ध
        'about_text': ' <b>हमारे VPN के बारे में</b>\n\n <b>सवर्र:</b> 50+ लोकेशन\n <b>स्पीड:</b> 10 Gbps 
        'admin_title': ' <b>एडिमन पैनल</b>\n\n <b>आंकड़े:</b>\n• कु ल यूज़र: {total_users}\n• सिक्रय
        'status_no_sub': ' कोई सिक्रय सब्सिक्रप्शन नहीं',
        'status_expired': ' सब्सिक्रप्शन समाप्त हो गया',
    },
        'status_active': ' सिक्रय ({days} िदन बचे)',
    'ar': {
        'flag': ' ',
        'name': 'اﻟﻌﺮﺑﯿﺔ',
        'welcome': ' ًﻣﺮﺣﺒﺎ، {name}!\n\n <b>ﺧﺪﻣﺔ VPN اﻟﻤﻤﯿﺰة</b>\n\n <b>اﻟﻤﻤﯿﺰات:</b>\n• 
        'welcome_referred': '\n\n <b>ﺗﻤﺖ إﺣﺎﻟﺘﻚ!</b>\n3 اﺣﺼﻞ ﻋﻠﻰ 7 أﯾﺎم ﺗﺠﺮﺑﺔ ﻣﺠﺎﻧﯿﺔ ﺑﺪﻻً ﻣﻦ
        'welcome_trial': '\n\n اﺣﺼﻞ ﻋﻠﻰ 3 أﯾﺎم <b>ﺗﺠﺮﺑﺔ ﻣﺠﺎﻧﯿﺔ</b> اﻵن!',
        'choose_option': '\n\nاﺧﺘﺮ ﺧﯿﺎراً أدﻧﺎه:',
        'welcome_back': ' ﻣﺮﺣﺒﺎً ﺑﻌﻮدﺗﻚ، {name}!\n\n <b>اﻟﺤﺎﻟﺔ:</b> {status}\n\nًاﺧﺘﺮ ﺧﯿﺎرا
        'btn_trial': ' (3 أﯾﺎم) ﺗﺠﺮﺑﺔ ﻣﺠﺎﻧﯿﺔ',
        'btn_buy': ' ﺷﺮاء اﺷﺘﺮاك',
        'btn_account': ' ﺣﺴﺎﺑﻲ',
        'btn_referral': ' ﺑﺮﻧﺎﻣﺞ اﻹﺣﺎﻟﺔ',
        'btn_promo': ' اﺳﺘﺨﺪام رﻣﺰ ﺗﺮوﯾﺠﻲ',
        'btn_about': ' ﻋﻦ VPN',
        'btn_help': ' ﻣﺴﺎﻋﺪة',
        'btn_support': ' اﻟﺪﻋﻢ',
        'btn_faq': ' اﻷﺳﺌﻠﺔ اﻟﺸﺎﺋﻌﺔ',
        'btn_admin': ' ﻟﻮﺣﺔ اﻹدارة',
        'btn_back': ' رﺟﻮع',
        'btn_language': ' ﺗﻐﯿﯿﺮ اﻟﻠﻐﺔ',
        'trial_used': ' <b>ﺗﻢ اﺳﺘﺨﺪام اﻟﺘﺠﺮﺑﺔ اﻟﻤﺠﺎﻧﯿﺔ</b>\n\nﺑﺘﻔﻌﯿﻞ ﺗﺠﺮﺑﺘﻚ اﻟﻤﺠﺎﻧﯿﺔ ﺑﺎﻟﻔﻌﻞ
        'trial_activated': ' <b>ﺗﻢ ﺗﻔﻌﯿﻞ اﻟﺘﺠﺮﺑﺔ اﻟﻤﺠﺎﻧﯿﺔ!</b>\n\n اﻟﻤﺪة: <b>{days} أﯾﺎم</b>\n
        'plans_title': ' <b>ﺧﻄﻂ اﻻﺷﺘﺮاك</b>\n\nاﺧﺘﺮ اﻟﺨﻄﺔ اﻟﺘﻲ ﺗﻨﺎﺳﺐ اﺣﺘﯿﺎﺟﺎﺗﻚ:\n\n',
        'plan_item': ' <b>{name}</b> - {devices} ﺟﮭﺎز{plural}\n   ,'n\n\ﺷﮭﺮ/}price{$ اﺑﺘﺪاءً ﻣ
ﻦ
        'plans_features': '\n ﺟﻤﯿﻊ اﻟﺨﻄﻂ ﺗﺘﻀﻤﻦ:\n• ﺑﺎﻧﺪوﯾﺚ ﻏﯿﺮ ﻣﺤﺪود\n• ﺑﺪون ﺣﺪ ﻟﻠﺴﺮﻋﺔ\n• ﻣﺘﻌﺪدة
        'duration_title': ' <b>ﺧﻄﺔ {plan_name}</b>\nاﻷﺟﮭﺰة: {devices}\n\n <b>اﺧﺘﺮ اﻟﻤﺪة:</b>\n\n',
        'duration_item': '• <b>{label}</b>: ${price} (${monthly}/ﺷﮭﺮ)\n',
        'payment_title': ' <b>اﻟﺪﻓﻊ</b>\n\n اﻟﺨﻄﺔ: {plan}\n اﻟﻤﺪة: {duration} ﯾﻮم\n 
        'payment_success': ' <b>ﺗﻢ اﻟﺪﻓﻊ ﺑﻨﺠﺎح!</b>\n\n اﻟﺨﻄﺔ: {plan}\n اﻟﻤﺪة: {duration} 
        'account_title': ' <b>ﺣﺴﺎﺑﻚ</b>\n\n اﻟﻤﻌﺮف: <code>{user_id}</code>\n اﻻﺳﻢ: {name}\n
        'referral_title': ' <b>ﺑﺮﻧﺎﻣﺞ اﻹﺣﺎﻟﺔ</b>\n\n <b>أرﺑﺎﺣﻚ:</b> ${earnings}\n <b>اﻹﺣﺎﻻت
        'help_text': ' <b>اﻟﻤﺴﺎﻋﺪة واﻷﺳﺌﻠﺔ اﻟﺸﺎﺋﻌﺔ</b>\n\n<b>س: ﻛﯿﻔﯿﺔ اﻻﺗﺼﺎل؟</b>\nاﻻﺗﺼﺎل ←
        'support_text': ' <b>اﻟﺪﻋﻢ</b>\n\n اﺗﺼﻞ ﺑﻔﺮﯾﻖ اﻟﺪﻋﻢ:\n{support}\n\n 24/7 ﻣﺘﺎح\n
        'about_text': ' <b>ﻋﻦ VPN اﻟﺨﺎص ﺑﻨﺎ</b>\n\n <b>اﻟﺨﻮادم:</b> ًأﻛﺜﺮ ﻣﻦ 50 ﻣﻮﻗﻌﺎ\n <b>
        'admin_title': ' <b>ﻟﻮﺣﺔ اﻹدارة</b>\n\n <b>اﻹﺣﺼﺎﺋﯿﺎت:</b>\n• إﺟﻤﺎﻟﻲ اﻟﻤﺴﺘﺨﺪﻣﯿﻦ: {total_users}\n• 
        'status_no_sub': ' ﻻ ﯾﻮﺟﺪ اﺷﺘﺮاك ﻧﺸﻂ',
        'status_expired': ' اﻧﺘﮭﻰ اﻻﺷﺘﺮاك',
        'status_active': ' ﻧﺸﻂ (ﻣﺘﺒﻘﻲ {days} أﯾﺎم)',
    }
}
# Database
class Database:
    def __init__(self):
        self.init_db()
    def init_db(self):
        try:
            conn = sqlite3.connect('vpn_shop.db')
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    language_code TEXT DEFAULT 'en',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    referrer_id INTEGER,
                    subscription_end TIMESTAMP,
                    is_trial_used BOOLEAN DEFAULT 0,
                    is_blocked BOOLEAN DEFAULT 0,
                    total_paid REAL DEFAULT 0
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS subscriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    plan_name TEXT,
                    devices INTEGER,
                    duration_days INTEGER,
                    price REAL DEFAULT 0,
                    currency TEXT DEFAULT 'USD',
                    payment_method TEXT,
                    started_at TIMESTAMP,
                    expires_at TIMESTAMP,
                    config_url TEXT,
                )
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS payments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    amount REAL,
                    currency TEXT DEFAULT 'USD',
                    payment_method TEXT,
                    payment_id TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            conn.commit()
            conn.close()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
    def get_user(self, user_id):
        try:
            conn = sqlite3.connect('vpn_shop.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            user = cursor.fetchone()
            conn.close()
            return dict(user) if user else None
        except Exception as e:
            logger.error(f"Error getting user {user_id}: {e}")
            return None
    def create_user(self, user_id, username, first_name, language='en', referrer_id=None):
        try:
            conn = sqlite3.connect('vpn_shop.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO users (user_id, username, first_name, language_code, referrer_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, username, first_name, language, referrer_id))
            conn.commit()
            conn.close()
            logger.info(f"User {user_id} created with language {language}")
        except Exception as e:
            logger.error(f"Error creating user {user_id}: {e}")
    def set_language(self, user_id, language):
        try:
            conn = sqlite3.connect('vpn_shop.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET language_code = ? WHERE user_id = ?', (language, user_id))
            conn.commit()
            conn.close()
            logger.info(f"Language set to {language} for user {user_id}")
        except Exception as e:
            logger.error(f"Error setting language for user {user_id}: {e}")
    def get_language(self, user_id):
        user = self.get_user(user_id)
        return user['language_code'] if user and 'language_code' in user else 'en'
    def get_referral_count(self, user_id):
        try:
            conn = sqlite3.connect('vpn_shop.db')
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM users WHERE referrer_id = ?', (user_id,))
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except Exception as e:
            logger.error(f"Error getting referral count for {user_id}: {e}")
            return 0
    def get_stats(self):
        try:
            conn = sqlite3.connect('vpn_shop.db')
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM users')
            total_users = cursor.fetchone()[0]
            cursor.execute('SELECT COUNT(*) FROM users WHERE subscription_end > datetime("now")')
            active_subs = cursor.fetchone()[0]
            cursor.execute('SELECT SUM(total_paid) FROM users')
            revenue = cursor.fetchone()[0] or 0
            today = datetime.now().date()
            cursor.execute('''
                SELECT SUM(amount) FROM payments 
                WHERE DATE(created_at) = ? AND status = "completed"
            ''', (today,))
            today_revenue = cursor.fetchone()[0] or 0
            conn.close()
            return {
                'total_users': total_users,
                'active_subs': active_subs,
                'revenue': revenue,
                'today_revenue': today_revenue
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {'total_users': 0, 'active_subs': 0, 'revenue': 0, 'today_revenue': 0}
db = Database()
# Helper functions
def t(user_id, key, **kwargs):
    """Translate text based on user's language"""
    try:
        lang = db.get_language(user_id)
        text = TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, TRANSLATIONS['en'].get(key, key))
        if kwargs:
            return text.format(**kwargs)
        return text
    except Exception as e:
        logger.error(f"Translation error for key {key}: {e}")
        return key
def get_language_keyboard():
    """Get language selection keyboard"""
    keyboard = []
    for lang_code, lang_data in TRANSLATIONS.items():
        keyboard.append([InlineKeyboardButton(
            f"{lang_data['flag']} {lang_data['name']}",
            callback_data=f"lang_{lang_code}"
        )])
    return InlineKeyboardMarkup(keyboard)
# Subscription plans
PLANS = {
    "durations": [30, 60, 180],
    "plans": [
        {"name": "Basic", "devices": 1, "prices": {"30": 100  ₽, "60": 190 ₽, "180": 280  ₽  }},
        {"name": "Standard", "devices": 3, "prices": {"30": 180 ₽, "60": 400 ₽, "180": 600 ₽  }},
        {"name": "Premium", "devices": 5, "prices": {"30": 400 ₽, "60": 900 ₽, "180":1300 ₽    }}
    ]
}
# Main handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args
    referrer_id = None
    if args and args[0].startswith('ref'):
        try:
            referrer_id = int(args[0][3:])
        except:
            pass
    db_user = db.get_user(user.id)
    if not db_user:
        # Show language selection for new users
        message = " <b>Welcome! / Добро пожаловать! / स्वागत! / ًﻣﺮﺣﺒﺎ!</b>\n\n"
        message += "Please select your language:\n"
        message += "Пожалуйста, выберите язык:\n"
        message += "कृपया अपनी भाषा चुनें:\n"
        message += "ﯾﺮﺟﻰ اﺧﺘﯿﺎر ﻟﻐﺘﻚ:"
        reply_markup = get_language_keyboard()
        # Store referrer_id in context for after language selection
        if referrer_id:
            context.user_data['referrer_id'] = referrer_id
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='HTML')
        return
    # Existing user - show main menu
    status = get_subscription_status(user.id)
    message = t(user.id, 'welcome_back', name=user.first_name, status=status)
    reply_markup = get_main_menu(user.id)
    await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='HTML')
def get_main_menu(user_id):
    """Get main menu with translated buttons"""
    user = db.get_user(user_id)
    if not user or user['is_trial_used'] == 0:
        keyboard = [
            [InlineKeyboardButton(t(user_id, 'btn_trial'), callback_data="trial")],
            [InlineKeyboardButton(t(user_id, 'btn_buy'), callback_data="plans")],
            [InlineKeyboardButton(t(user_id, 'btn_about'), callback_data="about"),
             InlineKeyboardButton(t(user_id, 'btn_support'), callback_data="support")],
            [InlineKeyboardButton(t(user_id, 'btn_language'), callback_data="change_lang")]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton(t(user_id, 'btn_buy'), callback_data="plans")],
            [InlineKeyboardButton(t(user_id, 'btn_account'), callback_data="account")],
            [InlineKeyboardButton(t(user_id, 'btn_referral'), callback_data="referrals"),
             InlineKeyboardButton(t(user_id, 'btn_help'), callback_data="help")],
            [InlineKeyboardButton(t(user_id, 'btn_support'), callback_data="support"),
             InlineKeyboardButton(t(user_id, 'btn_language'), callback_data="change_lang")]
        ]
    if user_id in ADMIN_IDS:
        keyboard.append([InlineKeyboardButton(t(user_id, 'btn_admin'), callback_data="admin")])
    return InlineKeyboardMarkup(keyboard)
def get_subscription_status(user_id):
    """Get translated subscription status"""
    user = db.get_user(user_id)
    if not user or not user['subscription_end']:
        return t(user_id, 'status_no_sub')
    sub_end = user['subscription_end']
    if isinstance(sub_end, str):
        sub_end = datetime.fromisoformat(sub_end)
    if sub_end < datetime.now():
        return t(user_id, 'status_expired')
    days_left = (sub_end - datetime.now()).days
    return t(user_id, 'status_active', days=days_left)
# Button handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id
    # Language selection
    if data.startswith("lang_"):
        lang = data.split("_")[1]
        # Check if user already exists
        existing_user = db.get_user(user_id)
        if existing_user:
            # Update language for existing user
            db.set_language(user_id, lang)
            # Show updated main menu
            status = get_subscription_status(user_id)
            message = t(user_id, 'welcome_back', name=query.from_user.first_name, status=status)
            reply_markup = get_main_menu(user_id)
            await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='HTML')
        else:
            # Get referrer_id from context if it exists
            referrer_id = context.user_data.get('referrer_id', None)
            # Create new user with selected language
            db.create_user(user_id, query.from_user.username, query.from_user.first_name, lang, referrer_id)
            # Show welcome message
            message = t(user_id, 'welcome', name=query.from_user.first_name)
            if referrer_id:
                message += t(user_id, 'welcome_referred')
            else:
                message += t(user_id, 'welcome_trial')
            message += t(user_id, 'choose_option')
            reply_markup = get_main_menu(user_id)
            await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='HTML')
        return
    # Change language
    if data == "change_lang":
        message = t(user_id, 'btn_language') + "\n\nSelect your language:"
        reply_markup = get_language_keyboard()
        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='HTML')
        return
    # Route to handlers
    if data == "trial":
        await handle_trial(query)
    elif data == "plans":
        await show_plans(query)
    elif data.startswith("plan_"):
        plan_index = int(data.split("_")[1])
        await show_durations(query, plan_index)
    elif data.startswith("dur_"):
        _, plan_index, duration = data.split("_")
        await show_payment_methods(query, int(plan_index), int(duration))
    elif data.startswith("pay_"):
        parts = data.split("_")
        method = parts[1]
        plan_index = int(parts[2])
        duration = int(parts[3])
        await process_payment(query, user_id, method, plan_index, duration)
    elif data == "account":
        await show_account(query)
    elif data == "referrals":
        await show_referrals(query)
    elif data == "help":
        await show_help(query)
    elif data == "support":
        await show_support(query)
    elif data == "about":
        await show_about(query)
    elif data == "admin":
        await show_admin(query)
    elif data == "back_main":
        await back_to_main(query)
# Feature handlers
async def handle_trial(query):
    user_id = query.from_user.id
    user = db.get_user(user_id)
    if user['is_trial_used']:
        message = t(user_id, 'trial_used')
        keyboard = [
            [InlineKeyboardButton(t(user_id, 'btn_buy'), callback_data="plans")],
            [InlineKeyboardButton(t(user_id, 'btn_back'), callback_data="back_main")]
        ]
    else:
        days = 7 if user['referrer_id'] else 3
        expires_at = datetime.now() + timedelta(days=days)
        config_url = f"vless://trial-{user_id}@demo.server:443"
        # Update database
        try:
            conn = sqlite3.connect('vpn_shop.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET subscription_end = ?, is_trial_used = 1 WHERE user_id = ?',
                          (expires_at, user_id))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error activating trial for {user_id}: {e}")
        message = t(user_id, 'trial_activated',
                   days=days,
                   expires=expires_at.strftime('%Y-%m-%d %H:%M'),
                   config=config_url)
        keyboard = [
            [InlineKeyboardButton(t(user_id, 'btn_buy'), callback_data="plans")],
            [InlineKeyboardButton(t(user_id, 'btn_back'), callback_data="back_main")]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='HTML')
async def show_plans(query):
    user_id = query.from_user.id
    message = t(user_id, 'plans_title')
    keyboard = []
    for i, plan in enumerate(PLANS['plans']):
        devices = plan['devices']
        plan_name = plan['name']
        price_30 = plan['prices']['30']
        plural = 's' if devices > 1 else ''
        message += t(user_id, 'plan_item',
                    name=plan_name,
                    devices=devices,
                    plural=plural,
                    price=price_30)
        keyboard.append([InlineKeyboardButton(
            f" {plan_name} ({devices} device{plural})",
            callback_data=f"plan_{i}"
        )])
    message += t(user_id, 'plans_features')
    keyboard.append([InlineKeyboardButton(t(user_id, 'btn_back'), callback_data="back_main")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='HTML')
async def show_durations(query, plan_index):
    user_id = query.from_user.id
    plan = PLANS['plans'][plan_index]
    message = t(user_id, 'duration_title', plan_name=plan['name'], devices=plan['devices'])
    keyboard = []
    for duration in PLANS['durations']:
        price = plan['prices'][str(duration)]
        label = f"{duration} days" if duration < 365 else "1 year"
        monthly_price = price / (duration / 30)
        message += t(user_id, 'duration_item',
                    label=label,
                    price=price,
                    monthly=f"{monthly_price:.2f}")
        keyboard.append([InlineKeyboardButton(
            f" {label} - ${price}",
            callback_data=f"dur_{plan_index}_{duration}"
        )])
    keyboard.append([InlineKeyboardButton(t(user_id, 'btn_back'), callback_data="plans")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='HTML')
async def show_payment_methods(query, plan_index, duration):
    user_id = query.from_user.id
    plan = PLANS['plans'][plan_index]
    price = plan['prices'][str(duration)]
    message = t(user_id, 'payment_title',
               plan=f"{plan['name']} ({plan['devices']} devices)",
               duration=duration,
               price=price)
    keyboard = [
        [InlineKeyboardButton(" Telegram Stars", callback_data=f"pay_stars_{plan_index}_{duration}")],
        [InlineKeyboardButton(" Credit Card (Demo)", callback_data=f"pay_card_{plan_index}_{duration}")],
        [InlineKeyboardButton(" Crypto (Demo)", callback_data=f"pay_crypto_{plan_index}_{duration}")],
        [InlineKeyboardButton(t(user_id, 'btn_back'), callback_data=f"plan_{plan_index}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='HTML')
async def process_payment(query, user_id, method, plan_index, duration):
    plan = PLANS['plans'][plan_index]
    price = plan['prices'][str(duration)]
    # For Telegram Stars payment
    if method == "stars":
        # Send invoice
        title = f"{plan['name']} Plan - {duration} days"
        description = f"VPN subscription for {duration} days with {plan['devices']} devices"
        payload = f"plan_{plan_index}_dur_{duration}"
        currency = "XTR"  # Telegram Stars
        prices = [LabeledPrice(label=title, amount=int(price))]  # Price in Stars
        await query.bot.send_invoice(
            chat_id=user_id,
            title=title,
            description=description,
            payload=payload,
            provider_token="",  # Empty for Telegram Stars
            currency=currency,
            prices=prices
        )
        await query.answer("Opening payment window...")
        return
    # Demo payment for other methods
    try:
        conn = sqlite3.connect('vpn_shop.db')
        cursor = conn.cursor()
        # Update subscription
        current_time = datetime.now()
        cursor.execute('SELECT subscription_end FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        current_end = result[0] if result and result[0] else current_time
        if isinstance(current_end, str):
            current_end = datetime.fromisoformat(current_end)
        if current_end < current_time:
            current_end = current_time
        new_end = current_end + timedelta(days=duration)
        cursor.execute('UPDATE users SET subscription_end = ?, total_paid = total_paid + ? WHERE user_id = ?',
                      (new_end, price, user_id))
        config_url = f"vless://sub-{user_id}@demo.server:443"
        cursor.execute('''
            INSERT INTO subscriptions 
            (user_id, plan_name, devices, duration_days, price, payment_method, started_at, expires_at, config_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, plan['name'], plan['devices'], duration, price, method, current_time, new_end, config_url))
        conn.commit()
        conn.close()
        message = t(user_id, 'payment_success',
                   plan=plan['name'],
                   duration=duration,
                   price=price,
                   expires=new_end.strftime('%Y-%m-%d'),
                   config=config_url)
        keyboard = [
            [InlineKeyboardButton(t(user_id, 'btn_account'), callback_data="account")],
            [InlineKeyboardButton(t(user_id, 'btn_buy'), callback_data="plans")],
            [InlineKeyboardButton(t(user_id, 'btn_referral'), callback_data="referrals")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='HTML')
    except Exception as e:
        logger.error(f"Payment processing error for user {user_id}: {e}")
        await query.answer("Payment error. Please try again.")
# New handlers
async def show_account(query):
    user_id = query.from_user.id
    user = db.get_user(user_id)
    if not user:
        await query.answer("Error loading account")
        return
    status = get_subscription_status(user_id)
    refs = db.get_referral_count(user_id)
    message = t(user_id, 'account_title',
               user_id=user_id,
               name=user['first_name'],
               date=user['created_at'][:10] if user['created_at'] else 'N/A',
               status=status,
               spent=user['total_paid'],
               refs=refs)
    keyboard = [
        [InlineKeyboardButton(t(user_id, 'btn_buy'), callback_data="plans")],
        [InlineKeyboardButton(t(user_id, 'btn_back'), callback_data="back_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='HTML')
async def show_referrals(query):
    user_id = query.from_user.id
    bot_username = (await query.bot.get_me()).username
    ref_link = f"https://t.me/{bot_username}?start=ref{user_id}"
    ref_count = db.get_referral_count(user_id)
    earnings = ref_count * 1.0  # Example
    message = t(user_id, 'referral_title',
               earnings=earnings,
               count=ref_count,
               link=ref_link)
    keyboard = [
        [InlineKeyboardButton(t(user_id, 'btn_back'), callback_data="back_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='HTML')
async def show_help(query):
    user_id = query.from_user.id
    message = t(user_id, 'help_text', support=SUPPORT_USERNAME)
    keyboard = [
        [InlineKeyboardButton(t(user_id, 'btn_support'), callback_data="support")],
        [InlineKeyboardButton(t(user_id, 'btn_back'), callback_data="back_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='HTML')
async def show_support(query):
    user_id = query.from_user.id
    message = t(user_id, 'support_text', support=SUPPORT_USERNAME)
    keyboard = [
        [InlineKeyboardButton(t(user_id, 'btn_back'), callback_data="back_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='HTML')
async def show_about(query):
    user_id = query.from_user.id
    message = t(user_id, 'about_text')
    keyboard = [
        [InlineKeyboardButton(t(user_id, 'btn_buy'), callback_data="plans")],
        [InlineKeyboardButton(t(user_id, 'btn_back'), callback_data="back_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='HTML')
async def show_admin(query):
    user_id = query.from_user.id
    if user_id not in ADMIN_IDS:
        await query.answer("Access denied")
        return
    stats = db.get_stats()
    message = t(user_id, 'admin_title',
               total_users=stats['total_users'],
               active_subs=stats['active_subs'],
               revenue=stats['revenue'],
               today_revenue=stats['today_revenue'])
    keyboard = [
        [InlineKeyboardButton(t(user_id, 'btn_back'), callback_data="back_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='HTML')
# Payment handlers
async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Answer pre-checkout query"""
    query = update.pre_checkout_query
    await query.answer(ok=True)
async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle successful payment"""
    user_id = update.effective_user.id
    payment_info = update.message.successful_payment
    # Parse payload
    payload = payment_info.invoice_payload
    parts = payload.split("_")
    plan_index = int(parts[1])
    duration = int(parts[3])
    plan = PLANS['plans'][plan_index]
    price = plan['prices'][str(duration)]
    # Update database
    try:
        conn = sqlite3.connect('vpn_shop.db')
        cursor = conn.cursor()
        current_time = datetime.now()
        cursor.execute('SELECT subscription_end FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        current_end = result[0] if result and result[0] else current_time
        if isinstance(current_end, str):
            current_end = datetime.fromisoformat(current_end)
        if current_end < current_time:
            current_end = current_time
        new_end = current_end + timedelta(days=duration)
        cursor.execute('UPDATE users SET subscription_end = ?, total_paid = total_paid + ? WHERE user_id = ?',
                      (new_end, price, user_id))
        config_url = f"vless://paid-{user_id}@demo.server:443"
        cursor.execute('''
            INSERT INTO subscriptions 
            (user_id, plan_name, devices, duration_days, price, payment_method, started_at, expires_at, config_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, plan['name'], plan['devices'], duration, price, 'telegram_stars', current_time, new_end, config_url))
        cursor.execute('''
            INSERT INTO payments (user_id, amount, currency, payment_method, payment_id, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, price, payment_info.currency, 'telegram_stars', payment_info.telegram_payment_charge_id, 'completed'))
        conn.commit()
        conn.close()
        message = t(user_id, 'payment_success',
                   plan=plan['name'],
                   duration=duration,
                   price=price,
                   expires=new_end.strftime('%Y-%m-%d'),
                   config=config_url)
        keyboard = [
            [InlineKeyboardButton(t(user_id, 'btn_account'), callback_data="account")],
            [InlineKeyboardButton(t(user_id, 'btn_buy'), callback_data="plans")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='HTML')
    except Exception as e:
        logger.error(f"Error processing payment for {user_id}: {e}")
async def back_to_main(query):
    user_id = query.from_user.id
    user = query.from_user
    status = get_subscription_status(user_id)
    message = t(user_id, 'welcome_back', name=user.first_name, status=status)
    reply_markup = get_main_menu(user_id)
    await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='HTML')
def main():
    if not BOT_TOKEN or BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        print(" ERROR: Please update config.json with your bot token!")
        print("1. Open config.json")
        print("2. Replace 'YOUR_BOT_TOKEN_HERE' with your actual bot token from @BotFather")
        return
    print("=" * 60)
    print(" MULTILINGUAL VPN SHOP BOT - FIXED VERSION")
    print("=" * 60)
    print("\n Languages:")
    print("   English")
    print("   Russian")
    print("   Hindi")
    print("   Arabic")
    print("\n Payment methods:")
    print("   Telegram Stars (Real)")
    print("   Credit Card (Demo)")
    print("   Crypto (Demo)")
    print("\n Fixes Applied:")
    print("   Removed imghdr dependency")
    print("   Fixed NameError issues")
    print("   Added all missing handlers")
    print("   Improved error handling")
    print("\n Bot is starting...")
    print("=" * 60)
    try:
        app = Application.builder().token(BOT_TOKEN).build()
        # Add handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(button_handler))
        app.add_handler(PreCheckoutQueryHandler(precheckout_callback))
        app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))
        print("\n Bot is running!")
        print(" Test all 4 languages!")
        print(" Telegram Stars payment enabled!\n")
        print("
  Press Ctrl+C to stop")
        print("=" * 60)
        # Use run_polling with proper configuration
        app.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True,
            close_loop=False
        )
    except Exception as e:
        logger.error(f"Bot startup error: {e}")
        print(f"\n Error starting bot: {e}")
        print("Please check your bot token in config.json")
if __name__ == '__main__':
    main()
