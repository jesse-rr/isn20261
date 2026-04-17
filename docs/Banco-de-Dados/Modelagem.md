# DynamoDB — Schema & Tipos

[JSON Schema (Draft 7)](https://json-schema.org/draft-07/json-schema-release-notes.html) 

> **Convenções**
> - Datas são sempre `string` no formato **ISO 8601** (`2024-01-15T10:30:00Z`)
> - Campos marcados com `"required"` são obrigatórios em toda operação de escrita
> - Campos do tipo `map` são documentados como `object` com suas propriedades explícitas
> - Campos do tipo `list` são documentados como `array` com o schema de cada item

---

## Tabelas

- [EmailToSub](#emailtosub)
- [Users](#users)
- [Tokens](#tokens)
- [Historico](#historico)
- [Logs](#logs)

---

## EmailToSub

Mapeamento de e-mail para `sub` do Cognito. Usado para lookup por e-mail.

| Chave | Tipo | Papel |
|-------|------|-------|
| `email` | `string` | Partition Key |
| `sub` | `string` | Atributo |

### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "EmailToSub",
  "type": "object",
  "required": ["email", "sub"],
  "additionalProperties": false,
  "properties": {
    "email": {
      "type": "string",
      "format": "email",
      "description": "Partition Key. E-mail do usuário."
    },
    "sub": {
      "type": "string",
      "description": "UUID do Cognito vinculado ao e-mail."
    }
  }
}
```

---

## Users

Registro principal do usuário. Utiliza `map` para simular um documento NoSQL com campos aninhados.

| Chave | Tipo | Papel |
|-------|------|-------|
| `sub` | `string` | Partition Key |

### Atributos de topo

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `sub` | `string` | ✅ | UUID do Cognito |
| `email` | `string` | ✅ | E-mail do usuário |
| `passwordHash` | `string` | ✅ | Hash bcrypt da senha |
| `emailVerified` | `boolean` | ✅ | Se o e-mail foi verificado |
| `preferences` | `object (map)` | ✅ | Preferências do usuário — ver detalhes abaixo |
| `watchLater` | `array (list)` | ✅ | Lista de filmes para ver depois — ver detalhes abaixo |
| `createdAt` | `string` | ✅ | ISO 8601 |
| `updatedAt` | `string` | ✅ | ISO 8601 |

### Map: `preferences`

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `language` | `string` | ✅ | Código de idioma (ex: `pt-BR`, `en-US`) |
| `theme` | `"light"` \| `"dark"` | ✅ | Tema da interface |
| `notifications` | `boolean` | ✅ | Se notificações estão ativadas |

### List: `watchLater`

Cada item da lista é um objeto com os campos:

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `movieId` | `string` | ✅ | ID do filme |
| `addedAt` | `string` | ✅ | ISO 8601 — quando foi adicionado |

### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "User",
  "type": "object",
  "required": [
    "sub",
    "email",
    "passwordHash",
    "emailVerified",
    "preferences",
    "watchLater",
    "createdAt",
    "updatedAt"
  ],
  "additionalProperties": false,
  "properties": {
    "sub": {
      "type": "string",
      "description": "Partition Key. UUID do Cognito."
    },
    "email": {
      "type": "string",
      "format": "email",
      "description": "E-mail do usuário."
    },
    "passwordHash": {
      "type": "string",
      "description": "Hash bcrypt da senha do usuário."
    },
    "emailVerified": {
      "type": "boolean",
      "description": "Indica se o e-mail foi verificado."
    },
    "preferences": {
      "type": "object",
      "description": "MAP — Preferências do usuário.",
      "required": ["language", "theme", "notifications"],
      "additionalProperties": false,
      "properties": {
        "language": {
          "type": "string",
          "description": "Código de idioma BCP 47. Ex: 'pt-BR', 'en-US'."
        },
        "theme": {
          "type": "string",
          "enum": ["light", "dark"],
          "description": "Tema da interface."
        },
        "notifications": {
          "type": "boolean",
          "description": "Se notificações push estão ativadas."
        }
      }
    },
    "watchLater": {
      "type": "array",
      "description": "LIST — Filmes salvos para ver depois.",
      "items": {
        "type": "object",
        "required": ["movieId", "addedAt"],
        "additionalProperties": false,
        "properties": {
          "movieId": {
            "type": "string",
            "description": "ID do filme."
          },
          "addedAt": {
            "type": "string",
            "format": "date-time",
            "description": "ISO 8601 — data em que o filme foi adicionado."
          }
        }
      }
    },
    "createdAt": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 — data de criação do registro."
    },
    "updatedAt": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 — data da última atualização."
    }
  }
}
```

---

## Tokens

Tokens temporários para verificação de e-mail e reset de senha.

| Chave | Tipo | Papel |
|-------|------|-------|
| `token` | `string` | Partition Key |

### Atributos

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `token` | `string` | ✅ | UUID do token |
| `sub` | `string` | ✅ | UUID do Cognito — dono do token |
| `type` | `"verify-email"` \| `"reset-password"` | ✅ | Finalidade do token |
| `expiresAt` | `string` | ✅ | ISO 8601 — data de expiração |

### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "Token",
  "type": "object",
  "required": ["token", "sub", "type", "expiresAt"],
  "additionalProperties": false,
  "properties": {
    "token": {
      "type": "string",
      "description": "Partition Key. UUID do token."
    },
    "sub": {
      "type": "string",
      "description": "UUID do Cognito do usuário dono do token."
    },
    "type": {
      "type": "string",
      "enum": ["verify-email", "reset-password"],
      "description": "Finalidade do token."
    },
    "expiresAt": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 — data e hora de expiração do token."
    }
  }
}
```

---

## Historico

Histórico de filmes assistidos por usuário. Cada entrada é identificada pelo par `sub` + `timestamp`.

| Chave | Tipo | Papel |
|-------|------|-------|
| `sub` | `string` | Partition Key |
| `timestamp` | `string` | Sort Key |

### Atributos

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `sub` | `string` | ✅ | UUID do Cognito |
| `timestamp` | `string` | ✅ | ISO 8601 — Sort Key |
| `movieTitle` | `string` | ✅ | Título do filme assistido |

### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "HistoricoItem",
  "type": "object",
  "required": ["sub", "timestamp", "movieTitle"],
  "additionalProperties": false,
  "properties": {
    "sub": {
      "type": "string",
      "description": "Partition Key. UUID do Cognito."
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "Sort Key. ISO 8601 — momento em que o filme foi assistido."
    },
    "movieTitle": {
      "type": "string",
      "description": "Título do filme assistido."
    }
  }
}
```

---

## Logs

Log de ações do usuário no sistema. Cada entrada é identificada pelo par `sub` + `timestamp`.

| Chave | Tipo | Papel |
|-------|------|-------|
| `sub` | `string` | Partition Key |
| `timestamp` | `string` | Sort Key |

### Atributos

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `sub` | `string` | ✅ | UUID do Cognito |
| `timestamp` | `string` | ✅ | ISO 8601 — Sort Key |
| `action` | `string` | ✅ | Ação executada (ex: `LOGIN`, `WATCH`, `PASSWORD_RESET`) |
| `metadata` | `object` | ✅ | Dados extras da ação — schema livre |

> **Nota sobre `metadata`:** Este campo é intencionalmente aberto (`additionalProperties: true`) pois cada `action` pode carregar dados diferentes. Se no futuro os metadados de uma ação específica se tornarem estáveis, considere criar um schema dedicado para ela usando `if/then` do JSON Schema.

### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "LogItem",
  "type": "object",
  "required": ["sub", "timestamp", "action", "metadata"],
  "additionalProperties": false,
  "properties": {
    "sub": {
      "type": "string",
      "description": "Partition Key. UUID do Cognito."
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "Sort Key. ISO 8601 — momento da ação."
    },
    "action": {
      "type": "string",
      "description": "Ação executada. Ex: LOGIN, WATCH, PASSWORD_RESET."
    },
    "metadata": {
      "type": "object",
      "description": "Dados extras da ação. Schema livre — varia por action.",
      "additionalProperties": true
    }
  }
}
```