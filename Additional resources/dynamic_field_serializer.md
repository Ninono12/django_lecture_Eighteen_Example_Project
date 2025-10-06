# Django REST Framework: Dynamic Field Serializer

---

## 🔹 What is a Dynamic Field Serializer?

A **dynamic field serializer** allows you to control which fields appear in the serialized output **at runtime**, rather than hardcoding them in `Meta.fields`.

> 🎯 Useful for optimizing APIs, hiding sensitive data, or customizing response based on the request.

---

## ✅ When to Use It

Use when:

* You want to expose different fields based on user roles (admin vs. user).
* You want to let clients specify fields (e.g., `?fields=name,email`).
* You want to reduce payload size dynamically.

---

## 🧱 Example: Customizing Fields via `__init__`

```python
class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
```

### Usage in Another Serializer

```python
class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']
```

---

## 🧪 Example in a View

```python
# example 1
@api_view(['GET'])
def user_detail(request, pk):
    user = User.objects.get(pk=pk)
    fields = request.query_params.get('fields')

    if fields:
        fields = fields.split(',')
        serializer = UserSerializer(user, fields=fields)
    else:
        serializer = UserSerializer(user)

    return Response(serializer.data)
```
```python
# example 2
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action == 'list':
            kwargs['fields'] = ('first_name', 'last_name')
        elif self.action == 'update':
            kwargs['fields'] = ('first_name', 'last_name', 'email')
        return super().get_serializer(*args, **kwargs)
```

**GET /api/users/1/?fields=id,username**
Returns only:

```json
{
  "id": 1,
  "username": "mariam"
}
```

---

## 🔐 Example: Dynamic Fields Based on User Role

```python
class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        if not user.is_staff:
            self.fields.pop('email')
```

---

## ⚙️ Summary

| Concept                        | Use Case                                     |
| ------------------------------ | -------------------------------------------- |
| `DynamicFieldsModelSerializer` | Base serializer that supports dynamic fields |
| `fields=` in `__init__()`      | Manually specify which fields to include     |
| `self.context`                 | Get current user/request                     |
| `.pop()` on `self.fields`      | Remove fields at runtime                     |
