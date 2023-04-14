from django.shortcuts import render

# Create your views here.


def daily_calendar(request):
    return render(request, template_name='tasks/daily-calendarTEMPLATE.html')
