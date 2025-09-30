# 📡 Примеры API запросов

Этот файл содержит готовые примеры запросов к API для тестирования в Postman, curl или через Swagger.

## 🔐 Аутентификация

Все запросы требуют аутентификации. Используйте Basic Authentication с учетными данными:
- **Username**: `employee`
- **Password**: `employee123`

### Пример с curl:

```bash
# Base64 кодирование: employee:employee123 -> ZW1wbG95ZWU6ZW1wbG95ZWUxMjM=
curl -H "Authorization: Basic ZW1wbG95ZWU6ZW1wbG95ZWUxMjM=" http://localhost:8000/api/network-nodes/
```

## 📋 Звенья торговой сети (Network Nodes)

### 1. Получить список всех звеньев

**GET** `/api/network-nodes/`

```bash
curl -X GET "http://localhost:8000/api/network-nodes/" \
  -H "Authorization: Basic ZW1wbG95ZWU6ZW1wbG95ZWUxMjM="
```

**Ответ:**
```json
{
  "count": 9,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Завод Samsung Electronics",
      "node_type": "FACTORY",
      "email": "contact@samsung.com",
      "country": "Южная Корея",
      "city": "Сеул",
      "supplier": null,
      "supplier_name": null,
      "hierarchy_level": 0,
      "debt": "0.00",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### 2. Получить детали конкретного звена

**GET** `/api/network-nodes/{id}/`

```bash
curl -X GET "http://localhost:8000/api/network-nodes/1/" \
  -H "Authorization: Basic ZW1wbG95ZWU6ZW1wbG95ZWUxMjM="
