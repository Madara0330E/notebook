from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from datetime import date
from .models import Person, Contact, Relationship, Greeting, GreetingTemplate, Event
from .forms import PersonForm, ContactForm, RelationshipForm


def get_reverse_relationship(relationship_type):
    reverse_map = {
        'Муж': 'Жена',
        'Жена': 'Муж',
        'Отец': 'Сын/Дочь',
        'Мать': 'Сын/Дочь',
        'Сын': 'Отец/Мать',
        'Дочь': 'Отец/Мать',
        'Сын/Дочь': 'Отец/Мать',
        'Брат': 'Брат/Сестра',
        'Сестра': 'Брат/Сестра',
        'Брат/Сестра': 'Брат/Сестра',
        'Друг': 'Друг',
        'Подруга': 'Подруга',
        'Коллега': 'Коллега',
        'Начальник': 'Подчинённый',
        'Подчинённый': 'Начальник',
    }
    return reverse_map.get(relationship_type, relationship_type)


def index(request):
    search_query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'last_name')
    persons = Person.objects.all()

    if search_query:
        persons = persons.filter(
            Q(last_name__icontains=search_query) | 
            Q(first_name__icontains=search_query) |
            Q(patronymic__icontains=search_query)
        )

    if sort_by == 'date':
        persons = persons.order_by('-id')
    elif sort_by == 'alphabet':
        persons = persons.order_by('last_name', 'first_name')
    else:
        persons = persons.order_by('last_name')

    today = date.today()
    birthday_people = Person.objects.filter(
        birth_date__month=today.month,
        birth_date__day=today.day
    )

    for person in birthday_people:
        event_type = f"День рождения {today.year}"
        event, created = Event.objects.get_or_create(
            person=person,
            event_type=event_type,
            defaults={
                'event_date': today,
                'reminder_days': 0
            }
        )
        
        if not Greeting.objects.filter(person=person, event=event).exists():
            template = GreetingTemplate.objects.filter(event_type__icontains="День рождения").first()
            if template:
                text = template.template_text.replace("{name}", person.first_name)
            else:
                text = f"С Днем Рождения, {person.first_name}!"
            
            Greeting.objects.create(
                person=person,
                event=event,
                greeting_text=text,
                template=template
            )

    greetings = Greeting.objects.filter(
        event__event_date=today,
        is_sent=False
    )

    context = {
        'persons': persons,
        'search_query': search_query,
        'birthday_people': birthday_people,
        'greetings': greetings,
    }
    return render(request, 'notebook/gallery.html', context)

def show(request, id):
    person = get_object_or_404(Person, id=id)
    contacts = person.contact_set.all()
    relations_as_person = person.person.all() 
    relations_as_related = Relationship.objects.filter(related_person=person)
    relations = list(relations_as_person) + list(relations_as_related)
    
    context = {
        'person': person,
        'contacts': contacts,
        'relations': relations,
    }
    return render(request, 'notebook/person_detail.html', context)

def create(request):
    if request.method == "POST":
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save()
            return redirect('show', id=person.id)
    else:
        form = PersonForm()
    return render(request, 'notebook/person_form.html', {'form': form, 'title': 'Добавить человека'})

def update(request, id):
    person = get_object_or_404(Person, id=id)
    if request.method == "POST":
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('show', id=person.id)
    else:
        form = PersonForm(instance=person)
    return render(request, 'notebook/person_form.html', {'form': form, 'title': 'Редактировать'})

def delete(request, id):
    person = get_object_or_404(Person, id=id)
    person.delete()
    return redirect('index')

def add_contact(request, id):
    person = get_object_or_404(Person, id=id)
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.person = person
            contact.save()
            return redirect('show', id=person.id)
    else:
        form = ContactForm()
    return render(request, 'notebook/contact_form.html', {'form': form, 'person': person, 'title': 'Добавить контакт'})

def add_relationship(request, id):
    person = get_object_or_404(Person, id=id)
    if request.method == "POST":
        form = RelationshipForm(request.POST)
        if form.is_valid():
            relation = form.save(commit=False)
            relation.person = person
            relation.save()
            
            related_person = relation.related_person
            reverse_relationship_type = get_reverse_relationship(relation.relationship_type)
            
            if not Relationship.objects.filter(
                person=related_person,
                related_person=person,
                relationship_type=reverse_relationship_type
            ).exists():
                Relationship.objects.create(
                    person=related_person,
                    related_person=person,
                    relationship_type=reverse_relationship_type,
                    note=relation.note
                )
            
            return redirect('show', id=person.id)
    else:
        form = RelationshipForm()
    return render(request, 'notebook/relationship_form.html', {'form': form, 'person': person, 'title': 'Добавить связь'})

def templates_list(request):
    templates = GreetingTemplate.objects.all()
    context = {'templates': templates}
    return render(request, 'notebook/templates_list.html', context)

def template_create(request):
    if request.method == "POST":
        event_type = request.POST.get('event_type')
        template_text = request.POST.get('template_text')
        
        GreetingTemplate.objects.create(
            event_type=event_type,
            template_text=template_text
        )
        return redirect('templates_list')
    
    return render(request, 'notebook/template_form.html', {'title': 'Создать шаблон'})

def template_delete(request, id):
    template = get_object_or_404(GreetingTemplate, id=id)
    template.delete()
    return redirect('templates_list')
