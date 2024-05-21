from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
from horses.models import (Equine, Lab_group, Employee,
                           Calendar, Manipulation, Antigen, Restriction)
from datetime import datetime
import pandas as pd
from itertools import chain
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Case, When, IntegerField


def get_duration(current_date, initial_date, time_factor):
    delta_time = current_date - initial_date
    time_in_use = int(delta_time.total_seconds()/(60*60*24*365))
    return time_in_use


@login_required
def index(request):
    try:
        current_date = datetime.now().date()
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
    except ObjectDoesNotExist:
        current_day_msgs = [f'''Сегодня {current_date} манипуляций с лошадьми не производится''']
    finally:
        current_date = datetime.now().date()
        equines = Equine.objects.all()
        employees = Employee.objects.all()
        antigens = Antigen.objects.all()
        return render(request,
                      "index.html",
                      context={
                          'equines': equines,
                          'employees': employees,
                          'current_day_msgs': current_day_msgs,
                          'antigens': antigens,
                            })


def horse(request, id):
    try:
        horse = Equine.objects.get(id=id)
        current_date = datetime.now().date()
        year = 60*60*24*365
        commissioning_duration = get_duration(current_date,
                                              horse.commissioning_date,
                                              year)

        antigen_type = horse.lab_group.antigen

        restrictions = Restriction.objects.filter(equine=horse)
        if restrictions:
            restrictions_dates = []
            for restriction in restrictions:
                restrictions_dates.append(pd.date_range(
                    start=restriction.begin_restriction,
                    end=restriction.end_restriction).tolist())
                restrictions_dates_p = list(
                    chain.from_iterable(restrictions_dates))
                exclude_dates = [date.date() for date in restrictions_dates_p]
                horse_acts = Calendar.objects.filter(
                    groups__antigen__title__contains=antigen_type).filter(
                        groups=horse.lab_group).exclude(
                            date_manipulation__in=exclude_dates)
        else:
            horse_acts = Calendar.objects.filter(
                groups__antigen__title__contains=antigen_type).filter(
                    groups=horse.lab_group) 

        immunisation_count = horse_acts.filter(
            manipulations__title__contains='ммунизац').count()
        bloodlets_count = horse_acts.filter(
            manipulations__title__contains='кров').count()
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
    duplicates = Calendar.objects.values('date_manipulation'
    ).annotate(date_count=Count('date_manipulation')).filter(date_count__gte=1
    ).order_by('date_manipulation').reverse()
    dates = []
    for duplicate in duplicates:
        record = {'date_manipulation': duplicate['date_manipulation'],
                  'objects': Calendar.objects.filter(
                       date_manipulation__in=[duplicate['date_manipulation']]),
                       }              
        dates.append(record)
    return render(request,
                  "calendar.html",
                  context={'dates': dates,
                           })


def group(request, title):
    try:
        group = Lab_group.objects.get(title=title)
        equines_in_use = group.equine.filter(in_operation=True)

    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Такая группа не найдена</h1>')

    return render(request,
                  "group.html",
                  context={'group': group,
                           'equines_in_use': equines_in_use,
                           })


def get_volume_stat(actions):
    manipulate_volumes = 0
    equines_count = 0
    for action in actions:
        date = action.date_manipulation
        group_number = action.groups
        equines_in_group = Equine.objects.filter(
            lab_group__title__contains=group_number).exclude(
                restriction_to_use__end_restriction__gte=date,
                restriction_to_use__begin_restriction__lte=date
                ).exclude(date_of_death__lte=date)
        equines_in_group_count = equines_in_group.count()
        manipulate_volume = action.manipulations.volume*equines_in_group_count
        manipulate_volumes += manipulate_volume
        equines_count += equines_in_group_count
    return manipulate_volumes,equines_count 


def statistics(request, name):
    dates = Calendar.objects.all()
    years_ = []
    for i in dates:
        years_.append((i.date_manipulation).year)
    years = list(dict.fromkeys(years_))
    year_period = request.POST.get('year')

    antigen = Antigen.objects.get(pk=name)

    horse_acts = Calendar.objects.filter(
        groups__antigen__title=antigen.title)
    acts_statistic = []
    year_antigen_volume = 0
    year_blood_volume = 0
    year_bloodlets_count = 0
    year_immunisations_count = 0
 
    for period in range(1, 13):
        acts_in_month = horse_acts.filter(
            date_manipulation__year=year_period).filter(
                date_manipulation__month=period)

        immunisations = acts_in_month.filter(
            manipulations__title__icontains='ммунизац')
        immunisations_count = immunisations.count()

        bloodlets = acts_in_month.filter(
            manipulations__title__icontains='кров').exclude(
                manipulations__title__icontains='пробирк')
        bloodlets_count = bloodlets.count()

        antigen_volumes, antigen_horse_count = get_volume_stat(immunisations)
        blood_volumes, blood_horse_count = get_volume_stat(bloodlets)

        act_statistic = {
            'immunisation_counts': immunisations_count,
            'bloodlet_counts': bloodlets_count,
            'antigen_volumes': antigen_volumes,
            'blood_volumes': blood_volumes,
            'antigen_horse_count': antigen_horse_count,
            'blood_horse_count': blood_horse_count,
            }
        acts_statistic.append(act_statistic)

        year_antigen_volume += antigen_volumes
        year_blood_volume += blood_volumes
##        year_bloodlets_count += bloodlets_count
##        year_immunisations_count += immunisations_count
        year_bloodlets_count += blood_horse_count
        year_immunisations_count += antigen_horse_count
    return render(request,
                  "statistics.html",
                  context={
                      'acts_statistic': acts_statistic,
                      'year_period': year_period,
                      'years': years,
                      'year_antigen_volume': year_antigen_volume,
                      'year_blood_volume': year_blood_volume,
                      'year_bloodlets_count': year_bloodlets_count,
                      'year_immunisations_count': year_immunisations_count,
                      'antigen': antigen,
                      'antigen_measure': antigen.volume_measure,
                           })