```

**Ответ:**
```json
{
  "id": 1,
  "name": "Завод Samsung Electronics",
  "node_type": "FACTORY",
  "email": "contact@samsung.com",
  "country": "Южная Корея",
  "city": "Сеул",
  "street": "Seocho-daero",
  "house_number": "1321",
  "full_address": "Южная Корея, Сеул, Seocho-daero, дом 1321",
  "supplier": null,
  "supplier_name": null,
  "hierarchy_level": 0,
  "debt": "0.00",
  "products": [
    {
      "id": 1,
      "name": "Смартфон",
      "model": "Galaxy S23",
      "release_date": "2023-03-20"
    }
  ],
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### 3. Создать новое звено (Завод)

**POST** `/api/network-nodes/`

```bash
curl -X POST "http://localhost:8000/api/network-nodes/" \
  -H "Authorization: Basic ZW1wbG95ZWU6ZW1wbG95ZWUxMjM=" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Завод LG Electronics",
    "node_type": "FACTORY",
    "email": "factory@lg.com",
    "country": "Южная Корея",
    "city": "Сеул",
    "street": "LG Twin Towers",
    "house_number": "128",
    "supplier": null
  }'
```

**Ответ (201 Created):**
```json
{
  "id": 10,
  "name": "Завод LG Electronics",
  "node_type": "FACTORY",
  "email": "factory@lg.com",
  "country": "Южная Корея",
  "city": "Сеул",
  "street": "LG Twin Towers",
  "house_number": "128",
  "supplier": null,
  "debt": "0.00"
}
```

### 4. Создать розничную сеть с поставщиком

**POST** `/api/network-nodes/`

```bash
curl -X POST "http://localhost:8000/api/network-nodes/" \
  -H "Authorization: Basic ZW1wbG95ZWU6ZW1wbG95ZWUxMjM=" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ситилинк",
    "node_type": "RETAIL",
    "email": "info@citilink.ru",
    "country": "Россия",
    "city": "Москва",
    "street": "Волгоградский проспект",
    "house_number": "32",
    "supplier": 1
  }'
```

### 5. Обновить звено (БЕЗ debt)

**PATCH** `/api/network-nodes/{id}/`

```bash
curl -X PATCH "http://localhost:8000/api/network-nodes/4/" \
  -H "Authorization: Basic ZW1wbG95ZWU6ZW1wbG95ZWUxMjM=" \
  -H "Content-Type: application/json" \
  -d '{
    "city": "Санкт-Петербург",
    "street": "Московский проспект",
    "house_number": "220"
  }'
```

**✅ Успешный ответ (200 OK)**

### 6. ❌ Попытка обновить debt (ЗАПРЕЩЕНО)

**PATCH** `/api/network-nodes/{id}/`

```bash
curl -X PATCH "http://localhost:8000/api/network-nodes/4/" \
  -H "Authorization: Basic ZW1wbG95ZWU6ZW1wbG95ZWUxMjM=" \
  -H "Content-Type: application/json" \
  -d '{
    "debt": "0.00"
  }'
```

**❌ Ошибка (400 Bad Request):**
```json
{
  "error": "Обновление поля \"debt\" через API запрещено.",
  "detail": "Задолженность можно изменить только через админ-панель."
}
```

### 7. ✅ Правильный способ очистить debt

**POST** `/api/network-nodes/{id}/clear_debt/`

```bash
curl -X POST "http://localhost:8000/api/network-nodes/4/clear_debt/" \
  -H "Authorization: Basic ZW1wbG95ZWU6ZW1wbG95ZWUxMjM="
```

**Ответ (200 OK):**
```json
{
  "message": "Задолженность успешно очищена.",
  "data": {
    "id": 4,
    "name": "М.Видео",
    "debt": "0.00",
    ...
  }
}
```

### 8. Получить статистику по сети

**GET** `/api/network-nodes/statistics/`

```bash
curl -X GET "http://localhost:8000/api/network-nodes/statistics/" \
  -H "Authorization: Basic ZW1wbG95ZWU6ZW1wbG95ZWUxMjM="
```

**Ответ:**
```json
{
  "total_nodes": 9,
  "total_factories": 3,
  "total_retail_networks": 3,
  "total_entrepreneurs": 3,
  "total_debt": "5055001.25",
  "average_hierarchy_level": 1.33
}
```

### 9. Удалить звено

**DELETE** `/api/network-nodes/{id}/`

```bash
curl -X DELETE "http://localhost:8000/api/network-nodes/10/" \
  -H "Authorization: Basic ZW1wbG95ZWU6ZW1wbG95ZWUxMjM="
```

**Ответ (204 No Content)** - пустой ответ

## 🔍 Фильтрация

### 10. Фильтр по стране (ТРЕБОВАНИЕ ТЗ)

**GET** `/api/network-nodes/?country=Россия`

```bash
curl -X GET "http://localhost:8000/api/network-nodes/?country=Россия" \
  -H "Authorization: Basic ZW1wbG95ZWU6ZW1wbG95ZWUxMjM="
```

Вернет только звенья из России.

### 11. Фильтр по городу

**GET** `/api/network-nodes/?city=Москва`

```bash
curl -X GET "http://localhost:8000/api/network-nodes/?city=Москва" \
  -H "Authorization: Basic ZW1wbG95ZWU6ZW1wbG95ZWUxMjM="
```

### 12. Фильтр по типу звена

**GET** `/api/network-nodes/?node_type=FACTORY`

```bash
curl -X GET "http://localhost:8000/api/network-nodes/?node_type=FACTORY" \
  -H "Authorization: Basic ZW1wbG95ZWU6ZW1wbG95ZWUxMjM="
```

Возможные значения: `FACTORY`, `RETAIL`, `IE`

### 13. Фильтр по уровню иерархии

**GET** `/api/network-nodes/?hierarchy_level=0`

```bash
curl -X GET "http://localhost:8000/api/network-nodes/?hierarchy_level=0" \
  -H "Authorization: Basic ZW1wbG95ZWU6ZW1wbG95ZWUxMjM="
```

Вернет только заводы (уровень 0).

### 14. Комбинированные фильтры

**GET** `/api/network-nodes/?country=Россия&has_debt=true`

```bash
curl -X GET "http://localhost:8000/api/network-nodes/?country=Россия&has_debt=true" \
  -H "Authorization: Basic ZW1wbG95ZWU6ZW1wbG95ZWUxMjM="
```

Вернет российские звенья с задолженностью.

### 15. Фильтр по диапазону долга

**GET** `/api/network-nodes/?debt_min=100000&debt_max=1000000`

```bash
curl -X GET "http://localhost:8000/api/network-nodes/?debt_min=100000&debt_max=1000000" \
  -H "Authorization: Basic ZW1wbG95ZWU6ZW1wbG95ZWUxMjM="
```

### 16. Фильтр: только с поставщиком

**GET** `/api/network-nodes/?has_supplier=true`

```bash
curl -X GET "http://localhost:8000/api/network-nodes/?has_supplier=true" \
  -H "Authorization: Basic ZW1wbG95ZWU6ZW1wbG95ZWUxMjM="
```

### 17. Поиск по названию

**GET** `/api/network-nodes/?search=Samsung`

```bash
curl -X GET "http://localhost:8000/api/network-nodes/?search=Samsung" \
  -H "Authorization: Basic ZW1wbG95ZWU6ZW1wbG95ZWUxMjM="
```

### 18. Сортировка

**GET** `/api/network-nodes/?ordering=debt`

```bash
# По возрастанию долга
curl -X GET "http://localhost:8000/api/network-nodes/?ordering=debt" \
  -H "Authorization: Basic ZW1wbG95ZWU6ZW1wbG95ZWUxMjM="

# По убыванию долга
curl -X GET "http://localhost:8000/api/network-nodes/?ordering=-debt" \
  -H "Authorization: Basic ZW1wbG95ZWU6ZW1wbG95ZWUxMjM="
```

Доступные поля для сортировки: `name`, `hierarchy_level`, `debt`, `created_at`

## 📦 Продукты (Products)

### 19. Получить список продуктов

**GET** `/api/products/`

```bash
curl -X GET "http://localhost:8000/api/products/" \
  -H "Authorization: Basic ZW1wbG95ZWU6ZW1wbG95ZWUxMjM="
```

### 20. Создать новый продукт

**POST** `/api/products/`

```bash
curl -X POST "http://localhost:8000/api/products/" \
  -H "Authorization: Basic ZW1wbG95ZWU6ZW1wbG95ZWUxMjM=" \
  -H "Content-Type: application/json" \
  -d '{
    "network_node": 1,
    "name": "Планшет",
    "model": "Galaxy Tab S9",
    "release_date": "2023-08-15"
  }'
```

### 21. Обновить продукт

**PATCH** `/api/products/{id}/`

```bash
curl -X PATCH "http://localhost:8000/api/products/1/" \
  -H "Authorization: Basic ZW1wbG95ZWU6ZW1wbG95ZWUxMjM=" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Смартфон (обновлен)",
    "model": "Galaxy S23 Ultra"
  }'
```

### 22. Фильтр продуктов по звену сети

**GET** `/api/products/?network_node=1`

```bash
curl -X GET "http://localhost:8000/api/products/?network_node=1" \
  -H "Authorization: Basic ZW1wbG95ZWU6ZW1wbG95ZWUxMjM="
```

### 23. Фильтр продуктов по году выпуска

**GET** `/api/products/?release_year=2023`

```bash
curl -X GET "http://localhost:8000/api/products/?release_year=2023" \
  -H "Authorization: Basic ZW1wbG95ZWU6ZW1wbG95ZWUxMjM="
```

### 24. Удалить продукт

**DELETE** `/api/products/{id}/`

```bash
curl -X DELETE "http://localhost:8000/api/products/1/" \
  -H "Authorization: Basic ZW1wbG95ZWU6ZW1wbG95ZWUxMjM="
```

## 🚫 Проверка прав доступа

### 25. Запрос без аутентификации (должен вернуть 403)

```bash
curl -X GET "http://localhost:8000/api/network-nodes/"
```

**Ответ (403 Forbidden):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 26. Запрос с неактивным пользователем (должен вернуть 403)

Создайте неактивного пользователя и попробуйте:

```bash
curl -X GET "http://localhost:8000/api/network-nodes/" \
  -H "Authorization: Basic aW5hY3RpdmU6aW5hY3RpdmUxMjM="
```

**Ответ (403 Forbidden):**
```json
{
  "detail": "Доступ разрешен только активным сотрудникам."
}
```

## 📝 Postman Collection

Вы можете импортировать следующую коллекцию в Postman:

```json
{
  "info": {
    "name": "Electronics Network API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "auth": {
    "type": "basic",
    "basic": [
      {"key": "username", "value": "employee"},
      {"key": "password", "value": "employee123"}
    ]
  },
  "item": [
    {
      "name": "Get Network Nodes",
      "request": {
        "method": "GET",
        "url": "{{baseUrl}}/api/network-nodes/"
      }
    },
    {
      "name": "Filter by Country",
      "request": {
        "method": "GET",
        "url": "{{baseUrl}}/api/network-nodes/?country=Россия"
      }
    }
  ],
  "variable": [
    {
      "key": "baseUrl",
      "value": "http://localhost:8000"
    }
  ]
}
```

## 💡 Полезные советия

1. **Swagger UI** - самый простой способ тестировать API: http://localhost:8000/swagger/
2. **Используйте jq** для форматирования JSON в терминале:
   ```bash
   curl ... | jq '.'
   ```
3. **Сохраняйте токены** - в реальном проекте используйте JWT или Token Authentication
4. **Проверяйте коды ответов**:
   - 200 - успех (GET, PATCH, PUT)
   - 201 - создано (POST)
   - 204 - успех без контента (DELETE)
   - 400 - ошибка валидации
   - 403 - нет доступа
   - 404 - не найдено
   - 500 - ошибка сервера