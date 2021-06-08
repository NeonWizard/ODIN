## API Documentation

---

### `GET /ping`
Returns 200 OK and the text "pong" to signal the server is online.

**Example Response**
```json
{
  "data": "pong"
}
```

---

### `GET /models`
Returns all available GPT-2 models by name.

**Example Response**
```json
{
  "data": [
    {
      "id": 0,
      "name": "john-keats-300"
    },
    {
      "id": 1,
      "name": "deiga-500"
    }
  ],
  "meta": {
    "result_count": 2
  }
}
```

---

### ```GET /models/<name>```
Generates text via a specified GPT-2 model.

**Query Parameters**
| Name | Type | Description |
| :-:  | :-: | ----------- |
| `words` | int | Number of words to generate. |

**Example Response**
```json
{
  "data": "Howdy, my name is Rawhide Kobayashi. I'm a 27 year old Japanese Japamerican (western culture fan for you foreigners). I brand and wrangle cattle on my ranch, and spend my days perfecting the craft and enjoying superior American passtimes. (Barbeque, Rodeo, Fireworks) I train with my branding iron every day.",
  "meta": {
    "generation_time": "15582" // milliseconds
  }
}
```
