# signupビュークラスとsignup_successビューを定義
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy

class SignUpView(CreateView):
    """サインアップページのビュー
    """
    
    # forms.pyで定義したフォームのクラス
    form_class = CustomUserCreationForm
    
    # レンダリング(コンテンツをブラウザに表示可能な形式に変換する)するテンプレート
    template_name = 'signup.html'

    # サインアップ完了後のリダイレクト先のURLパターン
    success_url = reverse_lazy('accounts:signup_success')

    def form_valid(self, form):
        """CreateViewクラスのform_valid()をオーバーライド

        フォームのバリデーション(与えられたデータが特定の条件や基準を満たしているかどうかを検証する)を通過した時に呼ばれるフォームデータの登録を行う
        parameters:
            form(django.forms.Form):
                form_classに格納されているCustomUserCreationFormオブジェクト
            return:
                HttpResponseRedirectオブジェクト:
                    スーパークラスのform_valid()の戻り値を返すことで、success_urlで格納されているURLにリダイレクトさせる
        """
        # formオブジェクトのフィールドの値をデータベースに保存
        user = form.save()
        self.object = user
        # 戻り値はスーパークラスのform_valid()の戻り値(HttpResponseRedirect)
        return super().form_valid(form)
    
class SignUpSuccessView(TemplateView):
    """
    サインアップ完了ページビュー
    """
    # レンダリングするテンプレート
    template_name = 'signup_success.html'


