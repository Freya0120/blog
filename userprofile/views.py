from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserRegisterForm, ProfileForm
from .models import Profile


def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return redirect("article:article_list")
            else:
                return HttpResponse("账号或密码输入有误，请重新输入")
        else:
            return HttpResponse("账号或密码输入不合法")
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form': user_login_form}
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


def user_logout(request):
    logout(request)
    return redirect("article:article_list")


def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect("article:article_list")
        else:
            return HttpResponse("注册表单输入有误，请重新输入")
    elif request.method == "GET":
        user_register_form = UserRegisterForm()
        context = {'form': user_register_form}
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


@login_required(login_url='/userprofile/login')
def user_delete(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        if request.user == user:
            # 退出登录，删除数据并返回博客列表
            logout(request)
            user.delete()
            return redirect("article:article_list")
        else:
            return HttpResponse("您没有删除的权限")
    else:
        return HttpResponse("仅接受POST请求")


# 编辑用户函数
@login_required(login_url='/userprofile/login')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    # user_id 是 OneToOneField 自动生成的字段
    if Profile.objects.filter(user_id=user).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        # 是否为本人修改数据
        if request.user != user:
            return HttpResponse("您没有权限修改此用户信息")

        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
    #     if profile_form.is_valid():
    #         profile_cd = profile_form.cleaned_data
    #         profile.phone = profile_cd['phone']
    #         if 'avatar' in request.FILES:
    #             profile.avatar = profile_cd["avatar"]
    #         profile.bio = profile_cd['bio']
    #         profile.save()
    #         # 带参数的重定向
    #         return redirect("userprofile:edit", id=id)
    #     else:
    #         return HttpResponse("表单输入有误，请重新输入")
    #
    # elif request.method == "GET":
    #     profile_form = ProfileForm()
    #     context = {'profile_form': profile_form, 'profile': profile, 'user': user}
    #     return render(request, 'userprofile/edit.html', context)
    # else:
    #     return HttpResponse("请使用GET或POST请求数据")
        if profile_form.is_valid():
            profile = profile_form.save()  # 你可以使用 save() 方法来保存表单并自动更新 profile 对象
            # 如果需要额外的逻辑，可以在这里添加
            return redirect("userprofile:edit", id=id)
        else:
            # 表单验证失败，重新显示表单
            context = {'profile_form': profile_form, 'profile': profile, 'user': user}
            return render(request, 'userprofile/edit.html', context)

            # GET 请求时创建空表单
    profile_form = ProfileForm(instance=profile)
    context = {'profile_form': profile_form, 'profile': profile, 'user': user}
    return render(request, 'userprofile/edit.html', context)