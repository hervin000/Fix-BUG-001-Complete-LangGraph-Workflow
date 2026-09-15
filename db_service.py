# persistence/db_service.py
import logging
import json
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

def generate_embedding(text: str) -> List[float]:
    """Generates vector embedding for semantic search (mock vector fallback if model unavailable)."""
    try:
        # Replace with your actual embedding client (e.g. OpenAI, FastEmbed, SentenceTransformers)
        # return embedding_client.embed(text)
        return [0.0] * 1536
    except Exception as e:
        logger.error(f"[BUG-012] Embedding generation failed: {e}")
        return [0.0] * 1536

def save_learning_path_to_db(path_data: Dict[str, Any], db_connection) -> bool:
    """Persists learning path and resources into PostgreSQL and PGVector."""
    if not path_data:
        logger.warning("[BUG-012] No learning path data provided for persistence.")
        return False

    try:
        path_id = path_data.get("path_id")
        title = path_data.get("title", "")
        summary = path_data.get("summary", "")
        
        # 1. Generate summary embedding for pgvector
        summary_vector = generate_embedding(f"{title} {summary}")
        
        cursor = db_connection.cursor()
        
        # 2. Insert into learning_paths table
        insert_path_query = """
            INSERT INTO learning_paths (path_id, title, domain, course, topic, target_level, estimated_hours, payload, embedding)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (path_id) DO UPDATE SET payload = EXCLUDED.payload;
        """
        cursor.execute(insert_path_query, (
            path_id,
            title,
            path_data.get("domain"),
            path_data.get("course"),
            path_data.get("topic"),
            path_data.get("target_level"),
            path_data.get("estimated_hours"),
            json.dumps(path_data),
            summary_vector
        ))
        
        # 3. Iterate modules and save resources with vector embeddings
        for module in path_data.get("modules", []):
            for res in module.get("resources", []):
                res_url = res.get("url")
                res_text = f"{res.get('title', '')} {res.get('summary', '')}"
                res_vector = generate_embedding(res_text)
                
                insert_res_query = """
                    INSERT INTO resources (url, title, type, quality_score, metadata, embedding)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (url) DO NOTHING;
                """
                cursor.execute(insert_res_query, (
                    res_url,
                    res.get("title"),
                    res.get("type"),
                    res.get("qualityScore", 0),
                    json.dumps(res),
                    res_vector
                ))
                
        db_connection.commit()
        cursor.close()
        logger.info(f"[BUG-012 DB Success] Persisted path '{path_id}' and resources into PostgreSQL/pgvector.")
        return True

    except Exception as e:
        db_connection.rollback()
        logger.error(f"[BUG-012 DB Error] Failed to persist path to PostgreSQL: {e}")
        return False