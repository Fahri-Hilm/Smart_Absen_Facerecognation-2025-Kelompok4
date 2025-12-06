"""
InsightFace/ArcFace Face Recognition Module
State-of-the-art face recognition dengan akurasi 99%+

Fitur:
- ArcFace model untuk ekstraksi 512-dimensional face embeddings
- Cosine similarity untuk matching wajah
- Lebih akurat dan robust dibanding KNN tradisional
- Hanya butuh 5-10 foto per orang untuk training
"""

import os
import cv2
import numpy as np
import pickle
import logging
from typing import Tuple, List, Optional, Dict
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

# Global InsightFace app instance
_insightface_app = None
_face_database = {}  # {name: [embeddings]}
_database_path = 'static/face_embeddings.pkl'

def get_insightface_app():
    """Initialize InsightFace app singleton"""
    global _insightface_app
    if _insightface_app is None:
        try:
            from insightface.app import FaceAnalysis
            _insightface_app = FaceAnalysis(
                name='buffalo_l',  # Best accuracy model
                providers=['CUDAExecutionProvider', 'CPUExecutionProvider']
            )
            _insightface_app.prepare(ctx_id=0, det_size=(640, 640))
            logger.info("InsightFace initialized successfully (ArcFace buffalo_l model)")
        except Exception as e:
            logger.error(f"Failed to initialize InsightFace: {e}")
            # Fallback to lighter model
            try:
                from insightface.app import FaceAnalysis
                _insightface_app = FaceAnalysis(
                    name='buffalo_sc',  # Lighter model
                    providers=['CPUExecutionProvider']
                )
                _insightface_app.prepare(ctx_id=-1, det_size=(320, 320))
                logger.info("InsightFace initialized with lighter model (buffalo_sc)")
            except Exception as e2:
                logger.error(f"Failed to initialize InsightFace fallback: {e2}")
                return None
    return _insightface_app


def extract_face_embedding(image: np.ndarray) -> Optional[np.ndarray]:
    """
    Extract 512-dimensional face embedding from image using ArcFace
    
    Args:
        image: BGR image (OpenCV format)
    
    Returns:
        512-dim normalized embedding vector or None if no face detected
    """
    app = get_insightface_app()
    if app is None:
        return None
    
    try:
        # Detect and analyze faces
        faces = app.get(image)
        
        if len(faces) == 0:
            logger.warning("No face detected in image")
            return None
        
        # Get the largest face (most prominent)
        largest_face = max(faces, key=lambda x: (x.bbox[2] - x.bbox[0]) * (x.bbox[3] - x.bbox[1]))
        
        # Return normalized embedding
        embedding = largest_face.embedding
        embedding = embedding / np.linalg.norm(embedding)  # L2 normalize
        
        return embedding
        
    except Exception as e:
        logger.error(f"Error extracting face embedding: {e}")
        return None


def detect_faces_insightface(image: np.ndarray) -> List[Dict]:
    """
    Detect faces using InsightFace
    
    Returns:
        List of face info dicts with bbox, embedding, landmarks
    """
    app = get_insightface_app()
    if app is None:
        return []
    
    try:
        faces = app.get(image)
        result = []
        for face in faces:
            result.append({
                'bbox': face.bbox.astype(int).tolist(),  # [x1, y1, x2, y2]
                'embedding': face.embedding,
                'det_score': float(face.det_score),
                'landmarks': face.kps.astype(int).tolist() if face.kps is not None else None
            })
        return result
    except Exception as e:
        logger.error(f"Error detecting faces: {e}")
        return []


def cosine_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
    """Calculate cosine similarity between two embeddings"""
    # Both should already be normalized, but ensure it
    e1 = embedding1 / np.linalg.norm(embedding1)
    e2 = embedding2 / np.linalg.norm(embedding2)
    return float(np.dot(e1, e2))


def load_face_database() -> Dict[str, List[np.ndarray]]:
    """Load face embeddings database from file"""
    global _face_database
    
    if os.path.exists(_database_path):
        try:
            with open(_database_path, 'rb') as f:
                _face_database = pickle.load(f)
            logger.info(f"Loaded face database with {len(_face_database)} identities")
        except Exception as e:
            logger.error(f"Error loading face database: {e}")
            _face_database = {}
    
    return _face_database


def save_face_database():
    """Save face embeddings database to file"""
    global _face_database
    try:
        os.makedirs(os.path.dirname(_database_path), exist_ok=True)
        with open(_database_path, 'wb') as f:
            pickle.dump(_face_database, f)
        logger.info(f"Saved face database with {len(_face_database)} identities")
    except Exception as e:
        logger.error(f"Error saving face database: {e}")


