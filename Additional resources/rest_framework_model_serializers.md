# Django REST Framework: ModelSerializer

---

## 🔹 What is a `ModelSerializer`?

A **`ModelSerializer`** is a shortcut for creating serializers that automatically include fields from a Django model. It works like Django's `ModelForm` but for APIs.

> ✅ Less boilerplate, more power.

---

## ✅ When to Use `ModelSerializer`

Use when:

* You’re working directly with a Django model.
* You want DRF to auto-generate fields.
* You want to add extra logic (custom fields, validation, etc.).

---

## Example: `BookSerializer`

### `models.py`

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published = models.DateField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField()
```

---

### 📁 `serializers.py`

```python
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published', 'price', 'stock']
```

---

## 🧰 Custom Fields with `SerializerMethodField`

```python
class BookSerializer(serializers.ModelSerializer):
    is_in_stock = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'stock', 'is_in_stock']

    def get_is_in_stock(self, obj):
        return obj.stock > 0
```

---

## 🧪 Custom Validation

### Field-Level

```python
def validate_price(self, value):
    if value <= 0:
        raise serializers.ValidationError("Price must be greater than zero.")
    return value
```

### Object-Level

```python
def validate(self, data):
    if data['stock'] == 0 and data['price'] > 0:
        raise serializers.ValidationError("Cannot sell a book with 0 stock.")
    return data
```

---

## 🔁 Nested ModelSerializer

### 📁 `models.py`

```python
class Category(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
```

### 📁 `serializers.py`

```python
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Book
        fields = ['id', 'title', 'category']

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        category = Category.objects.create(**category_data)
        return Book.objects.create(category=category, **validated_data)
```

---

## ⚙️ Options and Features

| Feature                 | Purpose                                 |
| ----------------------- | --------------------------------------- |
| `Meta.model`            | Binds to a Django model                 |
| `Meta.fields`           | Specifies which model fields to include |
| `SerializerMethodField` | Adds dynamic read-only fields           |
| `validate_<field>()`    | Custom validation for a specific field  |
| `validate()`            | Cross-field (object-level) validation   |
| `create()` / `update()` | Override to customize saving logic      |

---

## 🛠 Read-Only / Write-Only Fields

```python
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'price']
        read_only_fields = ['id']
```

Or:

```python
    price = serializers.DecimalField(max_digits=6, decimal_places=2, write_only=True)
```

---

## 🧠 Summary

| Term                    | Description                        |
| ----------------------- | ---------------------------------- |
| `ModelSerializer`       | Auto-generates fields from a model |
| `SerializerMethodField` | Adds a custom computed field       |
| `validate_<field>()`    | Field-level validation             |
| `validate()`            | Object-level validation            |
| `read_only_fields`      | Makes a field read-only            |
| `create()` / `update()` | Add custom creation/update logic   |
