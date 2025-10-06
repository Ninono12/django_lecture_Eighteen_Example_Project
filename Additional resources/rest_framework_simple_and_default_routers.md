# Django REST Framework: `SimpleRouter` vs `DefaultRouter`

---

## 🔹 What Are Routers?

**Routers** in Django REST Framework automatically generate URL patterns for your ViewSets — so you don't have to manually define them using `path()` or `url()`.

---

## 1. `SimpleRouter`

A **minimal router** that handles basic CRUD routes (like list, create, retrieve, update, delete) but does **not** include routes like `/api-auth/`.

### Example

```python
from rest_framework.routers import SimpleRouter
from .views import ProductViewSet

router = SimpleRouter()
router.register(r'products', ProductViewSet)

urlpatterns = router.urls
```

It generates URLs like:

| URL Pattern       | HTTP Method | Action   |
| ----------------- | ----------- | -------- |
| `/products/`      | GET         | list     |
| `/products/`      | POST        | create   |
| `/products/{id}/` | GET         | retrieve |
| `/products/{id}/` | PUT/PATCH   | update   |
| `/products/{id}/` | DELETE      | destroy  |

---

## 2. `DefaultRouter`

`DefaultRouter` extends `SimpleRouter` and **adds a default API root view** (like `/`) and optionally login/logout URLs for the browsable API if `rest_framework.urls` is included in `urlpatterns`.

### Example

```python
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = router.urls
```

It generates all the same routes as `SimpleRouter` **plus**:

| URL Pattern | Purpose                                                     |
| ----------- | ----------------------------------------------------------- |
| `/`         | API root view listing available endpoints (e.g. "products") |

If you include login support:

```python
from django.urls import include, path

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
```

Then you also get:

| URL Pattern         | Purpose    |
| ------------------- | ---------- |
| `/api-auth/login/`  | Login form |
| `/api-auth/logout/` | Logout     |

---

## 🧰 When to Use

| Use Case                         | Recommended Router |
| -------------------------------- | ------------------ |
| You need only basic CRUD routes  | `SimpleRouter`     |
| You want an API root (`/`) view  | `DefaultRouter`    |
| You want login/logout via DRF UI | `DefaultRouter`    |

---

##  Bonus: Registering Multiple ViewSets

```python
router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
```

Now the root URL (`/`) will show:

```json
{
  "products": "http://localhost:8000/products/",
  "orders": "http://localhost:8000/orders/"
}
```