def train_insightface_model() -> bool:
    """
    Train InsightFace model by extracting embeddings from all face images
    
    Reads images from static/faces/{name}/ and creates embedding database
    """
    global _face_database
    
    faces_dir = 'static/faces'
    if not os.path.exists(faces_dir):
        logger.warning(f"Faces directory not found: {faces_dir}")
        return False
    
    _face_database = {}
    total_images = 0
    
    try:
        for person_name in os.listdir(faces_dir):
            person_path = os.path.join(faces_dir, person_name)
            if not os.path.isdir(person_path):
                continue
            
            embeddings = []
            
            for img_file in os.listdir(person_path):
                img_path = os.path.join(person_path, img_file)
                
                # Read image
                img = cv2.imread(img_path)
                if img is None:
                    continue
                
                # Extract embedding
                embedding = extract_face_embedding(img)
                if embedding is not None:
                    embeddings.append(embedding)
                    total_images += 1
                    logger.debug(f"Processed: {person_name}/{img_file}")
            
            if embeddings:
                _face_database[person_name] = embeddings
                logger.info(f"Added {len(embeddings)} embeddings for {person_name}")
        
        if _face_database:
            save_face_database()
            logger.info(f"InsightFace model trained with {len(_face_database)} identities, {total_images} images")
            return True
        else:
            logger.warning("No face data found for training")
            return False
            
    except Exception as e:
        logger.error(f"Error training InsightFace model: {e}")
        return False


def identify_face_insightface(image: np.ndarray, threshold: float = 0.45) -> Tuple[str, float]:
    """
    Identify face using InsightFace embeddings
    
    Args:
        image: BGR image (OpenCV format)
        threshold: Minimum cosine similarity for recognition (0.45 = 45%)
    
    Returns:
        Tuple of (identity_name, confidence_score)
        Returns ("Unknown", 0.0) if no match found
    """
    global _face_database
    
    # Load database if not loaded
    if not _face_database:
        load_face_database()
    
    if not _face_database:
        logger.warning("Face database is empty")
        return ("Unknown", 0.0)
    
    # Extract embedding from input image
    query_embedding = extract_face_embedding(image)
    if query_embedding is None:
        return ("Unknown", 0.0)
    
    best_match = "Unknown"
    best_score = 0.0
    
    # Compare with all registered faces
    for person_name, embeddings in _face_database.items():
        # Calculate average similarity with all embeddings of this person
        similarities = [cosine_similarity(query_embedding, emb) for emb in embeddings]
        avg_similarity = np.mean(similarities)
        max_similarity = np.max(similarities)
        
        # Use weighted combination of avg and max for robustness
        score = 0.7 * max_similarity + 0.3 * avg_similarity
        
        if score > best_score:
            best_score = score
            best_match = person_name
    
    # Convert to percentage
    confidence = best_score * 100
    
    logger.info(f"Face recognition: {best_match} (confidence: {confidence:.1f}%)")
    
    # Apply threshold
    if confidence < threshold * 100:
        logger.warning(f"Low confidence ({confidence:.1f}%) - rejecting as Unknown")
        return ("Unknown", confidence)
    
    return (best_match, confidence)


def add_face_to_database(name: str, image: np.ndarray) -> bool:
    """
    Add a single face embedding to the database
    
    Args:
        name: Person's identity name
        image: BGR image containing the face
    
    Returns:
        True if successfully added
    """
    global _face_database
    
    if not _face_database:
        load_face_database()
    
    embedding = extract_face_embedding(image)
    if embedding is None:
        return False
    
    if name not in _face_database:
        _face_database[name] = []
    
    _face_database[name].append(embedding)
    save_face_database()
    
    logger.info(f"Added face embedding for {name} (total: {len(_face_database[name])})")
    return True


def remove_face_from_database(name: str) -> bool:
    """Remove all embeddings for a person from the database"""
    global _face_database
    
    if not _face_database:
        load_face_database()
    
    if name in _face_database:
        del _face_database[name]
        save_face_database()
        logger.info(f"Removed {name} from face database")
        return True
    
    return False


def get_database_stats() -> Dict:
    """Get statistics about the face database"""
    global _face_database
    
    if not _face_database:
        load_face_database()
    
    stats = {
        'total_identities': len(_face_database),
        'total_embeddings': sum(len(embs) for embs in _face_database.values()),
        'identities': {name: len(embs) for name, embs in _face_database.items()}
    }
    
    return stats


# Backward compatibility wrapper
def identify_face_with_insightface(facearray: np.ndarray) -> Tuple[List[str], float]:
    """
    Wrapper function for backward compatibility with existing code
    Accepts grayscale or color image array
    """
    # Convert grayscale to BGR if needed
    if len(facearray.shape) == 1:
        # Flattened array - reshape to image
        size = int(np.sqrt(len(facearray)))
        facearray = facearray.reshape(size, size).astype(np.uint8)
    
    if len(facearray.shape) == 2:
        # Grayscale - convert to BGR
        facearray = cv2.cvtColor(facearray, cv2.COLOR_GRAY2BGR)
    
    name, confidence = identify_face_insightface(facearray)
    return ([name], confidence)


# Initialize on import
logger.info("InsightFace module loaded - initializing...")
