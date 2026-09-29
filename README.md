# djangospice-htmx

**HTMX integration primitives for Django.**

`djangospice-htmx` provides a small, composable server-side HTMX layer for Django applications.

It bridges Django's request/response model with HTMX while keeping application code focused on application behavior, rendering, and interaction rather than manually managing HTMX headers and request metadata.

---

## Features

* HTMX request detection
* HTMX request metadata
* HTMX-aware responses
* Server-side template rendering
* HTML responses
* Response targeting
* Swap strategies
* Response selection
* Redirects
* Client-side locations
* Browser URL management
* Browser refresh
* Server-triggered browser events
* Out-of-band updates
* Composable response configuration
* Reusable HTMX components
* Django middleware integration

---

## Design Philosophy

### Server-first

Application state and business logic remain on the server.

HTMX provides the browser interaction layer without requiring the application to become a client-side SPA.

### Django-native

The package builds on Django's existing request, response, view, form and template systems.

It does not replace Django's application architecture.

### Composable

HTMX behavior can be composed onto a response rather than requiring a separate response type for every interaction.

```python
return (
    Response.render(
        "students/partials/student.html",
        student=student,
    )
    .target("#student-list")
    .swap("beforeend")
)
```

### Progressive enhancement

Applications can support both normal Django requests and HTMX requests using the same application logic.

### Small foundation

`djangospice-htmx` focuses specifically on HTMX integration.

It provides the primitives required to build interactive server-rendered Django applications without imposing a particular application architecture.

---

# Installation

Install from PyPI:

```bash
pip install djangospice-htmx
```

Add the package to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...

    "djangospice_htmx",
]
```

Add the middleware:

```python
MIDDLEWARE = [
    # ...

    "djangospice_htmx.middleware.HTMXMiddleware",
]
```

Include HTMX in your application's frontend:

```html
<script src="https://unpkg.com/htmx.org"></script>
```

---

# Requirements

* Python 3.12+
* Django 5.0+
* HTMX 2.x

---

# Core API

The main public API is intentionally small:

```python
from djangospice_htmx import HTMX, HTMXComponent, Response
```

| API             | Purpose                                |
| --------------- | -------------------------------------- |
| `HTMX`          | Access HTMX request information        |
| `Response`      | Build and configure server responses   |
| `HTMXComponent` | Build reusable HTMX-enabled components |

---

# HTMX Requests

HTMX requests can be identified through the request interface:

```python
def student_list(request):
    if request.htmx:
        ...
```

This allows views to distinguish between normal browser requests and HTMX requests without manually inspecting HTTP headers.

HTMX request information can also be accessed through the request's HTMX interface.

For example:

```python
request.htmx.target
request.htmx.trigger
request.htmx.trigger_name
request.htmx.current_url
request.htmx.boosted
```

---

# Responses

`Response` is the primary response API.

```python
from djangospice_htmx import Response
```

A response can render a template:

```python
return Response.render(
    "students/partials/list.html",
    students=students,
)
```

Or return HTML:

```python
return Response.content(
    "<div>Student created</div>"
)
```

An empty response can be returned when the interaction only requires response metadata:

```python
return Response.empty()
```

---

# Target

Set the element that should receive the response:

```python
return (
    Response.render(
        "students/partials/list.html",
        students=students,
    )
    .target("#student-list")
)
```

---

# Swap

Configure how the returned content should be inserted:

```python
return (
    Response.render(
        "students/partials/student.html",
        student=student,
    )
    .target("#student-list")
    .swap("beforeend")
)
```

Common swap strategies include:

```python
"innerHTML"
"outerHTML"
"beforebegin"
"afterbegin"
"beforeend"
"afterend"
"delete"
"none"
```

---

# Select

A response can select a specific element from the returned HTML:

```python
return (
    Response.render(
        "students/page.html",
        students=students,
    )
    .select("#student-list")
)
```

---

# Redirects

Redirect the browser after a server-side operation:

```python
return Response.empty().redirect(
    "students:list"
)
```

For example:

```python
def create_student(request):
    student = form.save()

    return Response.empty().redirect(
        "students:detail",
        kwargs={"pk": student.pk},
    )
