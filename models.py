"""
日本不動產投資分析工具 - 資料庫模型
包含用戶認證、案件管理、分析結果等資料模型
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """用戶資料模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(255), primary_key=True)
    google_id = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    avatar_url = db.Column(db.Text)
    preferences = db.Column(db.Text)  # JSON 格式存儲用戶偏好設定
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 關聯關係
    properties = db.relationship('Property', backref='owner', lazy=True, cascade='all, delete-orphan')
    analysis_results = db.relationship('AnalysisResult', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def get_preferences(self):
        """獲取用戶偏好設定"""
        if self.preferences:
            return json.loads(self.preferences)
        return {}
    
    def set_preferences(self, preferences_dict):
        """設定用戶偏好"""
        self.preferences = json.dumps(preferences_dict)
    
    def to_dict(self):
        """轉換為字典格式"""
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'avatar_url': self.avatar_url,
            'preferences': self.get_preferences(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Property(db.Model):
    """不動產案件資料模型"""
    __tablename__ = 'properties'
    
    id = db.Column(db.String(255), primary_key=True)
    user_id = db.Column(db.String(255), db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text)
    property_type = db.Column(db.String(50))  # 1LDK, 2LDK, tower, house
    price = db.Column(db.Numeric(15, 2))
    status = db.Column(db.String(50), default='considering')  # considering, purchased, sold
    parameters = db.Column(db.Text)  # JSON 格式存儲分析參數
    tags = db.Column(db.Text)  # JSON 格式存儲標籤
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 關聯關係
    analysis_results = db.relationship('AnalysisResult', backref='property', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Property {self.name}>'
    
    def get_parameters(self):
        """獲取分析參數"""
        if self.parameters:
            return json.loads(self.parameters)
        return {}
    
    def set_parameters(self, parameters_dict):
        """設定分析參數"""
        self.parameters = json.dumps(parameters_dict)
    
    def get_tags(self):
        """獲取標籤列表"""
        if self.tags:
            return json.loads(self.tags)
        return []
    
    def set_tags(self, tags_list):
        """設定標籤"""
        self.tags = json.dumps(tags_list)
    
    def to_dict(self):
        """轉換為字典格式"""
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'property_type': self.property_type,
            'price': float(self.price) if self.price else None,
            'status': self.status,
            'parameters': self.get_parameters(),
            'tags': self.get_tags(),
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class AnalysisResult(db.Model):
    """分析結果資料模型"""
    __tablename__ = 'analysis_results'
    
    id = db.Column(db.String(255), primary_key=True)
    user_id = db.Column(db.String(255), db.ForeignKey('users.id'), nullable=False)
    property_id = db.Column(db.String(255), db.ForeignKey('properties.id'), nullable=True)
    analysis_type = db.Column(db.String(50), nullable=False)  # financial, comparison, sensitivity
    parameters = db.Column(db.Text)  # JSON 格式存儲輸入參數
    results = db.Column(db.Text)  # JSON 格式存儲分析結果
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AnalysisResult {self.analysis_type}>'
    
    def get_parameters(self):
        """獲取分析參數"""
        if self.parameters:
            return json.loads(self.parameters)
        return {}
    
    def set_parameters(self, parameters_dict):
        """設定分析參數"""
        self.parameters = json.dumps(parameters_dict)
    
    def get_results(self):
        """獲取分析結果"""
        if self.results:
            return json.loads(self.results)
        return {}
    
    def set_results(self, results_dict):
        """設定分析結果"""
        self.results = json.dumps(results_dict)
    
    def to_dict(self):
        """轉換為字典格式"""
        return {
            'id': self.id,
            'property_id': self.property_id,
            'analysis_type': self.analysis_type,
            'parameters': self.get_parameters(),
            'results': self.get_results(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        } 