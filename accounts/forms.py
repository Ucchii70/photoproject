#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# UserCreationFormクラスをインポート
from django.contrib.auth.forms import UserCreationForm
# models.pyで定義したカスタムUserモデルをインポート
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    UserCreationFormのサブ (子)クラス
    """
    class Meta:
        """UserCreationFormのインナークラス
        Attributes:
            model:連携するUserモデル
            fields:フォームで使用するフィールド
        """
        # 連携するUserモデルを設定
        model = CustomUser
        
        # フォームで使用するフィールドを設定
        # ユーザー名、メールアドレス、パスワード、確認用パスワード
        fields =  ('username', 'email', 'password1', 'password2')
        