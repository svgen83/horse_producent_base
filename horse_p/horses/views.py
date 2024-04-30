from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.timezone import localtime
# Create your views here.
from horses.models import (Equine, Lab_group, Employee,
                           Calendar, Manipulation, Antigen, Restriction) 
##from django.views.generic.list import ListView
from datetime import datetime, timedelta, date
import pandas as pd
from itertools import chain
from django.contrib.auth.decorators import login_required



def get_duration(current_date, initial_date, time_factor):
    delta_time = current_date - initial_date
    time_in_use = int(delta_time.total_seconds()/(60*60*24*365))
    return time_in_use


@login_required 
def index(request):
    try:
        current_date =  datetime.now().date()
        equines = Equine.objects.all()
        employees = Employee.objects.all()
        current_day_msgs = []
        calendars = Calendar.objects.filter(date_manipulation=current_date)
        for calendar in calendars:
            current_day_msgs.append(f'''Сегодня {calendar}
                                    в группе {calendar.groups}
                                    осуществляется {calendar.manipulations}
                                    по {calendar.manipulations.volume}
                                    {calendar.manipulations.volume_measure}.
                                    Антиген {calendar.groups.antigen}.
                                    ''')
        #current_day_msg = "\n".join(current_day_msgs)
        print(current_day_msgs)
    except ObjectDoesNotExist:
        current_day_msgs = [f'''Сегодня {current_date} манипуляций с лошадьми не производится''']
    finally:
        current_date =  datetime.now().date()
        equines = Equine.objects.all()
        employees = Employee.objects.all()
        antigens = Antigen.objects.all()
        return render(request,
                      "index.html",
                      context={
                          'equines':equines,
                          'employees': employees,
                          'current_day_msgs': current_day_msgs,
                          'antigens': antigens,
                            })


def horse(request, id):
    try:
        horse = Equine.objects.get(id=id)
        current_date =  datetime.now().date()
        year = 60*60*24*365
        commissioning_duration = get_duration(current_date,
                                              horse.commissioning_date,
                                              year)

        antigen_type = horse.lab_group.antigen
        list_restrictions = []

        restrictions = Restriction.objects.filter(equine=horse)
        
        for restriction in restrictions:
            print(restriction.title)
                
        if restrictions:
            restrictions_dates = []                     
            restrictions_dates.append(pd.date_range(
                start=restriction.begin_restriction,
                end=restriction.end_restriction).tolist())
            restrictions_dates_p = list(
                chain.from_iterable(restrictions_dates))
            exclude_dates = [date.date() for date in restrictions_dates_p]
            
            horse_acts = Calendar.objects.filter(
            groups__antigen__title__contains=antigen_type).filter(
            groups=horse.lab_group).exclude(date_manipulation__in=exclude_dates)
        else:
            horse_acts = Calendar.objects.filter(
            groups__antigen__title__contains=antigen_type).filter(
            groups=horse.lab_group)

        immunisation_count = horse_acts.filter(
            manipulations__title__contains='ммунизац').count()
        bloodlets_count = horse_acts.filter(
            manipulations__title__contains='кров').count()
        #print(list_restrictions)
        return render(request, "horse.html",
                      context={
                          'horse': horse,
                          'commissioning_duratuon': commissioning_duration,
                          'antigen_type': antigen_type,
                          'immunisation_count': immunisation_count,
                          'bloodlets_count': bloodlets_count,
                          'restrictions': restrictions,
                           })
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Такая лошадь не найдена</h1>')


def calendar(request):
    dates = Calendar.objects.all()
    
    return render(request,
                  "calendar.html",
                  context={'dates': dates,
                           })


def group(request, title):
    try:
        group = Lab_group.objects.get(title=title)
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Такая группа не найдена</h1>')
    
    return render(request,
                  "group.html",
                  context={'group': group,
                           })


def get_volume_stat(actions):
    manipulate_volumes = 0
    for action in actions:
        date = action.date_manipulation
        group_number = action.groups
        equines_in_group = Equine.objects.filter(
            lab_group__title__contains=group_number).exclude(
                restriction_to_use__end_restriction__gte=date,
                restriction_to_use__begin_restriction__lte=date
                ).exclude(date_of_death__lte=date)      
        equines_in_group_count = equines_in_group.count()
        manipulate_volume = int(
            action.manipulations.volume)*equines_in_group_count
        print(date, equines_in_group, manipulate_volume)
        manipulate_volumes += manipulate_volume
    return manipulate_volumes


def statistics(request, name):
    year_period = 2024

    antigen = Antigen.objects.get(pk=name)
    
    rabies_horse_acts = Calendar.objects.filter(
        groups__antigen__title=antigen.title)
    acts_statistic = []
    equine_count = 0
    year_antigen_volume = 0
    year_blood_volume = 0
    year_bloodlets_count = 0
    year_immunisations_count = 0

    for period in range(1, 13):
        acts_in_month = rabies_horse_acts.filter(
            date_manipulation__year=year_period).filter(
                date_manipulation__month=period)
        
        immunisations = acts_in_month.filter(
            manipulations__title__contains='ммунизац')
        immunisations_count = immunisations.count()

        bloodlets = acts_in_month.filter(manipulations__title__contains='кров')
        bloodlets_count = bloodlets.count()
        
        antigen_volumes = get_volume_stat(immunisations)
        blood_volumes = get_volume_stat(bloodlets)

        act_statistic = {'immunisation_counts': immunisations_count,
                        'bloodlet_counts': bloodlets_count,
                        'antigen_volumes': antigen_volumes,
                        'blood_volumes': blood_volumes}
        acts_statistic.append(act_statistic)
        
        year_antigen_volume += antigen_volumes
        year_blood_volume += blood_volumes
        year_bloodlets_count += bloodlets_count
        year_immunisations_count += immunisations_count
    return render(request,
                  "statistics.html",
                  context={'acts_statistic': acts_statistic,
                           'year_period': year_period,
                           'year_antigen_volume': year_antigen_volume,
                           'year_blood_volume': year_blood_volume,
                           'year_bloodlets_count': year_bloodlets_count,
                           'year_immunisations_count': year_immunisations_count,
                           'antigen': antigen,
                           })
