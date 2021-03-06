from django.contrib import messages
from django.shortcuts import render, redirect

from routes.models import Rout
from trains.models import Train
from .forms import RoutForm, RoutModelForm


# Create your views here.

def dfs_paths(graph, start, goal):
    """Функция поиска всех возможных маршрутов
       из одного города в другой. Вариант посещения
       одного и того же города более одного раза,
        не рассматривается.
    """
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == goal:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_]))


def get_graph():
    qs = Train.objects.values('from_city')
    from_city_set = set(i['from_city'] for i in qs)
    graph = {}
    for city in from_city_set:
        trans = Train.objects.filter(from_city=city).values('to_city')
        tmp = set(i['to_city'] for i in trans)
        graph[city] = tmp
    return graph


def home(request):
    form = RoutForm()
    return render(request, 'routes/home.html', {'form': form})


def find_routes(request):
    if request.method == 'POST':
        form = RoutForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            from_city = data['from_city']
            to_city = data['to_city']
            across_cities_form = data['across_cities']
            travel_times = data['traveling_time']
            graph = get_graph()
            all_ways = list(dfs_paths(graph, from_city.id, to_city.id))
            if len(all_ways) == 0:
                messages.error(request, 'Нет такого маршрута')
                return render(request, 'routes/home.html', {'form': form})
            if across_cities_form:
                across_cities = [city.id for city in across_cities_form]
                right_ways = []
                for way in all_ways:
                    if all(point in way for point in across_cities):
                        right_ways.append(way)
                if not right_ways:
                    messages.error(request, 'Маршрут через эти города не возможен')
                    return render(request, 'routes/home.html', {'form': form})
            else:
                right_ways = all_ways

            trains = []
            for route in right_ways:
                tmp = {}
                tmp['trains'] = []
                total_time = 0
                for index in range(len(route) - 1):
                    qs = Train.objects.filter(from_city=route[index], to_city=route[index + 1])
                    qs = qs.order_by('travel_time').first()
                    total_time += qs.travel_time
                    tmp['trains'].append(qs)
                tmp['total_time'] = total_time
                if total_time <= travel_times:
                    trains.append(tmp)
            if not trains:
                messages.error(request, 'Время в дороге больше выбранного')
                return render(request, 'routes/home.html', {'form': form})
            routes = []
            cities = {'from_city': from_city.name, 'to_city': to_city.name}
            for tr in trains:
                routes.append({'route': tr['trains'], 'total_time': tr['total_time'], 'from_city': from_city.name,
                               'to_city': to_city.name})
            sorted_routes = []
            if len(routes) == 1:
                sorted_routes = routes
            else:
                times = list(set(x['total_time'] for x in routes))
                times = sorted(times)
                for time in times:
                    for route in routes:
                        if time == route['total_time']:
                            sorted_routes.append(route)

            context = {}
            form = RoutForm()
            context['form'] = form
            context['routes'] = sorted_routes
            context['cities'] = cities
            return render(request, 'routes/home.html', context)

        return render(request, 'routes/home.html', {'form': form})
    else:
        messages.error(request, 'Создайте маршрут')
        form = RoutForm()
        return render(request, 'routes/home.html', {'form': form})


def add_route(request):
    if request.method == 'POST':
        form = RoutModelForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            name = data['name']
            travel_times = data['travel_times']
            from_city = data['from_city']
            to_city = data['to_city']
            across_cities = data['across_cities']
            trains = [int(x) for x in across_cities if x.isalnum()]
            qs = Train.objects.filter(id__in=trains)
            route = Rout(name=name, from_city=from_city, to_city=to_city, travel_times=travel_times)
            route.save()
            for dr in qs:
                route.across_cities.add(dr.id)
            messages.success(request, 'Маршрут успешно сохранён')
            return redirect('/')

    else:
        data = request.GET
        if data:
            travel_times = data['travel_times']
            from_city = data['from_city']
            to_city = data['to_city']
            across_cities = data['across_cities']
            trains = [int(x) for x in across_cities if x.isalnum()]
            qs = Train.objects.filter(id__in=trains)
            train_list = ' '.join(str(i) for i in trains)
            form = RoutModelForm(initial={'from_city': from_city, 'to_city': to_city,
                                          'across_cities': train_list, 'travel_times': travel_times})
            route_desc = []
            for tr in qs:
                dsc = 'Поезд {} следующий из г.{} в г.{} .Время в пути {} '.format(tr.name, tr.from_city, tr.to_city, tr.travel_time)
                route_desc.append(dsc)
            context = {'form': form, 'descr': route_desc, 'from_city': from_city, 'to_city': to_city, 'travel_times': travel_times}

            #assert False
            return render(request, 'routes/create.html', context)
        else:
            messages.error(request, 'Невозможно сохранить маршрут')
            return redirect('/')
