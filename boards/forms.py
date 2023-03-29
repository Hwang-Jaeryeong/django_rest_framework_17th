from django import forms


class BoardForm(forms.Form):
    title = forms.CharField(
        error_messages={
            'required': '제목을 입력해주세요.'
        }, max_length=100, label="제목")
    contents = forms.CharField(
        error_messages={
            'required': '내용을 입력해주세요.'
        },widget=forms.Textarea, label = "내용")
    # 태그를 입력하지 않아도 오류가 뜨지 않게 기존의 필드 선언과는 다르게 required=False로 선언
    tags = forms.CharField(required=False, label="태그")


