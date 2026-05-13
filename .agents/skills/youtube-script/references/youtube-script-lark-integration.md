# YouTube Script Agent - Lark Base Integration

## Setup Lark Base for Script Storage

### 1. Create Base Structure

```bash
# Initialize lark-cli
lark-cli config init

# Create base for YouTube scripts
lark-cli base base-create --name "YouTube Scripts"

# Note the base token for configuration
```

### 2. Required Tables

**Table: Templates**
| Field | Type | Required |
|-------|------|----------|
| name | Text | Yes |
| type | SingleSelect (educacional, entretenimento, review, noticia) | Yes |
| structure_json | Text | Yes |
| description | Text | No |
| created_at | DateTime | Yes |

**Table: Roteiros**
| Field | Type | Required |
|-------|------|----------|
| titulo | Text | Yes |
| nicho | Text | Yes |
| duracao_alvo | SingleSelect | Yes |
| template_usado | Link (Templates) | Yes |
| estrutura_json | Text | Yes |
| score_viabilidade | Number | Yes |
| status | SingleSelect (draft, revisado, produzindo, publicado) | Yes |
| data_geracao | DateTime | Yes |
| palavras_chave | MultiSelect | No |

**Table: Tendências**
| Field | Type | Required |
|-------|------|----------|
| keyword | Text | Yes |
| volume_estimado | Number | No |
| competition | SingleSelect | No |
| related_keywords | MultiSelect | No |
| last_checked | DateTime | Yes |

### 3. Using with youtube-script

```python
# Example integration code
import lark_cli

def export_to_lark(script_data):
    # Upload script structure to Lark Base
    lark_cli.records.create({
        "table": "roteiros",
        "fields": {
            "titulo": script_data["titulo"],
            "nicho": script_data["nicho"],
            "estrutura_json": json.dumps(script_data["estrutura"]),
            "score_viabilidade": script_data["score_viabilidade"],
            "status": "draft"
        }
    })
```

### 4. View Existing Scripts

```bash
# List scripts from Lark Base
lark-cli base record-list --table roteiros --base [BASE_TOKEN]

# Get specific script
lark-cli base record-get --table roteiros --record [RECORD_ID]
```