```

---

# Location

HTMX client-side location behavior can be configured through the response:

```python
return Response.empty().location(
    "students:list"
)
```

---

# Browser URLs

Push a new URL into browser history:

```python
return (
    Response.render(
        "students/partials/list.html",
        students=students,
    )
    .push_url("/students/?page=2")
)
```

Replace the current URL:

```python
return (
    Response.render(
        "students/partials/list.html",
        students=students,
    )
    .replace_url("/students/?page=2")
)
```

---

# Refresh

Request a browser refresh:

```python
return Response.empty().refresh()
```

---

# Browser Events

Server-side operations can dispatch browser events.

```python
return (
    Response.render(
        "students/partials/student.html",
        student=student,
    )
    .event(
        "student.created",
        {
            "student_id": str(student.pk),
        },
    )
)
```

JavaScript can listen for the event:

```javascript
document.body.addEventListener(
    "student.created",
    (event) => {
        console.log(event.detail);
    }
);
```

Events can carry structured data:

```python
.event(
    "notification.show",
    {
        "type": "success",
        "message": "Student created successfully.",
    },
)
```

Multiple events can be attached to the same response:

```python
return (
    Response.empty()
    .event(
        "student.created",
        {"student_id": str(student.pk)},
    )
    .event(
        "notification.show",
        {"message": "Student created successfully."},
    )
)
```

---

# Out-of-Band Updates

HTMX supports updating elements outside the primary response target using out-of-band swaps.

`djangospice-htmx` allows additional fragments to be included with a response.

For example:

```python
return (
    Response.render(
        "students/partials/student.html",
        student=student,
    )
    .oob(
        "students/partials/count.html",
        count=student_count,
    )
)
```

An OOB fragment can also be supplied as HTML:

```python
return (
    Response.content(
        "<div>Student created</div>"
    )
    .oob_html(
        '<span id="student-count">42</span>'
    )
)
```

This makes it possible for a single server operation to update multiple areas of the page.

Typical uses include:

* counters
* badges
* totals
* status indicators
* dashboard metrics
* table summaries
* navigation elements

---

# Combining Response Behavior

Response operations can be composed together.

For example:

```python
return (
    Response.render(
        "students/partials/student.html",
        student=student,
    )
    .target("#student-list")
    .swap("beforeend")
    .oob(
        "students/partials/count.html",
        count=student_count,
    )
    .event(
        "student.created",
        {
            "student_id": str(student.pk),
        },
    )
)
```

A single response can therefore define:

* the returned content;
* the target;
* the swap strategy;
* additional page updates;
* browser events.

---

# HTMX Components

`HTMXComponent` provides a reusable abstraction for components that need HTMX behavior.

```python
from djangospice_htmx import HTMXComponent
```

A component can encapsulate its rendering and interaction behavior while using the same `Response` API.

For example:

```python
class StudentForm(HTMXComponent):

    template_name = "students/partials/form.html"

    def render(self):
        return Response.render(
            self.template_name,
            form=self.form,
        )
```

Components can be reused across Django views and applications.

---

# Django Views

`djangospice-htmx` does not require a special view architecture.

Normal Django views can use the package directly:

```python
def student_list(request):
    students = Student.objects.all()

    if request.htmx:
        return Response.render(
            "students/partials/list.html",
            students=students,
        )

    return Response.render(
        "students/list.html",
        students=students,
    )
```

This makes it possible to progressively enhance existing Django applications.

---

# Django Forms

Django forms work naturally with HTMX.

```python
def create_student(request):
    form = StudentForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        student = form.save()

        return (
            Response.render(
                "students/partials/student.html",
                student=student,
            )
            .event(
                "student.created",
                {
                    "student_id": str(student.pk),
                },
            )
        )

    return Response.render(
        "students/partials/form.html",
        form=form,
    )
```

Validation remains server-side using normal Django form behavior.

---

# Templates

HTMX remains visible in templates.

For example:

```html
<button
    hx-post="{% url 'students:create' %}"
    hx-target="#student-list"
    hx-swap="beforeend"
>
    Add Student
</button>
```

The package complements HTMX's HTML API rather than replacing it with a custom template language.

---

# Progressive Enhancement

A view can support both normal browser navigation and HTMX requests:

```python
def students(request):
    students = Student.objects.all()

    if request.htmx:
        return Response.render(
            "students/partials/list.html",
            students=students,
        )

    return Response.render(
        "students/list.html",
        students=students,
    )
```

This allows applications to progressively introduce HTMX without restructuring their Django application.

---

# Security

HTMX does not replace Django's security model.

Applications should continue to use:

* CSRF protection
* authentication
* authorization
* server-side validation
* Django permissions
* secure cookies
* standard HTTP security practices

For example:

```html
<form
    hx-post="{% url 'students:create' %}"
    hx-target="#student-form"
>
    {% csrf_token %}

    {{ form }}
</form>
```

Authorization must always be enforced on the server.

---

# Testing

HTMX requests can be tested using Django's test client:

```python
response = client.get(
    reverse("students:list"),
    HTTP_HX_REQUEST="true",
)

assert response.status_code == 200
```

Response behavior can also be tested through the normal Django response interface:

```python
assert response["HX-Redirect"] == expected_url
```

Browser-level interaction can be tested separately using the application's preferred end-to-end testing framework.

---

# API Reference

The primary public API is:

```python
from djangospice_htmx import (
    HTMX,
    HTMXComponent,
    Response,
)
```

## `HTMX`

Provides access to HTMX request information.

## `Response`

Provides composable response construction and HTMX behavior.

Common response operations include:

```python
Response.render(...)
Response.content(...)
Response.empty(...)

response.target(...)
response.swap(...)
response.select(...)

response.redirect(...)
response.location(...)

response.push_url(...)
response.replace_url(...)
response.refresh(...)

response.event(...)
response.oob(...)
response.oob_html(...)
```

## `HTMXComponent`

Provides a reusable abstraction for HTMX-enabled components.

---


# Scope

`djangospice-htmx` focuses on **HTMX integration for Django**.

It provides the primitives needed to build interactive server-rendered Django applications without imposing a particular frontend or application architecture.

The package does not define:

* application business logic;
* domain models;
* authentication;
* authorization;
* application-specific UI design;
* application-specific JavaScript behavior.

These remain the responsibility of the Django application.

---

# Contributing

Contributions are welcome.

When contributing:

1. Keep the public API small and composable.
2. Prefer Django-native behavior.
3. Keep HTMX-specific concerns within this package.
4. Avoid unnecessary JavaScript.
5. Add tests for new functionality.
6. Preserve backwards compatibility where practical.
7. Avoid introducing application-specific behavior.

---

# License

This package is licensed under the **MIT License**.

See [LICENSE](LICENSE) for the full license text.
