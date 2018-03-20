#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import redirect
from django.shortcuts import render


def index(request):
    return redirect('/navi/')



def test(request):
    return render(request,'test.html')